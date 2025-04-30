# test features_dallanq.py


import pytest

from recur_scan.features_dallanq import (
    amount_diff_from_mean,
    amount_diff_from_modal,
    amount_freq_fraction,
    amount_frequency_rank,
    amount_matches_modal,
    avg_txn_per_month,
    biweekly_tolerance,
    count_last_28_days,
    count_last_35_days,
    count_last_90_days,
    count_last_n_days,
    count_transactions,
    day_of_month,
    day_of_week,
    days_since_group_start,
    days_since_last,
    days_since_last_same_amount,
    days_until_next,
    days_until_next_same_amount,
    dom_diff_from_modal,
    ends_in_00,
    frac_intervals_within,
    frac_txns_in_same_month,
    fraction_active_months,
    fraction_modal_amount,
    fraction_mode_interval,
    fraction_same_day_of_month,
    get_ends_in_99,
    get_is_always_recurring,
    get_is_insurance,
    get_is_phone,
    get_is_utility,
    get_n_transactions_days_apart,
    get_n_transactions_days_apart_same_amount,
    get_n_transactions_same_amount,
    get_n_transactions_same_day,
    get_pct_transactions_days_apart,
    get_pct_transactions_days_apart_same_amount,
    get_pct_transactions_same_day,
    get_percent_transactions_same_amount,
    get_transaction_z_score,
    is_amazon_prime,
    is_amazon_prime_video,
    is_apple,
    is_carwash_company,
    is_cash_advance_company,
    is_insurance_company,
    is_likely_subscription_amount,
    is_loan_company,
    is_modal_dom,
    is_pay_in_four_company,
    is_phone_company,
    is_rental_company,
    is_subscription_company,
    is_usually_subscription_company,
    is_utility_company,
    is_weekend,
    mean_amount,
    mean_days_between,
    mean_days_between_same_amount,
    modal_amount,
    modal_day_of_month,
    mode_interval,
    monthly_tolerance,
    n_consecutive_months_same_amount,
    n_monthly_same_amount,
    n_same_day_same_amount,
    n_small_transactions,
    n_small_transactions_not_this_amount,
    next_interval_dev_from_mean,
    next_interval_dev_from_mode,
    next_within_monthly_tol,
    pct_consecutive_months_same_amount,
    pct_monthly_same_amount,
    pct_same_day_same_amount,
    pct_small_transactions,
    pct_small_transactions_not_this_amount,
    position_in_span,
    prev_interval_dev_from_mean,
    prev_interval_dev_from_mode,
    prev_within_monthly_tol,
    quarterly_tolerance,
    regularity_score,
    regularity_score_same_amount,
    rel_amount_diff_from_modal,
    relative_amount_diff,
    same_day_of_month_count,
    span_months,
    std_amount,
    std_days_between,
    std_days_between_same_amount,
    total_span_months,
    transaction_span_days,
    txns_in_same_month,
    weekly_tolerance,
)
from recur_scan.transactions import Transaction


def test_get_n_transactions_same_amount() -> None:
    """Test that get_n_transactions_same_amount returns the correct number of transactions with the same amount."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-01-02"),
        Transaction(id=4, user_id="user1", name="name1", amount=2.99, date="2024-01-03"),
    ]
    assert get_n_transactions_same_amount(transactions[0], transactions) == 2
    assert get_n_transactions_same_amount(transactions[2], transactions) == 1


def test_get_percent_transactions_same_amount() -> None:
    """
    Test that get_percent_transactions_same_amount returns correct percentage.
    Tests that the function calculates the right percentage of transactions with matching amounts.
    """
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-01-02"),
        Transaction(id=4, user_id="user1", name="name1", amount=2.99, date="2024-01-03"),
    ]
    assert pytest.approx(get_percent_transactions_same_amount(transactions[0], transactions)) == 2 / 4


def test_get_ends_in_99() -> None:
    """Test that get_ends_in_99 returns True for amounts ending in 99."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-01-02"),
        Transaction(id=4, user_id="user1", name="name1", amount=2.99, date="2024-01-03"),
    ]
    assert not get_ends_in_99(transactions[0])
    assert get_ends_in_99(transactions[3])


def test_get_n_transactions_same_day() -> None:
    """Test that get_n_transactions_same_day returns the correct number of transactions on the same day."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-01-02"),
        Transaction(id=4, user_id="user1", name="name1", amount=2.99, date="2024-01-03"),
    ]
    assert get_n_transactions_same_day(transactions[0], transactions, 0) == 2
    assert get_n_transactions_same_day(transactions[0], transactions, 1) == 3
    assert get_n_transactions_same_day(transactions[2], transactions, 0) == 1


def test_get_pct_transactions_same_day() -> None:
    """Test that get_pct_transactions_same_day returns the correct percentage of transactions on the same day."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-01-02"),
        Transaction(id=4, user_id="user1", name="name1", amount=2.99, date="2024-01-03"),
    ]
    assert get_pct_transactions_same_day(transactions[0], transactions, 0) == 2 / 4


