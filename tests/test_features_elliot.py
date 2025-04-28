import pytest

from recur_scan.features_elliot import (
    amount_similarity,
    amount_variability_ratio,
    get_is_always_recurring,
    get_is_near_same_amount,
    get_time_regularity_score,
    get_transaction_amount_variance,
    get_transaction_similarity,
    is_auto_pay,
    is_membership,
    is_price_trending,
    is_recurring_based_on_99,
    is_split_transaction,
    is_utility_bill,
    is_weekday_transaction,
    most_common_interval,
)
from recur_scan.transactions import Transaction


@pytest.fixture
def transactions():
    """Fixture providing test transactions."""
    return [
        Transaction(id=1, user_id="user1", name="Allstate Insurance", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="AT&T", amount=100, date="2024-01-01"),
        Transaction(id=3, user_id="user1", name="Duke Energy", amount=200, date="2024-01-02"),
        Transaction(id=4, user_id="user1", name="HighEnergy Soft Drinks", amount=2.99, date="2024-01-03"),
        Transaction(id=5, user_id="user1", name="Netflix", amount=15.99, date="2024-01-04"),
        Transaction(id=6, user_id="user1", name="AutoPay Subscription", amount=50, date="2024-01-05"),
        Transaction(id=7, user_id="user1", name="Gym Membership", amount=30, date="2024-01-06"),
    ]


def test_is_utility_bill(transactions) -> None:
    """Test is_utility_bill."""
    assert is_utility_bill(transactions[2])  # Assuming transactions[2] is a utility bill
    assert not is_utility_bill(transactions[3])  # Assuming transactions[3] is NOT a utility bill


def test_get_is_near_same_amount(transactions) -> None:
    """Test get_is_near_same_amount."""
    assert get_is_near_same_amount(transactions[0], transactions)
    assert not get_is_near_same_amount(transactions[3], transactions)


def test_get_is_always_recurring(transactions) -> None:
    """Test get_is_always_recurring."""
    assert get_is_always_recurring(transactions[4])
    assert not get_is_always_recurring(transactions[3])


def test_is_auto_pay(transactions) -> None:
    """Test is_auto_pay."""
    assert is_auto_pay(transactions[5])
    assert not is_auto_pay(transactions[0])


def test_is_membership(transactions) -> None:
    """Test is_membership."""
    assert is_membership(transactions[6])
    assert not is_membership(transactions[0])


