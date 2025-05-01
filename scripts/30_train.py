#!/usr/bin/env python
# mypy: disable-error-code="no-any-unimported"
"""
Train a model to identify recurring transactions.

This script extracts features from transaction data and trains a machine learning
model to predict which transactions are recurring. It uses the feature extraction
module from recur_scan.features to prepare the input data.
"""

# %%
import argparse
import json
import os
import traceback
from collections import defaultdict
from typing import Any

import joblib
import matplotlib.pyplot as plt
import numpy as np
import optuna
import pandas as pd
import shap
import xgboost as xgb
from loguru import logger
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_selection import RFECV
from sklearn.metrics import confusion_matrix, f1_score, make_scorer, precision_score, recall_score
from sklearn.model_selection import GridSearchCV, GroupKFold, GroupShuffleSplit, RandomizedSearchCV
from tqdm import tqdm
from xgboost.callback import EarlyStopping

from recur_scan.features import get_features
from recur_scan.transactions import (
    group_transactions,
    read_labeled_transactions,
    write_labeled_transactions,
    write_transactions,
)

# %%
# configure the script

use_precomputed_features = True
model_type = "xgb"  # "rf" or "xgb"
n_cv_folds = 5  # number of cross-validation folds, could be 5
do_hyperparameter_optimization = False  # set to False to use the default hyperparameters
search_type = "bayesian"  # "grid", "random", or "bayesian"
n_hpo_iters = 250  # number of hyperparameter optimization iterations
n_jobs = -1  # number of jobs to run in parallel (set to 1 if your laptop gets too hot)
recall_weight = 1.5  # weight for recall in custom scorer (higher values favor recall over precision)

in_path = "training data"
precomputed_features_path = "precomputed features"
out_dir = "training output"

# %%
# parse script arguments from command line
parser = argparse.ArgumentParser(description="Train a model to identify recurring transactions.")
parser.add_argument("--f", help="ignore; used by ipykernel_launcher")
parser.add_argument("--input", type=str, default=in_path, help="Path to the input CSV file containing transactions.")
parser.add_argument(
    "--use_precomputed_features",
    type=bool,
    default=use_precomputed_features,
    help="Use precomputed features instead of generating them from the input file.",
)
parser.add_argument(
    "--precomputed_features",
    type=str,
    default=precomputed_features_path,
    help="Path to the precomputed features CSV file.",
)
parser.add_argument("--output", type=str, default=out_dir, help="Path to the output directory.")
parser.add_argument(
    "--model_type",
    type=str,
    default=model_type,
    choices=["rf", "xgb"],
    help="Model type: 'rf' for Random Forest, 'xgb' for XGBoost.",
)
parser.add_argument(
    "--search_type",
    type=str,
    default=search_type,
    choices=["grid", "random", "bayesian"],
    help="Hyperparameter search type: 'grid' for GridSearchCV, 'random' for RandomizedSearchCV, 'bayesian' for Optuna.",
)
parser.add_argument(
    "--recall_weight",
    type=float,
    default=recall_weight,
    help="Weight for recall in the custom scorer (higher values favor recall over precision).",
)
parser.add_argument(
    "--n_hpo_iters",
    type=int,
    default=n_hpo_iters,
    help="Number of hyperparameter optimization iterations.",
)
parser.add_argument(
    "--n_jobs",
    type=int,
    default=n_jobs,
    help="Number of jobs to run in parallel (-1 for all available cores).",
)
args = parser.parse_args()
in_path = args.input
use_precomputed_features = args.use_precomputed_features
precomputed_features_path = args.precomputed_features
out_dir = args.output
model_type = args.model_type
search_type = args.search_type
recall_weight = args.recall_weight
n_hpo_iters = args.n_hpo_iters
n_jobs = args.n_jobs

# Create output directory if it doesn't exist
os.makedirs(out_dir, exist_ok=True)

# %%
# define some functions


