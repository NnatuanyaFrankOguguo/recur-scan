import re
from collections import Counter, defaultdict
from collections.abc import Sequence
from datetime import timedelta
from statistics import StatisticsError, mean, median, stdev

from datetime import date, datetime
from functools import lru_cache

from recur_scan.transactions import Transaction


import numpy as np


from recur_scan.transactions import Transaction

def get_is_always_recurring(transaction: Transaction) -> bool:
    """Check if the transaction is always recurring because of the vendor name - check lowercase match"""
    always_recurring_vendors = {
        "google storage",
        "netflix",
        "hulu",
        "spotify",
    }
    return transaction.name.lower() in always_recurring_vendors


def get_is_insurance(transaction: Transaction) -> bool:
    """Check if the transaction is an insurance payment."""
    # use a regular expression with boundaries to match case-insensitive insurance
    # and insurance-related terms
    match = re.search(r"\b(insurance|insur|insuranc)\b", transaction.name, re.IGNORECASE)
    return bool(match)


def get_is_utility(transaction: Transaction) -> bool:
    """Check if the transaction is a utility payment."""
    # use a regular expression with boundaries to match case-insensitive utility
    # and utility-related terms
    match = re.search(r"\b(utility|utilit|energy)\b", transaction.name, re.IGNORECASE)
    return bool(match)


def get_is_phone(transaction: Transaction) -> bool:
    """Check if the transaction is a phone payment."""
    # use a regular expression with boundaries to match case-insensitive phone
    # and phone-related terms
    match = re.search(r"\b(at&t|t-mobile|verizon)\b", transaction.name, re.IGNORECASE)
    return bool(match)


@lru_cache(maxsize=1024)
def _parse_date(date_str: str) -> date:
    """Parse a date string into a datetime.date object."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def get_n_transactions_days_apart(
    transaction: Transaction,
    all_transactions: list[Transaction],
    n_days_apart: int,
    n_days_off: int,
) -> int:
    """
    Get the number of transactions in all_transactions that are within n_days_off of
    being n_days_apart from transaction
    """
    n_txs = 0
    transaction_date = _parse_date(transaction.date)

    # Pre-calculate bounds for faster checking
    lower_remainder = n_days_apart - n_days_off
    upper_remainder = n_days_off

    for t in all_transactions:
        t_date = _parse_date(t.date)
        days_diff = abs((t_date - transaction_date).days)

        # Skip if the difference is less than minimum required
        if days_diff < n_days_apart - n_days_off:
            continue

        # Check if the difference is close to any multiple of n_days_apart
        remainder = days_diff % n_days_apart

        if remainder <= upper_remainder or remainder >= lower_remainder:
            n_txs += 1

    return n_txs


def _get_day(date: str) -> int:
    """Get the day of the month from a transaction date."""
    return int(date.split("-")[2])


def get_n_transactions_same_day(transaction: Transaction, all_transactions: list[Transaction], n_days_off: int) -> int:
    """Get the number of transactions in all_transactions that are on the same day of the month as transaction"""
    return len([t for t in all_transactions if abs(_get_day(t.date) - _get_day(transaction.date)) <= n_days_off])


def get_pct_transactions_same_day(
    transaction: Transaction, all_transactions: list[Transaction], n_days_off: int
) -> float:
    """Get the percentage of transactions in all_transactions that are on the same day of the month as transaction"""
    return get_n_transactions_same_day(transaction, all_transactions, n_days_off) / len(all_transactions)


def get_ends_in_99(transaction: Transaction) -> bool:
    """Check if the transaction amount ends in 99"""
    return (transaction.amount * 100) % 100 == 99


def get_n_transactions_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> int:
    """Get the number of transactions in all_transactions with the same amount as transaction"""
    return len([t for t in all_transactions if t.amount == transaction.amount])



def get_percent_transactions_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Returns the percentage of transactions with the same amount as the given transaction."""
    if not all_transactions:
        return 0.0
    amount_counts = Counter(t.amount for t in all_transactions)
    return amount_counts.get(transaction.amount, 0) / len(all_transactions)


