import re
from collections import Counter

import numpy as np

from recur_scan.transactions import Transaction
from recur_scan.utils import get_day, parse_date


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
    transaction_date = parse_date(transaction.date)

    # Pre-calculate bounds for faster checking
    lower_remainder = n_days_apart - n_days_off
    upper_remainder = n_days_off

    for t in all_transactions:
        t_date = parse_date(t.date)
        days_diff = abs((t_date - transaction_date).days)

        # Skip if the difference is less than minimum required
        if days_diff < n_days_apart - n_days_off:
            continue

        # Check if the difference is close to any multiple of n_days_apart
        remainder = days_diff % n_days_apart

        if remainder <= upper_remainder or remainder >= lower_remainder:
            n_txs += 1

    return n_txs


def get_pct_transactions_days_apart(
    transaction: Transaction, all_transactions: list[Transaction], n_days_apart: int, n_days_off: int
) -> float:
    """
    Get the percentage of transactions in all_transactions that are within
    n_days_off of being n_days_apart from transaction
    """
    return get_n_transactions_days_apart(transaction, all_transactions, n_days_apart, n_days_off) / len(
        all_transactions
    )


def get_n_transactions_same_day(transaction: Transaction, all_transactions: list[Transaction], n_days_off: int) -> int:
    """Get the number of transactions in all_transactions that are on the same day of the month as transaction"""
    return len([t for t in all_transactions if abs(get_day(t.date) - get_day(transaction.date)) <= n_days_off])


def get_pct_transactions_same_day(
    transaction: Transaction, all_transactions: list[Transaction], n_days_off: int
) -> float:
    """Get the percentage of transactions in all_transactions that are on the same day of the month as transaction"""
    return get_n_transactions_same_day(transaction, all_transactions, n_days_off) / len(all_transactions)


def get_ends_in_99(transaction: Transaction) -> bool:
    """Check if the transaction amount ends in 99"""
    return abs((transaction.amount * 100) % 100 - 99) < 0.001


def get_n_transactions_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> int:
    """Get the number of transactions in all_transactions with the same amount as transaction"""
    return len([t for t in all_transactions if t.amount == transaction.amount])


def get_percent_transactions_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Get the percentage of transactions in all_transactions with the same amount as transaction"""
    if not all_transactions:
        return 0.0
    n_same_amount = len([t for t in all_transactions if t.amount == transaction.amount])
    return n_same_amount / len(all_transactions)


def get_transaction_z_score(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Get the z-score of the transaction amount compared to the mean and standard deviation of all_transactions."""
    all_amounts = [t.amount for t in all_transactions]
    # if the standard deviation is 0, return 0
    try:
        std_dev = float(np.std(all_amounts))
    except Exception:
        std_dev = 0.0
    if abs(std_dev) < 1e-8:
        return 0.0
    return (transaction.amount - float(np.mean(all_amounts))) / std_dev


#
# new features
#

# ai new features

# ——— Basic Counts ———


def count_transactions(all_transactions: list[Transaction]) -> int:
    """Total number of transactions for this user/name."""
    return len(all_transactions)


# ——— Time-Interval Features ———


def days_since_last(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Days since the previous transaction (-1.0 if none)."""
    dates = sorted(parse_date(t.date) for t in all_transactions)
    cur = parse_date(transaction.date)
    prev = [d for d in dates if d < cur]
    return (cur - max(prev)).days if prev else -1.0


def days_until_next(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Days until the next transaction (-1.0 if none)."""
    dates = sorted(parse_date(t.date) for t in all_transactions)
    cur = parse_date(transaction.date)
    fut = [d for d in dates if d > cur]
    return (min(fut) - cur).days if fut else -1.0


def mean_days_between(all_transactions: list[Transaction]) -> float:
    """Mean interval (in days) between successive transactions."""
    dates = sorted(parse_date(t.date) for t in all_transactions)
    if len(dates) < 2:
        return -1.0
    diffs = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]
    return float(np.mean(diffs))


def std_days_between(all_transactions: list[Transaction]) -> float:
    """Std. dev. of intervals (in days) between successive transactions."""
    dates = sorted(parse_date(t.date) for t in all_transactions)
    if len(dates) < 2:
        return -1.0
    diffs = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]
    try:
        return float(np.std(diffs, ddof=1))
    except Exception:
        return 0.0


def regularity_score(all_transactions: list[Transaction]) -> float:
    """
    Ratio of mean interval to its stddev.
    Higher → more evenly spaced (common in recurring).
    """
    mean = mean_days_between(all_transactions)
    try:
        std_dev = std_days_between(all_transactions)
    except Exception:
        std_dev = 0.0
    if mean == -1.0 or std_dev == -1.0 or abs(std_dev) < 1e-8:
        return -1.0
    return mean / std_dev