# Define custom scorer that weights recall more than precision
def weighted_precision_recall_score(y_true: np.ndarray | list, y_pred: np.ndarray | list) -> float:
    """
    Custom scoring function that weights recall more than precision.

    Args:
        y_true: True labels (can be ndarray or list)
        y_pred: Predicted labels (can be ndarray or list)

    Returns:
        Weighted average of precision and recall
    """
    # Convert to numpy arrays if they're lists
    if isinstance(y_true, list):
        y_true = np.array(y_true)
    if isinstance(y_pred, list):
        y_pred = np.array(y_pred)

    recall = recall_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    # Calculate weighted average favoring recall
    return float((recall_weight * recall + precision) / (recall_weight + 1))


# Custom XGBoost evaluation metric for scikit-learn API
def weighted_sklearn_metric(y_true: np.ndarray, y_pred_proba: np.ndarray) -> float:
    """
    Custom evaluation metric for XGBoost that weights recall more than precision (for scikit-learn API).

    Args:
        y_true: True labels
        y_pred_proba: Predicted probabilities for the positive class

    Returns:
        Weighted score (higher is better)
    """
    # For binary classification problems, XGBoost passes probability of positive class
    if len(y_pred_proba.shape) > 1 and y_pred_proba.shape[1] > 1:
        # Multi-class case, take the highest probability
        y_binary = np.argmax(y_pred_proba, axis=1)
    else:
        # Binary case
        y_binary = (y_pred_proba > 0.5).astype(int)

    # Handle edge cases with all predictions of one class
    if len(np.unique(y_binary)) == 1:
        if y_binary[0] == 1:  # All positives
            precision_value = np.mean(y_true)  # TP / (TP + FP)
            recall_value = 1.0  # TP / (TP + FN)
        else:  # All negatives
            precision_value = 0.0
            recall_value = 0.0
    else:
        precision_value = precision_score(y_true, y_binary)
        recall_value = recall_score(y_true, y_binary)

    # Calculate weighted score (higher is better)
    return float((recall_weight * recall_value + precision_value) / (recall_weight + 1))


# %%
#
# LOAD AND PREPARE THE DATA
#

# read labeled transactions

transactions, y = read_labeled_transactions(in_path)
logger.info(f"Read {len(transactions)} transactions with {len(y)} labels")

# %%
# group transactions by user_id and name

grouped_transactions = group_transactions(transactions)
logger.info(f"Grouped {len(transactions)} transactions into {len(grouped_transactions)} groups")

user_ids = [transaction.user_id for transaction in transactions]

# %%
# get features

logger.info("Getting features")

if use_precomputed_features:
    # read the precomputed features
    features = pd.read_csv(precomputed_features_path).to_dict(orient="records")
    logger.info(f"Read {len(features)} precomputed features: {len(features[0])} features per transaction")
else:
    # feature generation is parallelized using joblib
    # Use backend that works better with shared memory
    try:
        with joblib.parallel_backend("loky", n_jobs=n_jobs):
            features = joblib.Parallel(
                verbose=1,
            )(
                joblib.delayed(get_features)(transaction, grouped_transactions[(transaction.user_id, transaction.name)])
                for transaction in tqdm(transactions, desc="Processing transactions")
            )
        # save the features to a csv file
        pd.DataFrame(features).to_csv(precomputed_features_path, index=False)
        logger.info(f"Generated {len(features)} features")
    except Exception:
        import traceback

        traceback.print_exc()

# %%
# add new features
# new_features = [
#     get_new_features(transaction, grouped_transactions[(transaction.user_id, transaction.name)])
#     for transaction in tqdm(transactions, desc="Processing transactions")
# ]

# %%
# add the new features to the existing features
# for i, new_transaction_features in enumerate(new_features):
#     features[i].update(new_transaction_features)  # type: ignore
# logger.info(f"Added {len(new_features[0])} new features")

# %%
# convert all features to a matrix for machine learning
dict_vectorizer = DictVectorizer(sparse=False)
X = dict_vectorizer.fit_transform(features)
feature_names = dict_vectorizer.get_feature_names_out()  # Get feature names from the vectorizer
logger.info(f"Converted {len(features)} features into a {X.shape} matrix")


# %%
#
# HYPERPARAMETER OPTIMIZATION
#