def frequency_features(all_transactions: list[Transaction]) -> dict:
    """Computes transaction frequency metrics (per month & per week)."""
    if not all_transactions:
        return {"transactions_per_month": 0.0, "transactions_per_week": 0.0}

    min_date = min(t.date for t in all_transactions)
    max_date = max(t.date for t in all_transactions)
    time_span_days = (max_date - min_date).days

    transactions_per_month = len(all_transactions) / ((time_span_days / 30) + 1e-8)
    transactions_per_week = len(all_transactions) / ((time_span_days / 7) + 1e-8)

    return {
        "transactions_per_month": transactions_per_month,
        "transactions_per_week": transactions_per_week,
    }


# 1. Recurrence Interval Variance:
def recurrence_interval_variance(all_transactions: list[Transaction]) -> float:
    """
    Returns the standard deviation (variance) of the days between consecutive transactions for the same vendor.
    A lower variance indicates a regular, recurring pattern.
    """
    if len(all_transactions) < 2:
        return 0.0
    all_transactions = sorted(all_transactions, key=lambda t: t.date)
    intervals = [
        (all_transactions[i].date - all_transactions[i - 1].date).days for i in range(1, len(all_transactions))
    ]
    return stdev(intervals) if len(intervals) > 1 else 0.0


# 2. Normalized Days Difference:
def normalized_days_difference(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """
    Computes the difference between the current transaction's days since last and the median interval,
    normalized by the standard deviation of intervals. Returns 0 if not enough data.
    """
    if len(all_transactions) < 2:
        return 0.0
    all_transactions = sorted(all_transactions, key=lambda t: t.date)
    intervals = [
        (all_transactions[i].date - all_transactions[i - 1].date).days for i in range(1, len(all_transactions))
    ]
    med_interval = median(intervals)
    try:
        std_interval = stdev(intervals)
    except Exception:
        std_interval = 0.0
    days_since_last = (transaction.date - all_transactions[-1].date).days
    # If std is 0 (i.e. intervals are identical), return 0 difference.
    if std_interval == 0:
        return 0.0
    return (days_since_last - med_interval) / std_interval


# 3. Recent Transaction Density:


# 6. Amount Stability Score:
def amount_stability_score(all_transactions: list[Transaction]) -> float:
    """
    Returns the ratio of the median transaction amount to its standard deviation for the vendor.
    A higher ratio indicates that amounts are stable.
    """
    amounts = [t.amount for t in all_transactions]
    if len(amounts) < 2:
        return 0.0
    med = median(amounts)
    try:
        std_amt = stdev(amounts)
    except Exception:
        std_amt = 0.0
    if std_amt == 0:
        return 1.0  # Perfect stability if no variation.
    return med / std_amt


# 7. Amount Z-Score:
def amount_z_score(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """
    Computes the Z-score of the current transaction's amount relative to the vendor's historical amounts.
    """
    amounts = [t.amount for t in all_transactions]
    if len(amounts) < 2:
        return 0.0
    med = median(amounts)
    try:
        std_amt = stdev(amounts)
    except Exception:
        std_amt = 0.0
    if std_amt == 0:
        return 0.0
    return (transaction.amount - med) / std_amt


def vendor_recurrence_trend(all_transactions: list[Transaction]) -> float:
    """
    Groups a vendor's transactions by (year, month) and counts transactions per month.
    Fits a simple linear regression (using np.polyfit) to these monthly counts.
    Returns the slope as an indicator of trend.
    If there is no increase, returns 0.0 (i.e. non-negative slope).
    """
    if len(all_transactions) < 2:
        return 0.0
    all_transactions = sorted(all_transactions, key=lambda t: t.date)
    monthly_counts: defaultdict[tuple[int, int], int] = defaultdict(int)
    for t in all_transactions:
        key = (t.date.year, t.date.month)
        monthly_counts[key] += 1
    keys = sorted(monthly_counts.keys(), key=lambda k: (k[0], k[1]))
    counts = [monthly_counts[k] for k in keys]
    x = np.arange(len(counts))
    slope: float
    if len(counts) < 2:
        return 0.0
    slope, _ = np.polyfit(x, counts, 1)
    # Instead of asserting strictly positive, return max(slope, 0)
    return max(float(slope), 0.0)


def weekly_spending_cycle(all_transactions: list[Transaction]) -> float:
    """
    Measures how much transaction amounts vary on a weekly basis with a flexible 2-3 day shift.
    Groups past transactions into weeks with slight flexibility
    (e.g., Friday transactions might count for Thursday-Saturday).
    Computes the coefficient of variation (std/mean) of weekly averages.
    A lower value suggests a stable weekly spending pattern.
    """
    if not all_transactions:
        return 0.0

    weekly_amounts = defaultdict(list)

    for t in all_transactions:
        week_number = (t.date - timedelta(days=t.date.weekday() % 3)).isocalendar()[1]
        # This adjusts week grouping, allowing slight shifts in weekday alignment (±2-3 days)
        weekly_amounts[week_number].append(t.amount)

    weekly_avgs = [mean(amounts) for amounts in weekly_amounts.values() if amounts]
    if len(weekly_avgs) < 2:
        return 0.0

    avg = mean(weekly_avgs)
    variation = stdev(weekly_avgs) if len(weekly_avgs) > 1 else 0.0
    return variation / avg if avg != 0 else 0.0


def seasonal_spending_cycle(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """
    Measures how much transaction amounts vary by month for a given vendor.
    Groups past transactions by month, computes each month's average, then returns
    the coefficient of variation (std/mean) of these averages.
    A lower value suggests a stable, seasonal pattern.
    """
    vendor_transactions = [t for t in all_transactions if t.name == transaction.name]
    if not vendor_transactions:
        return 0.0
    monthly_amounts = defaultdict(list)
    for t in vendor_transactions:
        monthly_amounts[t.date.month].append(t.amount)
    monthly_avgs = [mean(amounts) for amounts in monthly_amounts.values() if amounts]
    if len(monthly_avgs) < 2:
        return 0.0
    avg = mean(monthly_avgs)
    variation = stdev(monthly_avgs) if len(monthly_avgs) > 1 else 0.0
    return variation / avg if avg != 0 else 0.0


def get_days_since_last_transaction(transaction: Transaction, all_transactions: list[Transaction]) -> int:
    """Get the number of days since the last transaction with the same merchant"""
    same_merchant_transactions = [
        t for t in all_transactions if t.name == transaction.name and t.date < transaction.date
    ]

    if not same_merchant_transactions:
        return -1  # No previous transaction with the same merchant

    last_transaction = max(same_merchant_transactions, key=lambda t: t.date)
    return (transaction.date - last_transaction.date).days


def get_same_amount_ratio(
    transaction: Transaction, all_transactions: list[Transaction], tolerance: float = 0.05
) -> float:
    """
    Calculate the ratio of transactions with amounts within ±tolerance of the current transaction's amount.

    Args:
        transaction: The current transaction.
        all_transactions: List of all transactions for the same vendor.
        tolerance: Allowed variation in amounts (e.g., 0.05 for ±5%).

    Returns:
        Ratio of transactions with amounts within ±tolerance of the current transaction's amount.
    """
    if not all_transactions:
        return 0.0

    # Get the current transaction's amount
    current_amount = transaction.amount

    # Calculate the range of acceptable amounts
    lower_bound = current_amount * (1 - tolerance)
    upper_bound = current_amount * (1 + tolerance)

    # Count transactions within the acceptable range
    n_similar_amounts = sum(1 for t in all_transactions if lower_bound <= t.amount <= upper_bound)

    # Calculate the ratio
    return n_similar_amounts / len(all_transactions)


def trimmed_mean(values: Sequence[float], trim_percent: float = 0.1) -> float:
    """
    Compute a trimmed mean: remove the lowest and highest trim_percent of values.
    If there aren't enough values to trim, returns the standard mean.
    """
    converted_values = [float(x) for x in values]
    n = len(converted_values)
    if n == 0:
        return 0.0
    k = int(n * trim_percent)
    trimmed_values = sorted(converted_values)[k : n - k] if n > 2 * k else converted_values
    return mean(trimmed_values)


def get_transaction_intervals(transactions: list[Transaction]) -> dict[str, float]:
    """
    Extracts time-based features for recurring transactions.
    Returns:
      - avg_days_between_transactions: average days between transactions.
      - std_dev_days_between_transactions: sample standard deviation of intervals.
      - monthly_recurrence: ratio of intervals that are within 30±7 days.
      - same_weekday_ratio: ratio of transactions falling on the most common weekday.
      - same_amount: ratio of transactions with amounts within ±5% of the first transaction.
    """
    if len(transactions) < 2:
        return {
            "avg_days_between_transactions": 0.0,
            "std_dev_days_between_transactions": 0.0,
            "monthly_recurrence": 0.0,
            "same_weekday_ratio": 0.0,
            "same_amount": 0.0,
        }
    # Sort transactions by date
    dates = sorted([t.date for t in transactions])
    amounts = [t.amount for t in transactions]

    # Calculate intervals in days
    intervals = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]

    avg_days = mean(intervals)
    std_dev_days = stdev(intervals) if len(intervals) > 1 else 0.0

    # monthly recurrence: intervals that fall in 30 ± 7 days
    monthly_count = sum(1 for gap in intervals if 23 <= gap <= 37)
    monthly_recurrence = monthly_count / len(intervals) if intervals else 0.0

    # Instead of binary flag, compute ratio of most common weekday
    weekdays = [d.weekday() for d in dates]  # Monday=0 ... Sunday=6
    weekday_counts = Counter(weekdays)
    most_common_count = max(weekday_counts.values())
    same_weekday_ratio = most_common_count / len(weekdays)

    # same_amount: ratio of transactions with amount within ±5% of first transaction's amount
    base_amount = amounts[0] if amounts[0] != 0 else 1
    same_amount = sum(1 for amt in amounts if abs(amt - base_amount) / base_amount <= 0.05) / len(amounts)

    return {
        "avg_days_between_transactions": float(avg_days),
        "std_dev_days_between_transactions": float(std_dev_days),
        "monthly_recurrence": float(monthly_recurrence),
        "same_weekday_ratio": float(same_weekday_ratio),
        "same_amount": float(same_amount),
    }


def safe_interval_consistency(all_transactions: list[Transaction]) -> float:
    """
    Compute interval consistency for a given transaction using the intervals
    from previous transactions with the same vendor.

    The consistency is computed as:
        1 - (stdev(trimmed_intervals) / mean(trimmed_intervals))
    where trimmed_intervals are the intervals after clipping at the 5th and 95th percentiles.

    Returns 0 if there are fewer than 6 intervals or if the mean of the trimmed intervals is zero.
    """

    if len(all_transactions) < 2:
        # Not enough transactions to compute intervals
        return 0.0

    # Sort the filtered transactions by date
    dates = sorted([t.date for t in all_transactions])

    # Compute intervals (in days) between consecutive transactions
    intervals = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]

    if len(intervals) <= 5:
        # Not enough intervals to compute a robust consistency measure
        return 0.0

    # Clip intervals to remove outliers (5th to 95th percentile)
    lower_bound = np.percentile(intervals, 5)
    upper_bound = np.percentile(intervals, 95)
    trimmed_intervals = np.clip(intervals, lower_bound, upper_bound)

    m: float = float(mean(trimmed_intervals))
    if m == 0:
        return 0.0

    return float(1 - (stdev(trimmed_intervals) / m))


def get_vendor_recurrence_score(all_transactions: list[Transaction], total_transactions: int) -> float:
    """Compute a general recurrence score for a vendor instead of binary flags."""
    if total_transactions == 0:
        return 0.0
    return len(all_transactions) / total_transactions  # Proportion of transactions from this vendor


def get_enhanced_features(
    transaction: Transaction, all_transactions: list[Transaction], total_transactions: int
) -> dict:
    """Enhanced feature extraction with better temporal patterns and vendor analysis"""

    if not all_transactions:
        return defaultdict(float)

    # temporal features
    dates = sorted([t.date for t in all_transactions])
    amounts = [t.amount for t in all_transactions]
    intervals = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]

    # amount consistency
    amount_stats = {
        "amt_std": stdev(amounts) if len(amounts) > 1 else 0,
        "amt_med": median(amounts),
        "amt_iqr": np.subtract(*np.percentile(amounts, [75, 25])) if amounts else 0,
    }

    # interval patterns
    interval_stats = {
        "interval_std": stdev(intervals) if len(intervals) > 1 else 0,
        "interval_med": median(intervals) if intervals else 0,
        "interval_consistency": safe_interval_consistency(all_transactions),
    }

    # vendor analysis
    """Compute a general recurrence score for a vendor instead of binary flags."""

    vendor_features = {"proporption": get_vendor_recurrence_score(all_transactions, total_transactions)}

    # Transactions features
    pattern_features = {
        "day_of_month": transaction.date.day,
        "days_since_last": get_days_since_last_transaction(
            transaction, all_transactions
        ),  # get_days_since_last(transaction, all_transactions)
        "n_similar_last_90d": len([t for t in all_transactions if (transaction.date - t.date).days <= 90]),
    }

    return {
        **amount_stats,
        **interval_stats,
        **vendor_features,
        **pattern_features,
        "n_transactions": len(all_transactions),
        "same_amount_ratio": get_same_amount_ratio(transaction, all_transactions),
    }