def days_since_last_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Days since the previous transaction with the same amount (-1 if none)."""
    dates = sorted(parse_date(t.date) for t in all_transactions if t.amount == transaction.amount)
    cur = parse_date(transaction.date)
    prev = [d for d in dates if d < cur]
    return (cur - max(prev)).days if prev else -1.0


def days_until_next_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Days until the next transaction with the same amount (-1 if none)."""
    dates = sorted(parse_date(t.date) for t in all_transactions if t.amount == transaction.amount)
    cur = parse_date(transaction.date)
    fut = [d for d in dates if d > cur]
    return (min(fut) - cur).days if fut else -1.0


def mean_days_between_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Mean interval (in days) between successive transactions with the same amount."""
    dates = sorted(parse_date(t.date) for t in all_transactions if t.amount == transaction.amount)
    if len(dates) < 2:
        return -1.0
    diffs = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]
    return float(np.mean(diffs))


def std_days_between_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Std. dev. of intervals (in days) between successive transactions with the same amount."""
    dates = sorted(parse_date(t.date) for t in all_transactions if t.amount == transaction.amount)
    if len(dates) < 2:
        return -1.0
    diffs = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]
    try:
        return float(np.std(diffs, ddof=1))
    except Exception:
        return 0.0


def regularity_score_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """
    Ratio of mean interval to its stddev.
    Higher → more evenly spaced (common in recurring).
    """
    mean = mean_days_between_same_amount(transaction, all_transactions)
    std_dev = std_days_between_same_amount(transaction, all_transactions)
    if mean == -1.0 or std_dev == -1.0 or std_dev == 0:
        return -1.0
    return mean / std_dev


def transaction_span_days(all_transactions: list[Transaction]) -> float:
    """Total span (in days) from first to last transaction."""
    dates = [parse_date(t.date) for t in all_transactions]
    return (max(dates) - min(dates)).days if dates else -1.0


# ——— Recency / Frequency ———


def count_last_n_days(transaction: Transaction, all_transactions: list[Transaction], n: int = 30) -> int:
    """
    Count of transactions in the past n days *before* this transaction.
    """
    cur = parse_date(transaction.date)
    prior = [t for t in all_transactions if 0 < (cur - parse_date(t.date)).days <= n]
    return len(prior)


def count_last_28_days(transaction: Transaction, all_transactions: list[Transaction]) -> int:
    return count_last_n_days(transaction, all_transactions, n=28)


def count_last_35_days(transaction: Transaction, all_transactions: list[Transaction]) -> int:
    return count_last_n_days(transaction, all_transactions, n=35)


def count_last_90_days(transaction: Transaction, all_transactions: list[Transaction]) -> int:
    return count_last_n_days(transaction, all_transactions, n=90)


# ——— Amount-Based Features ———


def mean_amount(all_transactions: list[Transaction]) -> float:
    """Average transaction amount for this group."""
    amounts = [t.amount for t in all_transactions]
    return float(np.mean(amounts)) if amounts else -1.0


def std_amount(all_transactions: list[Transaction]) -> float:
    """Std. dev. of transaction amounts."""
    amounts = [t.amount for t in all_transactions]
    if len(amounts) <= 1:
        return 0.0
    try:
        return float(np.std(amounts, ddof=1))
    except Exception:
        return 0.0


