#!/usr/bin/env python
"""
Load a model and make predictions on transaction files
"""

# %%
import argparse
import gc
import glob
import os

import joblib
from loguru import logger
from tqdm import tqdm

from recur_scan.features import get_features
from recur_scan.transactions import (
    group_transactions,
    read_earnin_test_transactions,
    read_test_transactions,
    write_transactions,
)

# %%
# configure the script

read_earnin_transaction = True

model_dir = "training output"  # directory containing model.joblib and dict_vectorizer.joblib
in_dir = "test data"
out_dir = "test output"
n_jobs = -1  # number of jobs to run in parallel

# %%
# parse script arguments from command line
parser = argparse.ArgumentParser(description="Load a model and make predictions on transaction files.")
parser.add_argument("--f", help="ignore; used by ipykernel_launcher")
parser.add_argument("--model_dir", type=str, default=model_dir, help="Directory containing the trained model files.")
parser.add_argument("--input", type=str, default=in_dir, help="Path to the input directory containing CSV files.")
parser.add_argument("--output", type=str, default=out_dir, help="Path to the output directory.")
parser.add_argument("--jobs", type=int, default=n_jobs, help="Number of jobs to run in parallel.")
args = parser.parse_args()

model_dir = args.model_dir
in_dir = args.input
out_dir = args.output
n_jobs = args.jobs

# Create output directory if it doesn't exist
os.makedirs(out_dir, exist_ok=True)

# %%
# Load the trained model
model_path = os.path.join(model_dir, "model.joblib")
logger.info(f"Loading model from {model_path}")
model = joblib.load(model_path)
logger.info("Model loaded successfully")

# Load the vectorizer from the model directory
dict_vectorizer_path = os.path.join(model_dir, "dict_vectorizer.joblib")
logger.info(f"Loading vectorizer from {dict_vectorizer_path}")
dict_vectorizer = joblib.load(dict_vectorizer_path)
logger.info("Vectorizer loaded successfully")

# %%
# Process each CSV file in the input directory
csv_files = glob.glob(os.path.join(in_dir, "*.csv"))
logger.info(f"Found {len(csv_files)} CSV files to process")

for csv_file in csv_files:
    file_name = os.path.basename(csv_file)
    logger.info(f"Processing {file_name}")

    # Read transactions from the CSV file using the new function for test data
    if read_earnin_transaction:
        transactions = read_earnin_test_transactions(csv_file)
    else:
        transactions = read_test_transactions(csv_file)
    logger.info(f"Read {len(transactions)} transactions from {file_name}")

    # Group transactions by user_id and name
    grouped_transactions = group_transactions(transactions)
    logger.info(f"Grouped {len(transactions)} transactions into {len(grouped_transactions)} groups")

    # Generate features, vectorize, and predict in batches to avoid memory issues
    logger.info("Generating features")
    # Split transactions into sublists of up to 100000 transactions
    batch_size = 100000
    transaction_batches = [transactions[i : i + batch_size] for i in range(0, len(transactions), batch_size)]
    logger.info(f"Split {len(transactions)} transactions into {len(transaction_batches)} batches")

    all_predictions = []
    total_processed = 0

    for batch_idx, batch in enumerate(transaction_batches):
        logger.info(f"Processing batch {batch_idx + 1}/{len(transaction_batches)} with {len(batch)} transactions")

        # Generate features for this batch
        with joblib.parallel_backend("loky", n_jobs=n_jobs):
            batch_features = joblib.Parallel(verbose=1)(
                joblib.delayed(get_features)(transaction, grouped_transactions[(transaction.user_id, transaction.name)])
                for transaction in tqdm(batch, desc=f"Processing batch {batch_idx + 1} of {file_name}")
            )
        logger.info(f"Generated features for batch {batch_idx + 1}")

        # Transform batch features to matrix and release memory
        X_batch = dict_vectorizer.transform(batch_features)
        batch_features = None  # Release memory
        gc.collect()  # Force garbage collection
        logger.info(f"Vectorized batch {batch_idx + 1}")

        # Make predictions on batch
        y_pred_batch = model.predict(X_batch)
        X_batch = None  # Release memory
        gc.collect()  # Force garbage collection

        # Save predictions
        all_predictions.extend(y_pred_batch)
        total_processed += len(y_pred_batch)
        logger.info(f"Made {len(y_pred_batch)} predictions for batch {batch_idx + 1}, {total_processed} total")

    # Combine all batch predictions
    y_pred = all_predictions
    logger.info(f"Made {len(y_pred)} predictions total")

    # Count positive predictions
    positive_count = sum(y_pred)
    pct = positive_count / len(y_pred) * 100
    logger.info(f"Predicted {positive_count} recurring transactions out of {len(y_pred)} ({pct:.2f}%)")

    # Save predictions to output directory
    out_file = os.path.join(out_dir, file_name)
    write_transactions(out_file, transactions, y_pred)
    logger.info(f"Saved predictions to {out_file}")

logger.info("All files processed successfully")

# %%