# Define common subscription cycles (allowing ±3 days flexibility)
COMMON_CYCLES = [7, 14, 30, 90, 365]
CYCLE_RANGE = 3  # Allowed variation in cycle detection


def detect_common_interval(intervals: list[int]) -> bool:
    """
    Checks if the transaction intervals match common subscription cycles (with flexibility).
    """
    return any(any(abs(interval - cycle) <= CYCLE_RANGE for interval in intervals) for cycle in COMMON_CYCLES)


def get_transaction_stability_features(transactions: list[Transaction]) -> dict[str, float]:
    if len(transactions) < 2:
        return {
            "transaction_frequency": 0.0,
            "robust_interval_median": 0.0,
            "robust_interval_iqr": 0.0,
            "coefficient_of_variation_intervals": 0.0,
            "amount_variability_ratio": 0.0,
            "matches_common_cycle": 0.0,
            "recurring_confidence": 0.0,
        }

    # Sort transactions by date
    dates = sorted([t.date for t in transactions])
    amounts = [t.amount for t in transactions]
    company_names = [t.name for t in transactions]

    # Compute intervals (in days) between consecutive transactions
    intervals = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]
    intervals = sorted(intervals)

    # Compute robust median interval (using sorted intervals)
    robust_interval_median: float = float(median(intervals))
    if len(intervals) > 1:
        iqr_intervals: float = float(
            np.percentile(intervals, 75, method="midpoint") - np.percentile(intervals, 25, method="midpoint")
        )
    else:
        iqr_intervals = 0.0
    coefficient_of_variation_intervals: float = (
        iqr_intervals / robust_interval_median if robust_interval_median > 0 else 0.0
    )

    # Transaction frequency: number of transactions per month
    total_days = (dates[-1] - dates[0]).days
    months = max(total_days / 30, 1)
    transaction_frequency: float = float(len(transactions) / months)

    # Compute amount variability using robust measures
    robust_amount_median: float = float(median(amounts))
    if len(amounts) > 1:
        iqr_amounts: float = float(
            np.percentile(amounts, 75, method="midpoint") - np.percentile(amounts, 25, method="midpoint")
        )
    else:
        iqr_amounts = 0.0
    amount_variability_ratio: float = iqr_amounts / robust_amount_median if robust_amount_median > 0 else 0.0

    # Check if the transaction follows a common cycle
    matches_common_cycle = 1.0 if detect_common_interval(intervals) else 0.0

    # Compute recurring confidence by checking company name detection
    recurring_confidence = 0.0
    for name in company_names:
        company_features = detect_recurring_company(name)
        recurring_confidence = max(recurring_confidence, company_features["recurring_score"])

    return {
        "transaction_frequency": float(transaction_frequency),
        "robust_interval_median": float(robust_interval_median),
        "robust_interval_iqr": float(iqr_intervals),
        "coefficient_of_variation_intervals": float(coefficient_of_variation_intervals),
        "amount_variability_ratio": float(amount_variability_ratio),
        "matches_common_cycle": float(matches_common_cycle),
        "recurring_confidence": float(recurring_confidence),
    }