def test_get_n_transactions_days_apart() -> None:
    """Test get_n_transactions_days_apart."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=2.99, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=2.99, date="2024-01-02"),
        Transaction(id=3, user_id="user1", name="name1", amount=2.99, date="2024-01-14"),
        Transaction(id=4, user_id="user1", name="name1", amount=2.99, date="2024-01-15"),
        Transaction(id=5, user_id="user1", name="name1", amount=2.99, date="2024-01-16"),
        Transaction(id=6, user_id="user1", name="name1", amount=2.99, date="2024-01-29"),
        Transaction(id=7, user_id="user1", name="name1", amount=2.99, date="2024-01-31"),
    ]
    assert get_n_transactions_days_apart(transactions[0], transactions, 14, 0) == 2
    assert get_n_transactions_days_apart(transactions[0], transactions, 14, 1) == 4


def test_get_pct_transactions_days_apart() -> None:
    """Test get_pct_transactions_days_apart."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=2.99, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=2.99, date="2024-01-02"),
        Transaction(id=3, user_id="user1", name="name1", amount=2.99, date="2024-01-14"),
        Transaction(id=4, user_id="user1", name="name1", amount=2.99, date="2024-01-15"),
        Transaction(id=5, user_id="user1", name="name1", amount=2.99, date="2024-01-16"),
        Transaction(id=6, user_id="user1", name="name1", amount=2.99, date="2024-01-29"),
        Transaction(id=7, user_id="user1", name="name1", amount=2.99, date="2024-01-31"),
    ]
    assert get_pct_transactions_days_apart(transactions[0], transactions, 14, 0) == 2 / 7
    assert get_pct_transactions_days_apart(transactions[0], transactions, 14, 1) == 4 / 7


def test_get_is_insurance() -> None:
    """Test get_is_insurance."""
    assert get_is_insurance(
        Transaction(id=1, user_id="user1", name="Allstate Insurance", amount=100, date="2024-01-01")
    )
    assert not get_is_insurance(Transaction(id=2, user_id="user1", name="AT&T", amount=100, date="2024-01-01"))


def test_get_is_phone() -> None:
    """Test get_is_phone."""
    assert get_is_phone(Transaction(id=2, user_id="user1", name="AT&T", amount=100, date="2024-01-01"))
    assert not get_is_phone(Transaction(id=3, user_id="user1", name="Duke Energy", amount=200, date="2024-01-02"))


def test_get_is_utility() -> None:
    """Test get_is_utility."""
    assert get_is_utility(Transaction(id=3, user_id="user1", name="Duke Energy", amount=200, date="2024-01-02"))
    assert not get_is_utility(
        Transaction(id=4, user_id="user1", name="HighEnergy Soft Drinks", amount=2.99, date="2024-01-03")
    )


def test_get_is_always_recurring() -> None:
    """Test get_is_always_recurring."""
    assert get_is_always_recurring(Transaction(id=1, user_id="user1", name="netflix", amount=100, date="2024-01-01"))
    assert not get_is_always_recurring(
        Transaction(id=2, user_id="user1", name="walmart", amount=100, date="2024-01-01")
    )


def test_get_transaction_z_score():
    """Test get_transaction_z_score."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-01"),
    ]
    assert get_transaction_z_score(transactions[0], transactions) == 0

    # Test with varying amounts
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=90, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=3, user_id="user1", name="name1", amount=110, date="2024-01-01"),
    ]
    # Use approximate comparison with pytest
    z_score = get_transaction_z_score(transactions[0], transactions)
    assert -1.3 < z_score < -1.1  # Allow a small tolerance for floating-point precision


def test_is_amazon_prime():
    """Test is_amazon_prime."""
    assert is_amazon_prime(Transaction(id=1, user_id="user1", name="amazon prime", amount=100, date="2024-01-01"))
    assert not is_amazon_prime(Transaction(id=2, user_id="user1", name="netflix", amount=100, date="2024-01-01"))


# New feature tests


def test_count_transactions() -> None:
    """Test count_transactions function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-02-01"),
    ]
    assert count_transactions(transactions) == 3
    assert count_transactions([]) == 0


