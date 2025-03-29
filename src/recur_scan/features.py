from collections import defaultdict

from recur_scan.features_adeyinka import (
    get_average_days_between_transactions,
    get_outlier_score,
    get_recurring_confidence_score,
    get_same_amount_vendor_transactions,
    get_subscription_keyword_score,
    get_time_regularity_score,
    get_transaction_amount_variance,
)
from recur_scan.features_adeyinka import (
    get_is_always_recurring as get_is_always_recurring_adeyinka,
)
from recur_scan.features_adeyinka import (
    get_n_transactions_days_apart as get_n_transactions_days_apart_adeyinka,
)
from recur_scan.features_asimi import (
    get_amount_category,
    get_amount_pattern_features,
    get_temporal_consistency_features,
    get_user_recurring_vendor_count,
    get_user_specific_features,
    get_user_transaction_frequency,
    get_user_vendor_interaction_count,
    get_user_vendor_recurrence_rate,
    get_user_vendor_relationship_features,
    get_user_vendor_transaction_count,
    get_vendor_amount_std,
    get_vendor_recurrence_profile,
    get_vendor_recurring_user_count,
    get_vendor_transaction_frequency,
    is_valid_recurring_transaction,
)
from recur_scan.features_asimi import (
    get_amount_features as get_amount_features_asimi,
)
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
from recur_scan.features_ebenezer import (
    get_avg_amount_same_day_of_week,
    get_avg_amount_same_month,
    get_avg_amount_same_name,
    get_n_transactions_same_month,
    get_n_transactions_same_name,
    get_n_transactions_same_user_id,
    get_n_transactions_within_amount_range,
    get_percent_transactions_same_day_of_week,
    get_percent_transactions_same_month,
    get_percent_transactions_same_name,
    get_percent_transactions_same_user_id,
    get_percent_transactions_within_amount_range,
    get_std_amount_same_day_of_week,
    get_std_amount_same_month,
    get_std_amount_same_name,
)
from recur_scan.features_elliot import (
    get_is_always_recurring as get_is_always_recurring_elliot,
)
from recur_scan.features_elliot import (
    get_is_near_same_amount,
    get_transaction_similarity,
    is_auto_pay,
    is_membership,
    is_price_trending,
    is_recurring_based_on_99,
    is_split_transaction,
    is_utility_bill,
    is_weekday_transaction,
)
from recur_scan.features_emmanuel_ezechukwu1 import (
    get_amount_cv,
    get_days_between_std,
    get_exact_amount_count,
    get_has_recurring_keyword,
    get_is_convenience_store,
)
from recur_scan.features_emmanuel_ezechukwu1 import (
    get_day_of_month_consistency as get_day_of_month_consistency_emmanuel1,
)
from recur_scan.features_emmanuel_ezechukwu1 import (
    get_is_always_recurring as get_is_always_recurring_emmanuel1,
)
from recur_scan.features_emmanuel_ezechukwu1 import (
    get_is_insurance as get_is_insurance_emmanuel1,
)
from recur_scan.features_emmanuel_ezechukwu1 import (
    get_is_phone as get_is_phone_emmanuel1,
)
from recur_scan.features_emmanuel_ezechukwu1 import (
    get_is_utility as get_is_utility_emmanuel1,
)
from recur_scan.features_emmanuel_ezechukwu1 import (
    get_n_transactions_days_apart as get_n_transactions_days_apart_emmanuel1,
)
from recur_scan.features_emmanuel_ezechukwu1 import (
    get_n_transactions_same_amount as get_n_transactions_same_amount_emmanuel1,
)
from recur_scan.features_emmanuel_ezechukwu1 import (
    get_percent_transactions_same_amount as get_percent_transactions_same_amount_emmanuel1,
)
from recur_scan.features_emmanuel_ezechukwu2 import (
    classify_subscription_tier,
    get_monthly_spending_trend,
    get_recurrence_patterns,
    get_recurring_consistency_score,
    get_refund_features,
    get_user_behavior_features,
    validate_recurring_transaction,
)
from recur_scan.features_emmanuel_ezechukwu2 import (
    get_amount_features as get_amount_features_emmanuel2,
)
from recur_scan.features_felix import (
    get_average_transaction_amount as get_average_transaction_amount_felix,
)
from recur_scan.features_felix import (
    get_day as get_day_felix,
)
from recur_scan.features_felix import (
    get_dispersion_transaction_amount as get_dispersion_transaction_amount_felix,
)
from recur_scan.features_felix import (
    get_is_always_recurring as get_is_always_recurring_felix,
)
from recur_scan.features_felix import (
    get_is_insurance as get_is_insurance_felix,
)
from recur_scan.features_felix import (
    get_is_phone as get_is_phone_felix,
)
from recur_scan.features_felix import (
    get_is_utility as get_is_utility_felix,
)
from recur_scan.features_felix import (
    get_max_transaction_amount as get_max_transaction_amount_felix,
)
from recur_scan.features_felix import (
    get_median_variation_transaction_amount,
    get_month,
    get_n_transactions_same_vendor,
    get_transaction_rate,
    get_transactions_interval_stability,
    get_variation_ratio,
    get_year,
)
from recur_scan.features_felix import (
    get_min_transaction_amount as get_min_transaction_amount_felix,
)
from recur_scan.features_felix import (
    get_transaction_intervals as get_transaction_intervals_felix,
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
from recur_scan.features_happy import (
    get_day_of_month_consistency as get_day_of_month_consistency_happy,
)
from recur_scan.features_happy import (
    get_n_transactions_same_description,
    get_percent_transactions_same_description,
)
from recur_scan.features_happy import (
    get_transaction_frequency as get_transaction_frequency_happy,
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
from recur_scan.features_nnanna import (
    get_average_transaction_amount,
    get_dispersion_transaction_amount,
    get_mad_transaction_amount,
    get_mobile_transaction,
    get_time_interval_between_transactions,
    get_transaction_interval_consistency,
)
from recur_scan.features_nnanna import (
    get_coefficient_of_variation as get_coefficient_of_variation_nnanna,
)
from recur_scan.features_nnanna import (
    get_transaction_frequency as get_transaction_frequency_nnanna,
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
from recur_scan.features_osasere import (
    get_day_of_month_consistency as get_day_of_month_consistency_osasere,
)
from recur_scan.features_osasere import (
    get_day_of_month_variability,
    get_median_period,
    get_recurrence_confidence,
    has_min_recurrence_period,
    is_weekday_consistent,
)
from recur_scan.features_praise import (
    amount_ends_in_00,
    amount_ends_in_99,
    get_avg_days_between_same_merchant_amount,
    get_days_since_last_same_merchant_amount,
    get_interval_variance_coefficient,
    get_max_transaction_amount,
    get_min_transaction_amount,
    get_most_frequent_names,
    get_n_transactions_same_merchant_amount,
    get_percent_transactions_same_merchant_amount,
    get_stddev_days_between_same_merchant_amount,
    has_consistent_reference_codes,
    has_incrementing_numbers,
    is_expected_transaction_date,
    is_recurring,
    is_recurring_merchant,
)
from recur_scan.features_praise import (
    get_average_transaction_amount as get_average_transaction_amount_praise,
)
from recur_scan.features_precious import (
    amount_ends_in_00 as amount_ends_in_00_precious,
)
from recur_scan.features_precious import (
    get_additional_features,
    get_amount_variation_features,
    get_recurring_frequency,
    is_subscription_amount,
)
from recur_scan.features_precious import (
    get_avg_days_between_same_merchant_amount as get_avg_days_between_same_merchant_amount_precious,
)
from recur_scan.features_precious import (
    get_days_since_last_same_merchant_amount as get_days_since_last_same_merchant_amount_precious,
)
from recur_scan.features_precious import (
    get_n_transactions_same_merchant_amount as get_n_transactions_same_merchant_amount_precious,
)
from recur_scan.features_precious import (
    get_percent_transactions_same_merchant_amount as get_percent_transactions_same_merchant_amount_precious,
)
from recur_scan.features_precious import (
    get_stddev_days_between_same_merchant_amount as get_stddev_days_between_same_merchant_amount_precious,
)
from recur_scan.features_precious import (
    is_recurring_merchant as is_recurring_merchant_precious,
)
from recur_scan.features_samuel import (
    get_amount_std_dev,
    get_is_weekend_transaction,
    get_median_transaction_amount,
)
from recur_scan.features_samuel import (
    get_is_always_recurring as get_is_always_recurring_samuel,
)
from recur_scan.features_samuel import (
    get_transaction_frequency as get_transaction_frequency_samuel,
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
        # Emmanuel Ezechukwu (2)'s features
        **get_recurrence_patterns(transaction, all_transactions),
        **get_recurring_consistency_score(transaction, all_transactions),
        "is_recurring": int(validate_recurring_transaction(transaction)),
        "subscription_tier": classify_subscription_tier(transaction),
        **get_amount_features_emmanuel2(transaction, all_transactions),
        **get_user_behavior_features(transaction, all_transactions),
        **get_refund_features(transaction, all_transactions),
        **get_monthly_spending_trend(transaction, all_transactions),
        # Nnanna's features
        "time_interval_between_transactions": get_time_interval_between_transactions(transaction, all_transactions),
        "mobile_company": get_mobile_transaction(transaction),
        "transaction_frequency_nnanna": get_transaction_frequency_nnanna(transaction, all_transactions),
        "transaction_amount_dispersion": get_dispersion_transaction_amount(transaction, all_transactions),
        "mad_transaction_amount": get_mad_transaction_amount(transaction, all_transactions),
        "coefficient_of_variation_nnanna": get_coefficient_of_variation_nnanna(transaction, all_transactions),
        "transaction_interval_consistency": get_transaction_interval_consistency(transaction, all_transactions),
        "average_transaction_amount": get_average_transaction_amount(transaction, all_transactions),
        # Ebenezer's features
        "n_transactions_same_name_ebenezer": get_n_transactions_same_name(transaction, all_transactions),
        "percent_transactions_same_name": get_percent_transactions_same_name(transaction, all_transactions),
        "avg_amount_same_name": get_avg_amount_same_name(transaction, all_transactions),
        "std_amount_same_name": get_std_amount_same_name(transaction, all_transactions),
        "n_transactions_same_month": get_n_transactions_same_month(transaction, all_transactions),
        "percent_transactions_same_month": get_percent_transactions_same_month(transaction, all_transactions),
        "avg_amount_same_month": get_avg_amount_same_month(transaction, all_transactions),
        "std_amount_same_month": get_std_amount_same_month(transaction, all_transactions),
        "n_transactions_same_user_id": get_n_transactions_same_user_id(transaction, all_transactions),
        "percent_transactions_same_user_id": get_percent_transactions_same_user_id(transaction, all_transactions),
        "percent_transactions_same_day_of_week": get_percent_transactions_same_day_of_week(
            transaction, all_transactions
        ),
        "avg_amount_same_day_of_week": get_avg_amount_same_day_of_week(transaction, all_transactions),
        "std_amount_same_day_of_week": get_std_amount_same_day_of_week(transaction, all_transactions),
        "n_transactions_within_amount_range": get_n_transactions_within_amount_range(transaction, all_transactions),
        "percent_transactions_within_amount_range": get_percent_transactions_within_amount_range(
            transaction, all_transactions
        ),
        # Praise's features
        "is_recurring_merchant": is_recurring_merchant(transaction),
        "avg_days_between_same_merchant_amount": get_avg_days_between_same_merchant_amount(
            transaction, all_transactions
        ),
        "average_transaction_amount_praise": get_average_transaction_amount_praise(all_transactions),
        "max_transaction_amount": get_max_transaction_amount(all_transactions),
        "min_transaction_amount": get_min_transaction_amount(all_transactions),
        "most_frequent_names": len(get_most_frequent_names(all_transactions)),
        "is_recurring_praise": is_recurring(transaction, all_transactions),
        "amount_ends_in_99": amount_ends_in_99(transaction),
        "amount_ends_in_00": amount_ends_in_00(transaction),
        "n_transactions_same_merchant_amount": get_n_transactions_same_merchant_amount(transaction, all_transactions),
        "percent_transactions_same_merchant_amount": get_percent_transactions_same_merchant_amount(
            transaction, all_transactions
        ),
        "interval_variance_coefficient": get_interval_variance_coefficient(transaction, all_transactions),
        "stddev_days_between_same_merchant_amount": get_stddev_days_between_same_merchant_amount(
            transaction, all_transactions
        ),
        "days_since_last_same_merchant_amount": get_days_since_last_same_merchant_amount(transaction, all_transactions),
        "is_expected_transaction_date": is_expected_transaction_date(transaction, all_transactions),
        "has_incrementing_numbers": has_incrementing_numbers(transaction, all_transactions),
        "has_consistent_reference_codes": has_consistent_reference_codes(transaction, all_transactions),
        # Emmanuel Ezechukwu (1)'s features
        "n_transactions_same_amount_emmanuel1": get_n_transactions_same_amount_emmanuel1(transaction, all_transactions),
        "percent_transactions_same_amount_emmanuel1": get_percent_transactions_same_amount_emmanuel1(
            transaction, all_transactions
        ),
        "days_between_std": get_days_between_std(transaction, all_transactions),
        "amount_cv": get_amount_cv(transaction, all_transactions),
        "day_of_month_consistency_emmanuel1": get_day_of_month_consistency_emmanuel1(transaction, all_transactions),
        "exact_amount_count": get_exact_amount_count(transaction, all_transactions),
        "has_recurring_keyword": get_has_recurring_keyword(transaction),
        "is_always_recurring_emmanuel1": int(get_is_always_recurring_emmanuel1(transaction)),
        "n_transactions_30_days_apart": get_n_transactions_days_apart_emmanuel1(transaction, all_transactions, 30, 2),
        "is_convenience_store_emmanuel1": get_is_convenience_store(transaction),
        "is_insurance_emmanuel1": int(get_is_insurance_emmanuel1(transaction)),
        "is_utility_emmanuel1": int(get_is_utility_emmanuel1(transaction)),
        "is_phone_emmanuel1": int(get_is_phone_emmanuel1(transaction)),
        # Asimi's features
        **get_amount_features_asimi(transaction),
        **get_user_recurring_vendor_count(transaction, all_transactions),
        **get_user_transaction_frequency(transaction, all_transactions),
        **get_vendor_amount_std(transaction, all_transactions),
        **get_vendor_recurring_user_count(transaction, all_transactions),
        **get_vendor_transaction_frequency(transaction, all_transactions),
        **get_user_vendor_transaction_count(transaction, all_transactions),
        **get_user_vendor_recurrence_rate(transaction, all_transactions),
        **get_user_vendor_interaction_count(transaction, all_transactions),
        **get_amount_category(transaction),
        **get_amount_pattern_features(transaction, all_transactions),
        **get_temporal_consistency_features(transaction, all_transactions),
        **get_vendor_recurrence_profile(transaction, all_transactions),
        **get_user_vendor_relationship_features(transaction, all_transactions),
        "is_recurring_asimi": is_valid_recurring_transaction(transaction),
        **get_user_specific_features(transaction, all_transactions),
        # Samuel's features
        "transaction_frequency_samuel": get_transaction_frequency_samuel(transaction, all_transactions),
        "amount_std_dev": get_amount_std_dev(transaction, all_transactions),
        "median_transaction_amount": get_median_transaction_amount(transaction, all_transactions),
        "is_weekend_transaction": get_is_weekend_transaction(transaction),
        "is_always_recurring_samuel": get_is_always_recurring_samuel(transaction),
        # Precious's features
        "amount_ends_in_00_precious": amount_ends_in_00_precious(transaction),
        "is_recurring_merchant_precious": is_recurring_merchant_precious(transaction),
        "n_transactions_same_merchant_amount_precious": get_n_transactions_same_merchant_amount_precious(
            transaction, all_transactions
        ),
        "percent_transactions_same_merchant_amount_precious": get_percent_transactions_same_merchant_amount_precious(
            transaction, all_transactions
        ),
        "avg_days_between_same_merchant_amount_precious": get_avg_days_between_same_merchant_amount_precious(
            transaction, all_transactions
        ),
        "stddev_days_between_same_merchant_amount_precious": get_stddev_days_between_same_merchant_amount_precious(
            transaction, all_transactions
        ),
        "days_since_last_same_merchant_amount_precious": get_days_since_last_same_merchant_amount_precious(
            transaction, all_transactions
        ),
        "recurring_frequency": get_recurring_frequency(transaction, all_transactions),
        "is_subscription_amount": is_subscription_amount(transaction),
        **get_additional_features(transaction, all_transactions),
        **get_amount_variation_features(transaction, all_transactions),
        # Happy's features
        "get_n_transactions_same_description": get_n_transactions_same_description(transaction, all_transactions),
        "get_percent_transactions_same_description": get_percent_transactions_same_description(
            transaction, all_transactions
        ),
        "get_transaction_same_frequency": get_transaction_frequency_happy(transaction, all_transactions),
        "get_day_of_month_consistency": get_day_of_month_consistency_happy(transaction, all_transactions),
        # Osasere's features
        "has_min_recurrence_period_osasere": has_min_recurrence_period(transaction, all_transactions),
        "day_of_month_consistency_osasere": get_day_of_month_consistency_osasere(transaction, all_transactions),
        "day_of_month_variability": get_day_of_month_variability(transaction, all_transactions),
        "recurrence_confidence": get_recurrence_confidence(transaction, all_transactions),
        "median_period_days": get_median_period(transaction, all_transactions),
        "is_weekday_consistent": is_weekday_consistent(transaction, all_transactions),
        # Felix's features
        "n_transactions_same_vendor": get_n_transactions_same_vendor(transaction, all_transactions),
        "max_transaction_amount_felix": get_max_transaction_amount_felix(all_transactions),
        "min_transaction_amount_felix": get_min_transaction_amount_felix(all_transactions),
        "is_phone_felix": get_is_phone_felix(transaction),
        "month": get_month(transaction),
        "day_felix": get_day_felix(transaction),
        "year": get_year(transaction),
        "is_insurance_felix": get_is_insurance_felix(transaction),
        "is_utility_felix": get_is_utility_felix(transaction),
        "is_always_recurring_felix": get_is_always_recurring_felix(transaction),
        "median_variation_transaction_amount": get_median_variation_transaction_amount(transaction, all_transactions),
        "variation_ratio": get_variation_ratio(transaction, all_transactions),
        "transactions_interval_stability": get_transactions_interval_stability(transaction, all_transactions),
        "average_transaction_amount_felix": get_average_transaction_amount_felix(transaction, all_transactions),
        "dispersion_transaction_amount_felix": get_dispersion_transaction_amount_felix(transaction, all_transactions),
        "transaction_rate": get_transaction_rate(transaction, all_transactions),
        **get_transaction_intervals_felix(all_transactions),
        # Adeyinka's features
        "avg_days_between_transactions_adeyinka": get_average_days_between_transactions(transaction, all_transactions),
        "time_regularity_score_adeyinka": get_time_regularity_score(transaction, all_transactions),
        "is_always_recurring_adeyinka": get_is_always_recurring_adeyinka(transaction),
        "transaction_amount_variance_adeyinka": get_transaction_amount_variance(transaction, all_transactions),
        "outlier_score_adeyinka": get_outlier_score(transaction, all_transactions),
        "recurring_confidence_score_adeyinka": get_recurring_confidence_score(transaction, all_transactions),
        "subscription_keyword_score_adeyinka": get_subscription_keyword_score(transaction),
        "same_amount_vendor_transactions_adeyinka": get_same_amount_vendor_transactions(transaction, all_transactions),
        "30_days_apart_exact_adeyinka": get_n_transactions_days_apart_adeyinka(transaction, all_transactions, 30, 0),
        "30_days_apart_off_by_1_adeyinka": get_n_transactions_days_apart_adeyinka(transaction, all_transactions, 30, 1),
        "14_days_apart_exact_adeyinka": get_n_transactions_days_apart_adeyinka(transaction, all_transactions, 14, 0),
        "14_days_apart_off_by_1_adeyinka": get_n_transactions_days_apart_adeyinka(transaction, all_transactions, 14, 1),
        "7_days_apart_exact_adeyinka": get_n_transactions_days_apart_adeyinka(transaction, all_transactions, 7, 0),
        "7_days_apart_off_by_1_adeyinka": get_n_transactions_days_apart_adeyinka(transaction, all_transactions, 7, 1),
        # Elliot's features
        "is_utility_elliot": is_utility_bill(transaction),
        "is_always_recurring_elliot": get_is_always_recurring_elliot(transaction),
        "is_auto_pay": is_auto_pay(transaction),
        "is_membership": is_membership(transaction),
        "is_near_same_amount": get_is_near_same_amount(transaction, all_transactions),
        "is_recurring_based_on_99": is_recurring_based_on_99(transaction, all_transactions),
        "transaction_similarity": get_transaction_similarity(transaction, all_transactions),
        "is_weekday_transaction": is_weekday_transaction(transaction),
        "is_split_transaction": is_split_transaction(transaction, all_transactions),
        "is_price_trending_5pct": is_price_trending(transaction, all_transactions, 5),
        "is_price_trending_10pct": is_price_trending(transaction, all_transactions, 10),
    }