# Predefined lists of known recurring companies and keywords
KNOWN_RECURRING_COMPANIES = {
    "netflix",
    "spotify",
    "amazon prime",
    "hulu",
    "disney+",
    "youtube",
    "adobe",
    "microsoft",
    "verizon",
    "at&t",
    "t-mobile",
    "comcast",
    "spectrum",
    "onlyfans",
    "albert",
    "ipsy",
    "experian",
    "walmart+",
    "sirius xm",
    "pandora",
    "sezzle",
    "apple",
    "amazon+",
    "BET+",
    "HBO",
    "Credit Genie",
    "amazon kids+",
    "paramount+",
    "afterpay",
    "cricut",
}

UTILITY_KEYWORDS = {
    "energy",
    "power",
    "electric",
    "utility",
    "gas",
    "water",
    "sewer",
    "trash",
    "internet",
    "phone",
    "cable",
    "wifi",
    "broadband",
    "telecom",
    "member",
    "fitness",
    "gym",
    "insurance",
    "rent",
    "hoa",
    "subscription",
    "mobile",
    "pay",
    "light",
    "tv",
}

# Precompile regex patterns for performance
RECURRING_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(keyword) for keyword in KNOWN_RECURRING_COMPANIES) + r")\b", re.IGNORECASE
)