def amount_diff_from_mean(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Absolute difference between this amount and the group mean."""
    mean = mean_amount(all_transactions)
    return abs(transaction.amount - mean) if mean != -1.0 else -1.0


def relative_amount_diff(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """
    (this_amount - mean) / mean;
    recurring payments often have small relative diffs.
    """
    mean = mean_amount(all_transactions)
    if mean == -1.0 or mean == 0:
        return -1.0
    return (transaction.amount - mean) / mean


# ——— Calendar Features ———


def day_of_week(transaction: Transaction) -> int:
    """0=Monday … 6=Sunday."""
    return parse_date(transaction.date).weekday()


def is_weekend(transaction: Transaction) -> int:
    """1 if Saturday/Sunday else 0."""
    return int(day_of_week(transaction) >= 5)


def day_of_month(transaction: Transaction) -> int:
    """1-31."""
    return parse_date(transaction.date).day


def month_of_year(transaction: Transaction) -> int:
    """1-12."""
    return parse_date(transaction.date).month


def same_day_of_month_count(transaction: Transaction, all_transactions: list[Transaction]) -> int:
    """
    How many transactions in this group fall on the same
    day-of-month as the current one.
    """
    dom = day_of_month(transaction)
    return sum(1 for t in all_transactions if parse_date(t.date).day == dom)


def fraction_same_day_of_month(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """same_day_of_month_count / total_count."""
    cnt = same_day_of_month_count(transaction, all_transactions)
    total = count_transactions(all_transactions)
    return cnt / total if total else -1.0


# —— 1. Periodic-tolerance features ——


def frac_intervals_within(txns: list[Transaction], period_days: int, tol_days: int = 3) -> float:
    """
    What fraction of successive-txn intervals fall within
    [period_days - tol_days, period_days + tol_days]?
    """
    dates = sorted(parse_date(t.date) for t in txns)
    if len(dates) < 2:
        return -1.0
    diffs = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]
    good = sum(1 for d in diffs if period_days - tol_days <= d <= period_days + tol_days)
    return good / len(diffs)


def monthly_tolerance(txns: list[Transaction]) -> float:
    """Monthly ≈30 days ±5."""
    return frac_intervals_within(txns, period_days=30, tol_days=5)


def quarterly_tolerance(txns: list[Transaction]) -> float:
    """Quarterly ≈90 days ±10."""
    return frac_intervals_within(txns, period_days=90, tol_days=10)


def weekly_tolerance(txns: list[Transaction]) -> float:
    """Weekly ≈7 days ±1."""
    return frac_intervals_within(txns, period_days=7, tol_days=1)


def biweekly_tolerance(txns: list[Transaction]) -> float:
    """Biweekly ≈14 days ±2."""
    return frac_intervals_within(txns, period_days=14, tol_days=2)


# —— 2. Month-span / coverage features ——


def span_months(txns: list[Transaction]) -> float:
    """Number of distinct calendar-months covered by this group."""
    dates = [parse_date(t.date) for t in txns]
    if not dates:
        return -1.0
    ys = [d.year for d in dates]
    ms = [d.month for d in dates]
    unique_months = set(zip(ys, ms, strict=True))
    return len(unique_months)


def total_span_months(txns: list[Transaction]) -> float:
    """
    Approximate span in months = (last - first).days / 30,
    rounded up to 1 if <30 days.
    """
    dates = sorted(parse_date(t.date) for t in txns)
    if len(dates) < 2:
        return 1
    span_days = (dates[-1] - dates[0]).days
    return max(1, int(np.ceil(span_days / 30)))


def fraction_active_months(txns: list[Transaction]) -> float:
    """
    # distinct months with ≥1 txn divided by total months spanned.
    Catches patterns that “skip” months but are still recurring.
    """
    covered = span_months(txns)
    total = total_span_months(txns)
    return covered / total if total else -1.0


def avg_txn_per_month(txns: list[Transaction]) -> float:
    """Average count of txns per spanned month."""
    total = total_span_months(txns)
    return len(txns) / total if total else -1.0


# —— 3. Modal-amount features ——


def modal_amount(txns: list[Transaction]) -> float:
    """The most-common transaction amount in this group."""
    amounts = [t.amount for t in txns]
    if not amounts:
        return -1.0
    return Counter(amounts).most_common(1)[0][0]


def fraction_modal_amount(txns: list[Transaction]) -> float:
    """
    Fraction of transactions whose amount equals the modal amount.
    Recurring will often be 1.0 here.
    """
    modal = modal_amount(txns)
    total = len(txns)
    if total == 0 or modal == -1.0:
        return -1.0
    cnt = sum(1 for t in txns if t.amount == modal)
    return cnt / total


def amount_matches_modal(txn: Transaction, txns: list[Transaction]) -> float:
    """1.0 if this txn's amount = modal amount, else 0.0."""
    modal = modal_amount(txns)
    return float(txn.amount == modal)


# —— 4. Mode-interval features ——


def mode_interval(txns: list[Transaction]) -> float:
    """Most-common gap (in days) between successive txns."""
    dates = sorted(parse_date(t.date) for t in txns)
    if len(dates) < 2:
        return -1.0
    diffs = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]
    return Counter(diffs).most_common(1)[0][0]


def fraction_mode_interval(txns: list[Transaction]) -> float:
    """
    Fraction of all successive-txn gaps that equal the mode.
    If >0.8, that's a very strong “regular” signal.
    """
    dates = sorted(parse_date(t.date) for t in txns)
    if len(dates) < 2:
        return -1.0
    diffs = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]
    _, freq = Counter(diffs).most_common(1)[0]
    return freq / len(diffs)


# ——— 1. Interval-deviation features ———


def prev_interval_dev_from_mean(txn: Transaction, txns: list[Transaction]) -> float:
    """days_since_last - mean_interval"""
    prev = days_since_last(txn, txns)
    mean = mean_days_between(txns)
    return prev - mean if prev != -1.0 and mean != -1.0 else -1.0


