from recur_scan.features_christopher import (
    detect_skipped_months,
    follows_regular_interval,
    get_coefficient_of_variation,
    get_day_of_month_consistency,
    get_median_interval,
    get_n_transactions_same_amount_chris,
    get_percent_transactions_same_amount_chris,
    get_transaction_frequency,
    get_transaction_std_amount,
    is_known_fixed_subscription,
    is_known_recurring_company,
)
from recur_scan.features_frank import (
    amount_coefficient_of_variation,
    amount_similarity,
    amount_stability_score,
    amount_z_score,
    detect_non_recurring_pattern,
    detect_recurring_company,
    detect_subscription_pattern,
    frequency_features,
    get_enhanced_features,
    get_same_amount_ratio,
    get_transaction_intervals,
    get_transaction_stability_features,
    merchant_category_features,
    normalized_days_difference,
    one_time_features,
    proportional_timing_deviation,
    recurrence_interval_variance,
    seasonal_spending_cycle,
    vendor_recurrence_trend,
    weekly_spending_cycle,
)
from recur_scan.features_original import (
    get_ends_in_99,
    get_is_always_recurring,
    get_is_insurance,
    get_is_phone,
    get_is_utility,
    get_n_transactions_days_apart,
    get_n_transactions_same_amount,
    get_n_transactions_same_day,
    get_pct_transactions_days_apart,
    get_pct_transactions_same_day,
    get_percent_transactions_same_amount,
    get_transaction_z_score,
)
from recur_scan.transactions import Transaction


def get_features(transaction: Transaction, all_transactions: list[Transaction]) -> dict[str, float | int | bool]:
    """Get the features for a transaction"""

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
        # Frank's features
        "likely_same_amount": amount_similarity(transaction, all_transactions),
        "normalized_days_difference": normalized_days_difference(transaction, all_transactions),
        "amount_stability_score": amount_stability_score(all_transactions),
        "amount_z_score": amount_z_score(transaction, all_transactions),
        "weekly_spendings ": weekly_spending_cycle(all_transactions),
        "vendor_recurrence_trend": vendor_recurrence_trend(all_transactions),
        "seasonal_spending_cycle": seasonal_spending_cycle(transaction, all_transactions),
        "recurrence_interval_variance": recurrence_interval_variance(all_transactions),
        **frequency_features(all_transactions),
        **detect_non_recurring_pattern(all_transactions),  # Merges non-recurring pattern features
        **get_transaction_intervals(all_transactions),  # Merges new time-based features
        "amount_ratio": get_same_amount_ratio(transaction, all_transactions),
        "amount_coefficient_of_variation": amount_coefficient_of_variation(all_transactions),
        "proportional_timing_deviation": proportional_timing_deviation(transaction, all_transactions),
        **detect_recurring_company(transaction.name),  # Merges recurring company features
        **merchant_category_features(transaction.name),  # Merges merchant category features
        **one_time_features(all_transactions),  # Merges one-time purchase features
        **detect_subscription_pattern(all_transactions),  # Merges subscription-based features
        **get_enhanced_features(transaction, all_transactions, len(all_transactions)),  # Merges new enhanced features
        **get_transaction_stability_features(all_transactions),  # Merges new stability-based features
        # "days_since_last_transaction": get_days_since_last_transaction(transaction, all_transactions),
        # **measure_transaction_freq
        # Christopher's features
        "n_transactions_same_name": len(all_transactions),
        "n_transactions_same_amount_chris": get_n_transactions_same_amount_chris(transaction, all_transactions),
        "percent_transactions_same_amount_chris": get_percent_transactions_same_amount_chris(
            transaction, all_transactions
        ),
        "transaction_frequency": get_transaction_frequency(all_transactions),
        "transaction_std_amount": get_transaction_std_amount(all_transactions),
        "follows_regular_interval": follows_regular_interval(all_transactions),
        "skipped_months": detect_skipped_months(all_transactions),
        "day_of_month_consistency": get_day_of_month_consistency(all_transactions),
        "coefficient_of_variation": get_coefficient_of_variation(all_transactions),
        "median_interval": get_median_interval(all_transactions),
        "is_known_recurring_company": is_known_recurring_company(transaction.name),
        "is_known_fixed_subscription": is_known_fixed_subscription(transaction),
    }