UTILITY_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(keyword) for keyword in UTILITY_KEYWORDS) + r")\b", re.IGNORECASE
)


def clean_company_name(name: str) -> str:
    """Normalize company name for better matching."""
    return re.sub(r"[^a-zA-Z0-9\s]", "", name).strip().lower()


def detect_recurring_company(company_name: str) -> dict[str, float]:
    """
    Detects if a company is likely to offer recurring payments (e.g., subscriptions, utilities).
     Returns a dictionary of features:
    - is_recurring_company: 1 if the company is known to offer recurring payments, else 0
    - is_utility_company: 1 if the company is a utility provider, else 0
    - recurring_score: Confidence score (0 to 1) based on keyword matches
    """
    cleaned_name = clean_company_name(company_name)

    # Check if the company is a known recurring company
    is_recurring_company = 1 if RECURRING_PATTERN.search(cleaned_name) else 0

    # Check if the company is a utility provider
    is_utility_company = 1 if UTILITY_PATTERN.search(cleaned_name) else 0

    # Calculate a recurring score based on keyword matches
    recurring_score = 0.0
    if is_recurring_company:
        recurring_score = 1.0
    elif is_utility_company:
        recurring_score = 0.8  # Utilities are highly likely to be recurring
    else:
        # Check for partial matches (e.g., "Netflix Inc.")
        for keyword in KNOWN_RECURRING_COMPANIES:
            if keyword in cleaned_name:
                recurring_score = max(recurring_score, 0.7)  # Partial match confidence

    return {
        "is_recurring_company": is_recurring_company,
        "is_utility_company": is_utility_company,
        "recurring_score": recurring_score,
    }