# select the features tu use for hyperparameter optimizatino
# (we can uncomment the following line to use the selected features)

# X_hpo = X[:, selected_features]  # type: ignore
X_hpo = X
print(X_hpo.shape)

# %%

if do_hyperparameter_optimization:
    # Create custom scorer
    custom_scorer = make_scorer(weighted_precision_recall_score)

    # Define Optuna optimization function
    def objective(trial: optuna.Trial) -> float:  # type: ignore[misc]
        """
        Objective function for Optuna hyperparameter optimization.

        Args:
            trial: Optuna trial object

        Returns:
            Average score across cross-validation folds
        """
        # Set up parameters based on model type
        if model_type == "rf":
            params: dict[str, Any] = {
                "n_estimators": trial.suggest_int("n_estimators", 300, 1000, step=100),
                "max_depth": trial.suggest_int("max_depth", 10, 50),
                "min_samples_split": trial.suggest_int("min_samples_split", 2, 10),
                "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 10),
                "max_features": trial.suggest_categorical("max_features", ["sqrt", "log2"]),
                "bootstrap": trial.suggest_categorical("bootstrap", [True, False]),
            }
            # Create model
            model = RandomForestClassifier(random_state=42, n_jobs=n_jobs, **params)

        elif model_type == "xgb":
            params = {
                "scale_pos_weight": trial.suggest_float("scale_pos_weight", 27, 35),
                "max_depth": trial.suggest_int("max_depth", 5, 9),  # Shallower trees
                "learning_rate": trial.suggest_float("learning_rate", 0.05, 0.15, log=True),  # Slower learning
                "n_estimators": trial.suggest_int("n_estimators", 100, 500, step=50),
                "min_child_weight": trial.suggest_int("min_child_weight", 1, 7),  # Higher to avoid noise
                "reg_alpha": trial.suggest_float("reg_alpha", 0.5, 1.5, log=True),  # Stronger L1 regularization
                "reg_lambda": trial.suggest_float("reg_lambda", 0.5, 1.5, log=True),  # Stronger L2 regularization
                "subsample": trial.suggest_float("subsample", 0.5, 1.0),  # Stronger subsampling
                "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),  # Use fewer features per tree
                "colsample_bylevel": trial.suggest_float("colsample_bylevel", 0.5, 1.0),  # Use fewer features per level
                "gamma": trial.suggest_float("gamma", 0.2, 1.0, log=True),  # Higher min split gain
            }

        # Perform cross-validation
        cv = GroupKFold(n_splits=n_cv_folds)
        scores = []

        for train_idx, test_idx in cv.split(X_hpo, y, groups=user_ids):
            X_train, X_test = X_hpo[train_idx], X_hpo[test_idx]
            y_train = np.array([y[i] for i in train_idx])
            y_test = np.array([y[i] for i in test_idx])

            if model_type == "xgb":
                # For XGBoost, create validation set for early stopping
                gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
                train_idx2, val_idx = next(gss.split(X_train, y_train, groups=[user_ids[i] for i in train_idx]))
                X_train_final, X_val = X_train[train_idx2], X_train[val_idx]
                y_train_final = np.array([y_train[i] for i in train_idx2])
                y_val = np.array([y_train[i] for i in val_idx])

                # Create early stopping callback explicitly set to maximize our metric
                early_stopping = EarlyStopping(
                    rounds=50,
                    min_delta=0.001,
                    save_best=True,
                    maximize=True,  # Important: we want to maximize our weighted metric
                    data_name="validation_0",
                )

                # Create and train model with early stopping
                model = xgb.XGBClassifier(
                    random_state=42,
                    n_jobs=n_jobs,
                    eval_metric=weighted_sklearn_metric,  # Use our custom sklearn-compatible metric
                    callbacks=[early_stopping],  # Use callback instead of early_stopping_rounds
                    **params,
                )
                model.fit(
                    X_train_final,
                    y_train_final,
                    eval_set=[(X_val, y_val)],
                    verbose=False,
                )
            else:
                # For RF, just train on full training set
                model = RandomForestClassifier(random_state=42, n_jobs=n_jobs, **params)
                model.fit(X_train, y_train)

            # Make predictions and calculate custom score
            y_pred = model.predict(X_test)
            score = weighted_precision_recall_score(y_test, y_pred)
            scores.append(score)

        # Return mean score across folds
        return float(np.mean(scores))

    # Set up Optuna study
    if search_type == "bayesian":
        logger.info(f"Starting Bayesian optimization with Optuna for {model_type} model")
        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=n_hpo_iters, show_progress_bar=True)

        # Get best parameters
        best_params = study.best_params
        best_score = study.best_value
        logger.info(f"Best weighted score: {best_score:.4f}")

        print("Best Hyperparameters:")
        for param, value in best_params.items():
            print(f"  {param}: {value}")

    elif search_type == "grid" or search_type == "random":
        # Define parameter grid for traditional sklearn optimizers
        if model_type == "rf":
            param_dist = {
                "n_estimators": [300, 400, 500, 600, 700, 800],
                "max_depth": [20, 30, 40, 50],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 4, 8],
                "max_features": ["sqrt", "log2"],
                "bootstrap": [True, False],
            }
        elif model_type == "xgb":
            param_dist = {
                "scale_pos_weight": [25, 30, 35, 40],
                "max_depth": [3, 4, 5, 6, 7],
                "learning_rate": [0.01, 0.025, 0.05, 0.1],
                "n_estimators": [800, 1000, 1200, 1500],
                "min_child_weight": [1, 2, 3],
                "reg_alpha": [0, 0.5, 1.0],
                "reg_lambda": [0.1, 1.0, 5.0],
                "subsample": [0.7, 0.8, 0.9, 1.0],
                "colsample_bytree": [0.6, 0.7, 0.8, 0.9],
                "gamma": [0, 0.1, 0.2, 0.5],
            }

        # Set up model
        if model_type == "rf":
            model = RandomForestClassifier(random_state=42, n_jobs=n_jobs)
        elif model_type == "xgb":
            model = xgb.XGBClassifier(random_state=42, n_jobs=n_jobs, early_stopping_rounds=50)

        # Set up cross-validation
        cv = GroupKFold(n_splits=n_cv_folds)

        # Set up the search
        if search_type == "grid":
            search = GridSearchCV(model, param_dist, cv=cv, scoring=custom_scorer, n_jobs=n_jobs, verbose=3)
        else:  # random search
            search = RandomizedSearchCV(
                model, param_dist, n_iter=n_hpo_iters, cv=cv, scoring=custom_scorer, n_jobs=n_jobs, verbose=3
            )

        logger.info(f"Searching for best hyperparameters for {model_type} with {search_type} search")
        search.fit(X_hpo, y, groups=user_ids)
        logger.info(f"Best weighted score: {search.best_score_}")

        print("Best Hyperparameters:")
        for param, value in search.best_params_.items():
            print(f"  {param}: {value}")

        best_params = search.best_params_
