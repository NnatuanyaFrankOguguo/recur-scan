# test features_original.py
from datetime import date

import pytest

from recur_scan.features_original import get_transaction_z_score, parse_date
from recur_scan.transactions import Transaction


def test_parse_date():
    """Test parse_date function."""
    # Test with valid date format
    assert parse_date("2024-01-01") == date(2024, 1, 1)

    # Test with invalid date format
    with pytest.raises(ValueError, match=r"does not match format"):
        parse_date("01/01/2024")


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