def test_is_recurring_based_on_99(transactions):
    """Test the is_recurring_based_on_99 function."""
    transactions = [
        Transaction(id=1, user_id="user1", name="Spotify", amount=9.99, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Spotify", amount=9.99, date="2024-01-08"),  # 7 days later
        Transaction(id=3, user_id="user1", name="Spotify", amount=9.99, date="2024-01-15"),  # 7 days later
        Transaction(id=4, user_id="user1", name="Spotify", amount=9.99, date="2024-02-14"),  # 30 days later
        Transaction(id=5, user_id="user1", name="Netflix", amount=14.99, date="2024-01-01"),  # Different vendor
        Transaction(id=6, user_id="user1", name="Spotify", amount=9.99, date="2024-03-14"),  # 30 days later
        Transaction(id=7, user_id="user1", name="Spotify", amount=10.00, date="2024-04-14"),  # Not ending in .99
    ]

    # Case 1: Transaction follows the recurring pattern (7-day interval, at least 3 occurrences)
    assert is_recurring_based_on_99(transactions[0], transactions)

    # Case 2: Different vendor, should return False
    assert not is_recurring_based_on_99(transactions[4], transactions)

    # Case 3: Amount does not end in .99, should return False
    assert not is_recurring_based_on_99(transactions[6], transactions)

    # Case 4: Only two transactions exist with .99, should return False
    small_list = transactions[:2]  # Only two transactions
    assert not is_recurring_based_on_99(transactions[1], small_list)

    # Case 5: Transaction is in a valid 30-day recurring pattern
    assert is_recurring_based_on_99(transactions[5], transactions)

    # Case 6: Transaction is in a valid 30-day recurring pattern
    assert is_recurring_based_on_99(transactions[3], transactions)


# New tests


@pytest.fixture
def new_transactions():
    """Fixture providing new test transactions."""
    return [
        Transaction(id=1, user_id="user1", name="Spotify", amount=9.99, date="2024-03-18"),  # Monday
        Transaction(id=2, user_id="user1", name="Spotify Premium", amount=9.99, date="2024-03-19"),  # Tuesday
        Transaction(id=3, user_id="user1", name="Spotify US", amount=9.99, date="2024-03-20"),  # Wednesday
        Transaction(id=4, user_id="user1", name="Amazon Prime", amount=14.99, date="2024-03-21"),  # Thursday
        Transaction(id=5, user_id="user1", name="Netflix", amount=15.99, date="2024-03-22"),  # Friday
        Transaction(id=6, user_id="user1", name="Spotify", amount=10.99, date="2024-03-23"),  # Saturday
        Transaction(id=7, user_id="user1", name="Spotify", amount=11.99, date="2024-03-24"),  # Sunday
    ]


def test_get_transaction_similarity(new_transactions):
    """Test get_transaction_similarity function."""
    # Check similarity between slightly different names
    score = get_transaction_similarity(new_transactions[0], new_transactions)
    assert score > 50  # Adjusted similarity threshold

    # Different vendor should have low similarity
    score = get_transaction_similarity(new_transactions[4], new_transactions)
    assert score < 50  # Netflix should not match Spotify


def test_is_weekday_transaction(new_transactions):
    """Test is_weekday_transaction function."""
    assert is_weekday_transaction(new_transactions[0]) is True  # Monday
    assert is_weekday_transaction(new_transactions[4]) is True  # Friday
    assert is_weekday_transaction(new_transactions[5]) is False  # Saturday
    assert is_weekday_transaction(new_transactions[6]) is False  # Sunday


def test_is_price_trending(new_transactions):
    """Test is_price_trending function."""
    assert (
        is_price_trending(new_transactions[0], new_transactions, threshold=15) is True
    )  # Small increase within 15% threshold
    assert (
        is_price_trending(new_transactions[0], new_transactions, threshold=5) is False
    )  # Larger increase, exceeds 5% threshold


def test_is_split_transaction():
    """Test is_split_transaction function."""
    all_transactions = [
        Transaction(id=1, user_id="user1", name="Laptop Payment", amount=1000, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Laptop Payment", amount=500, date="2024-01-10"),
        Transaction(id=3, user_id="user1", name="Laptop Payment", amount=500, date="2024-01-20"),
        Transaction(id=4, user_id="user1", name="Amazon", amount=100, date="2024-02-01"),
    ]

    assert is_split_transaction(all_transactions[0], all_transactions) is True  # Two smaller related transactions
    assert is_split_transaction(all_transactions[3], all_transactions) is False  # No split transactions


# NEW FEATURES TESTS


def test_get_time_regularity_score():
    """Test get_time_regularity_score function."""
    txns = [
        {"name": "Spotify", "date": "2024-01-01"},
        {"name": "Spotify", "date": "2024-01-08"},  # 7 days later
        {"name": "Spotify", "date": "2024-01-15"},  # 7 days later
        {"name": "Netflix", "date": "2024-01-01"},  # Different vendor
    ]
    txn = {"name": "Spotify", "date": "2024-01-01"}

    # Case 1: Regular intervals (7 days)
    assert get_time_regularity_score(txn, txns) > 0.5

    # Case 2: Very irregular intervals (adjusted expectation)
    very_irregular_txns = [
        {"name": "Spotify", "date": "2024-01-01"},
        {"name": "Spotify", "date": "2024-01-05"},  # 4 days later
        {"name": "Spotify", "date": "2024-01-30"},  # 25 days later
        {"name": "Spotify", "date": "2024-02-20"},  # 21 days later
    ]
    # The implementation uses 1.0 / (1.0 + stddev / 5.0), so we need larger variance
    assert get_time_regularity_score(txn, very_irregular_txns) < 0.5

    # Case 3: Not enough transactions
    small_txns = [{"name": "Spotify", "date": "2024-01-01"}]
    assert get_time_regularity_score(txn, small_txns) == 0.0


def test_get_transaction_amount_variance():
    """Test get_transaction_amount_variance function."""
    txns = [
        {"name": "Spotify", "amount": 9.99},
        {"name": "Spotify", "amount": 10.99},
        {"name": "Spotify", "amount": 11.99},
        {"name": "Netflix", "amount": 15.99},  # Different vendor
    ]
    txn = {"name": "Spotify", "amount": 9.99}

    # Case 1: Variance exists
    assert get_transaction_amount_variance(txn, txns) > 0.0

    # Case 2: No variance (all amounts are the same)
    uniform_txns = [
        {"name": "Spotify", "amount": 9.99},
        {"name": "Spotify", "amount": 9.99},
        {"name": "Spotify", "amount": 9.99},
    ]
    assert get_transaction_amount_variance(txn, uniform_txns) == 0.0

    # Case 3: Not enough transactions
    small_txns = [{"name": "Spotify", "amount": 9.99}]
    assert get_transaction_amount_variance(txn, small_txns) == 0.0


def test_most_common_interval():
    """Test most_common_interval function."""
    # Case 1: Regular intervals
    transactions = [
        Transaction(id=1, user_id="user1", name="Spotify", amount=9.99, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Spotify", amount=9.99, date="2024-01-08"),
        Transaction(id=3, user_id="user1", name="Spotify", amount=9.99, date="2024-01-15"),
        Transaction(id=4, user_id="user1", name="Spotify", amount=9.99, date="2024-01-22"),
    ]
    # Since the most common interval is 7 days
    interval = most_common_interval(transactions)
    assert interval == 7 or interval == 7.0  # Accept either int or float

    # Case 2: Irregular intervals but with a common difference of 9 days
    transactions_irregular = [
        Transaction(id=1, user_id="user1", name="Spotify", amount=9.99, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Spotify", amount=9.99, date="2024-01-10"),
        Transaction(id=3, user_id="user1", name="Spotify", amount=9.99, date="2024-01-19"),
    ]
    interval = most_common_interval(transactions_irregular)
    assert interval == 9 or interval == 9.0  # Accept either int or float

    # Case 3: Single transaction
    transactions_single = [
        Transaction(id=1, user_id="user1", name="Spotify", amount=9.99, date="2024-01-01"),
    ]
    assert most_common_interval(transactions_single) == 0


def test_amount_variability_ratio():
    """Test amount_variability_ratio function."""
    # Case 1: Variability exists
    transactions = [
        Transaction(id=1, user_id="user1", name="Vendor", amount=9.99, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Vendor", amount=10.99, date="2024-01-08"),
        Transaction(id=3, user_id="user1", name="Vendor", amount=11.99, date="2024-01-15"),
        Transaction(id=4, user_id="user1", name="Vendor", amount=12.99, date="2024-01-22"),
    ]
    assert amount_variability_ratio(transactions) > 0.0

    # Case 2: No variability (all amounts are the same)
    uniform_transactions = [
        Transaction(id=1, user_id="user1", name="Vendor", amount=9.99, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Vendor", amount=9.99, date="2024-01-08"),
        Transaction(id=3, user_id="user1", name="Vendor", amount=9.99, date="2024-01-15"),
    ]
    assert amount_variability_ratio(uniform_transactions) == 0.0

    # Case 3: Empty list
    empty_transactions = []
    assert amount_variability_ratio(empty_transactions) == 0.0


def test_amount_similarity():
    """Test amount_similarity function."""
    # Case 1: High similarity - transactions with similar amounts
    similar_transactions = [
        Transaction(id=1, user_id="user1", name="Vendor", amount=9.99, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Vendor", amount=10.00, date="2024-01-08"),
        Transaction(id=3, user_id="user1", name="Vendor", amount=10.01, date="2024-01-15"),
        Transaction(id=4, user_id="user1", name="Vendor", amount=10.02, date="2024-01-22"),
    ]
    # The function now takes a list of transactions and an optional tolerance
    assert amount_similarity(similar_transactions, 0.1) > 0.75

    # Case 2: Low similarity - transactions with very different amounts
    dissimilar_transactions = [
        Transaction(id=1, user_id="user1", name="Vendor", amount=9.99, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Vendor", amount=20.00, date="2024-01-08"),
        Transaction(id=3, user_id="user1", name="Vendor", amount=30.00, date="2024-01-15"),
        Transaction(id=4, user_id="user1", name="Vendor", amount=40.00, date="2024-01-22"),
    ]
    assert amount_similarity(dissimilar_transactions, 0.1) < 0.5

    # Case 3: Empty transaction list
    empty_transactions = []
    assert amount_similarity(empty_transactions) == 0.0


def test_parse_date():
    """Test parse_date function - using imported parse_date from features_elliot."""
    from datetime import datetime

    from recur_scan.features_elliot import parse_date

    # Valid date strings
    assert parse_date("2024-01-01") == datetime(2024, 1, 1)
    assert parse_date("01/01/2024") == datetime(2024, 1, 1)
    assert parse_date("January 1, 2024") == datetime(2024, 1, 1)

    # Invalid date strings
    assert parse_date("invalid-date") is None
    assert parse_date("") is None
    # Note: The parse_date in features_elliot can handle None by catching TypeError