else:
    # default hyperparameters
    if model_type == "rf":
        best_params = {
            "n_estimators": 500,
            "min_samples_split": 5,
            "min_samples_leaf": 8,
            "max_features": "sqrt",
            "max_depth": 40,
            "bootstrap": False,
        }
    elif model_type == "xgb":
        best_params = {
            "scale_pos_weight": 33.6339939208229,
            "max_depth": 6,
            "learning_rate": 0.08416195644648089,
            "n_estimators": 190,  # 450
            "min_child_weight": 2,
            "reg_alpha": 0.8615845471900394,
            "reg_lambda": 0.7831593559508362,
            "subsample": 0.7470770012776469,
            "colsample_bytree": 0.5497212934566775,
            "colsample_bylevel": 0.9665628464460082,
            "gamma": 0.696977126868726,
        }

# %%
#
# TRAIN THE MODEL
#

# now that we have the best hyperparameters, train a model with them

# X_m = X[:, selected_features]
X_m = X
print(X_m.shape)

logger.info(f"Training the {model_type} model with {best_params}")
if model_type == "rf":
    model = RandomForestClassifier(random_state=42, **best_params, n_jobs=n_jobs)
    model.fit(X_m, y)
elif model_type == "xgb":
    # For the final XGBoost model, use early stopping with a validation set
    # Create a validation set using GroupShuffleSplit to respect user_id boundaries
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, val_idx = next(gss.split(X_m, y, groups=user_ids))
    X_train_final, X_val = X_m[train_idx], X_m[val_idx]
    y_train_final = np.array([y[i] for i in train_idx])
    y_val = np.array([y[i] for i in val_idx])

    # Create early stopping callback explicitly set to maximize our metric
    early_stopping = EarlyStopping(
        rounds=50,
        min_delta=0.001,
        save_best=True,
        maximize=True,  # Important: we want to maximize our weighted metric
        data_name="validation_0",
    )

    # Create XGBoost model with early stopping
    model = xgb.XGBClassifier(
        random_state=42,
        eval_metric=weighted_sklearn_metric,  # Use our custom sklearn-compatible metric
        callbacks=[early_stopping],  # Use callback instead of early_stopping_rounds
        **best_params,
        n_jobs=n_jobs,
    )

    # Train with early stopping using validation set
    model.fit(X_train_final, y_train_final, eval_set=[(X_val, y_val)], verbose=True)

    logger.info(f"Best iteration: {model.best_iteration}")
    logger.info(f"Best score: {model.best_score}")

    # Now retrain on full dataset using the best number of iterations found
    if hasattr(model, "best_iteration"):
        # Retrain on full dataset with the optimal number of boosting rounds
        best_params["n_estimators"] = model.best_iteration

