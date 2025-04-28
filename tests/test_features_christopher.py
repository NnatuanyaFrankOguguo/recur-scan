# test features

import pytest

from recur_scan.features_christopher import (
    amount_consistency_chris,
    amount_deviation_chris,
    day_of_month_consistency_chris,
    detect_skipped_months_chris,
    follows_regular_interval_chris,
    get_coefficient_of_variation_chris,
    get_day_of_month_consistency_chris,
    get_median_interval_chris,
    get_n_transactions_same_amount_chris,
    get_percent_transactions_same_amount_chris,
    get_transaction_frequency_chris,
    get_transaction_gaps_chris,
    get_transaction_std_amount_chris,
    get_user_vendor_history,
    is_known_fixed_subscription_chris,
    is_known_recurring_company_chris,
    is_regular_interval_chris,
    std_amount_all_chris,
    transaction_frequency_chris,
    # New Feature Functions
)
from recur_scan.transactions import Transaction
from recur_scan.utils import parse_date


def test_parse_date_invalid_format() -> None:
    """Test that parse_date raises ValueError for invalid date format."""
    with pytest.raises(ValueError, match="time data '03/27/2024' does not match format '%Y-%m-%d'"):
        parse_date("03/27/2024")  # Invalid format, should raise ValueError


def test_std_amount_all_chris():
    """Test std_amount_all function with valid and invalid inputs."""

    # Test with a valid list of transactions
    transactions = [
        Transaction(id=1, user_id="user1", name="Store A", amount=50, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Store A", amount=70, date="2024-01-02"),
        Transaction(id=3, user_id="user1", name="Store A", amount=90, date="2024-01-03"),
    ]
    std_amount = std_amount_all_chris(transactions)
    assert std_amount > 0  # The standard deviation should be greater than 0

    # Test with an empty list, should return 0.0
    assert std_amount_all_chris([]) == 0.0

    # Test with a single transaction, should return 0.0
    single_transaction = [Transaction(id=1, user_id="user1", name="Store A", amount=50, date="2024-01-01")]
    assert std_amount_all_chris(single_transaction) == 0.0

    # Test with all transactions having the same amount (standard deviation should be 0)
    same_amount_transactions = [
        Transaction(id=1, user_id="user1", name="Store A", amount=50, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Store A", amount=50, date="2024-01-02"),
        Transaction(id=3, user_id="user1", name="Store A", amount=50, date="2024-01-03"),
    ]
    assert std_amount_all_chris(same_amount_transactions) == 0.0


def test_get_n_transactions_same_amount_chris() -> None:
    """Test get_n_transactions_same_amount_chris with tolerance logic."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        # Within 1% tolerance (tol = 1.0)
        Transaction(id=2, user_id="user1", name="name1", amount=100.5, date="2024-01-01"),
        # Outside tolerance
        Transaction(id=3, user_id="user1", name="name1", amount=102, date="2024-01-02"),
    ]
    # For transaction 1, only transaction 2 is within tolerance.
    assert get_n_transactions_same_amount_chris(transactions[0], transactions) == 2
    # For transaction 2, transaction 1 and itself count.
    assert get_n_transactions_same_amount_chris(transactions[1], transactions) == 2


def test_get_percent_transactions_same_amount_chris() -> None:
    """Test get_percent_transactions_same_amount_chris returns the correct percentage."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100.5, date="2024-01-01"),
        Transaction(id=3, user_id="user1", name="name1", amount=102, date="2024-01-02"),
    ]
    count = get_n_transactions_same_amount_chris(transactions[0], transactions)
    expected = count / len(transactions)
    assert pytest.approx(get_percent_transactions_same_amount_chris(transactions[0], transactions)) == expected


def test_get_transaction_gaps_chris() -> None:
    """Test get_transaction_gaps_chris with valid and invalid inputs."""
    transactions = [
        Transaction(id=1, user_id="user1", name="Store A", amount=50, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Store A", amount=50, date="2024-01-10"),
        Transaction(id=3, user_id="user1", name="Store A", amount=50, date="2024-01-20"),
    ]
    assert get_transaction_gaps_chris(transactions) == [9, 10]
    assert get_transaction_gaps_chris([]) == []


def test_get_transaction_frequency_chris() -> None:
    """Test get_transaction_frequency_chris with valid and invalid inputs."""
    transactions = [
        Transaction(id=1, user_id="user1", name="Store A", amount=50, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Store A", amount=50, date="2024-01-10"),
        Transaction(id=3, user_id="user1", name="Store A", amount=50, date="2024-01-20"),
    ]
    assert pytest.approx(get_transaction_frequency_chris(transactions)) == 9.5
    assert get_transaction_frequency_chris([]) == 0.0


def test_get_transaction_std_amount_chris() -> None:
    """Test get_transaction_std_amount_chris with valid and invalid inputs."""
    # Sample transactions for valid input
    transactions = [
        Transaction(id=1, user_id="user1", name="Store A", amount=50, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Store A", amount=70, date="2024-01-02"),
        Transaction(id=3, user_id="user1", name="Store A", amount=90, date="2024-01-03"),
    ]

    # Test with valid transactions, should return standard deviation > 0
    std_amount = get_transaction_std_amount_chris(transactions)
    assert std_amount > 0

    # Test with an empty list, should return 0.0
    assert get_transaction_std_amount_chris([]) == 0.0

    # Test with all same amounts (no variation), should return 0.0
    transactions_same = [
        Transaction(id=1, user_id="user1", name="Store A", amount=50, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Store A", amount=50, date="2024-01-02"),
        Transaction(id=3, user_id="user1", name="Store A", amount=50, date="2024-01-03"),
    ]
    assert get_transaction_std_amount_chris(transactions_same) == 0.0


def test_get_coefficient_of_variation_chris() -> None:
    """Test get_coefficient_of_variation with valid and invalid inputs."""
    transactions = [
        Transaction(id=1, user_id="user1", name="Store A", amount=50, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Store A", amount=70, date="2024-01-02"),
        Transaction(id=3, user_id="user1", name="Store A", amount=90, date="2024-01-03"),
    ]

    # Test with valid transactions, should return coefficient of variation > 0
    cv = get_coefficient_of_variation_chris(transactions)
    assert cv > 0

    # Test with an empty list, should return 0.0
    assert get_coefficient_of_variation_chris([]) == 0.0

    # Test with all same amounts (no variation), should return 0.0 for coefficient of variation
    transactions_same = [
        Transaction(id=1, user_id="user1", name="Store A", amount=50, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Store A", amount=50, date="2024-01-02"),
        Transaction(id=3, user_id="user1", name="Store A", amount=50, date="2024-01-03"),
    ]
    assert get_coefficient_of_variation_chris(transactions_same) == 0.0


def test_follows_regular_interval_chris() -> None:
    """Test follows_regular_interval with valid and invalid inputs."""
    transactions = [
        Transaction(id=1, user_id="user1", name="Store A", amount=50, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Store A", amount=50, date="2024-02-01"),
        Transaction(id=3, user_id="user1", name="Store A", amount=50, date="2024-03-01"),
    ]
    assert follows_regular_interval_chris(transactions)
    assert not follows_regular_interval_chris([])


def test_detect_skipped_months_chris() -> None:
    """Test detect_skipped_months with valid and invalid inputs."""
    transactions = [
        Transaction(id=1, user_id="user1", name="Store A", amount=50, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Store A", amount=50, date="2024-03-01"),
        Transaction(id=3, user_id="user1", name="Store A", amount=50, date="2024-04-01"),
    ]
    assert detect_skipped_months_chris(transactions) == 1
    assert detect_skipped_months_chris([]) == 0


def test_get_day_of_month_consistency_chris() -> None:
    """Test get_day_of_month_consistency with valid and invalid inputs."""
    transactions = [
        Transaction(id=1, user_id="user1", name="Store A", amount=50, date="2024-01-15"),
        Transaction(id=2, user_id="user1", name="Store A", amount=60, date="2024-02-15"),
        Transaction(id=3, user_id="user1", name="Store A", amount=70, date="2024-03-15"),
    ]
    assert get_day_of_month_consistency_chris(transactions) == 1.0
    assert get_day_of_month_consistency_chris([]) == 0.0


def test_get_median_interval_chris() -> None:
    """Test get_median_interval with valid and invalid inputs."""
    transactions = [
        Transaction(id=1, user_id="user1", name="Store A", amount=50, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Store A", amount=50, date="2024-01-04"),
        Transaction(id=3, user_id="user1", name="Store A", amount=50, date="2024-01-10"),
    ]
    assert pytest.approx(get_median_interval_chris(transactions), 0.1) == 4.5
    assert get_median_interval_chris([]) == 0.0


def test_is_known_recurring_company() -> None:
    """Test is_known_recurring_company with valid and invalid inputs."""
    assert is_known_recurring_company_chris("Netflix")
    assert is_known_recurring_company_chris("Hulu")
    assert not is_known_recurring_company_chris("Local Grocery")


def test_is_known_fixed_subscription_chris() -> None:
    """Test is_known_fixed_subscription_chris with valid and invalid inputs."""

    # Valid known subscription: Cleo with amount 5.99
    assert is_known_fixed_subscription_chris(
        Transaction(id=1, user_id="user1", name="Cleo", amount=5.99, date="2024-01-01")
    )

    # Valid known subscription: Albert with amount 14.99
    assert is_known_fixed_subscription_chris(
        Transaction(
            id=3,
            user_id="user1",
            name="Albert Subscription",
            amount=14.99,
            date="2024-01-01",
        )
    )

    # Invalid: Known company but wrong amount
    assert not is_known_fixed_subscription_chris(
        Transaction(id=4, user_id="user1", name="Cleo", amount=9.99, date="2024-01-01")
    )

    # Invalid: Unknown company
    assert not is_known_fixed_subscription_chris(
        Transaction(id=2, user_id="user1", name="Local Gym", amount=30, date="2024-01-01")
    )


# ------------------- NEW TEST FUNCTIONS -------------------


def test_get_user_vendor_history() -> None:
    """Test get_user_vendor_history returns only past transactions."""
    transactions = [
        Transaction(id=1, user_id="user1", name="Vendor", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Vendor", amount=100, date="2024-02-01"),
    ]

    transaction = Transaction(id=3, user_id="user1", name="Vendor", amount=100, date="2024-03-01")
    history = get_user_vendor_history(transaction, transactions)
    assert len(history) == 2
    assert all(t.date < transaction.date for t in history)


def test_is_regular_interval_chris() -> None:
    """Test is_regular_interval_chris detects regularity."""
    transactions = [
        Transaction(id=1, user_id="user1", name="Vendor", amount=50, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Vendor", amount=50, date="2024-02-01"),
        Transaction(id=3, user_id="user1", name="Vendor", amount=50, date="2024-03-01"),
    ]
    transaction = Transaction(id=4, user_id="user1", name="Vendor", amount=50, date="2024-04-01")
    assert is_regular_interval_chris(transaction, transactions) is True


def test_amount_deviation_chris() -> None:
    """Test amount_deviation_chris returns correct relative difference."""
    transactions = [
        Transaction(id=1, user_id="user1", name="Vendor", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Vendor", amount=100, date="2024-02-01"),
    ]
    transaction = Transaction(id=3, user_id="user1", name="Vendor", amount=110, date="2024-03-01")
    deviation = amount_deviation_chris(transaction, transactions)
    assert pytest.approx(deviation, 0.01) == 0.1  # 10% deviation


def test_transaction_frequency_chris() -> None:
    """Test transaction_frequency_chris counts transactions within last 6 months."""
    transactions = [
        Transaction(id=1, user_id="user1", name="Vendor", amount=30, date="2023-07-01"),  # older than 6 months
        Transaction(id=2, user_id="user1", name="Vendor", amount=30, date="2024-01-01"),  # within 6 months
    ]
    transaction = Transaction(id=3, user_id="user1", name="Vendor", amount=30, date="2024-02-01")
    assert transaction_frequency_chris(transaction, transactions) == 1


def test_day_of_month_consistency_chris() -> None:
    """Test day_of_month_consistency_chris checks calendar day consistency."""
    transactions = [
        Transaction(id=1, user_id="user1", name="Vendor", amount=60, date="2024-01-05"),
        Transaction(id=2, user_id="user1", name="Vendor", amount=60, date="2024-02-05"),
        Transaction(id=3, user_id="user1", name="Vendor", amount=60, date="2024-03-05"),
    ]
    transaction = Transaction(id=4, user_id="user1", name="Vendor", amount=60, date="2024-04-05")
    assert day_of_month_consistency_chris(transaction, transactions) is True


def test_amount_consistency_chris() -> None:
    """Test amount_consistency_chris checks low variability of amounts."""
    transactions = [
        Transaction(id=1, user_id="user1", name="Vendor", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Vendor", amount=101, date="2024-02-01"),
        Transaction(id=3, user_id="user1", name="Vendor", amount=99, date="2024-03-01"),
    ]
    transaction = Transaction(id=4, user_id="user1", name="Vendor", amount=100, date="2024-04-01")
    assert amount_consistency_chris(transaction, transactions) is True