def next_interval_dev_from_mean(txn: Transaction, txns: list[Transaction]) -> float:
    nxt = days_until_next(txn, txns)
    mean = mean_days_between(txns)
    return nxt - mean if nxt != -1.0 and mean != -1.0 else -1.0


def prev_interval_dev_from_mode(txn: Transaction, txns: list[Transaction]) -> float:
    prev = days_since_last(txn, txns)
    mode = mode_interval(txns)
    return prev - mode if prev != -1.0 and mode != -1.0 else -1.0


def next_interval_dev_from_mode(txn: Transaction, txns: list[Transaction]) -> float:
    nxt = days_until_next(txn, txns)
    mode = mode_interval(txns)
    return nxt - mode if nxt != -1.0 and mode != -1.0 else -1.0


# Boolean “within tolerance” flags for this txn
def prev_within_monthly_tol(txn: Transaction, txns: list[Transaction]) -> float:
    d = days_since_last(txn, txns)
    return float(25 <= d <= 35) if d != -1.0 else 0.0


def next_within_monthly_tol(txn: Transaction, txns: list[Transaction]) -> float:
    d = days_until_next(txn, txns)
    return float(25 <= d <= 35) if d != -1.0 else 0.0


# ——— 2. Modal-day-of-month features ———


def modal_day_of_month(txns: list[Transaction]) -> float:
    dates = [parse_date(t.date) for t in txns]
    doms = [d.day for d in dates]
    return Counter(doms).most_common(1)[0][0] if doms else -1.0


def dom_diff_from_modal(txn: Transaction, txns: list[Transaction]) -> float:
    dom = parse_date(txn.date).day
    modal = modal_day_of_month(txns)
    return abs(dom - modal) if modal != -1.0 else -1.0


def is_modal_dom(txn: Transaction, txns: list[Transaction]) -> float:
    return float(parse_date(txn.date).day == modal_day_of_month(txns))


# ——— 3. Amount-rank & deviation features ———


def amount_diff_from_modal(txn: Transaction, txns: list[Transaction]) -> float:
    modal = modal_amount(txns)
    return abs(txn.amount - modal) if modal != -1.0 else -1.0


def rel_amount_diff_from_modal(txn: Transaction, txns: list[Transaction]) -> float:
    modal = modal_amount(txns)
    if modal == -1.0 or modal == 0:
        return -1.0
    return (txn.amount - modal) / modal


def amount_frequency_rank(txn: Transaction, txns: list[Transaction]) -> float:
    """1 = modal amount, 2 = second-most, etc."""
    counts = Counter(t.amount for t in txns)
    # sort by descending freq, tie-break by amount
    ranked = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    for rank, (amt, _) in enumerate(ranked, start=1):
        if amt == txn.amount:
            return rank
    return -1.0


def amount_freq_fraction(txn: Transaction, txns: list[Transaction]) -> float:
    counts = Counter(t.amount for t in txns)
    total = len(txns)
    return counts.get(txn.amount, 0) / total if total else -1.0


# ——— 4. Calendar-month local density features ———


def txns_in_same_month(txn: Transaction, txns: list[Transaction]) -> int:
    """Count of transactions for this vendor in the txn's calendar-month."""
    d = parse_date(txn.date)
    same = [t for t in txns if (parse_date(t.date).year, parse_date(t.date).month) == (d.year, d.month)]
    return len(same)


def frac_txns_in_same_month(txn: Transaction, txns: list[Transaction]) -> float:
    tot = len(txns)
    return txns_in_same_month(txn, txns) / tot if tot else -1.0


# ——— 5. Timeline-position features ———


def days_since_group_start(txn: Transaction, txns: list[Transaction]) -> float:
    dates = sorted(parse_date(t.date) for t in txns)
    if not dates:
        return -1.0
    return (parse_date(txn.date) - dates[0]).days


def position_in_span(txn: Transaction, txns: list[Transaction]) -> float:
    span = (max(parse_date(t.date) for t in txns) - min(parse_date(t.date) for t in txns)).days
    ds = days_since_group_start(txn, txns)
    return ds / span if span and ds != -1.0 else -1.0


# my new features


def n_small_transactions(all_transactions: list[Transaction], threshold: float = 20) -> int:
    """Number of transactions with amount less than threshold."""
    return len([t for t in all_transactions if t.amount <= threshold])


def pct_small_transactions(all_transactions: list[Transaction], threshold: float = 20) -> float:
    """Percentage of transactions with amount less than threshold."""
    return n_small_transactions(all_transactions, threshold) / len(all_transactions)


def n_small_transactions_not_this_amount(
    transaction: Transaction, all_transactions: list[Transaction], threshold: float = 20
) -> int:
    """Number of transactions with amount less than threshold that are not the same amount as the current tx."""
    return len([t for t in all_transactions if t.amount <= threshold and t.amount != transaction.amount])