def test_days_since_last() -> None:
    """Test days_since_last function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-02-01"),
    ]
    assert days_since_last(transactions[2], transactions) == 17
    assert days_since_last(transactions[1], transactions) == 14
    assert days_since_last(transactions[0], transactions) == -1.0


def test_days_until_next() -> None:
    """Test days_until_next function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-02-01"),
    ]
    assert days_until_next(transactions[0], transactions) == 14
    assert days_until_next(transactions[1], transactions) == 17
    assert days_until_next(transactions[2], transactions) == -1.0


def test_mean_days_between() -> None:
    """Test mean_days_between function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-02-01"),
    ]
    assert mean_days_between(transactions) == 15.5
    assert mean_days_between([transactions[0]]) == -1.0


def test_std_days_between() -> None:
    """Test std_days_between function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-02-01"),
    ]
    assert pytest.approx(std_days_between(transactions)) == 2.12132
    assert std_days_between([transactions[0]]) == -1.0


def test_regularity_score() -> None:
    """Test regularity_score function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-02-01"),
    ]
    assert pytest.approx(regularity_score(transactions)) == 15.5 / 2.12132
    assert regularity_score([transactions[0]]) == -1.0


def test_days_since_last_same_amount() -> None:
    """Test days_since_last_same_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-10"),
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-01-15"),
    ]
    assert days_since_last_same_amount(transactions[2], transactions) == 14
    assert days_since_last_same_amount(transactions[0], transactions) == -1.0


def test_days_until_next_same_amount() -> None:
    """Test days_until_next_same_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-10"),
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-01-15"),
    ]
    assert days_until_next_same_amount(transactions[0], transactions) == 14
    assert days_until_next_same_amount(transactions[2], transactions) == -1.0


def test_mean_days_between_same_amount() -> None:
    """Test mean_days_between_same_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-10"),
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=4, user_id="user1", name="name1", amount=100, date="2024-01-30"),
    ]
    assert mean_days_between_same_amount(transactions[0], transactions) == 14.5
    assert mean_days_between_same_amount(transactions[1], transactions) == -1.0


def test_std_days_between_same_amount() -> None:
    """Test std_days_between_same_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-10"),
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=4, user_id="user1", name="name1", amount=100, date="2024-01-30"),
    ]
    # Standard deviation of intervals (14, 15) = approx 0.7071
    result = std_days_between_same_amount(transactions[0], transactions)
    assert 0.7 < result < 0.71  # Wider tolerance for floating point
    assert std_days_between_same_amount(transactions[1], transactions) == -1.0


def test_regularity_score_same_amount() -> None:
    """Test regularity_score_same_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-10"),
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=4, user_id="user1", name="name1", amount=100, date="2024-01-30"),
    ]
    # Mean is 14.5, std is 0.7071, so ratio is around 20.5
    result = regularity_score_same_amount(transactions[0], transactions)
    assert 20.4 < result < 20.6  # Wider tolerance for floating point
    assert regularity_score_same_amount(transactions[1], transactions) == -1.0


def test_transaction_span_days() -> None:
    """Test transaction_span_days function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-02-01"),
    ]
    assert transaction_span_days(transactions) == 31
    assert transaction_span_days([]) == -1.0


def test_count_last_n_days() -> None:
    """Test count_last_n_days function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-02-01"),
    ]
    assert count_last_n_days(transactions[2], transactions, 30) == 1
    assert count_last_n_days(transactions[2], transactions, 60) == 2


def test_count_last_28_days() -> None:
    """Test count_last_28_days function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-02-01"),
    ]
    assert count_last_28_days(transactions[2], transactions) == 1


def test_count_last_35_days() -> None:
    """Test count_last_35_days function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-02-01"),
    ]
    assert count_last_35_days(transactions[2], transactions) == 2


def test_count_last_90_days() -> None:
    """Test count_last_90_days function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2023-11-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-02-01"),
    ]
    # Only transaction[1] is in the past 90 days before transaction[2]
    # transaction[0] is older than 90 days, and transaction[2] is the reference transaction
    assert count_last_90_days(transactions[2], transactions) == 1


def test_mean_amount() -> None:
    """Test mean_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-02-01"),
    ]
    assert mean_amount(transactions) == 200
    assert mean_amount([]) == -1.0


def test_std_amount() -> None:
    """Test std_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-02-01"),
    ]
    assert pytest.approx(std_amount(transactions)) == 100
    assert std_amount([]) == 0.0


def test_amount_diff_from_mean() -> None:
    """Test amount_diff_from_mean function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-02-01"),
    ]
    assert amount_diff_from_mean(transactions[0], transactions) == 100
    assert amount_diff_from_mean(transactions[1], transactions) == 0


