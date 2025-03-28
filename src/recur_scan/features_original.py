from datetime import date, datetime
from functools import lru_cache

import numpy as np

from recur_scan.transactions import Transaction


@lru_cache(maxsize=1024)
def parse_date(date_str: str) -> date:
    """Parse a date string into a datetime.date object."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def get_transaction_z_score(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Get the z-score of the transaction amount compared to the mean and standard deviation of all_transactions."""
    all_amounts = [t.amount for t in all_transactions]
    # if the standard deviation is 0, return 0
    if np.std(all_amounts) == 0:
        return 0
    return (transaction.amount - np.mean(all_amounts)) / np.std(all_amounts)  # type: ignore