def pct_small_transactions_not_this_amount(
    transaction: Transaction, all_transactions: list[Transaction], threshold: float = 20
) -> float:
    """Percentage of transactions with amount less than threshold that are not the same amount as the current tx."""
    return n_small_transactions_not_this_amount(transaction, all_transactions, threshold) / len(all_transactions)


def ends_in_00(transaction: Transaction) -> bool:
    """Check if the transaction amount ends in 00."""
    return abs((transaction.amount * 100) % 100 - 00) < 0.001


def is_likely_subscription_amount(transaction: Transaction) -> bool:
    """Check if the transaction amount is likely a subscription amount."""
    return transaction.amount in [0.99, 1.99, 2.99, 4.99, 5.99, 9.99, 14.99, 19.99, 24.99, 29.99, 34.99, 39.99]


def is_amazon_prime(transaction: Transaction) -> bool:
    """Check if the transaction is an Amazon Prime payment."""
    return any(company in transaction.name.lower() for company in ["amazon prime", "amazon.ca prime"])


def is_amazon_prime_video(transaction: Transaction) -> bool:
    """Check if the transaction is an Amazon Prime Video payment."""
    return "amazon prime video" in transaction.name.lower()


def is_apple(transaction: Transaction) -> bool:
    """Check if the transaction is an Apple payment."""
    return "apple" in transaction.name.lower()


def is_loan_company(transaction: Transaction) -> bool:
    """Check if the transaction is a loan company payment."""
    return any(loan_company in transaction.name.lower() for loan_company in ["lending", "credit ninja", "creditninja"])


def is_pay_in_four_company(transaction: Transaction) -> bool:
    """Check if the transaction is a loan company payment."""
    return any(loan_company in transaction.name.lower() for loan_company in ["afterpay", "sezzle"])


def is_cash_advance_company(transaction: Transaction) -> bool:
    """Check if the transaction is a loan company payment."""
    return any(
        loan_company in transaction.name.lower()
        for loan_company in [
            "empower",
            "brigit",
            "cleo",
            "credit genie",
            "creditgenie",
            "dave",
            "albert",
            "moneylion",
            "money lion",
        ]
    )


def is_phone_company(transaction: Transaction) -> bool:
    """Check if the transaction is a phone company payment."""
    return any(
        phone_company in transaction.name.lower() for phone_company in ["verizon", "t-mobile", "wireless", "sprint"]
    )


def is_subscription_company(transaction: Transaction) -> bool:
    """Check if the transaction is a subscription company payment."""
    return any(
        subscription_company in transaction.name.lower()
        for subscription_company in [
            "spotify",
            "spectrum",
            "comcast",
            "youtube premium",
            "espn+",
            "amazon music",
            "audible",
            "netflix",
            "disney+",
            "bet+",
            "hulu",
            "hbo max",
            "peacock",
            "paramount+",
            "showtime",
            "walmart+",
            "amazon kids+",
            "starz",
            "twitch",
            "wix",
            "linkedin",
            "xfinity",
        ]
    )


def is_usually_subscription_company(transaction: Transaction) -> bool:
    """Check if the transaction is a usually a subscription company payment."""
    return any(
        subscription_company in transaction.name.lower()
        for subscription_company in [
            "membership",
            "fitness",
            "gym",
            "club",
            "monthly",
            "property",
            "credit",
            "storage",
            "amazon digital",
            "amazon kindle",
            "disney",
            "siriusxm",
            "adobe",
            "youtube",
            "patreon",
            "google",
            "directv",
            "rocket money",
        ]
    )


def is_utility_company(transaction: Transaction) -> bool:
    """Check if the transaction is a utility company payment."""
    return any(
        utility_company in transaction.name.lower()
        for utility_company in ["utility", "utilities", "energy", "electric", "water", "pg&e", "municipal"]
    )


def is_insurance_company(transaction: Transaction) -> bool:
    """Check if the transaction is an insurance company payment."""
    return any(
        insurance_company in transaction.name.lower()
        for insurance_company in [
            "insurance",
            "geico",
            "progressive",
            "allstate",
            "state farm",
            "farmers",
            "liberty mutual",
        ]
    )


def is_carwash_company(transaction: Transaction) -> bool:
    """Check if the transaction is a carwash company payment."""
    return any(carwash_company in transaction.name.lower() for carwash_company in [" wash", "carwash"])


def is_rental_company(transaction: Transaction) -> bool:
    """Check if the transaction is a rental company payment."""
    return any(rentals_company in transaction.name.lower() for rentals_company in ["rent", "property"])