def test_relative_amount_diff() -> None:
    """Test relative_amount_diff function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-02-01"),
    ]
    assert relative_amount_diff(transactions[0], transactions) == -0.5
    assert relative_amount_diff(transactions[1], transactions) == 0


def test_day_of_week() -> None:
    """Test day_of_week function."""
    transaction = Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01")  # A Monday
    assert day_of_week(transaction) == 0

    transaction = Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-07")  # A Sunday
    assert day_of_week(transaction) == 6


def test_is_weekend() -> None:
    """Test is_weekend function."""
    transaction = Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01")  # A Monday
    assert is_weekend(transaction) == 0

    transaction = Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-07")  # A Sunday
    assert is_weekend(transaction) == 1


def test_day_of_month() -> None:
    """Test day_of_month function."""
    transaction = Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15")
    assert day_of_month(transaction) == 15


def test_month_of_year() -> None:
    """Test month_of_year function."""
    from recur_scan.features_dallanq import month_of_year

    transaction = Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-02-15")
    assert month_of_year(transaction) == 2


def test_same_day_of_month_count() -> None:
    """Test same_day_of_month_count function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-02-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-03-16"),
    ]
    assert same_day_of_month_count(transactions[0], transactions) == 2


def test_fraction_same_day_of_month() -> None:
    """Test fraction_same_day_of_month function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-02-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-03-16"),
    ]
    assert fraction_same_day_of_month(transactions[0], transactions) == 2 / 3


def test_frac_intervals_within() -> None:
    """Test frac_intervals_within function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-15"),  # 14 days diff
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-01-29"),  # 14 days diff
        Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-02-17"),  # 19 days diff
    ]
    assert frac_intervals_within(transactions, 14, 1) == 2 / 3


def test_monthly_tolerance() -> None:
    """Test monthly_tolerance function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-31"),  # 30 days diff
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-03-01"),  # 30 days diff
        Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-04-15"),  # 45 days diff
    ]
    assert monthly_tolerance(transactions) == 2 / 3


def test_quarterly_tolerance() -> None:
    """Test quarterly_tolerance function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-04-01"),  # 91 days diff
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-07-01"),  # 91 days diff
        Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-12-15"),  # 167 days diff
    ]
    assert quarterly_tolerance(transactions) == 2 / 3


def test_weekly_tolerance() -> None:
    """Test weekly_tolerance function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-08"),  # 7 days diff
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-01-15"),  # 7 days diff
        Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-01-26"),  # 11 days diff
    ]
    assert weekly_tolerance(transactions) == 2 / 3


def test_biweekly_tolerance() -> None:
    """Test biweekly_tolerance function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-15"),  # 14 days diff
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-01-29"),  # 14 days diff
        Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-02-17"),  # 19 days diff
    ]
    assert biweekly_tolerance(transactions) == 2 / 3


def test_span_months() -> None:
    """Test span_months function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-02-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-02-28"),
        Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-04-17"),
    ]
    assert span_months(transactions) == 3
    assert span_months([]) == -1.0


def test_total_span_months() -> None:
    """Test total_span_months function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-03-31"),  # ~3 months span
    ]
    assert total_span_months(transactions) == 3

    # Test with a single transaction
    assert total_span_months([transactions[0]]) == 1


def test_fraction_active_months() -> None:
    """Test fraction_active_months function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-02-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-04-17"),  # No March transaction
    ]
    assert fraction_active_months(transactions) == 3 / 4


def test_avg_txn_per_month() -> None:
    """Test avg_txn_per_month function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-02-28"),
        Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-03-17"),
    ]
    assert avg_txn_per_month(transactions) == 4 / 3


def test_modal_amount() -> None:
    """Test modal_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-02-28"),
    ]
    assert modal_amount(transactions) == 100
    assert modal_amount([]) == -1.0


def test_fraction_modal_amount() -> None:
    """Test fraction_modal_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-02-28"),
    ]
    assert fraction_modal_amount(transactions) == 2 / 3
    assert fraction_modal_amount([]) == -1.0


def test_amount_matches_modal() -> None:
    """Test amount_matches_modal function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-02-28"),
    ]
    assert amount_matches_modal(transactions[0], transactions) == 1.0
    assert amount_matches_modal(transactions[2], transactions) == 0.0


def test_mode_interval() -> None:
    """Test mode_interval function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-15"),  # 14 days
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-01-29"),  # 14 days
        Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-02-13"),  # 15 days
    ]
    assert mode_interval(transactions) == 14
    assert mode_interval([transactions[0]]) == -1.0