# %%
# train the full model with the best hyperparameters

model = xgb.XGBClassifier(random_state=42, **best_params, n_jobs=n_jobs)
model.fit(X, y)
logger.info(f"Ttrain full model with {model.n_estimators} estimators")

# %%
# review feature importances

importances = model.feature_importances_

# sort the importances
sorted_importances = sorted(zip(importances, feature_names, strict=True), key=lambda x: x[0], reverse=True)

# print the features and their importances
for importance, feature in sorted_importances:
    print(f"{feature}: {importance}")

# %%
# save the model using joblib

logger.info(f"Saving the {model_type} model to {out_dir}")
joblib.dump(model, os.path.join(out_dir, "model.joblib"))
# save the dict vectorizer as well
joblib.dump(dict_vectorizer, os.path.join(out_dir, "dict_vectorizer.joblib"))
# save the best params to a json file
with open(os.path.join(out_dir, "best_params.json"), "w") as f:
    json.dump(best_params, f)
logger.info(f"Model saved to {out_dir}")

# %%
#
# PREDICT ON THE TRAINING DATA
#

y_pred = model.predict(X)

# %%
#
# EVALUATE THE PREDICTIONS
#

# calculate the precision, recall, f1 score, and weighted score for the positive class

precision = precision_score(y, y_pred)
recall = recall_score(y, y_pred)
f1 = f1_score(y, y_pred)
weighted_score = weighted_precision_recall_score(y, y_pred)

print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1 Score: {f1:.3f}")
print(f"Weighted Score (recall x{recall_weight}): {weighted_score:.3f}")
print("Confusion Matrix:")

print("                Predicted Non-Recurring  Predicted Recurring")
print("Actual Non-Recurring", end="")
cm = confusion_matrix(y, y_pred)
print(f"     {cm[0][0]:<20} {cm[0][1]}")
print("Actual Recurring    ", end="")
print(f"     {cm[1][0]:<20} {cm[1][1]}")


# %%
# get the misclassified transactions

misclassified = [transactions[i] for i, yp in enumerate(y_pred) if yp != y[i]]
logger.info(f"Found {len(misclassified)} misclassified transactions (bias error)")

# save the misclassified transactions to a csv file in the output directory
write_transactions(os.path.join(out_dir, "bias_errors.csv"), misclassified, y)

# %%
#
# USE CROSS-VALIDATION TO GET THE VARIANCE ERRORS
#

# select the features tu use for cross-validation
# (we can uncomment the following line to use the selected features)

# X_cv = X[:, selected_features]
X_cv = X
print(X_cv.shape)

# %%