def n_monthly_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> int:
    """Return the number of months with the same amount as the current transaction."""
    months = []
    for t in all_transactions:
        if t.amount == transaction.amount:
            date = parse_date(t.date)
            months.append(f"{date.month}-{date.year}")
    return len(set(months))


def pct_monthly_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Return the percentage of months with the same amount as the current transaction."""
    return n_monthly_same_amount(transaction, all_transactions) / get_n_transactions_same_amount(
        transaction, all_transactions
    )


def n_consecutive_months_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> int:
    """Return the number of consecutive months with the same amount as the current transaction."""
    same_amount_dates = [parse_date(t.date) for t in all_transactions if t.amount == transaction.amount]
    if not same_amount_dates:
        return 0
    # return 0 if there are multiple transactions in the same month
    tx_month = parse_date(transaction.date).month
    tx_year = parse_date(transaction.date).year
    if sum(1 for d in same_amount_dates if d.month == tx_month and d.year == tx_year) > 1:
        return 0
    consecutive_months = 0
    # go back one month at a time and check if there is one transaction in that month
    month_delta = -1
    while True:
        prev_month = tx_month + month_delta
        prev_year = tx_year if prev_month > 0 else tx_year - 1
        prev_month = 12 if prev_month == 0 else prev_month
        if sum(1 for d in same_amount_dates if d.month == prev_month and d.year == prev_year) == 1:
            consecutive_months += 1
        else:
            break
        month_delta -= 1
    # now go forward one month at a time and check if there is one transaction in that month
    month_delta = 1
    while True:
        next_month = tx_month + month_delta
        next_year = tx_year if next_month <= 12 else tx_year + 1
        next_month = 1 if next_month == 12 else next_month
        if sum(1 for d in same_amount_dates if d.month == next_month and d.year == next_year) == 1:
            consecutive_months += 1
        else:
            break
        month_delta += 1
    return consecutive_months


def pct_consecutive_months_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Return the percentage of consecutive months with the same amount as the current transaction."""
    return n_consecutive_months_same_amount(transaction, all_transactions) / get_n_transactions_same_amount(
        transaction, all_transactions
    )


def n_same_day_same_amount(transaction: Transaction, all_transactions: list[Transaction], n_days_off: int = 0) -> int:
    """Return the number of transactions in the same day of the month with the same amount as the current tx."""
    tx_day = day_of_month(transaction)
    return len([
        t
        for t in all_transactions
        if t.amount == transaction.amount and abs(parse_date(t.date).day - tx_day) <= n_days_off
    ])


def pct_same_day_same_amount(
    transaction: Transaction, all_transactions: list[Transaction], n_days_off: int = 0
) -> float:
    """Return the percentage of transactions in the same day of the month with the same amount as the current tx."""
    return n_same_day_same_amount(transaction, all_transactions, n_days_off) / get_n_transactions_same_amount(
        transaction, all_transactions
    )


def get_n_transactions_days_apart_same_amount(
    transaction: Transaction,
    all_transactions: list[Transaction],
    n_days_apart: int,
    n_days_off: int,
) -> int:
    """
    Get the number of transactions in all_transactions that are within n_days_off of
    being n_days_apart from transaction and have the same amount as the current tx
    """
    n_txs = 0
    transaction_date = parse_date(transaction.date)

    # Pre-calculate bounds for faster checking
    lower_remainder = n_days_apart - n_days_off
    upper_remainder = n_days_off

    for t in all_transactions:
        if t.amount != transaction.amount:
            continue
        t_date = parse_date(t.date)
        days_diff = abs((t_date - transaction_date).days)

        # Skip if the difference is less than minimum required
        if days_diff < n_days_apart - n_days_off:
            continue

        # Check if the difference is close to any multiple of n_days_apart
        remainder = days_diff % n_days_apart

        if remainder <= upper_remainder or remainder >= lower_remainder:
            n_txs += 1

    return n_txs


def get_pct_transactions_days_apart_same_amount(
    transaction: Transaction, all_transactions: list[Transaction], n_days_apart: int, n_days_off: int
) -> float:
    """
    Get the percentage of transactions in all_transactions that are within
    n_days_off of being n_days_apart from transaction and have the same amount as the current tx
    """
    return get_n_transactions_days_apart_same_amount(
        transaction, all_transactions, n_days_apart, n_days_off
    ) / get_n_transactions_same_amount(transaction, all_transactions)