def test_fraction_mode_interval() -> None:
    """Test fraction_mode_interval function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-15"),  # 14 days
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-01-29"),  # 14 days
        Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-02-13"),  # 15 days
    ]
    assert fraction_mode_interval(transactions) == 2 / 3
    assert fraction_mode_interval([transactions[0]]) == -1.0


def test_prev_interval_dev_from_mean() -> None:
    """Test prev_interval_dev_from_mean function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-15"),  # 14 days
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-01-29"),  # 14 days
        Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-02-13"),  # 15 days
    ]
    # Mean interval is (14 + 14 + 15) / 3 = 14.333
    result = prev_interval_dev_from_mean(transactions[3], transactions)
    assert 0.65 < result < 0.68  # Wider tolerance for floating point
    assert prev_interval_dev_from_mean(transactions[0], transactions) == -1.0


def test_next_interval_dev_from_mean() -> None:
    """Test next_interval_dev_from_mean function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-15"),  # 14 days
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-01-29"),  # 14 days
        Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-02-13"),  # 15 days
    ]
    # Mean interval is (14 + 14 + 15) / 3 = 14.333
    result = next_interval_dev_from_mean(transactions[0], transactions)
    assert -0.35 < result < -0.32  # Wider tolerance for floating point
    assert next_interval_dev_from_mean(transactions[3], transactions) == -1.0


def test_prev_interval_dev_from_mode() -> None:
    """Test prev_interval_dev_from_mode function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-15"),  # 14 days
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-01-29"),  # 14 days
        Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-02-13"),  # 15 days
    ]
    # Mode interval is 14
    assert prev_interval_dev_from_mode(transactions[3], transactions) == 15 - 14
    assert prev_interval_dev_from_mode(transactions[0], transactions) == -1.0


def test_next_interval_dev_from_mode() -> None:
    """Test next_interval_dev_from_mode function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-15"),  # 14 days
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-01-29"),  # 14 days
        Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-02-13"),  # 15 days
    ]
    # Mode interval is 14
    assert next_interval_dev_from_mode(transactions[0], transactions) == 14 - 14
    assert next_interval_dev_from_mode(transactions[3], transactions) == -1.0


def test_prev_within_monthly_tol() -> None:
    """Test prev_within_monthly_tol function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-30"),  # 29 days
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-03-01"),  # 31 days
    ]
    assert prev_within_monthly_tol(transactions[2], transactions) == 1.0
    assert prev_within_monthly_tol(transactions[0], transactions) == 0.0


def test_next_within_monthly_tol() -> None:
    """Test next_within_monthly_tol function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-30"),  # 29 days
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-03-01"),  # 31 days
    ]
    assert next_within_monthly_tol(transactions[0], transactions) == 1.0
    assert next_within_monthly_tol(transactions[2], transactions) == 0.0


def test_modal_day_of_month() -> None:
    """Test modal_day_of_month function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-02-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-03-16"),
        Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-04-15"),
    ]
    assert modal_day_of_month(transactions) == 15
    assert modal_day_of_month([]) == -1.0


def test_dom_diff_from_modal() -> None:
    """Test dom_diff_from_modal function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-02-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-03-16"),
        Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-04-15"),
    ]
    assert dom_diff_from_modal(transactions[0], transactions) == 0
    assert dom_diff_from_modal(transactions[2], transactions) == 1


def test_is_modal_dom() -> None:
    """Test is_modal_dom function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-02-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-03-16"),
        Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-04-15"),
    ]
    assert is_modal_dom(transactions[0], transactions) == 1.0
    assert is_modal_dom(transactions[2], transactions) == 0.0


def test_amount_diff_from_modal() -> None:
    """Test amount_diff_from_modal function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-02-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-03-16"),
    ]
    assert amount_diff_from_modal(transactions[0], transactions) == 0
    assert amount_diff_from_modal(transactions[2], transactions) == 100


def test_rel_amount_diff_from_modal() -> None:
    """Test rel_amount_diff_from_modal function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-02-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-03-16"),
    ]
    assert rel_amount_diff_from_modal(transactions[0], transactions) == 0
    assert rel_amount_diff_from_modal(transactions[2], transactions) == 1.0