# n_estimators = 240
# best_params["n_estimators"] = n_estimators

for n_estimators in range(210, 220, 10):
    best_params["n_estimators"] = n_estimators
    cv = GroupKFold(n_splits=n_cv_folds)

    misclassified = []
    false_positives = set()
    false_negatives = set()
    precisions = []
    recalls = []
    f1s = []
    weighted_scores = []

    logger.info(f"Starting cross-validation with {n_cv_folds} folds and {best_params}")
    for fold, (train_idx, val_idx) in enumerate(cv.split(X_cv, y, groups=user_ids)):
        logger.info(f"Fold {fold + 1} of {n_cv_folds}")
        # Get training and validation data
        X_train, X_val = X_cv[train_idx], X_cv[val_idx]
        y_train, y_val = np.array(y)[train_idx], np.array(y)[val_idx]
        transactions_val = [transactions[i] for i in val_idx]  # Keep the original transaction instances for this fold

        # Train the model
        if model_type == "rf":
            model = RandomForestClassifier(random_state=42, **best_params, n_jobs=n_jobs)
            model.fit(X_train, y_train)

        elif model_type == "xgb":
            # No need for early stopping during cross-validation evaluation
            # We've already determined the optimal n_estimators in the model training phase
            model = xgb.XGBClassifier(
                random_state=42,
                n_jobs=n_jobs,
                **best_params,  # This already contains the optimized n_estimators
            )
            model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_val)

        # Find misclassified instances
        misclassified_fold = [transactions_val[i] for i in range(len(y_val)) if y_val[i] != y_pred[i]]
        misclassified.extend(misclassified_fold)

        # track false positives and false negatives
        false_positives.update([
            transactions_val[i] for i in range(len(y_val)) if y_val[i] != y_pred[i] and y_val[i] == 0
        ])
        false_negatives.update([
            transactions_val[i] for i in range(len(y_val)) if y_val[i] != y_pred[i] and y_val[i] == 1
        ])

        # Calculate and report scores
        precision = precision_score(y_val, y_pred)
        recall = recall_score(y_val, y_pred)
        f1 = f1_score(y_val, y_pred)
        weighted_score = weighted_precision_recall_score(y_val, y_pred)

        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)
        weighted_scores.append(weighted_score)

        print(
            f"Fold {fold + 1} Precision: {precision:.2f}, Recall: {recall:.2f}, F1: {f1:.2f}, "
            f"Weighted: {weighted_score:.2f}"
        )
        print(f"Misclassified Instances in Fold {fold + 1}: {len(misclassified_fold)}")

    # print the average precision, recall, and f1 score for all folds
    print(f"Model type: {model_type}")
    print(f"n_estimators: {n_estimators}")
    print(f"\nAverage Metrics Across {n_cv_folds} Folds:")
    print(f"Precision: {sum(precisions) / len(precisions):.3f}")
    print(f"Recall: {sum(recalls) / len(recalls):.3f}")
    print(f"F1 Score: {sum(f1s) / len(f1s):.3f}")
    print(f"Weighted Score (recall x{recall_weight}): {sum(weighted_scores) / len(weighted_scores):.3f}")
    print(f"False positives: {len(false_positives)}")
    print(f"False negatives: {len(false_negatives)}")

# %%
# save the misclassified transactions to a csv file in the output directory

logger.info(f"Found {len(misclassified)} misclassified transactions (variance errors)")

write_transactions(os.path.join(out_dir, "variance_errors.csv"), misclassified, y)

# %%
# count the number of misclassified transactions by transaction.name

# print the misclassified transactions by name
print("Misclassified transactions by name:")
misclassified_by_name: dict[str, int] = defaultdict(int)
for transaction in misclassified:
    misclassified_by_name[transaction.name] += 1
for name, count in sorted(misclassified_by_name.items(), key=lambda x: x[1], reverse=True):
    print(f"{name}: {count}")

# print the false positives and false negatives by name
print("\nFalse positives by name:")
false_positives_by_name: dict[str, int] = defaultdict(int)
for transaction in false_positives:
    false_positives_by_name[transaction.name] += 1
