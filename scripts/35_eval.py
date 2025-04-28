#!/usr/bin/env python
"""
Analyze recurring transactions by name and amount.

This script reads transaction data from a CSV file and identifies:
1. Vendor names where at least 90% of transactions are labeled as recurring
2. Transaction amounts where at least 50% of transactions are labeled as recurring
"""

from pathlib import Path

import numpy as np
import pandas as pd


def find_highly_recurring_names(df: pd.DataFrame, threshold: float = 0.9) -> pd.DataFrame:
    """
    Find transaction names where at least threshold% of transactions are marked recurring.

    Args:
        df: DataFrame with transaction data
        threshold: Minimum percentage (0.0-1.0) of recurring transactions

    Returns:
        DataFrame with names and their recurring percentages
    """
    # Group by name and calculate percentage of recurring transactions
    name_stats = (
        df.groupby("name")
        .agg(
            total_count=("recurring", "count"),
            recurring_count=("recurring", "sum"),
        )
        .reset_index()
    )

    # Calculate the percentage of recurring transactions
    name_stats["recurring_pct"] = name_stats["recurring_count"] / name_stats["total_count"]

    # Filter for names with at least threshold% recurring transactions
    highly_recurring = name_stats[name_stats["recurring_pct"] >= threshold]

    # Sort by recurring count (highest first), then by percentage (highest first)
    highly_recurring = highly_recurring.sort_values(["recurring_count", "recurring_pct"], ascending=[False, False])

    return highly_recurring


def find_highly_recurring_amounts(df: pd.DataFrame, threshold: float = 0.5, min_count: int = 10) -> pd.DataFrame:
    """
    Find transaction amounts where at least threshold% of transactions are marked recurring.

    Args:
        df: DataFrame with transaction data
        threshold: Minimum percentage (0.0-1.0) of recurring transactions
        min_count: Minimum number of transactions for an amount to be considered

    Returns:
        DataFrame with amounts and their recurring percentages
    """
    # Round amounts to 2 decimal places to handle floating point precision issues
    df["amount_rounded"] = np.round(df["amount"], 2)

    # Group by amount and calculate percentage of recurring transactions
    amount_stats = (
        df.groupby("amount_rounded")
        .agg(
            total_count=("recurring", "count"),
            recurring_count=("recurring", "sum"),
        )
        .reset_index()
    )

    # Calculate the percentage of recurring transactions
    amount_stats["recurring_pct"] = amount_stats["recurring_count"] / amount_stats["total_count"]

    # Filter for amounts with at least threshold% recurring transactions and minimum count
    highly_recurring = amount_stats[
        (amount_stats["recurring_pct"] >= threshold) & (amount_stats["total_count"] >= min_count)
    ]
    # Sort by recurring count (highest first), then by percentage (highest first)
    highly_recurring = highly_recurring.sort_values(["recurring_count", "recurring_pct"], ascending=[False, False])

    return highly_recurring


if __name__ == "__main__":
    # Path to the training data
    csv_path = Path("../data/train.csv")
    out_dir = Path("../data/training_out")
    out_dir.mkdir(exist_ok=True)

    # Read the CSV file
    df = pd.read_csv(csv_path)
    print(f"Read {len(df)} transactions from {csv_path}")

    # Find names with at least 90% recurring transactions
    highly_recurring_names = find_highly_recurring_names(df, threshold=0.9)

    # Print results for names
    print(f"\nFound {len(highly_recurring_names)} transaction names with ≥90% recurring transactions")

    print("\nTop recurring transaction names:")
    for _, row in highly_recurring_names.head(20).iterrows():
        print(f"{row['name']}: {row['recurring_pct']:.1%} ({row['recurring_count']}/{row['total_count']})")

    # Save to CSV for further analysis
    names_file = out_dir / "highly_recurring_names.csv"
    highly_recurring_names.to_csv(names_file, index=False)
    print(f"Results saved to {names_file}")

    # Find amounts with at least 50% recurring transactions and at least 10 instances
    highly_recurring_amounts = find_highly_recurring_amounts(df, threshold=0.5, min_count=10)

    # Print results for amounts
    print(f"\nFound {len(highly_recurring_amounts)} tx amounts with ≥50% recurring txs (min 10 occurrences)")

    print("\nTop recurring transaction amounts:")
    for _, row in highly_recurring_amounts.head(20).iterrows():
        print(
            f"${row['amount_rounded']:.2f}: {row['recurring_pct']:.1%} ({row['recurring_count']}/{row['total_count']})"
        )

    # Save to CSV for further analysis
    amounts_file = out_dir / "highly_recurring_amounts.csv"
    highly_recurring_amounts.to_csv(amounts_file, index=False)
    print(f"Results saved to {amounts_file}")