def detect_subscription_pattern(all_transactions: list[Transaction]) -> dict[str, float]:
    """
    Detects subscription-like payment patterns based on:
    - Regular intervals (e.g., monthly)
    - Similar amounts (allowing for small variations)
    - Flexible timing (within a one-week range)

    Returns a dictionary of features:
    - subscription_score: Likelihood of being a subscription (0 to 1)
    - interval_consistency: How consistent the intervals are (0 to 1)
    - amount_consistency: How consistent the amounts are (0 to 1)
    """
    if len(all_transactions) < 2:
        return {
            "subscription_score": 0.0,
            "interval_consistency": 0.0,
            "amount_consistency": 0.0,
            "detected_cycle": 0.0,
        }

    # Sort transactions by date
    all_transactions.sort(key=lambda t: t.date)
    dates = [t.date for t in all_transactions]
    amounts = [t.amount for t in all_transactions]

    # Compute intervals between transactions (in days)
    intervals = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]
    if not intervals:
        return {
            "subscription_score": 0.0,
            "interval_consistency": 0.0,
            "amount_consistency": 0.0,
            "detected_cycle": 0.0,
        }

    median_interval: float = float(median(intervals))

    # Define flexible subscription cycles with ±3-day tolerance
    base_cycles = [7, 14, 30, 90, 365]  # Weekly, biweekly, monthly, quarterly, yearly
    cycle_ranges = {cycle: (cycle - 3, cycle + 3) for cycle in base_cycles}

    # Find the closest matching cycle based on range
    detected_cycle = min(
        base_cycles,
        key=lambda c: abs(median_interval - c)
        if cycle_ranges[c][0] <= median_interval <= cycle_ranges[c][1]
        else float("inf"),
    )

    # Adaptive threshold: Allow ±15% variation in interval
    interval_deviation_threshold = 0.15 * detected_cycle
    interval_consistency = sum(
        1 for interval in intervals if abs(interval - median_interval) <= interval_deviation_threshold
    ) / len(intervals)

    # Adaptive amount consistency: Allow up to ±15% variation
    median_amount = median(amounts)
    amount_deviation_threshold = 0.15 * median_amount
    amount_consistency = sum(
        1 for amount in amounts if abs(amount - median_amount) <= amount_deviation_threshold
    ) / len(amounts)

    # Combine into a final subscription score
    subscription_score = (interval_consistency + amount_consistency) / 2

    return {
        "subscription_score": subscription_score,
        "interval_consistency": interval_consistency,
        "amount_consistency": amount_consistency,
        "detected_cycle": float(detected_cycle) if detected_cycle != float("inf") else 0.0,  # Avoid invalid cycle
    }