for name, count in sorted(false_positives_by_name.items(), key=lambda x: x[1], reverse=True):
    print(f"{name}: {count}")

print("\nFalse negatives by name:")
false_negatives_by_name: dict[str, int] = defaultdict(int)
for transaction in false_negatives:
    false_negatives_by_name[transaction.name] += 1
for name, count in sorted(false_negatives_by_name.items(), key=lambda x: x[1], reverse=True):
    print(f"{name}: {count}")

# %%
# for each user_id, name pair in misclassified transactions,
# save all of the transactions with that user_id and name to a transactions_to_review.csv file
# include a new column "label" that is either "fp" for false positive or "fn" for false negative
# or empty if the transaction is correctly classified

# create a dictionary of names -> user_id's with misclassified transactions for that name
misclassified_name_to_user_ids = defaultdict(set)
for transaction in misclassified:
    misclassified_name_to_user_ids[transaction.name].add(transaction.user_id)

transactions_to_review = []
labels = []
# loop through the names in reverse order of misclassified transactions
for name, _ in sorted(misclassified_by_name.items(), key=lambda x: x[1], reverse=True):
    for user_id in misclassified_name_to_user_ids[name]:
        for transaction in transactions:
            if transaction.name == name and transaction.user_id == user_id:
                transactions_to_review.append(transaction)
                label = ""
                if transaction in false_positives:
                    label = "fp"
                elif transaction in false_negatives:
                    label = "fn"
                labels.append(label)

# save the transactions to a csv file
logger.info(
    f"Saving {len(transactions_to_review)} transactions to {os.path.join(out_dir, 'transactions_to_review.csv')}"
)
write_labeled_transactions(os.path.join(out_dir, "transactions_to_review.csv"), transactions_to_review, y, labels)

# %%
#
# analyze the features using SHAP
# this step takes a LONG time and is optional

# create a tree explainer
# explainer = shap.TreeExplainer(model)
# Faster approximation using PermutationExplainer
X_sample = X[:10000]  # type: ignore
explainer = shap.TreeExplainer(model)

logger.info("Calculating SHAP values")
shap_values = explainer.shap_values(X_sample)

# Plot SHAP summary
shap.summary_plot(shap_values, X_sample, feature_names=feature_names)

# %%
#
# do recursive feature elimination to identify the most important features
# this step also takes a LONG time and is optional

print("Best params:", best_params)
if model_type == "rf":
    model = RandomForestClassifier(random_state=42, **best_params, n_jobs=n_jobs)
elif model_type == "xgb":
    model = xgb.XGBClassifier(random_state=42, **best_params, n_jobs=n_jobs)
custom_scorer = make_scorer(weighted_precision_recall_score)

# First split data into train/test sets respecting user grouping
logger.info("Splitting data into train/test sets respecting user grouping")
gss = GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=42)
train_idx, test_idx = next(gss.split(X, y, groups=user_ids))

X_train, X_test = X[train_idx], X[test_idx]
y_train = np.array([y[i] for i in train_idx])
y_test = np.array([y[i] for i in test_idx])
user_ids_train = [user_ids[i] for i in train_idx]

# Calculate step size as percentage of features (more efficient)
step_pct = 0.005
step_size = max(1, int(step_pct * X.shape[1]))  # 1% of features per step

# RFECV performs recursive feature elimination with cross-validation
# to find the optimal number of features
logger.info(f"Performing recursive feature elimination with step size {step_size}")
cv = GroupKFold(n_splits=n_cv_folds)
rfecv = RFECV(
    estimator=model,
    step=step_size,
    cv=cv,
    scoring=custom_scorer,  # Using our custom scorer that weights recall more than precision
    min_features_to_select=50,  # Minimum number of features to select
    n_jobs=n_jobs,
)

# Fit the RFECV on training data only
rfecv.fit(X_train, y_train, groups=user_ids_train)
logger.info(f"Optimal number of features: {rfecv.n_features_}")

# Get the selected features
selected_features = [i for i, selected in enumerate(rfecv.support_) if selected]
selected_feature_names = [feature_names[i] for i in selected_features]
print(f"Selected {len(selected_feature_names)} features")

