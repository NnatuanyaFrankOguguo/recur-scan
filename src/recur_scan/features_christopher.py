from datetime import datetime, timedelta
from statistics import StatisticsError, mean, median, stdev

from recur_scan.transactions import Transaction
from recur_scan.utils import parse_date


def get_transaction_gaps_chris(all_transactions: list[Transaction]) -> list[int]:
    """Get the number of days between consecutive transactions."""
    try:
        dates = sorted(parse_date(t.date) for t in all_transactions)
    except Exception:
        return []
    return [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))] if len(dates) > 1 else []


def std_amount_all_chris(all_transactions: list[Transaction]) -> float:
    """
    Compute the standard deviation of transaction amounts for a list of transactions.
    """
    amounts = [t.amount for t in all_transactions]
    try:
        return stdev(amounts) if len(amounts) > 1 else 0.0
    except StatisticsError:
        return 0.0


def get_n_transactions_same_amount_chris(transaction: Transaction, all_transactions: list[Transaction]) -> int:
    """
    Count transactions with amounts that match within a 1% tolerance.
    This tolerance helps capture minor variations due to rounding.
    """
    tol = 0.01 * transaction.amount if transaction.amount != 0 else 0.01
    return sum(1 for t in all_transactions if abs(t.amount - transaction.amount) <= tol)