def get_features(transaction: Transaction, all_transactions: list[Transaction]) -> dict[str, int | bool | float]:
    """Get the original features for the transaction."""
    return {
        "n_transactions_same_amount": get_n_transactions_same_amount(transaction, all_transactions),
        "percent_transactions_same_amount": get_percent_transactions_same_amount(transaction, all_transactions),
        "ends_in_99": get_ends_in_99(transaction),
        "amount": transaction.amount,
        "same_day_exact": get_n_transactions_same_day(transaction, all_transactions, 0),
        "pct_transactions_same_day": get_pct_transactions_same_day(transaction, all_transactions, 0),
        "same_day_off_by_1": get_n_transactions_same_day(transaction, all_transactions, 1),
        "same_day_off_by_2": get_n_transactions_same_day(transaction, all_transactions, 2),
        "14_days_apart_exact": get_n_transactions_days_apart(transaction, all_transactions, 14, 0),
        "pct_14_days_apart_exact": get_pct_transactions_days_apart(transaction, all_transactions, 14, 0),
        "14_days_apart_off_by_1": get_n_transactions_days_apart(transaction, all_transactions, 14, 1),
        "pct_14_days_apart_off_by_1": get_pct_transactions_days_apart(transaction, all_transactions, 14, 1),
        "7_days_apart_exact": get_n_transactions_days_apart(transaction, all_transactions, 7, 0),
        "pct_7_days_apart_exact": get_pct_transactions_days_apart(transaction, all_transactions, 7, 0),
        "7_days_apart_off_by_1": get_n_transactions_days_apart(transaction, all_transactions, 7, 1),
        "pct_7_days_apart_off_by_1": get_pct_transactions_days_apart(transaction, all_transactions, 7, 1),
        "is_insurance": get_is_insurance(transaction),
        "is_utility": get_is_utility(transaction),
        "is_phone": get_is_phone(transaction),
        "is_always_recurring": get_is_always_recurring(transaction),
        "z_score": get_transaction_z_score(transaction, all_transactions),
        "abs_z_score": abs(get_transaction_z_score(transaction, all_transactions)),
    }