# Get the eliminated features
eliminated_features = [feature_names[i] for i in range(len(feature_names)) if i not in selected_features]
print(f"Eliminated {len(eliminated_features)} features")

# Save selected features to a text file
selected_features_path = os.path.join(out_dir, "selected_features.txt")
with open(selected_features_path, "w") as f:
    for feature in selected_feature_names:
        f.write(f"{feature}\n")
logger.info(f"Saved {len(selected_feature_names)} selected features to {selected_features_path}")

# Save eliminated features to a text file
eliminated_features_path = os.path.join(out_dir, "eliminated_features.txt")
with open(eliminated_features_path, "w") as f:
    for feature in eliminated_features:
        f.write(f"{feature}\n")
logger.info(f"Saved {len(eliminated_features)} eliminated features to {eliminated_features_path}")

# %%
# plot the RFECV results

# Plot the CV scores vs number of features
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(rfecv.cv_results_["mean_test_score"]) + 1), rfecv.cv_results_["mean_test_score"], "o-")
plt.xlabel(f"Number of features (multiply by {step_size})")
plt.ylabel("Cross-validation accuracy")
plt.title("Accuracy vs. Number of Features")
plt.grid(True)
plt.savefig(os.path.join(out_dir, "feature_selection_curve.png"))
plt.show()

# %%
# Train models with selected features using the already created train/test split

X_train_selected = X_train[:, selected_features]  # type: ignore
X_test_selected = X_test[:, selected_features]  # type: ignore

logger.info("Training model with selected features")
if model_type == "rf":
    model_selected = RandomForestClassifier(random_state=42, **best_params, n_jobs=n_jobs)
elif model_type == "xgb":
    model_selected = xgb.XGBClassifier(random_state=42, **best_params, n_jobs=n_jobs)
model_selected.fit(X_train_selected, y_train)

# Evaluate model with selected features
y_pred_selected = model_selected.predict(X_test_selected)
precision = precision_score(y_test, y_pred_selected)
recall = recall_score(y_test, y_pred_selected)
f1 = f1_score(y_test, y_pred_selected)
weighted_score = weighted_precision_recall_score(y_test, y_pred_selected)
print("Selected Features:")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1 Score: {f1:.3f}")
print(f"Weighted Score (recall x{recall_weight}): {weighted_score:.3f}")

# %%
# Compare with model using all features
logger.info("Training model with all features")
if model_type == "rf":
    model_all = RandomForestClassifier(random_state=42, **best_params, n_jobs=n_jobs)
elif model_type == "xgb":
    model_all = xgb.XGBClassifier(random_state=42, **best_params, n_jobs=n_jobs)
model_all.fit(X_train, y_train)
y_pred_all = model_all.predict(X_test)
precision_all = precision_score(y_test, y_pred_all)
recall_all = recall_score(y_test, y_pred_all)
f1_all = f1_score(y_test, y_pred_all)
weighted_score_all = weighted_precision_recall_score(y_test, y_pred_all)
print("All Features:")
print(f"Precision: {precision_all:.3f}")
print(f"Recall: {recall_all:.3f}")
print(f"F1 Score: {f1_all:.3f}")
print(f"Weighted Score (recall x{recall_weight}): {weighted_score_all:.3f}")

# Save comparison results
with open(os.path.join(out_dir, "feature_selection_results.txt"), "w") as f:
    f.write(f"Selected Features ({len(selected_feature_names)}):\n")
    f.write(f"Precision: {precision:.3f}\n")
    f.write(f"Recall: {recall:.3f}\n")
    f.write(f"F1 Score: {f1:.3f}\n")
    f.write(f"Weighted Score (recall x{recall_weight}): {weighted_score:.3f}\n\n")
    f.write(f"All Features ({len(feature_names)}):\n")
    f.write(f"Precision: {precision_all:.3f}\n")
    f.write(f"Recall: {recall_all:.3f}\n")
    f.write(f"F1 Score: {f1_all:.3f}\n")
    f.write(f"Weighted Score (recall x{recall_weight}): {weighted_score_all:.3f}\n")

# %%
