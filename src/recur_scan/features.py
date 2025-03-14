import re
from statistics import mean, stdev

from recur_scan.transactions import Transaction


def get_n_transactions_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> int:
    """Get the number of transactions in all_transactions with the same amount as transaction"""
    return len([t for t in all_transactions if t.amount == transaction.amount])
    # If many transactions have the same amount,
    # it's likely to be a recurring payment. This feature captures that information.


def get_percent_transactions_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Get the percentage of transactions in all_transactions with the same amount as transaction"""
    if not all_transactions:
        return 0.0
    n_same_amount = len([t for t in all_transactions if t.amount == transaction.amount])
    return n_same_amount / len(all_transactions)
    # A high percentage means that transactions often happen at the same amount.
    # Recurring transactions usually repeat the same amount (e.g., Netflix subscription = $15/month).


def get_transaction_intervals(transactions: list[Transaction]) -> dict[str, float]:
    """
    Extracts time-based features for recurring transactions.
    - Computes average days between transactions.
    - Computes standard deviation of intervals.
    - Checks for flexible monthly recurrence (±7 days).
    - Identifies if transactions occur on the same weekday.
    - Checks if payment amounts are within ±5% of each other.
    """
    if len(transactions) < 2:
        return {
            "avg_days_between_transactions": 0.0,
            "std_dev_days_between_transactions": 0.0,
            "monthly_recurrence": 0,
            "same_weekday": 0,
            "same_amount": 0,
        }
    # Sort transactions by date
    dates = sorted([trans.date for trans in transactions])

    # calculate days between each consecutive grouped transactions
    intervals = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]

    # compute average and standard deviation of transaction intervals
    avg_days = mean(intervals) if intervals else 0.0
    std_dev_days = stdev(intervals) if len(intervals) > 1 else 0.0

    # check for flexible monthly recurrence (±7 days)
    monthly_count = sum(
        1
        for gap in intervals
        if 23 <= gap <= 38  # 30 ± 7 days
    )
    monthly_recurrence = monthly_count / len(intervals) if intervals else 0.0

    # check if transactions occur on the same weekday
    weekdays = [date.weekday() for date in dates]  # Monday = 0, Sunday = 6
    same_weekday = 1 if len(set(weekdays)) == 1 else 0  # 1 if all transactions happen on the same weekday

    # check if payment amounts are within ±5% of each other
    amounts = [trans.amount for trans in transactions]
    if not amounts or all(a == 0 for a in amounts):  # Prevent ZeroDivisionError
        consistent_amount = 0.0
    else:
        base_amount = amounts[0] if amounts[0] > 0 else 1  # Avoid division by zero
        consistent_amount = sum(1 for amt in amounts if abs(amt - base_amount) / base_amount <= 0.05) / len(amounts)

    return {
        "avg_days_between_transactions": avg_days,
        "std_dev_days_between_transactions": std_dev_days,
        "monthly_recurrence": monthly_recurrence,
        "same_weekday": same_weekday,
        "same_amount": consistent_amount,
    }


def is_known_recurring_vendor(transaction: Transaction) -> int:
    """
    Checks if the transaction vendor is a well-known subscription or
    utility company using regex.
    Returns 1 if it's a known recurring vendor, else 0.
    """
    known_recurring_keywords = [
        "netflix",
        "spotify",
        "amazon prime",
        "apple music",
        "amazon music",
        "google play",
        "hulu",
        "disney+",
        "sirius xm",
        "pandora",
        "youtube premium",
        "cable",
        "internet",
        "phone",
        "electric",
        "gas",
        "water",
        "sewer",
        "trash",
        "hoa",
        "rent",
        "mortgage",
        "car payment",
        "insurance",
        "student loan",
        "credit card",
        "health insurance",
        "life insurance",
        "car insurance",
        "home insurance",
        "renters insurance",
        "adobe",
        "microsoft",
        "verizon",
        "at&t",
        "afterpay",
        "walmart+",
        "t-mobile",
        "charter comm",
        "energy",
        "boostmobile",
        "fitness",
        "utilities",
        "membership",
        "water",
        "light",
        "x-box",
        "spectrum",
    ]

    vendor_name = transaction.name.lower()
    # Create a regex pattern to match any of the known recurring keywords
    pattern = r"\b(" + "|".join(re.escape(keyword) for keyword in known_recurring_keywords) + r")\b"
    # Check if the vendor name matches the pattern
    return 1 if re.search(pattern, vendor_name, re.IGNORECASE) else 0


def get_features(transaction: Transaction, all_transactions: list[Transaction]) -> dict[str, float | int]:
    """
    Extract numerical features from a transaction for machine learning.
    """
    time_features = get_transaction_intervals(all_transactions)

    return {
        "n_transactions_same_amount": get_n_transactions_same_amount(transaction, all_transactions),
        "percent_transactions_same_amount": get_percent_transactions_same_amount(transaction, all_transactions),
        **time_features,  # Merges new time-based features
        "known_recurring_vendor": is_known_recurring_vendor(transaction),
    }
