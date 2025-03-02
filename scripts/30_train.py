#!/usr/bin/env python
"""
Train a model to identify recurring transactions.

This script extracts features from transaction data and trains a machine learning
model to predict which transactions are recurring. It uses the feature extraction
module from recur_scan.features to prepare the input data.
"""

# %%

from loguru import logger

from recur_scan.features import get_features

# %%

logger.info("Getting features")
features = get_features()
logger.info(f"Got {len(features)} features")

# %%