def test_amount_frequency_rank() -> None:
    """Test amount_frequency_rank function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-02-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-03-16"),
        Transaction(id=4, user_id="user1", name="name1", amount=200, date="2024-04-16"),
        Transaction(id=5, user_id="user1", name="name1", amount=300, date="2024-05-17"),
    ]
    # Here 100 and 200 amounts both appear twice, but 100 is lower amount so it ranks 1st
    assert amount_frequency_rank(transactions[0], transactions) == 1
    # 200 is ranked 2nd because while it also appears twice, 100 comes first due to tie-breaking by amount
    assert amount_frequency_rank(transactions[2], transactions) == 2
    # 300 appears only once and has the highest amount, so ranked 3rd
    assert amount_frequency_rank(transactions[4], transactions) == 3


def test_amount_freq_fraction() -> None:
    """Test amount_freq_fraction function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-02-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-03-16"),
        Transaction(id=4, user_id="user1", name="name1", amount=200, date="2024-04-16"),
        Transaction(id=5, user_id="user1", name="name1", amount=300, date="2024-05-17"),
    ]
    assert amount_freq_fraction(transactions[0], transactions) == 2 / 5
    assert amount_freq_fraction(transactions[2], transactions) == 2 / 5
    assert amount_freq_fraction(transactions[4], transactions) == 1 / 5


def test_txns_in_same_month() -> None:
    """Test txns_in_same_month function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-25"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-02-16"),
    ]
    assert txns_in_same_month(transactions[0], transactions) == 2
    assert txns_in_same_month(transactions[2], transactions) == 1


def test_frac_txns_in_same_month() -> None:
    """Test frac_txns_in_same_month function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-25"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-02-16"),
    ]
    assert frac_txns_in_same_month(transactions[0], transactions) == 2 / 3
    assert frac_txns_in_same_month(transactions[2], transactions) == 1 / 3


def test_days_since_group_start() -> None:
    """Test days_since_group_start function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-02-01"),
    ]
    assert days_since_group_start(transactions[0], transactions) == 0
    assert days_since_group_start(transactions[1], transactions) == 14
    assert days_since_group_start(transactions[2], transactions) == 31
    assert (
        days_since_group_start(Transaction(id=4, user_id="user1", name="name1", amount=300, date="2024-02-15"), [])
        == -1.0
    )


def test_position_in_span() -> None:
    """Test position_in_span function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-16"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-02-01"),
    ]
    # Total span is 31 days
    assert position_in_span(transactions[0], transactions) == 0
    assert pytest.approx(position_in_span(transactions[1], transactions)) == 15 / 31
    assert position_in_span(transactions[2], transactions) == 1.0