def detect_non_recurring_pattern(all_transactions: list[Transaction]) -> dict[str, float]:
    """
    Detects patterns typical of non-recurring transactions based on:
    - Irregular intervals between transactions.
    - Inconsistent payment amounts.

    Returns a dictionary of features:
    - is_non_recurring: 1 if the transaction is likely non-recurring, else 0.
    - irregular_interval_score: Score indicating irregularity in transaction intervals (0 to 1).
    - inconsistent_amount_score: Score indicating inconsistency in payment amounts (0 to 1).
    - non_recurring_score: Combined score indicating likelihood of being non-recurring (0 to 1).
    """
    if not all_transactions or len(all_transactions) < 2:
        return {
            "irregular_interval_score": 0.0,
            "inconsistent_amount_score": 0.0,
            "non_recurring_score": 0.0,
        }

    # Sort transactions by date
    sorted_transactions = sorted(all_transactions, key=lambda t: t.date)
    dates = [t.date for t in sorted_transactions]
    amounts = [t.amount for t in sorted_transactions]

    # Calculate intervals between transactions (in days)
    intervals = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]

    # Calculate irregularity in intervals
    interval_std = stdev(intervals) if len(intervals) > 1 else 0.0
    median_interval = median(intervals) if intervals else 0.0
    irregular_interval_score = min(interval_std / (median_interval + 1e-8), 1.0)  # Normalize to [0, 1]

    # Calculate inconsistency in amounts
    amount_std = stdev(amounts) if len(amounts) > 1 else 0.0
    median_amount = median(amounts) if amounts else 0.0
    inconsistent_amount_score = min(amount_std / (median_amount + 1e-8), 1.0)  # Normalize to [0, 1]

    # Combine scores into a non-recurring score
    non_recurring_score = (irregular_interval_score + inconsistent_amount_score) / 2

    # Threshold to classify as non-recurring

    return {
        "irregular_interval_score": irregular_interval_score,
        "inconsistent_amount_score": inconsistent_amount_score,
        "non_recurring_score": non_recurring_score,
    }


def one_time_features(all_transactions: list[Transaction]) -> dict:
    """Identifies patterns typical of one-time purchases with safe calculations"""
    # Convert to list first to handle empty cases
    months = [t.date.month for t in all_transactions]

    # Safe standard deviation calculation
    try:
        date_std = stdev(months) if len(months) >= 2 else 0
    except StatisticsError:
        date_std = 0

    return {
        "varying_amounts": 1 if len({t.amount for t in all_transactions}) / len(all_transactions) > 0.7 else 0,
        "irregular_dates": 1 if date_std > 1.5 else 0,
    }


def merchant_category_features(name: str) -> dict:
    """Identifies merchants unlikely to have recurring payments"""
    cleaned = name.lower()
    return {
        "is_retail": 1
        if any(kw in cleaned for kw in {"amazon", "walmart", "store", "shop", "motorsports", "gallery"})
        else 0,
        "is_entertainment": 1
        if any(kw in cleaned for kw in {"movie", "theatre", "bet", "nfl", "roku", "starz"})
        else 0,
    }


# Helper: Calculate days between dates in a transaction list
def _get_intervals(transactions: list[Transaction]) -> list[int]:
    sorted_dates = sorted([t.date for t in transactions])
    return [(sorted_dates[i] - sorted_dates[i - 1]).days for i in range(1, len(sorted_dates))]


def proportional_timing_deviation(
    transaction: Transaction, transactions: list[Transaction], days_flexibility: int = 7
) -> float:
    """Measures deviation from historical median interval, allowing a flexible timing window"""

    if len(transactions) < 2:
        return 0.0

    intervals = _get_intervals(transactions)
    median_interval: float = float(median(intervals))
    current_interval: int = (transaction.date - transactions[-1].date).days

    # Allow a ±7 day window for delay flexibility
    if abs(current_interval - median_interval) <= days_flexibility:
        return 1.0  # Fully consistent if within range

    if median_interval == 0:
        return 0.0

    return 1 - (abs(current_interval - median_interval) / median_interval)