def get_new_features(transaction: Transaction, all_transactions: list[Transaction]) -> dict[str, int | bool | float]:
    """Get the new features for the transaction."""

    # NOTE: Do NOT add features that are already in the original features.py file.
    # NOTE: Each feature should be on a separate line. Do not use **dict shorthand.
    return {
        # ai new features
        "count_transactions_original": count_transactions(all_transactions),
        "days_since_last_original": days_since_last(transaction, all_transactions),
        "days_until_next_original": days_until_next(transaction, all_transactions),
        "mean_days_between_original": mean_days_between(all_transactions),
        "std_days_between_original": std_days_between(all_transactions),
        "regularity_score_original": regularity_score(all_transactions),
        "transaction_span_days_original": transaction_span_days(all_transactions),
        "count_last_n_days_original": count_last_n_days(transaction, all_transactions),
        "count_last_28_days_original": count_last_28_days(transaction, all_transactions),
        "count_last_35_days_original": count_last_35_days(transaction, all_transactions),
        "count_last_90_days_original": count_last_90_days(transaction, all_transactions),
        "mean_amount_original": mean_amount(all_transactions),
        "std_amount_original": std_amount(all_transactions),
        "amount_diff_from_mean_original": amount_diff_from_mean(transaction, all_transactions),
        "relative_amount_diff_original": relative_amount_diff(transaction, all_transactions),
        "day_of_week_original": day_of_week(transaction),
        "is_weekend_original": is_weekend(transaction),
        "day_of_month_original": day_of_month(transaction),
        "month_of_year_original": month_of_year(transaction),
        "same_day_of_month_count_original": same_day_of_month_count(transaction, all_transactions),
        "fraction_same_day_of_month_original": fraction_same_day_of_month(transaction, all_transactions),
        "monthly_tolerance_original": monthly_tolerance(all_transactions),
        "quarterly_tolerance_original": quarterly_tolerance(all_transactions),
        "weekly_tolerance_original": weekly_tolerance(all_transactions),
        "biweekly_tolerance_original": biweekly_tolerance(all_transactions),
        "span_months_original": span_months(all_transactions),
        "total_span_months_original": total_span_months(all_transactions),
        "fraction_active_months_original": fraction_active_months(all_transactions),
        "avg_txn_per_month_original": avg_txn_per_month(all_transactions),
        "modal_amount_original": modal_amount(all_transactions),
        "fraction_modal_amount_original": fraction_modal_amount(all_transactions),
        "amount_matches_modal_original": amount_matches_modal(transaction, all_transactions),
        "mode_interval_original": mode_interval(all_transactions),
        "fraction_mode_interval_original": fraction_mode_interval(all_transactions),
        "prev_interval_dev_from_mean_original": prev_interval_dev_from_mean(transaction, all_transactions),
        "next_interval_dev_from_mean_original": next_interval_dev_from_mean(transaction, all_transactions),
        "prev_interval_dev_from_mode_original": prev_interval_dev_from_mode(transaction, all_transactions),
        "next_interval_dev_from_mode_original": next_interval_dev_from_mode(transaction, all_transactions),
        "prev_within_monthly_tol_original": prev_within_monthly_tol(transaction, all_transactions),
        "next_within_monthly_tol_original": next_within_monthly_tol(transaction, all_transactions),
        "modal_day_of_month_original": modal_day_of_month(all_transactions),
        "dom_diff_from_modal_original": dom_diff_from_modal(transaction, all_transactions),
        "is_modal_dom_original": is_modal_dom(transaction, all_transactions),
        "amount_diff_from_modal_original": amount_diff_from_modal(transaction, all_transactions),
        "rel_amount_diff_from_modal_original": rel_amount_diff_from_modal(transaction, all_transactions),
        "amount_frequency_rank_original": amount_frequency_rank(transaction, all_transactions),
        "amount_freq_fraction_original": amount_freq_fraction(transaction, all_transactions),
        "txns_in_same_month_original": txns_in_same_month(transaction, all_transactions),
        "frac_txns_in_same_month_original": frac_txns_in_same_month(transaction, all_transactions),
        "days_since_group_start_original": days_since_group_start(transaction, all_transactions),
        "position_in_span_original": position_in_span(transaction, all_transactions),
        # my new features
        "is_amazon_prime_original": is_amazon_prime(transaction),
        "is_amazon_prime_video_original": is_amazon_prime_video(transaction),
        "is_apple_original": is_apple(transaction),
        "is_loan_company_original": is_loan_company(transaction),
        "is_pay_in_four_company_original": is_pay_in_four_company(transaction),
        "is_cash_advance_company_original": is_cash_advance_company(transaction),
        "is_phone_company_original": is_phone_company(transaction),
        "is_subscription_company_original": is_subscription_company(transaction),
        "is_usually_subscription_company_original": is_usually_subscription_company(transaction),
        "is_utility_company_original": is_utility_company(transaction),
        "is_insurance_company_original": is_insurance_company(transaction),
        "is_carwash_company_original": is_carwash_company(transaction),
        "is_rental_company_original": is_rental_company(transaction),
        "ends_in_00_original": ends_in_00(transaction),
        "is_likely_subscription_amount_original": is_likely_subscription_amount(transaction),
        "n_small_transactions_original": n_small_transactions(all_transactions, 20),
        "pct_small_transactions_original": pct_small_transactions(all_transactions, 20),
        "n_small_transactions_not_this_amount_original": n_small_transactions_not_this_amount(
            transaction, all_transactions, 20
        ),
        "pct_small_transactions_not_this_amount_original": pct_small_transactions_not_this_amount(
            transaction, all_transactions, 20
        ),
        "n_monthly_same_amount_original": n_monthly_same_amount(transaction, all_transactions),
        "pct_monthly_same_amount_original": pct_monthly_same_amount(transaction, all_transactions),
        "n_consecutive_months_same_amount_original": n_consecutive_months_same_amount(transaction, all_transactions),
        "pct_consecutive_months_same_amount_original": pct_consecutive_months_same_amount(
            transaction, all_transactions
        ),
        "n_same_day_same_amount_1_original": n_same_day_same_amount(transaction, all_transactions, 1),
        "n_same_day_same_amount_3_original": n_same_day_same_amount(transaction, all_transactions, 3),
        "n_same_day_same_amount_5_original": n_same_day_same_amount(transaction, all_transactions, 5),
        "pct_same_day_same_amount_1_original": pct_same_day_same_amount(transaction, all_transactions, 1),
        "pct_same_day_same_amount_3_original": pct_same_day_same_amount(transaction, all_transactions, 3),
        "pct_same_day_same_amount_5_original": pct_same_day_same_amount(transaction, all_transactions, 5),
        "n_days_apart_same_amount_14_2_original": get_n_transactions_days_apart_same_amount(
            transaction, all_transactions, 14, 2
        ),
        "pct_days_apart_same_amount_14_2_original": get_pct_transactions_days_apart_same_amount(
            transaction, all_transactions, 14, 2
        ),
        "n_days_apart_same_amount_28_2_original": get_n_transactions_days_apart_same_amount(
            transaction, all_transactions, 28, 2
        ),
        "pct_days_apart_same_amount_28_2_original": get_pct_transactions_days_apart_same_amount(
            transaction, all_transactions, 28, 2
        ),
        "n_days_apart_same_amount_28_4_original": get_n_transactions_days_apart_same_amount(
            transaction, all_transactions, 28, 4
        ),
        "pct_days_apart_same_amount_28_4_original": get_pct_transactions_days_apart_same_amount(
            transaction, all_transactions, 28, 4
        ),
    }