def test_ends_in_00() -> None:
    """Test ends_in_00 function."""
    assert ends_in_00(Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"))
    assert ends_in_00(Transaction(id=2, user_id="user1", name="name1", amount=10.00, date="2024-01-01"))
    assert not ends_in_00(Transaction(id=3, user_id="user1", name="name1", amount=10.01, date="2024-01-01"))


def test_is_likely_subscription_amount() -> None:
    """Test is_likely_subscription_amount function."""
    assert is_likely_subscription_amount(
        Transaction(id=1, user_id="user1", name="name1", amount=9.99, date="2024-01-01")
    )
    assert is_likely_subscription_amount(
        Transaction(id=2, user_id="user1", name="name1", amount=14.99, date="2024-01-01")
    )
    assert not is_likely_subscription_amount(
        Transaction(id=3, user_id="user1", name="name1", amount=10.00, date="2024-01-01")
    )


def test_is_amazon_prime_video() -> None:
    """Test is_amazon_prime_video function."""
    assert is_amazon_prime_video(
        Transaction(id=1, user_id="user1", name="Amazon Prime Video", amount=100, date="2024-01-01")
    )
    assert not is_amazon_prime_video(
        Transaction(id=2, user_id="user1", name="Amazon Prime", amount=100, date="2024-01-01")
    )


def test_is_apple() -> None:
    """Test is_apple function."""
    assert is_apple(Transaction(id=1, user_id="user1", name="Apple Music", amount=100, date="2024-01-01"))
    assert not is_apple(Transaction(id=2, user_id="user1", name="Microsoft", amount=100, date="2024-01-01"))


def test_is_loan_company() -> None:
    """Test is_loan_company function."""
    assert is_loan_company(Transaction(id=1, user_id="user1", name="Personal Lending", amount=100, date="2024-01-01"))
    assert is_loan_company(Transaction(id=2, user_id="user1", name="Credit Ninja", amount=100, date="2024-01-01"))
    assert not is_loan_company(Transaction(id=3, user_id="user1", name="Netflix", amount=100, date="2024-01-01"))


def test_is_pay_in_four_company() -> None:
    """Test is_pay_in_four_company function."""
    assert is_pay_in_four_company(Transaction(id=1, user_id="user1", name="Afterpay", amount=100, date="2024-01-01"))
    assert not is_pay_in_four_company(Transaction(id=2, user_id="user1", name="Netflix", amount=100, date="2024-01-01"))


def test_is_cash_advance_company() -> None:
    """Test is_cash_advance_company function."""
    assert is_cash_advance_company(Transaction(id=1, user_id="user1", name="Empower", amount=100, date="2024-01-01"))
    assert is_cash_advance_company(Transaction(id=2, user_id="user1", name="Dave", amount=100, date="2024-01-01"))
    assert not is_cash_advance_company(
        Transaction(id=3, user_id="user1", name="Netflix", amount=100, date="2024-01-01")
    )


def test_is_phone_company() -> None:
    """Test is_phone_company function."""
    assert is_phone_company(Transaction(id=1, user_id="user1", name="Verizon", amount=100, date="2024-01-01"))
    assert is_phone_company(Transaction(id=2, user_id="user1", name="T-Mobile", amount=100, date="2024-01-01"))
    assert not is_phone_company(Transaction(id=3, user_id="user1", name="Netflix", amount=100, date="2024-01-01"))


def test_is_subscription_company() -> None:
    """Test is_subscription_company function."""
    assert is_subscription_company(Transaction(id=1, user_id="user1", name="Netflix", amount=100, date="2024-01-01"))
    assert is_subscription_company(Transaction(id=2, user_id="user1", name="Hulu", amount=100, date="2024-01-01"))
    assert not is_subscription_company(
        Transaction(id=3, user_id="user1", name="Walmart", amount=100, date="2024-01-01")
    )


def test_is_usually_subscription_company() -> None:
    """Test is_usually_subscription_company function."""
    assert is_usually_subscription_company(
        Transaction(id=1, user_id="user1", name="Disney", amount=100, date="2024-01-01")
    )
    assert is_usually_subscription_company(
        Transaction(id=2, user_id="user1", name="SiriusXM", amount=100, date="2024-01-01")
    )
    assert not is_usually_subscription_company(
        Transaction(id=3, user_id="user1", name="Walmart", amount=100, date="2024-01-01")
    )


def test_is_utility_company() -> None:
    """Test is_utility_company function."""
    assert is_utility_company(
        Transaction(id=1, user_id="user1", name="Electric Company", amount=100, date="2024-01-01")
    )
    assert is_utility_company(Transaction(id=2, user_id="user1", name="PG&E", amount=100, date="2024-01-01"))
    assert not is_utility_company(Transaction(id=3, user_id="user1", name="Walmart", amount=100, date="2024-01-01"))


def test_is_insurance_company() -> None:
    """Test is_insurance_company function."""
    assert is_insurance_company(Transaction(id=1, user_id="user1", name="Geico", amount=100, date="2024-01-01"))
    assert is_insurance_company(Transaction(id=2, user_id="user1", name="Progressive", amount=100, date="2024-01-01"))
    assert not is_insurance_company(Transaction(id=3, user_id="user1", name="Walmart", amount=100, date="2024-01-01"))


def test_is_carwash_company() -> None:
    """Test is_carwash_company function."""
    assert is_carwash_company(Transaction(id=1, user_id="user1", name="Quick Wash", amount=100, date="2024-01-01"))
    assert is_carwash_company(Transaction(id=2, user_id="user1", name="Carwash Express", amount=100, date="2024-01-01"))
    assert not is_carwash_company(Transaction(id=3, user_id="user1", name="Walmart", amount=100, date="2024-01-01"))


def test_is_rental_company() -> None:
    """Test is_rental_company function."""
    assert is_rental_company(Transaction(id=1, user_id="user1", name="Apartment Rent", amount=100, date="2024-01-01"))
    assert is_rental_company(
        Transaction(id=2, user_id="user1", name="Property Management", amount=100, date="2024-01-01")
    )
    assert not is_rental_company(Transaction(id=3, user_id="user1", name="Walmart", amount=100, date="2024-01-01"))


def test_n_small_transactions() -> None:
    """Test n_small_transactions function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=10, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=15, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=25, date="2024-02-01"),
        Transaction(id=4, user_id="user1", name="name1", amount=100, date="2024-02-15"),
    ]
    assert n_small_transactions(transactions, 20) == 2
    assert n_small_transactions(transactions, 30) == 3


def test_pct_small_transactions() -> None:
    """Test pct_small_transactions function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=10, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=15, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=25, date="2024-02-01"),
        Transaction(id=4, user_id="user1", name="name1", amount=100, date="2024-02-15"),
    ]
    assert pct_small_transactions(transactions, 20) == 0.5
    assert pct_small_transactions(transactions, 30) == 0.75