def amount_similarity(transaction: Transaction, transactions: list[Transaction], tolerance: float = 0.05) -> float:
    """
    Calculate the ratio of transactions with amounts within ±tolerance of the current transaction's amount.
    """
    if not transactions:
        return 0.0
    current_amount = transaction.amount
    lower_bound = current_amount * (1 - tolerance)
    upper_bound = current_amount * (1 + tolerance)
    similar_count = sum(1 for t in transactions if lower_bound <= t.amount <= upper_bound)
    return float(similar_count) / float(len(transactions))


def amount_coefficient_of_variation(transactions: list[Transaction]) -> float:
    """
    Measures amount consistency using the population standard deviation.
    Returns (population stdev / mean). If not enough data, returns 0.0.
    """
    amounts = [t.amount for t in transactions]
    if len(amounts) < 2 or mean(amounts) == 0:
        return 0.0
    # Use population std (ddof=0) to match test expectations.
    pop_std = np.std(amounts, ddof=0)
    return float(pop_std / mean(amounts))


def get_features(transaction: Transaction, all_transactions: list[Transaction]) -> dict[str, float | int]:
    """
    Extract numerical features from a transaction for machine learning.
    """
    time_features = get_transaction_intervals(all_transactions)
    enchanced_features = get_enhanced_features(transaction, all_transactions, len(all_transactions))
    stability_features = get_transaction_stability_features(all_transactions)
    recurring_features = detect_recurring_company(transaction.name)
    subscription_features = detect_subscription_pattern(all_transactions)
    non_recurring_features = detect_non_recurring_pattern(all_transactions)
    detect_one_time_features = one_time_features(all_transactions)
    frequency_features_cons = frequency_features(all_transactions)
    merchant_categories_features = merchant_category_features(transaction.name)

    return {
        "likely_same_amount": amount_similarity(transaction, all_transactions),
        "percent_transactions_same_amount": get_percent_transactions_same_amount(transaction, all_transactions),

        "normalized_days_difference": normalized_days_difference(transaction, all_transactions),
        "amount_stability_score": amount_stability_score(all_transactions),
        "amount_z_score": amount_z_score(transaction, all_transactions),
        "weekly_spendings ": weekly_spending_cycle(all_transactions),
        "vendor_recurrence_trend": vendor_recurrence_trend(all_transactions),
        "seasonal_spending_cycle": seasonal_spending_cycle(transaction, all_transactions),
        "recurrence_interval_variance": recurrence_interval_variance(all_transactions),
        **frequency_features_cons,
        **non_recurring_features,  # Merges non-recurring pattern features
        **time_features,  # Merges new time-based features
        "amount_ratio": get_same_amount_ratio(transaction, all_transactions),
        "amount_coefficient_of_variation": amount_coefficient_of_variation(all_transactions),
        "proportional_timing_deviation": proportional_timing_deviation(transaction, all_transactions),
        **recurring_features,  # Merges recurring company features
        **merchant_categories_features,  # Merges merchant category features
        **detect_one_time_features,  # Merges one-time purchase features
        **subscription_features,  # Merges subscription-based features
        **enchanced_features,  # Merges new enhanced features
        **stability_features,  # Merges new stability-based features
        # "days_since_last_transaction": get_days_since_last_transaction(transaction, all_transactions),
        # **measure_transaction_freq

        "ends_in_99": get_ends_in_99(transaction),
        "amount": transaction.amount,
        "same_day_exact": get_n_transactions_same_day(transaction, all_transactions, 0),
        "pct_transactions_same_day": get_pct_transactions_same_day(transaction, all_transactions, 0),
        "same_day_off_by_1": get_n_transactions_same_day(transaction, all_transactions, 1),
        "same_day_off_by_2": get_n_transactions_same_day(transaction, all_transactions, 2),
        "14_days_apart_exact": get_n_transactions_days_apart(transaction, all_transactions, 14, 0),
        "14_days_apart_off_by_1": get_n_transactions_days_apart(transaction, all_transactions, 14, 1),
        "7_days_apart_exact": get_n_transactions_days_apart(transaction, all_transactions, 7, 0),
        "7_days_apart_off_by_1": get_n_transactions_days_apart(transaction, all_transactions, 7, 1),
        "is_insurance": get_is_insurance(transaction),
        "is_utility": get_is_utility(transaction),
        "is_phone": get_is_phone(transaction),
        "is_always_recurring": get_is_always_recurring(transaction),

    }
