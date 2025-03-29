from collections import defaultdict

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
from recur_scan.features_laurels import (
    _aggregate_transactions,
    _calculate_intervals,
    _calculate_statistics,
    date_irregularity_dominance,
    day_consistency_score_feature,
    day_of_week_feature,
    identical_transaction_ratio_feature,
    interval_variability_feature,
    is_deposit_feature,
    is_monthly_recurring_feature,
    is_near_periodic_interval_feature,
    is_single_transaction_feature,
    is_varying_amount_recurring_feature,
    low_amount_variation_feature,
    merchant_amount_frequency_feature,
    merchant_amount_std_feature,
    merchant_interval_mean_feature,
    merchant_interval_std_feature,
    non_recurring_irregularity_score,
    recurrence_likelihood_feature,
    rolling_amount_mean_feature,
    time_since_last_transaction_same_merchant_feature,
    transaction_month_feature,
    transaction_pattern_complexity,
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
    parse_date,
)
from recur_scan.transactions import Transaction


def get_features(transaction: Transaction, all_transactions: list[Transaction]) -> dict[str, float | int | bool]:
    """Get the features for a transaction"""
    """Extract all features for a transaction by calling individual feature functions.
    This prepares a dictionary of features for model training.

    Args:
        transaction (Transaction): The transaction to extract features for.
        all_transactions (List[Transaction]): List of all transactions for context.

    Returns:
        Dict[str, Union[float, int]]: Dictionary mapping feature names to their computed values.
    """
    # Compute groups and amount counts internally
    groups = _aggregate_transactions(all_transactions)
    amount_counts: defaultdict[float, int] = defaultdict(int)
    for t in all_transactions:
        amount_counts[t.amount] += 1

    # Extract user ID and merchant name from the transaction
    user_id, merchant_name = transaction.user_id, transaction.name
    # Get transactions for this user and merchant
    merchant_trans = groups.get(user_id, {}).get(merchant_name, [])
    # Sort transactions by date for chronological analysis
    merchant_trans.sort(key=lambda x: x.date)

    # Parse all dates for this merchant's transactions once
    parsed_dates = []
    for trans in merchant_trans:
        date = parse_date(trans.date)
        if date is not None:
            parsed_dates.append(date)

    # Calculate intervals and amounts for statistical analysis
    intervals = _calculate_intervals(parsed_dates)
    amounts = [trans.amount for trans in merchant_trans]
    interval_stats = _calculate_statistics([float(i) for i in intervals])
    amount_stats = _calculate_statistics(amounts)

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
        # Laurels' features
        # "n_transactions_same_amount": n_transactions_same_amount_feature(transaction, amount_counts),
        # "percent_transactions_same_amount": percent_transactions_same_amount_feature(
        #     transaction, all_transactions, amount_counts
        # ),
        "identical_transaction_ratio": identical_transaction_ratio_feature(
            transaction, all_transactions, merchant_trans
        ),
        "is_monthly_recurring": is_monthly_recurring_feature(merchant_trans),
        "recurrence_likelihood": recurrence_likelihood_feature(merchant_trans, interval_stats, amount_stats),
        "is_varying_amount_recurring": is_varying_amount_recurring_feature(interval_stats, amount_stats),
        "day_consistency_score": day_consistency_score_feature(merchant_trans),
        "is_near_periodic_interval": is_near_periodic_interval_feature(interval_stats),
        "merchant_amount_std": merchant_amount_std_feature(amount_stats),
        "merchant_interval_std": merchant_interval_std_feature(interval_stats),
        "merchant_interval_mean": merchant_interval_mean_feature(interval_stats),
        "time_since_last_transaction_same_merchant": time_since_last_transaction_same_merchant_feature(parsed_dates),
        "is_deposit": is_deposit_feature(transaction, merchant_trans),
        "day_of_week": day_of_week_feature(transaction),
        "transaction_month": transaction_month_feature(transaction),
        "rolling_amount_mean": rolling_amount_mean_feature(merchant_trans),
        "low_amount_variation": low_amount_variation_feature(amount_stats),
        "is_single_transaction": is_single_transaction_feature(merchant_trans),
        "interval_variability": interval_variability_feature(interval_stats),
        "merchant_amount_frequency": merchant_amount_frequency_feature(merchant_trans),
        "non_recurring_irregularity_score": non_recurring_irregularity_score(
            merchant_trans, interval_stats, amount_stats
        ),
        "transaction_pattern_complexity": transaction_pattern_complexity(merchant_trans, interval_stats),
        "date_irregularity_dominance": date_irregularity_dominance(merchant_trans, interval_stats, amount_stats),
    }