def test_n_small_transactions_not_this_amount() -> None:
    """Test n_small_transactions_not_this_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=10, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=10, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=15, date="2024-02-01"),
        Transaction(id=4, user_id="user1", name="name1", amount=100, date="2024-02-15"),
    ]
    assert n_small_transactions_not_this_amount(transactions[0], transactions, 20) == 1
    assert n_small_transactions_not_this_amount(transactions[2], transactions, 20) == 2


def test_pct_small_transactions_not_this_amount() -> None:
    """Test pct_small_transactions_not_this_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=10, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=10, date="2024-01-15"),
        Transaction(id=3, user_id="user1", name="name1", amount=15, date="2024-02-01"),
        Transaction(id=4, user_id="user1", name="name1", amount=100, date="2024-02-15"),
    ]
    assert pct_small_transactions_not_this_amount(transactions[0], transactions, 20) == 0.25
    assert pct_small_transactions_not_this_amount(transactions[2], transactions, 20) == 0.5


def test_n_monthly_same_amount() -> None:
    """Test n_monthly_same_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),  # Same month
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-02-01"),  # Different month
        Transaction(id=4, user_id="user1", name="name1", amount=200, date="2024-03-01"),  # Different amount
    ]
    assert n_monthly_same_amount(transactions[0], transactions) == 2


def test_pct_monthly_same_amount() -> None:
    """Test pct_monthly_same_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),  # Same month
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-02-01"),  # Different month
        Transaction(id=4, user_id="user1", name="name1", amount=200, date="2024-03-01"),  # Different amount
    ]
    # 2 months with same amount / 3 transactions with same amount
    assert pytest.approx(pct_monthly_same_amount(transactions[0], transactions)) == 2 / 3


def test_n_consecutive_months_same_amount() -> None:
    """Test n_consecutive_months_same_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-02-15"),  # Consecutive month
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-03-15"),  # Consecutive month
        Transaction(id=4, user_id="user1", name="name1", amount=100, date="2024-05-15"),  # Skip April
    ]
    assert n_consecutive_months_same_amount(transactions[1], transactions) == 2

    # Test with multiple transactions in same month
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-20"),  # Same month
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-02-15"),
    ]
    assert n_consecutive_months_same_amount(transactions[0], transactions) == 0


def test_pct_consecutive_months_same_amount() -> None:
    """Test pct_consecutive_months_same_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-02-15"),  # Consecutive month
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-03-15"),  # Consecutive month
        Transaction(id=4, user_id="user1", name="name1", amount=100, date="2024-05-15"),  # Skip April
    ]
    # 2 consecutive / 4 total with same amount
    assert pytest.approx(pct_consecutive_months_same_amount(transactions[1], transactions)) == 2 / 4


def test_n_same_day_same_amount() -> None:
    """Test n_same_day_same_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-02-15"),  # Same day, same amount
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-03-16"),  # Different day, same amount
        Transaction(id=4, user_id="user1", name="name1", amount=200, date="2024-04-15"),  # Same day, different amount
    ]
    assert n_same_day_same_amount(transactions[0], transactions, 0) == 2
    assert n_same_day_same_amount(transactions[0], transactions, 1) == 3


def test_pct_same_day_same_amount() -> None:
    """Test pct_same_day_same_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-02-15"),  # Same day, same amount
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-03-16"),  # Different day, same amount
        Transaction(id=4, user_id="user1", name="name1", amount=200, date="2024-04-15"),  # Same day, different amount
    ]
    # 2 same day (exact) / 3 total same amount
    assert pytest.approx(pct_same_day_same_amount(transactions[0], transactions, 0)) == 2 / 3
    # 3 same day (±1) / 3 total same amount
    assert pytest.approx(pct_same_day_same_amount(transactions[0], transactions, 1)) == 3 / 3


def test_get_n_transactions_days_apart_same_amount() -> None:
    """Test get_n_transactions_days_apart_same_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),  # 14 days apart, same amount
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-01-29"),  # 14 days apart, same amount
        Transaction(
            id=4, user_id="user1", name="name1", amount=200, date="2024-01-15"
        ),  # 14 days apart, different amount
    ]
    assert get_n_transactions_days_apart_same_amount(transactions[0], transactions, 14, 0) == 2
    assert get_n_transactions_days_apart_same_amount(transactions[0], transactions, 14, 2) == 2


def test_get_pct_transactions_days_apart_same_amount() -> None:
    """Test get_pct_transactions_days_apart_same_amount function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-15"),  # 14 days apart, same amount
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-01-29"),  # 14 days apart, same amount
        Transaction(
            id=4, user_id="user1", name="name1", amount=100, date="2024-02-01"
        ),  # Not 14 days apart, same amount
    ]
    # 2 transactions 14 days apart / 4 total same amount
    assert pytest.approx(get_pct_transactions_days_apart_same_amount(transactions[0], transactions, 14, 0)) == 2 / 4