def get_percent_transactions_same_amount_chris(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Calculate the percentage of transactions with nearly the same amount."""
    count = get_n_transactions_same_amount_chris(transaction, all_transactions)
    return count / len(all_transactions) if all_transactions else 0.0


def get_transaction_frequency_chris(all_transactions: list[Transaction]) -> float:
    """Calculate the average number of days between transactions."""
    gaps = get_transaction_gaps_chris(all_transactions)
    return sum(gaps) / len(gaps) if gaps else 0.0


def get_transaction_std_amount_chris(all_transactions: list[Transaction]) -> float:
    """Compute the standard deviation of transaction amounts."""
    amounts = [t.amount for t in all_transactions]
    try:
        return stdev(amounts) if len(amounts) > 1 else 0.0
    except StatisticsError:
        return 0.0


def get_coefficient_of_variation_chris(all_transactions: list[Transaction]) -> float:
    """
    Compute the coefficient of variation (std/mean) for transaction amounts.
    """
    amounts = [t.amount for t in all_transactions]
    if not amounts:
        return 0.0
    avg = sum(amounts) / len(amounts)
    if avg == 0:
        return 0.0
    return std_amount_all_chris(all_transactions) / avg


def follows_regular_interval_chris(all_transactions: list[Transaction]) -> bool:
    """
    Check if transactions follow a regular pattern (~monthly).
    """
    gaps = get_transaction_gaps_chris(all_transactions)
    if not gaps:
        return False
    avg_gap = sum(gaps) / len(gaps)
    try:
        gap_std = stdev(gaps) if len(gaps) > 1 else 0.0
    except StatisticsError:
        gap_std = 0.0
    return (27 <= avg_gap <= 33) and (gap_std < 3)


def detect_skipped_months_chris(all_transactions: list[Transaction]) -> int:
    """Count how many months were skipped in a recurring pattern."""
    try:
        dates = sorted(parse_date(t.date) for t in all_transactions)
    except Exception:
        return 0
    if not dates:
        return 0
    months = {d.year * 12 + d.month for d in dates}
    return (max(months) - min(months) + 1 - len(months)) if len(months) > 1 else 0


def get_day_of_month_consistency_chris(all_transactions: list[Transaction]) -> float:
    """
    Calculate the consistency of the day of the month for transactions.
    """
    days = [parse_date(t.date).day for t in all_transactions]
    if not days:
        return 0.0
    most_common_day = max(set(days), key=days.count)
    return days.count(most_common_day) / len(days)


def get_median_interval_chris(all_transactions: list[Transaction]) -> float:
    """Calculate the median gap (in days) between transactions."""
    gaps = get_transaction_gaps_chris(all_transactions)
    return median(gaps) if gaps else 0.0


def is_known_recurring_company_chris(transaction_name: str) -> bool:
    """
    Flags transactions as recurring if the company name contains specific keywords,
    regardless of price variation.
    """
    known_recurring_keywords = [
        "amazon prime",
        "american water works",
        "ancestry",
        "at&t",
        "canva",
        "comcast",
        "cox",
        "cricket wireless",
        "disney",
        "disney+",
        "energy",
        "geico",
        "google storage",
        "hulu",
        "hbo max",
        "insurance",
        "mobile",
        "national grid",
        "netflix",
        "ngrid",
        "peacock",
        # "placer county water age",  # too specific
        "spotify",
        "sezzle",
        # "smyrna finance",  # too specific
        "spectrum",
        "utility",
        "utilities",
        "verizon",
        "walmart+",
        "wireless",
        "wix",
        "youtube",
    ]

    transaction_name_lower = transaction_name.lower()
    return any(keyword in transaction_name_lower for keyword in known_recurring_keywords)


# Updated this function with new values
def is_known_fixed_subscription_chris(transaction: Transaction) -> bool:
    """
    Flags transactions as recurring based on known company name substrings and specific amounts.
    Matches are case-insensitive and flexible (e.g., 'Albert123' or 'Cleo AI' will match).
    """
    known_subscriptions = {
        "albert": [14.99, 8.00, 19.99, 11.99, 16.99, 12.99],
        "cleo": [2.99, 5.99, 14.99],
        "moneylion": [9.20],
        "brigit": [9.99, 14.99, 8.99],
        "credit genie": [3.99, 4.99],
        "dave": [1.00],
        "empower": [8.00],
        "grid": [10.00],
    }

    transaction_name_lower = transaction.name.lower()

    for company, amounts in known_subscriptions.items():
        if company in transaction_name_lower and round(transaction.amount, 2) in amounts:
            return True
    return False


# ------------------------NEW FEATURES ------------------------


def get_user_vendor_history(transaction: Transaction, all_transactions: list[Transaction]) -> list[Transaction]:
    """Get historical transactions for same user-vendor pair."""
    current_date = datetime.strptime(transaction.date, "%Y-%m-%d")
    return [t for t in all_transactions if datetime.strptime(t.date, "%Y-%m-%d") < current_date]


def is_regular_interval_chris(transaction: Transaction, all_transactions: list[Transaction]) -> bool:
    """Check if transaction follows regular time intervals with same vendor."""
    history = get_user_vendor_history(transaction, all_transactions)
    if len(history) < 2:
        return False

    dates = sorted([datetime.strptime(t.date, "%Y-%m-%d") for t in history])
    deltas = [(dates[i + 1] - dates[i]).days for i in range(len(dates) - 1)]
    standard_deviation = stdev(deltas) if len(deltas) > 1 else 0
    return standard_deviation < 3  # Allow small variation in interval days


def amount_deviation_chris(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Measure relative difference from historical average amount."""
    history = get_user_vendor_history(transaction, all_transactions)
    if not history:
        return 0.0

    avg_amount = mean(t.amount for t in history)
    return abs(transaction.amount - avg_amount) / avg_amount


def transaction_frequency_chris(transaction: Transaction, all_transactions: list[Transaction]) -> int:
    """Count transactions from same user-vendor pair in last 6 months."""
    cutoff = datetime.strptime(transaction.date, "%Y-%m-%d") - timedelta(days=180)
    return sum(
        1
        for t in get_user_vendor_history(transaction, all_transactions)
        if datetime.strptime(t.date, "%Y-%m-%d") > cutoff
    )


def day_of_month_consistency_chris(transaction: Transaction, all_transactions: list[Transaction]) -> bool:
    """Check if transaction consistently occurs on same calendar day."""
    history = get_user_vendor_history(transaction, all_transactions)
    if not history:
        return False

    transaction_day = datetime.strptime(transaction.date, "%Y-%m-%d").day
    same_day_count = sum(1 for t in history if datetime.strptime(t.date, "%Y-%m-%d").day == transaction_day)
    return same_day_count / len(history) > 0.8


def amount_consistency_chris(transaction: Transaction, all_transactions: list[Transaction]) -> bool:
    """Check if amounts have low historical variability."""
    history = get_user_vendor_history(transaction, all_transactions)
    if len(history) < 2:
        return False

    amounts = [t.amount for t in history]
    standard_deviation = stdev(amounts)
    return standard_deviation < (mean(amounts) * 0.1)


def get_new_features(transaction: Transaction, all_transactions: list[Transaction]) -> dict[str, int | bool | float]:
    """Get the new features for the transaction."""

    # NOTE: Do NOT add features that are already in the original features.py file.
    # NOTE: Each feature should be on a separate line. Do not use **dict shorthand.
    return {
        # "is_known_fixed_subscription_chris": is_known_fixed_subscription_chris(transaction),  # too specific
        "is_regular_interval_chris": is_regular_interval_chris(transaction, all_transactions),
        "amount_deviation_chris": amount_deviation_chris(transaction, all_transactions),
        "transaction_frequency_chris": transaction_frequency_chris(transaction, all_transactions),
        "day_of_month_consistency_chris": day_of_month_consistency_chris(transaction, all_transactions),
        "amount_consistency_chris": amount_consistency_chris(transaction, all_transactions),
    }
