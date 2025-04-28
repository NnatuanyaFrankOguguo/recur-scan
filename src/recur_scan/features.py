from collections import defaultdict

from recur_scan.features_adedotun import (
    amount_variability_score as amount_variability_score_adedotun,
    compute_recurring_inputs_at as compute_recurring_inputs_adedotun,
    get_amount_uniqueness_score_at as get_amount_uniqueness_score_adedotun,
    get_contains_common_nonrecurring_keywords_at as get_contains_common_nonrecurring_keywords_adedotun,
    get_days_since_last_occurrence_at as get_days_since_last_occurrence_adedotun,
    get_interval_histogram as get_interval_histogram_adedotun,
    get_interval_variance_coefficient as get_interval_variance_coefficient_adedotun,
    get_is_always_recurring_at as get_is_always_recurring_adedotun,
    get_is_communication_or_energy_at as get_is_communication_or_energy_adedotun,
    get_is_entertainment_at as get_is_entertainment_adedotun,
    get_is_food_dining_at as get_is_food_dining_adedotun,
    get_is_gambling_at as get_is_gambling_adedotun,
    get_is_gaming_at as get_is_gaming_adedotun,
    get_is_insurance_at as get_is_insurance_adedotun,
    get_is_month_end_at as get_is_month_end_adedotun,
    get_is_one_time_vendor_at as get_is_one_time_vendor_adedotun,
    get_is_phone_at as get_is_phone_adedotun,
    get_is_retail_at as get_is_retail_adedotun,
    get_is_travel_at as get_is_travel_adedotun,
    get_is_utility_at as get_is_utility_adedotun,
    get_is_weekend_at as get_is_weekend_adedotun,
    get_n_transactions_same_amount_chris as get_n_transactions_same_amount_adedotun,
    get_percent_transactions_same_amount_chris as get_percent_transactions_same_amount_adedotun,
    get_percent_transactions_same_amount_tolerant as get_percent_transactions_same_amount_tolerant_adedotun,
    get_same_amount_count_at as get_same_amount_count_adedotun,
    get_similar_amount_count_at as get_similar_amount_count_adedotun,
    get_user_vendor_occurrence_count_at as get_user_vendor_occurrence_count_adedotun,
    get_vendor_name_entropy_at as get_vendor_name_entropy_adedotun,
    get_vendor_occurrence_count_at as get_vendor_occurrence_count_adedotun,
    is_known_recurring_company as is_known_recurring_company_adedotun,
    is_price_trending as is_price_trending_adedotun,
    is_recurring_allowance_at as is_recurring_allowance_adedotun,
    is_recurring_based_on_99 as is_recurring_based_on_99_adedotun,
    is_recurring_core_at as is_recurring_core_adedotun,
)
from recur_scan.features_adeyinka import (
    get_average_days_between_transactions as get_average_days_between_transactions_adeyinka,
    get_is_always_recurring as get_is_always_recurring_adeyinka,
    get_n_transactions_days_apart as get_n_transactions_days_apart_adeyinka,
    get_outlier_score as get_outlier_score_adeyinka,
    get_recurring_confidence_score as get_recurring_confidence_score_adeyinka,
    get_same_amount_vendor_transactions as get_same_amount_vendor_transactions_adeyinka,
    get_subscription_keyword_score as get_subscription_keyword_score_adeyinka,
    get_time_regularity_score as get_time_regularity_score_adeyinka,
    get_transaction_amount_variance as get_transaction_amount_variance_adeyinka,
)
from recur_scan.features_asimi import (
    get_amount_category as get_amount_category_asimi,
    get_amount_features as get_amount_features_asimi,
    get_amount_pattern_features as get_amount_pattern_features_asimi,
    get_temporal_consistency_features as get_temporal_consistency_features_asimi,
    get_user_recurring_vendor_count as get_user_recurring_vendor_count_asimi,
    get_user_specific_features as get_user_specific_features_asimi,
    get_user_transaction_frequency as get_user_transaction_frequency_asimi,
    get_user_vendor_interaction_count as get_user_vendor_interaction_count_asimi,
    get_user_vendor_recurrence_rate as get_user_vendor_recurrence_rate_asimi,
    get_user_vendor_relationship_features as get_user_vendor_relationship_features_asimi,
    get_user_vendor_transaction_count as get_user_vendor_transaction_count_asimi,
    get_vendor_amount_std as get_vendor_amount_std_asimi,
    get_vendor_recurrence_profile as get_vendor_recurrence_profile_asimi,
    get_vendor_recurring_user_count as get_vendor_recurring_user_count_asimi,
    get_vendor_transaction_frequency as get_vendor_transaction_frequency_asimi,
    is_valid_recurring_transaction as is_valid_recurring_transaction_asimi,
)
from recur_scan.features_bassey import (
    get_days_since_last_transaction_bassey,
    get_is_frequent_merchant_bassey,
    get_is_gym_membership as get_is_gym_membership_bassey,
    get_is_high_value_transaction_bassey,
    get_is_merchant_recurring_bassey,
    get_is_recurring_apple_bassey,
    get_is_same_day_multiple_transactions_bassey,
    get_is_streaming_service as get_is_streaming_service_bassey,
    get_is_subscription as get_is_subscription_bassey,
    get_is_weekend_transaction_bassey,
    get_is_weekly_recurring_apple_bassey,
    get_monthly_spending_average_bassey,
)
from recur_scan.features_christopher import (
    detect_skipped_months as detect_skipped_months_christopher,
    follows_regular_interval as follows_regular_interval_christopher,
    get_coefficient_of_variation as get_coefficient_of_variation_christopher,
    get_day_of_month_consistency as get_day_of_month_consistency_christopher,
    get_median_interval as get_median_interval_christopher,
    get_n_transactions_same_amount_chris as get_n_transactions_same_amount_christopher,
    get_percent_transactions_same_amount_chris as get_percent_transactions_same_amount_christopher,
    get_transaction_frequency as get_transaction_frequency_christopher,
    get_transaction_std_amount as get_transaction_std_amount_christopher,
    is_known_fixed_subscription as is_known_fixed_subscription_christopher,
    is_known_recurring_company as is_known_recurring_company_christopher,
)
from recur_scan.features_dallanq import (
    amount_diff_from_mean as amount_diff_from_mean_dallanq,
    amount_diff_from_modal as amount_diff_from_modal_dallanq,
    amount_freq_fraction as amount_freq_fraction_dallanq,
    amount_frequency_rank as amount_frequency_rank_dallanq,
    amount_matches_modal as amount_matches_modal_dallanq,
    avg_txn_per_month as avg_txn_per_month_dallanq,
    biweekly_tolerance as biweekly_tolerance_dallanq,
    count_last_28_days as count_last_28_days_dallanq,
    count_last_35_days as count_last_35_days_dallanq,
    count_last_90_days as count_last_90_days_dallanq,
    count_last_n_days as count_last_n_days_dallanq,
    count_transactions as count_transactions_dallanq,
    day_of_month as day_of_month_dallanq,
    day_of_week as day_of_week_dallanq,
    days_since_group_start as days_since_group_start_dallanq,
    days_since_last as days_since_last_dallanq,
    days_until_next as days_until_next_dallanq,
    dom_diff_from_modal as dom_diff_from_modal_dallanq,
    ends_in_00 as ends_in_00_dallanq,
    frac_txns_in_same_month as frac_txns_in_same_month_dallanq,
    fraction_active_months as fraction_active_months_dallanq,
    fraction_modal_amount as fraction_modal_amount_dallanq,
    fraction_mode_interval as fraction_mode_interval_dallanq,
    fraction_same_day_of_month as fraction_same_day_of_month_dallanq,
    get_ends_in_99 as get_ends_in_99_dallanq,
    get_is_always_recurring as get_is_always_recurring_dallanq,
    get_is_insurance as get_is_insurance_dallanq,
    get_is_phone as get_is_phone_dallanq,
    get_is_utility as get_is_utility_dallanq,
    get_n_transactions_days_apart as get_n_transactions_days_apart_dallanq,
    get_n_transactions_days_apart_same_amount as get_n_transactions_days_apart_same_amount_dallanq,
    get_n_transactions_same_amount as get_n_transactions_same_amount_dallanq,
    get_n_transactions_same_day as get_n_transactions_same_day_dallanq,
    get_pct_transactions_days_apart as get_pct_transactions_days_apart_dallanq,
    get_pct_transactions_days_apart_same_amount as get_pct_transactions_days_apart_same_amount_dallanq,
    get_pct_transactions_same_day as get_pct_transactions_same_day_dallanq,
    get_percent_transactions_same_amount as get_percent_transactions_same_amount_dallanq,
    get_transaction_z_score as get_transaction_z_score_dallanq,
    is_amazon_prime as is_amazon_prime_dallanq,
    is_amazon_prime_video as is_amazon_prime_video_dallanq,
    is_apple as is_apple_dallanq,
    is_carwash_company as is_carwash_company_dallanq,
    is_cash_advance_company as is_cash_advance_company_dallanq,
    is_insurance_company as is_insurance_company_dallanq,
    is_likely_subscription_amount as is_likely_subscription_amount_dallanq,
    is_loan_company as is_loan_company_dallanq,
    is_modal_dom as is_modal_dom_dallanq,
    is_pay_in_four_company as is_pay_in_four_company_dallanq,
    is_phone_company as is_phone_company_dallanq,
    is_rental_company as is_rental_company_dallanq,
    is_subscription_company as is_subscription_company_dallanq,
    is_usually_subscription_company as is_usually_subscription_company_dallanq,
    is_utility_company as is_utility_company_dallanq,
    is_weekend as is_weekend_dallanq,
    mean_amount as mean_amount_dallanq,
    mean_days_between as mean_days_between_dallanq,
    modal_amount as modal_amount_dallanq,
    modal_day_of_month as modal_day_of_month_dallanq,
    mode_interval as mode_interval_dallanq,
    month_of_year as month_of_year_dallanq,
    monthly_tolerance as monthly_tolerance_dallanq,
    n_consecutive_months_same_amount as n_consecutive_months_same_amount_dallanq,
    n_monthly_same_amount as n_monthly_same_amount_dallanq,
    n_same_day_same_amount as n_same_day_same_amount_dallanq,
    n_small_transactions as n_small_transactions_dallanq,
    n_small_transactions_not_this_amount as n_small_transactions_not_this_amount_dallanq,
    next_interval_dev_from_mean as next_interval_dev_from_mean_dallanq,
    next_interval_dev_from_mode as next_interval_dev_from_mode_dallanq,
    next_within_monthly_tol as next_within_monthly_tol_dallanq,
    pct_consecutive_months_same_amount as pct_consecutive_months_same_amount_dallanq,
    pct_monthly_same_amount as pct_monthly_same_amount_dallanq,
    pct_same_day_same_amount as pct_same_day_same_amount_dallanq,
    pct_small_transactions as pct_small_transactions_dallanq,
    pct_small_transactions_not_this_amount as pct_small_transactions_not_this_amount_dallanq,
    position_in_span as position_in_span_dallanq,
    prev_interval_dev_from_mean as prev_interval_dev_from_mean_dallanq,
    prev_interval_dev_from_mode as prev_interval_dev_from_mode_dallanq,
    prev_within_monthly_tol as prev_within_monthly_tol_dallanq,
    quarterly_tolerance as quarterly_tolerance_dallanq,
    regularity_score as regularity_score_dallanq,
    rel_amount_diff_from_modal as rel_amount_diff_from_modal_dallanq,
    relative_amount_diff as relative_amount_diff_dallanq,
    same_day_of_month_count as same_day_of_month_count_dallanq,
    span_months as span_months_dallanq,
    std_amount as std_amount_dallanq,
    std_days_between as std_days_between_dallanq,
    total_span_months as total_span_months_dallanq,
    transaction_span_days as transaction_span_days_dallanq,
    txns_in_same_month as txns_in_same_month_dallanq,
    weekly_tolerance as weekly_tolerance_dallanq,
)
from recur_scan.features_ebenezer import (
    get_avg_amount_same_day_of_week as get_avg_amount_same_day_of_week_ebenezer,
    get_avg_amount_same_month as get_avg_amount_same_month_ebenezer,
    get_avg_amount_same_name as get_avg_amount_same_name_ebenezer,
    get_n_transactions_same_month as get_n_transactions_same_month_ebenezer,
    get_n_transactions_same_name as get_n_transactions_same_name_ebenezer,
    get_n_transactions_same_user_id as get_n_transactions_same_user_id_ebenezer,
    get_n_transactions_within_amount_range as get_n_transactions_within_amount_range_ebenezer,
    get_percent_transactions_same_day_of_week as get_percent_transactions_same_day_of_week_ebenezer,
    get_percent_transactions_same_month as get_percent_transactions_same_month_ebenezer,
    get_percent_transactions_same_name as get_percent_transactions_same_name_ebenezer,
    get_percent_transactions_same_user_id as get_percent_transactions_same_user_id_ebenezer,
    get_percent_transactions_within_amount_range as get_percent_transactions_within_amount_range_ebenezer,
    get_std_amount_same_day_of_week as get_std_amount_same_day_of_week_ebenezer,
    get_std_amount_same_month as get_std_amount_same_month_ebenezer,
    get_std_amount_same_name as get_std_amount_same_name_ebenezer,
)
from recur_scan.features_efehi import (
    get_irregular_periodicity as get_irregular_periodicity_efehi,
    get_irregular_periodicity_with_tolerance as get_irregular_periodicity_with_tolerance_efehi,
    get_n_same_name_transactions as get_n_same_name_transactions_efehi,
    get_time_between_transactions as get_time_between_transactions_efehi,
    get_transaction_amount_stability as get_transaction_amount_stability_efehi,
    get_transaction_frequency as get_transaction_frequency_efehi,
    get_transaction_time_of_month as get_transaction_time_of_month_efehi,
    get_user_transaction_frequency as get_user_transaction_frequency_efehi,
    get_vendor_recurrence_consistency as get_vendor_recurrence_consistency_efehi,
    get_vendor_recurring_ratio as get_vendor_recurring_ratio_efehi,
)
from recur_scan.features_elliot import (
    get_is_always_recurring as get_is_always_recurring_elliot,
    get_is_near_same_amount as get_is_near_same_amount_elliot,
    get_transaction_similarity as get_transaction_similarity_elliot,
    is_auto_pay as is_auto_pay_elliot,
    is_membership as is_membership_elliot,
    is_price_trending as is_price_trending_elliot,
    is_recurring_based_on_99 as is_recurring_based_on_99_elliot,
    is_split_transaction as is_split_transaction_elliot,
    is_utility_bill as is_utility_bill_elliot,
    is_weekday_transaction as is_weekday_transaction_elliot,
)
from recur_scan.features_emmanuel_eze import (
    detect_sequence_patterns as detect_sequence_patterns_emmanuel_eze,
    get_is_recurring as get_is_recurring_emmanuel_eze,
    get_recurring_transaction_confidence as get_recurring_transaction_confidence_emmanuel_eze,
)
from recur_scan.features_emmanuel_ezechukwu1 import (
    get_amount_cv as get_amount_cv_emmanuel1,
    get_day_of_month_consistency as get_day_of_month_consistency_emmanuel1,
    get_days_between_std as get_days_between_std_emmanuel1,
    get_exact_amount_count as get_exact_amount_count_emmanuel1,
    get_has_recurring_keyword as get_has_recurring_keyword_emmanuel1,
    get_is_always_recurring as get_is_always_recurring_emmanuel1,
    get_is_convenience_store as get_is_convenience_store_emmanuel1,
    get_is_insurance as get_is_insurance_emmanuel1,
    get_is_phone as get_is_phone_emmanuel1,
    get_is_utility as get_is_utility_emmanuel1,
    get_n_transactions_days_apart as get_n_transactions_days_apart_emmanuel1,
    get_n_transactions_same_amount as get_n_transactions_same_amount_emmanuel1,
    get_percent_transactions_same_amount as get_percent_transactions_same_amount_emmanuel1,
)
from recur_scan.features_emmanuel_ezechukwu2 import (
    classify_subscription_tier as classify_subscription_tier_emmanuel2,
    get_amount_features as get_amount_features_emmanuel2,
    get_monthly_spending_trend as get_monthly_spending_trend_emmanuel2,
    get_recurrence_patterns as get_recurrence_patterns_emmanuel2,
    get_recurring_consistency_score as get_recurring_consistency_score_emmanuel2,
    get_refund_features as get_refund_features_emmanuel2,
    get_user_behavior_features as get_user_behavior_features_emmanuel2,
    validate_recurring_transaction as validate_recurring_transaction_emmanuel2,
)
from recur_scan.features_ernest import (
    get_average_transaction_amount as get_average_transaction_amount_ernest,
    get_is_biweekly as get_is_biweekly_ernest,
    get_is_fixed_amount as get_is_fixed_amount_ernest,
    get_is_high_frequency_vendor as get_is_high_frequency_vendor_ernest,
    get_is_monthly as get_is_monthly_ernest,
    get_is_quarterly as get_is_quarterly_ernest,
    get_is_recurring_vendor as get_is_recurring_vendor_ernest,
    get_is_round_amount as get_is_round_amount_ernest,
    get_is_same_day_of_month as get_is_same_day_of_month_ernest,
    get_is_small_amount as get_is_small_amount_ernest,
    get_is_subscription_based as get_is_subscription_based_ernest,
    get_is_weekend_transaction as get_is_weekend_transaction_ernest,
    get_is_weekly as get_is_weekly_ernest,
    get_recurring_interval_score as get_recurring_interval_score_ernest,
    get_transaction_frequency as get_transaction_frequency_ernest,
    get_transaction_gap_stats as get_transaction_gap_stats_ernest,
    get_vendor_amount_variance as get_vendor_amount_variance_ernest,
    get_vendor_transaction_count as get_vendor_transaction_count_ernest,
)
from recur_scan.features_felix import (
    get_average_transaction_amount as get_average_transaction_amount_felix,
    get_day as get_day_felix,
    get_dispersion_transaction_amount as get_dispersion_transaction_amount_felix,
    get_is_always_recurring as get_is_always_recurring_felix,
    get_is_insurance as get_is_insurance_felix,
    get_is_phone as get_is_phone_felix,
    get_is_utility as get_is_utility_felix,
    get_max_transaction_amount as get_max_transaction_amount_felix,
    get_median_variation_transaction_amount as get_median_variation_transaction_amount_felix,
    get_min_transaction_amount as get_min_transaction_amount_felix,
    get_month as get_month_felix,
    get_n_transactions_same_vendor as get_n_transactions_same_vendor_felix,
    get_transaction_intervals as get_transaction_intervals_felix,
    get_transaction_rate as get_transaction_rate_felix,
    get_transactions_interval_stability as get_transactions_interval_stability_felix,
    get_variation_ratio as get_variation_ratio_felix,
    get_year as get_year_felix,
)
from recur_scan.features_frank import (
    amount_coefficient_of_variation as amount_coefficient_of_variation_frank,
    amount_similarity as amount_similarity_frank,
    amount_stability_score as amount_stability_score_frank,
    amount_variability_ratio as amount_variability_ratio_frank,
    amount_variability_score as amount_variability_score_frank,
    amount_z_score as amount_z_score_frank,
    calculate_cycle_consistency as calculate_cycle_consistency_frank,
    coefficient_of_variation_intervals as coefficient_of_variation_intervals_frank,
    date_irregularity_score as date_irregularity_score_frank,
    enhanced_amt_iqr as enhanced_amt_iqr_frank,
    enhanced_days_since_last as enhanced_days_since_last_frank,
    enhanced_n_similar_last_n_days as enhanced_n_similar_last_n_days_frank,
    get_amount_consistency as get_amount_consistency_frank,
    get_same_amount_ratio as get_same_amount_ratio_frank,
    get_subscription_score as get_subscription_score_frank,
    inconsistent_amount_score as inconsistent_amount_score_frank,
    irregular_interval_score as irregular_interval_score_frank,
    is_recurring_company as is_recurring_company_frank,
    is_utility_company as is_utility_company_frank,
    matches_common_cycle as matches_common_cycle_frank,
    most_common_interval as most_common_interval_frank,
    non_recurring_score as non_recurring_score_frank,
    normalized_days_difference as normalized_days_difference_frank,
    proportional_timing_deviation as proportional_timing_deviation_frank,
    recurrence_interval_variance as recurrence_interval_variance_frank,
    recurring_confidence as recurring_confidence_frank,
    recurring_score as recurring_score_frank,
    robust_interval_iqr as robust_interval_iqr_frank,
    robust_interval_median as robust_interval_median_frank,
    seasonal_spending_cycle as seasonal_spending_cycle_frank,
    transaction_frequency as transaction_frequency_frank,
    transactions_per_month as transactions_per_month_frank,
    transactions_per_week as transactions_per_week_frank,
    vendor_recurrence_trend as vendor_recurrence_trend_frank,
    weekly_spending_cycle as weekly_spending_cycle_frank,
)
from recur_scan.features_freedom import (
    get_day_of_week as get_day_of_week_freedom,
    get_days_until_next_transaction as get_days_until_next_transaction_freedom,
    get_periodicity_confidence as get_periodicity_confidence_freedom,
    get_recurrence_streak as get_recurrence_streak_freedom,
)
from recur_scan.features_gideon import (
    is_microsoft_xbox_same_or_near_day as is_microsoft_xbox_same_or_near_day_gideon,
)
from recur_scan.features_happy import (
    get_day_of_month_consistency as get_day_of_month_consistency_happy,
    get_n_transactions_same_description as get_n_transactions_same_description_happy,
    get_percent_transactions_same_description as get_percent_transactions_same_description_happy,
    get_transaction_frequency as get_transaction_frequency_happy,
)
from recur_scan.features_laurels import (
    _aggregate_transactions as _aggregate_transactions_laurels,
    _calculate_intervals as _calculate_intervals_laurels,
    _calculate_statistics as _calculate_statistics_laurels,
    date_irregularity_dominance as date_irregularity_dominance_laurels,
    day_consistency_score_feature as day_consistency_score_feature_laurels,
    day_of_week_feature as day_of_week_feature_laurels,
    identical_transaction_ratio_feature as identical_transaction_ratio_feature_laurels,
    interval_variability_feature as interval_variability_feature_laurels,
    is_deposit_feature as is_deposit_feature_laurels,
    is_monthly_recurring_feature as is_monthly_recurring_feature_laurels,
    is_near_periodic_interval_feature as is_near_periodic_interval_feature_laurels,
    is_single_transaction_feature as is_single_transaction_feature_laurels,
    is_varying_amount_recurring_feature as is_varying_amount_recurring_feature_laurels,
    low_amount_variation_feature as low_amount_variation_feature_laurels,
    merchant_amount_frequency_feature as merchant_amount_frequency_feature_laurels,
    merchant_amount_std_feature as merchant_amount_std_feature_laurels,
    merchant_interval_mean_feature as merchant_interval_mean_feature_laurels,
    merchant_interval_std_feature as merchant_interval_std_feature_laurels,
    non_recurring_irregularity_score as non_recurring_irregularity_score_laurels,
    recurrence_likelihood_feature as recurrence_likelihood_feature_laurels,
    rolling_amount_mean_feature as rolling_amount_mean_feature_laurels,
    time_since_last_transaction_same_merchant_feature as time_since_last_transaction_same_merchant_feature_laurels,
    transaction_month_feature as transaction_month_feature_laurels,
    transaction_pattern_complexity as transaction_pattern_complexity_laurels,
)
from recur_scan.features_naomi import (
    get_cluster_label as get_cluster_label_naomi,
    get_is_monthly_recurring as get_is_monthly_recurring_naomi,
    get_is_similar_amount as get_is_similar_amount_naomi,
    get_outlier_score as get_outlier_score_naomi,
    get_recurring_confidence_score as get_recurring_confidence_score_naomi,
    get_subscription_keyword_score as get_subscription_keyword_score_naomi,
    get_time_regularity_score as get_time_regularity_score_naomi,
    get_transaction_interval_consistency as get_transaction_interval_consistency_naomi,
)
from recur_scan.features_nnanna import (
    get_average_transaction_amount as get_average_transaction_amount_nnanna,
    get_coefficient_of_variation as get_coefficient_of_variation_nnanna,
    get_dispersion_transaction_amount as get_dispersion_transaction_amount_nnanna,
    get_mad_transaction_amount as get_mad_transaction_amount_nnanna,
    get_mobile_transaction as get_mobile_transaction_nnanna,
    get_time_interval_between_transactions as get_time_interval_between_transactions_nnanna,
    get_transaction_frequency as get_transaction_frequency_nnanna,
    get_transaction_interval_consistency as get_transaction_interval_consistency_nnanna,
)
from recur_scan.features_osasere import (
    get_day_of_month_consistency as get_day_of_month_consistency_osasere,
    get_day_of_month_variability as get_day_of_month_variability_osasere,
    get_median_period as get_median_period_osasere,
    get_recurrence_confidence as get_recurrence_confidence_osasere,
    has_min_recurrence_period as has_min_recurrence_period_osasere,
    is_weekday_consistent as is_weekday_consistent_osasere,
)
from recur_scan.features_praise import (
    amount_ends_in_00 as amount_ends_in_00_praise,
    amount_ends_in_99 as amount_ends_in_99_praise,
    get_average_transaction_amount as get_average_transaction_amount_praise,
    get_avg_days_between_same_merchant_amount as get_avg_days_between_same_merchant_amount_praise,
    get_days_since_last_same_merchant_amount as get_days_since_last_same_merchant_amount_praise,
    get_interval_variance_coefficient as get_interval_variance_coefficient_praise,
    get_max_transaction_amount as get_max_transaction_amount_praise,
    get_min_transaction_amount as get_min_transaction_amount_praise,
    get_most_frequent_names as get_most_frequent_names_praise,
    get_n_transactions_same_merchant_amount as get_n_transactions_same_merchant_amount_praise,
    get_percent_transactions_same_merchant_amount as get_percent_transactions_same_merchant_amount_praise,
    get_stddev_days_between_same_merchant_amount as get_stddev_days_between_same_merchant_amount_praise,
    has_consistent_reference_codes as has_consistent_reference_codes_praise,
    has_incrementing_numbers as has_incrementing_numbers_praise,
    is_expected_transaction_date as is_expected_transaction_date_praise,
    is_recurring as is_recurring_praise,
    is_recurring_merchant as is_recurring_merchant_praise,
)
from recur_scan.features_precious import (
    amount_ends_in_00 as amount_ends_in_00_precious,
    get_additional_features,
    get_amount_variation_features,
    get_avg_days_between_same_merchant_amount as get_avg_days_between_same_merchant_amount_precious,
    get_days_since_last_same_merchant_amount as get_days_since_last_same_merchant_amount_precious,
    get_n_transactions_same_merchant_amount as get_n_transactions_same_merchant_amount_precious,
    get_percent_transactions_same_merchant_amount as get_percent_transactions_same_merchant_amount_precious,
    get_recurring_frequency,
    get_stddev_days_between_same_merchant_amount as get_stddev_days_between_same_merchant_amount_precious,
    is_recurring_merchant as is_recurring_merchant_precious,
    is_subscription_amount,
)
from recur_scan.features_raphael import (
    get_has_irregular_spike as get_has_irregular_spike_raphael,
    get_is_common_subscription_amount as get_is_common_subscription_amount_raphael,
    get_is_first_of_month as get_is_first_of_month_raphael,
    get_is_fixed_interval as get_is_fixed_interval_raphael,
    get_is_similar_name as get_is_similar_name_raphael,
    get_n_transactions_days_apart as get_n_transactions_days_apart_raphael,
    get_n_transactions_same_day as get_n_transactions_same_day_raphael,
    get_occurs_same_week as get_occurs_same_week_raphael,
    get_pct_transactions_days_apart as get_pct_transactions_days_apart_raphael,
    get_pct_transactions_same_day as get_pct_transactions_same_day_raphael,
)
from recur_scan.features_samuel import (
    get_amount_std_dev as get_amount_std_dev_samuel,
    get_is_always_recurring as get_is_always_recurring_samuel,
    get_is_weekend_transaction as get_is_weekend_transaction_samuel,
    get_median_transaction_amount as get_median_transaction_amount_samuel,
    get_transaction_frequency as get_transaction_frequency_samuel,
)
from recur_scan.features_segun import (
    get_average_transaction_amount as get_average_transaction_amount_segun,
    get_average_transaction_interval as get_average_transaction_interval_segun,
    get_max_transaction_amount as get_max_transaction_amount_segun,
    get_min_transaction_amount as get_min_transaction_amount_segun,
    get_total_transaction_amount as get_total_transaction_amount_segun,
    get_transaction_amount_frequency as get_transaction_amount_frequency_segun,
    get_transaction_amount_median as get_transaction_amount_median_segun,
    get_transaction_amount_range as get_transaction_amount_range_segun,
    get_transaction_amount_std as get_transaction_amount_std_segun,
    get_transaction_day_of_week as get_transaction_day_of_week_segun,
    get_transaction_time_of_day as get_transaction_time_of_day_segun,
    get_unique_transaction_amount_count as get_unique_transaction_amount_count_segun,
)
from recur_scan.features_tife import (
    get_amount_cluster_count as get_amount_cluster_count_tife,
    get_amount_range as get_amount_range_tife,
    get_amount_relative_change as get_amount_relative_change_tife,
    get_amount_stability_score as get_amount_stability_score_tife,
    get_amount_variability as get_amount_variability_tife,
    get_days_since_last_same_amount as get_days_since_last_same_amount_tife,
    get_dominant_interval_strength as get_dominant_interval_strength_tife,
    get_interval_consistency as get_interval_consistency_tife,
    get_interval_histogram as get_interval_histogram_tife,
    get_interval_mode as get_interval_mode_tife,
    get_merchant_amount_signature as get_merchant_amount_signature_tife,
    get_merchant_name_frequency as get_merchant_name_frequency_tife,
    get_near_amount_consistency as get_near_amount_consistency_tife,
    get_normalized_interval_consistency as get_normalized_interval_consistency_tife,
    get_transaction_count as get_transaction_count_tife,
    get_transaction_density as get_transaction_density_tife,
    get_transaction_frequency as get_transaction_frequency_tife,
)
from recur_scan.features_victor import (
    get_avg_days_between as get_avg_days_between_victor,
)
from recur_scan.features_yoloye import (
    get_delayed_annual as get_delayed_annual_yoloye,
    get_delayed_fortnightly as get_delayed_fortnightly_yoloye,
    get_delayed_monthly as get_delayed_monthly_yoloye,
    get_delayed_quarterly as get_delayed_quarterly_yoloye,
    get_delayed_semi_annual as get_delayed_semi_annual_yoloye,
    get_delayed_weekly as get_delayed_weekly_yoloye,
    get_early_annual as get_early_annual_yoloye,
    get_early_fortnightly as get_early_fortnightly_yoloye,
    get_early_monthly as get_early_monthly_yoloye,
    get_early_quarterly as get_early_quarterly_yoloye,
    get_early_semi_annual as get_early_semi_annual_yoloye,
    get_early_weekly as get_early_weekly_yoloye,
)
from recur_scan.transactions import Transaction
from recur_scan.utils import parse_date


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
    groups = _aggregate_transactions_laurels(all_transactions)
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
    intervals = _calculate_intervals_laurels(parsed_dates)
    amounts = [trans.amount for trans in merchant_trans]
    interval_stats = _calculate_statistics_laurels([float(i) for i in intervals])
    amount_stats = _calculate_statistics_laurels(amounts)

    histogram = get_interval_histogram_tife(all_transactions)

    vendor_txns, user_vendor_txns, preprocessed = compute_recurring_inputs_adedotun(transaction, all_transactions)
    date_obj = preprocessed["date_objects"][transaction]
    total_txns = len(vendor_txns)

    sequence_features = detect_sequence_patterns_emmanuel_eze(transaction, all_transactions)

    return {
        # DallanQ's features
        "n_transactions_same_amount_dallanq": get_n_transactions_same_amount_dallanq(transaction, all_transactions),
        "percent_transactions_same_amount_dallanq": get_percent_transactions_same_amount_dallanq(
            transaction, all_transactions
        ),
        "ends_in_99_dallanq": get_ends_in_99_dallanq(transaction),
        "amount_dallanq": transaction.amount,
        "same_day_exact_dallanq": get_n_transactions_same_day_dallanq(transaction, all_transactions, 0),
        "pct_transactions_same_day_dallanq": get_pct_transactions_same_day_dallanq(transaction, all_transactions, 0),
        "same_day_off_by_1_dallanq": get_n_transactions_same_day_dallanq(transaction, all_transactions, 1),
        "same_day_off_by_2_dallanq": get_n_transactions_same_day_dallanq(transaction, all_transactions, 2),
        "14_days_apart_exact_dallanq": get_n_transactions_days_apart_dallanq(transaction, all_transactions, 14, 0),
        "pct_14_days_apart_exact_dallanq": get_pct_transactions_days_apart_dallanq(
            transaction, all_transactions, 14, 0
        ),
        "14_days_apart_off_by_1_dallanq": get_n_transactions_days_apart_dallanq(transaction, all_transactions, 14, 1),
        "pct_14_days_apart_off_by_1_dallanq": get_pct_transactions_days_apart_dallanq(
            transaction, all_transactions, 14, 1
        ),
        "7_days_apart_exact_dallanq": get_n_transactions_days_apart_dallanq(transaction, all_transactions, 7, 0),
        "pct_7_days_apart_exact_dallanq": get_pct_transactions_days_apart_dallanq(transaction, all_transactions, 7, 0),
        "7_days_apart_off_by_1_dallanq": get_n_transactions_days_apart_dallanq(transaction, all_transactions, 7, 1),
        "pct_7_days_apart_off_by_1_dallanq": get_pct_transactions_days_apart_dallanq(
            transaction, all_transactions, 7, 1
        ),
        "is_insurance_dallanq": get_is_insurance_dallanq(transaction),
        "is_utility_dallanq": get_is_utility_dallanq(transaction),
        "is_phone_dallanq": get_is_phone_dallanq(transaction),
        "is_always_recurring_dallanq": get_is_always_recurring_dallanq(transaction),
        "z_score_dallanq": get_transaction_z_score_dallanq(transaction, all_transactions),
        "abs_z_score_dallanq": abs(get_transaction_z_score_dallanq(transaction, all_transactions)),
        "count_transactions_dallanq": count_transactions_dallanq(all_transactions),
        "days_since_last_dallanq": days_since_last_dallanq(transaction, all_transactions),
        "days_until_next_dallanq": days_until_next_dallanq(transaction, all_transactions),
        "mean_days_between_dallanq": mean_days_between_dallanq(all_transactions),
        "std_days_between_dallanq": std_days_between_dallanq(all_transactions),
        "regularity_score_dallanq": regularity_score_dallanq(all_transactions),
        "transaction_span_days_dallanq": transaction_span_days_dallanq(all_transactions),
        "count_last_n_days_dallanq": count_last_n_days_dallanq(transaction, all_transactions),
        "count_last_28_days_dallanq": count_last_28_days_dallanq(transaction, all_transactions),
        "count_last_35_days_dallanq": count_last_35_days_dallanq(transaction, all_transactions),
        "count_last_90_days_dallanq": count_last_90_days_dallanq(transaction, all_transactions),
        "mean_amount_dallanq": mean_amount_dallanq(all_transactions),
        "std_amount_dallanq": std_amount_dallanq(all_transactions),
        "amount_diff_from_mean_dallanq": amount_diff_from_mean_dallanq(transaction, all_transactions),
        "relative_amount_diff_dallanq": relative_amount_diff_dallanq(transaction, all_transactions),
        "day_of_week_dallanq": day_of_week_dallanq(transaction),
        "is_weekend_dallanq": is_weekend_dallanq(transaction),
        "day_of_month_dallanq": day_of_month_dallanq(transaction),
        "month_of_year_dallanq": month_of_year_dallanq(transaction),
        "same_day_of_month_count_dallanq": same_day_of_month_count_dallanq(transaction, all_transactions),
        "fraction_same_day_of_month_dallanq": fraction_same_day_of_month_dallanq(transaction, all_transactions),
        "monthly_tolerance_dallanq": monthly_tolerance_dallanq(all_transactions),
        "quarterly_tolerance_dallanq": quarterly_tolerance_dallanq(all_transactions),
        "weekly_tolerance_dallanq": weekly_tolerance_dallanq(all_transactions),
        "biweekly_tolerance_dallanq": biweekly_tolerance_dallanq(all_transactions),
        "span_months_dallanq": span_months_dallanq(all_transactions),
        "total_span_months_dallanq": total_span_months_dallanq(all_transactions),
        "fraction_active_months_dallanq": fraction_active_months_dallanq(all_transactions),
        "avg_txn_per_month_dallanq": avg_txn_per_month_dallanq(all_transactions),
        "modal_amount_dallanq": modal_amount_dallanq(all_transactions),
        "fraction_modal_amount_dallanq": fraction_modal_amount_dallanq(all_transactions),
        "amount_matches_modal_dallanq": amount_matches_modal_dallanq(transaction, all_transactions),
        "mode_interval_dallanq": mode_interval_dallanq(all_transactions),
        "fraction_mode_interval_dallanq": fraction_mode_interval_dallanq(all_transactions),
        "prev_interval_dev_from_mean_dallanq": prev_interval_dev_from_mean_dallanq(transaction, all_transactions),
        "next_interval_dev_from_mean_dallanq": next_interval_dev_from_mean_dallanq(transaction, all_transactions),
        "prev_interval_dev_from_mode_dallanq": prev_interval_dev_from_mode_dallanq(transaction, all_transactions),
        "next_interval_dev_from_mode_dallanq": next_interval_dev_from_mode_dallanq(transaction, all_transactions),
        "prev_within_monthly_tol_dallanq": prev_within_monthly_tol_dallanq(transaction, all_transactions),
        "next_within_monthly_tol_dallanq": next_within_monthly_tol_dallanq(transaction, all_transactions),
        "modal_day_of_month_dallanq": modal_day_of_month_dallanq(all_transactions),
        "dom_diff_from_modal_dallanq": dom_diff_from_modal_dallanq(transaction, all_transactions),
        "is_modal_dom_dallanq": is_modal_dom_dallanq(transaction, all_transactions),
        "amount_diff_from_modal_dallanq": amount_diff_from_modal_dallanq(transaction, all_transactions),
        "rel_amount_diff_from_modal_dallanq": rel_amount_diff_from_modal_dallanq(transaction, all_transactions),
        "amount_frequency_rank_dallanq": amount_frequency_rank_dallanq(transaction, all_transactions),
        "amount_freq_fraction_dallanq": amount_freq_fraction_dallanq(transaction, all_transactions),
        "txns_in_same_month_dallanq": txns_in_same_month_dallanq(transaction, all_transactions),
        "frac_txns_in_same_month_dallanq": frac_txns_in_same_month_dallanq(transaction, all_transactions),
        "days_since_group_start_dallanq": days_since_group_start_dallanq(transaction, all_transactions),
        "position_in_span_dallanq": position_in_span_dallanq(transaction, all_transactions),
        "is_amazon_prime_dallanq": is_amazon_prime_dallanq(transaction),
        "is_amazon_prime_video_dallanq": is_amazon_prime_video_dallanq(transaction),
        "is_apple_dallanq": is_apple_dallanq(transaction),
        "is_loan_company_dallanq": is_loan_company_dallanq(transaction),
        "is_pay_in_four_company_dallanq": is_pay_in_four_company_dallanq(transaction),
        "is_cash_advance_company_dallanq": is_cash_advance_company_dallanq(transaction),
        "is_phone_company_dallanq": is_phone_company_dallanq(transaction),
        "is_subscription_company_dallanq": is_subscription_company_dallanq(transaction),
        "is_usually_subscription_company_dallanq": is_usually_subscription_company_dallanq(transaction),
        "is_utility_company_dallanq": is_utility_company_dallanq(transaction),
        "is_insurance_company_dallanq": is_insurance_company_dallanq(transaction),
        "is_carwash_company_dallanq": is_carwash_company_dallanq(transaction),
        "is_rental_company_dallanq": is_rental_company_dallanq(transaction),
        "ends_in_00_dallanq": ends_in_00_dallanq(transaction),
        "is_likely_subscription_amount_dallanq": is_likely_subscription_amount_dallanq(transaction),
        "n_small_transactions_dallanq": n_small_transactions_dallanq(all_transactions, 20),
        "pct_small_transactions_dallanq": pct_small_transactions_dallanq(all_transactions, 20),
        "n_small_transactions_not_this_amount_dallanq": n_small_transactions_not_this_amount_dallanq(
            transaction, all_transactions, 20
        ),
        "pct_small_transactions_not_this_amount_dallanq": pct_small_transactions_not_this_amount_dallanq(
            transaction, all_transactions, 20
        ),
        "n_monthly_same_amount_dallanq": n_monthly_same_amount_dallanq(transaction, all_transactions),
        "pct_monthly_same_amount_dallanq": pct_monthly_same_amount_dallanq(transaction, all_transactions),
        "n_consecutive_months_same_amount_dallanq": n_consecutive_months_same_amount_dallanq(
            transaction, all_transactions
        ),
        "pct_consecutive_months_same_amount_dallanq": pct_consecutive_months_same_amount_dallanq(
            transaction, all_transactions
        ),
        "n_same_day_same_amount_1_dallanq": n_same_day_same_amount_dallanq(transaction, all_transactions, 1),
        "n_same_day_same_amount_3_dallanq": n_same_day_same_amount_dallanq(transaction, all_transactions, 3),
        "n_same_day_same_amount_5_dallanq": n_same_day_same_amount_dallanq(transaction, all_transactions, 5),
        "pct_same_day_same_amount_1_dallanq": pct_same_day_same_amount_dallanq(transaction, all_transactions, 1),
        "pct_same_day_same_amount_3_dallanq": pct_same_day_same_amount_dallanq(transaction, all_transactions, 3),
        "pct_same_day_same_amount_5_dallanq": pct_same_day_same_amount_dallanq(transaction, all_transactions, 5),
        "n_days_apart_same_amount_14_2_dallanq": get_n_transactions_days_apart_same_amount_dallanq(
            transaction, all_transactions, 14, 2
        ),
        "pct_days_apart_same_amount_14_2_dallanq": get_pct_transactions_days_apart_same_amount_dallanq(
            transaction, all_transactions, 14, 2
        ),
        "n_days_apart_same_amount_28_2_dallanq": get_n_transactions_days_apart_same_amount_dallanq(
            transaction, all_transactions, 28, 2
        ),
        "pct_days_apart_same_amount_28_2_dallanq": get_pct_transactions_days_apart_same_amount_dallanq(
            transaction, all_transactions, 28, 2
        ),
        "n_days_apart_same_amount_28_4_dallanq": get_n_transactions_days_apart_same_amount_dallanq(
            transaction, all_transactions, 28, 4
        ),
        "pct_days_apart_same_amount_28_4_dallanq": get_pct_transactions_days_apart_same_amount_dallanq(
            transaction, all_transactions, 28, 4
        ),
        # Frank's features
        "likely_same_amount_frank": amount_similarity_frank(transaction, all_transactions),
        "normalized_days_difference_frank": normalized_days_difference_frank(transaction, all_transactions),
        "amount_stability_score_frank": amount_stability_score_frank(all_transactions),
        "amount_z_score_frank": amount_z_score_frank(transaction, all_transactions),
        "weekly_spendings_frank": weekly_spending_cycle_frank(all_transactions),
        "vendor_recurrence_trend_frank": vendor_recurrence_trend_frank(all_transactions),
        "seasonal_spending_cycle_frank": seasonal_spending_cycle_frank(transaction, all_transactions),
        "recurrence_interval_variance_frank": recurrence_interval_variance_frank(all_transactions),
        "transaction_per_week_frank": transactions_per_week_frank(all_transactions),
        "transaction_per_month_frank": transactions_per_month_frank(all_transactions),
        "irregular_interval_score_frank": irregular_interval_score_frank(all_transactions),
        "inconsistent_amount_score_frank": inconsistent_amount_score_frank(all_transactions),
        "non_recurring_score_frank": non_recurring_score_frank(all_transactions),
        "amount_ratio_frank": get_same_amount_ratio_frank(transaction, all_transactions),
        "amount_coefficient_of_variation_frank": amount_coefficient_of_variation_frank(all_transactions),
        "proportional_timing_deviation_frank": proportional_timing_deviation_frank(transaction, all_transactions),
        "recurring_confidence_frank": recurring_confidence_frank(all_transactions),
        "matches_common_cycle_frank": matches_common_cycle_frank(all_transactions),
        "amount_variability_ratio_frank": amount_variability_ratio_frank(all_transactions),
        "robust_interval_iqr_frank": robust_interval_iqr_frank(all_transactions),
        "robust_interval_median_frank": robust_interval_median_frank(all_transactions),
        "transaction_frequency_frank": transaction_frequency_frank(all_transactions),
        "most_common_interval_frank": most_common_interval_frank(all_transactions),
        "enhanced_amt_iqr_frank": enhanced_amt_iqr_frank(all_transactions),
        "enhanced_days_since_last_frank": enhanced_days_since_last_frank(transaction, all_transactions),
        "enhanced_n_similar_last_n_days_frank": enhanced_n_similar_last_n_days_frank(transaction, all_transactions),
        "get_subscription_score_frank": get_subscription_score_frank(all_transactions),
        "get_amount_consistency_frank": get_amount_consistency_frank(all_transactions),
        "coefficient_of_variation_intervals_frank": coefficient_of_variation_intervals_frank(all_transactions),
        "calculate_cycle_consistency_frank": calculate_cycle_consistency_frank(all_transactions),
        "date_irregularity_score_frank": date_irregularity_score_frank(all_transactions),
        "amount_variability_score_frank": amount_variability_score_frank(all_transactions),
        "is_recurring_company_frank": is_recurring_company_frank(transaction.name),
        "is_utility_company_frank": is_utility_company_frank(transaction.name),
        "recurring_score_frank": recurring_score_frank(transaction.name),
        # Christopher's features
        "n_transactions_same_name_christopher": len(all_transactions),
        "n_transactions_same_amount_christopher": get_n_transactions_same_amount_christopher(
            transaction, all_transactions
        ),
        "percent_transactions_same_amount_christopher": get_percent_transactions_same_amount_christopher(
            transaction, all_transactions
        ),
        "transaction_frequency_christopher": get_transaction_frequency_christopher(all_transactions),
        "transaction_std_amount_christopher": get_transaction_std_amount_christopher(all_transactions),
        "follows_regular_interval_christopher": follows_regular_interval_christopher(all_transactions),
        "skipped_months_christopher": detect_skipped_months_christopher(all_transactions),
        "day_of_month_consistency_christopher": get_day_of_month_consistency_christopher(all_transactions),
        "coefficient_of_variation_christopher": get_coefficient_of_variation_christopher(all_transactions),
        "median_interval_christopher": get_median_interval_christopher(all_transactions),
        "is_known_recurring_company_christopher": is_known_recurring_company_christopher(transaction.name),
        "is_known_fixed_subscription_christopher": is_known_fixed_subscription_christopher(transaction),
        # Laurels' features
        "identical_transaction_ratio_laurels": identical_transaction_ratio_feature_laurels(
            transaction, all_transactions, merchant_trans
        ),
        "is_monthly_recurring_laurels": is_monthly_recurring_feature_laurels(merchant_trans),
        "recurrence_likelihood_laurels": recurrence_likelihood_feature_laurels(
            merchant_trans, interval_stats, amount_stats
        ),
        "is_varying_amount_recurring_laurels": is_varying_amount_recurring_feature_laurels(
            interval_stats, amount_stats
        ),
        "day_consistency_score_laurels": day_consistency_score_feature_laurels(merchant_trans),
        "is_near_periodic_interval_laurels": is_near_periodic_interval_feature_laurels(interval_stats),
        "merchant_amount_std_laurels": merchant_amount_std_feature_laurels(amount_stats),
        "merchant_interval_std_laurels": merchant_interval_std_feature_laurels(interval_stats),
        "merchant_interval_mean_laurels": merchant_interval_mean_feature_laurels(interval_stats),
        "time_since_last_transaction_same_merchant_laurels": time_since_last_transaction_same_merchant_feature_laurels(
            parsed_dates
        ),
        "is_deposit_laurels": is_deposit_feature_laurels(transaction, merchant_trans),
        "day_of_week_laurels": day_of_week_feature_laurels(transaction),
        "transaction_month_laurels": transaction_month_feature_laurels(transaction),
        "rolling_amount_mean_laurels": rolling_amount_mean_feature_laurels(merchant_trans),
        "low_amount_variation_laurels": low_amount_variation_feature_laurels(amount_stats),
        "is_single_transaction_laurels": is_single_transaction_feature_laurels(merchant_trans),
        "interval_variability_laurels": interval_variability_feature_laurels(interval_stats),
        "merchant_amount_frequency_laurels": merchant_amount_frequency_feature_laurels(merchant_trans),
        "non_recurring_irregularity_score_laurels": non_recurring_irregularity_score_laurels(
            merchant_trans, interval_stats, amount_stats
        ),
        "transaction_pattern_complexity_laurels": transaction_pattern_complexity_laurels(
            merchant_trans, interval_stats
        ),
        "date_irregularity_dominance_laurels": date_irregularity_dominance_laurels(
            merchant_trans, interval_stats, amount_stats
        ),
        # Emmanuel Ezechukwu (2)'s features
        **get_recurrence_patterns_emmanuel2(transaction, all_transactions),
        **get_recurring_consistency_score_emmanuel2(transaction, all_transactions),
        "is_recurring_emmanuel2": int(validate_recurring_transaction_emmanuel2(transaction)),
        "subscription_tier_emmanuel2": classify_subscription_tier_emmanuel2(transaction),
        **get_amount_features_emmanuel2(transaction, all_transactions),
        **get_user_behavior_features_emmanuel2(transaction, all_transactions),
        **get_refund_features_emmanuel2(transaction, all_transactions),
        **get_monthly_spending_trend_emmanuel2(transaction, all_transactions),
        # Nnanna's features
        "time_interval_between_transactions_nnanna": get_time_interval_between_transactions_nnanna(
            transaction, all_transactions
        ),
        "mobile_company_nnanna": get_mobile_transaction_nnanna(transaction),
        "transaction_frequency_nnanna": get_transaction_frequency_nnanna(transaction, all_transactions),
        "transaction_amount_dispersion_nnanna": get_dispersion_transaction_amount_nnanna(transaction, all_transactions),
        "mad_transaction_amount_nnanna": get_mad_transaction_amount_nnanna(transaction, all_transactions),
        "coefficient_of_variation_nnanna": get_coefficient_of_variation_nnanna(transaction, all_transactions),
        "transaction_interval_consistency_nnanna": get_transaction_interval_consistency_nnanna(
            transaction, all_transactions
        ),
        "average_transaction_amount_nnanna": get_average_transaction_amount_nnanna(transaction, all_transactions),
        # Ebenezer's features
        "n_transactions_same_name_ebenezer": get_n_transactions_same_name_ebenezer(transaction, all_transactions),
        "percent_transactions_same_name_ebenezer": get_percent_transactions_same_name_ebenezer(
            transaction, all_transactions
        ),
        "avg_amount_same_name_ebenezer": get_avg_amount_same_name_ebenezer(transaction, all_transactions),
        "std_amount_same_name_ebenezer": get_std_amount_same_name_ebenezer(transaction, all_transactions),
        "n_transactions_same_month_ebenezer": get_n_transactions_same_month_ebenezer(transaction, all_transactions),
        "percent_transactions_same_month_ebenezer": get_percent_transactions_same_month_ebenezer(
            transaction, all_transactions
        ),
        "avg_amount_same_month_ebenezer": get_avg_amount_same_month_ebenezer(transaction, all_transactions),
        "std_amount_same_month_ebenezer": get_std_amount_same_month_ebenezer(transaction, all_transactions),
        "n_transactions_same_user_id_ebenezer": get_n_transactions_same_user_id_ebenezer(transaction, all_transactions),
        "percent_transactions_same_user_id_ebenezer": get_percent_transactions_same_user_id_ebenezer(
            transaction, all_transactions
        ),
        "percent_transactions_same_day_of_week_ebenezer": get_percent_transactions_same_day_of_week_ebenezer(
            transaction, all_transactions
        ),
        "avg_amount_same_day_of_week_ebenezer": get_avg_amount_same_day_of_week_ebenezer(transaction, all_transactions),
        "std_amount_same_day_of_week_ebenezer": get_std_amount_same_day_of_week_ebenezer(transaction, all_transactions),
        "n_transactions_within_amount_range_ebenezer": get_n_transactions_within_amount_range_ebenezer(
            transaction, all_transactions
        ),
        "percent_transactions_within_amount_range_ebenezer": get_percent_transactions_within_amount_range_ebenezer(
            transaction, all_transactions
        ),
        # Praise's features
        "is_recurring_merchant_praise": is_recurring_merchant_praise(transaction),
        "avg_days_between_same_merchant_amount_praise": get_avg_days_between_same_merchant_amount_praise(
            transaction, all_transactions
        ),
        "average_transaction_amount_praise": get_average_transaction_amount_praise(all_transactions),
        "max_transaction_amount_praise": get_max_transaction_amount_praise(all_transactions),
        "min_transaction_amount_praise": get_min_transaction_amount_praise(all_transactions),
        "most_frequent_names_praise": len(get_most_frequent_names_praise(all_transactions)),
        "is_recurring_praise": is_recurring_praise(transaction, all_transactions),
        "amount_ends_in_99_praise": amount_ends_in_99_praise(transaction),
        "amount_ends_in_00_praise": amount_ends_in_00_praise(transaction),
        "n_transactions_same_merchant_amount_praise": get_n_transactions_same_merchant_amount_praise(
            transaction, all_transactions
        ),
        "percent_transactions_same_merchant_amount_praise": get_percent_transactions_same_merchant_amount_praise(
            transaction, all_transactions
        ),
        "interval_variance_coefficient_praise": get_interval_variance_coefficient_praise(transaction, all_transactions),
        "stddev_days_between_same_merchant_amount_praise": get_stddev_days_between_same_merchant_amount_praise(
            transaction, all_transactions
        ),
        "days_since_last_same_merchant_amount_praise": get_days_since_last_same_merchant_amount_praise(
            transaction, all_transactions
        ),
        "is_expected_transaction_date_praise": is_expected_transaction_date_praise(transaction, all_transactions),
        "has_incrementing_numbers_praise": has_incrementing_numbers_praise(transaction, all_transactions),
        "has_consistent_reference_codes_praise": has_consistent_reference_codes_praise(transaction, all_transactions),
        # Emmanuel Ezechukwu (1)'s features
        "n_transactions_same_amount_emmanuel1": get_n_transactions_same_amount_emmanuel1(transaction, all_transactions),
        "percent_transactions_same_amount_emmanuel1": get_percent_transactions_same_amount_emmanuel1(
            transaction, all_transactions
        ),
        "days_between_std_emmanuel1": get_days_between_std_emmanuel1(transaction, all_transactions),
        "amount_cv_emmanuel1": get_amount_cv_emmanuel1(transaction, all_transactions),
        "day_of_month_consistency_emmanuel1": get_day_of_month_consistency_emmanuel1(transaction, all_transactions),
        "exact_amount_count_emmanuel1": get_exact_amount_count_emmanuel1(transaction, all_transactions),
        "has_recurring_keyword_emmanuel1": get_has_recurring_keyword_emmanuel1(transaction),
        "is_always_recurring_emmanuel1": int(get_is_always_recurring_emmanuel1(transaction)),
        "n_transactions_30_days_apart_emmanuel1": get_n_transactions_days_apart_emmanuel1(
            transaction, all_transactions, 30, 2
        ),
        "is_convenience_store_emmanuel1": get_is_convenience_store_emmanuel1(transaction),
        "is_insurance_emmanuel1": int(get_is_insurance_emmanuel1(transaction)),
        "is_utility_emmanuel1": int(get_is_utility_emmanuel1(transaction)),
        "is_phone_emmanuel1": int(get_is_phone_emmanuel1(transaction)),
        # Asimi's features
        **get_amount_features_asimi(transaction),
        **get_user_recurring_vendor_count_asimi(transaction, all_transactions),
        **get_user_transaction_frequency_asimi(transaction, all_transactions),
        **get_vendor_amount_std_asimi(transaction, all_transactions),
        **get_vendor_recurring_user_count_asimi(transaction, all_transactions),
        **get_vendor_transaction_frequency_asimi(transaction, all_transactions),
        **get_user_vendor_transaction_count_asimi(transaction, all_transactions),
        **get_user_vendor_recurrence_rate_asimi(transaction, all_transactions),
        **get_user_vendor_interaction_count_asimi(transaction, all_transactions),
        **get_amount_category_asimi(transaction),
        **get_amount_pattern_features_asimi(transaction, all_transactions),
        **get_temporal_consistency_features_asimi(transaction, all_transactions),
        **get_vendor_recurrence_profile_asimi(transaction, all_transactions),
        **get_user_vendor_relationship_features_asimi(transaction, all_transactions),
        "is_recurring_asimi": is_valid_recurring_transaction_asimi(transaction),
        **get_user_specific_features_asimi(transaction, all_transactions),
        # Samuel's features
        "transaction_frequency_samuel": get_transaction_frequency_samuel(transaction, all_transactions),
        "amount_std_dev_samuel": get_amount_std_dev_samuel(transaction, all_transactions),
        "median_transaction_amount_samuel": get_median_transaction_amount_samuel(transaction, all_transactions),
        "is_weekend_transaction_samuel": get_is_weekend_transaction_samuel(transaction),
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
        "get_n_transactions_same_description_happy": get_n_transactions_same_description_happy(
            transaction, all_transactions
        ),
        "get_percent_transactions_same_description_happy": get_percent_transactions_same_description_happy(
            transaction, all_transactions
        ),
        "get_transaction_same_frequency": get_transaction_frequency_happy(transaction, all_transactions),
        "get_day_of_month_consistency": get_day_of_month_consistency_happy(transaction, all_transactions),
        # Osasere's features
        "has_min_recurrence_period_osasere": has_min_recurrence_period_osasere(transaction, all_transactions),
        "day_of_month_consistency_osasere": get_day_of_month_consistency_osasere(transaction, all_transactions),
        "day_of_month_variability_osasere": get_day_of_month_variability_osasere(transaction, all_transactions),
        "recurrence_confidence_osasere": get_recurrence_confidence_osasere(transaction, all_transactions),
        "median_period_days_osasere": get_median_period_osasere(transaction, all_transactions),
        "is_weekday_consistent_osasere": is_weekday_consistent_osasere(transaction, all_transactions),
        # Felix's features
        "n_transactions_same_vendor_felix": get_n_transactions_same_vendor_felix(transaction, all_transactions),
        "max_transaction_amount_felix": get_max_transaction_amount_felix(all_transactions),
        "min_transaction_amount_felix": get_min_transaction_amount_felix(all_transactions),
        "is_phone_felix": get_is_phone_felix(transaction),
        "month_felix": get_month_felix(transaction),
        "day_felix": get_day_felix(transaction),
        "year_felix": get_year_felix(transaction),
        "is_insurance_felix": get_is_insurance_felix(transaction),
        "is_utility_felix": get_is_utility_felix(transaction),
        "is_always_recurring_felix": get_is_always_recurring_felix(transaction),
        "median_variation_transaction_amount_felix": get_median_variation_transaction_amount_felix(
            transaction, all_transactions
        ),
        "variation_ratio_felix": get_variation_ratio_felix(transaction, all_transactions),
        "transactions_interval_stability_felix": get_transactions_interval_stability_felix(
            transaction, all_transactions
        ),
        "average_transaction_amount_felix": get_average_transaction_amount_felix(transaction, all_transactions),
        "dispersion_transaction_amount_felix": get_dispersion_transaction_amount_felix(transaction, all_transactions),
        "transaction_rate_felix": get_transaction_rate_felix(transaction, all_transactions),
        **get_transaction_intervals_felix(all_transactions),
        # Adeyinka's features
        "avg_days_between_transactions_adeyinka": get_average_days_between_transactions_adeyinka(
            transaction, all_transactions
        ),
        "time_regularity_score_adeyinka": get_time_regularity_score_adeyinka(transaction, all_transactions),
        "is_always_recurring_adeyinka": get_is_always_recurring_adeyinka(transaction),
        "transaction_amount_variance_adeyinka": get_transaction_amount_variance_adeyinka(transaction, all_transactions),
        "outlier_score_adeyinka": get_outlier_score_adeyinka(transaction, all_transactions),
        "recurring_confidence_score_adeyinka": get_recurring_confidence_score_adeyinka(transaction, all_transactions),
        "subscription_keyword_score_adeyinka": get_subscription_keyword_score_adeyinka(transaction),
        "same_amount_vendor_transactions_adeyinka": get_same_amount_vendor_transactions_adeyinka(
            transaction, all_transactions
        ),
        "30_days_apart_exact_adeyinka": get_n_transactions_days_apart_adeyinka(transaction, all_transactions, 30, 0),
        "30_days_apart_off_by_1_adeyinka": get_n_transactions_days_apart_adeyinka(transaction, all_transactions, 30, 1),
        "14_days_apart_exact_adeyinka": get_n_transactions_days_apart_adeyinka(transaction, all_transactions, 14, 0),
        "14_days_apart_off_by_1_adeyinka": get_n_transactions_days_apart_adeyinka(transaction, all_transactions, 14, 1),
        "7_days_apart_exact_adeyinka": get_n_transactions_days_apart_adeyinka(transaction, all_transactions, 7, 0),
        "7_days_apart_off_by_1_adeyinka": get_n_transactions_days_apart_adeyinka(transaction, all_transactions, 7, 1),
        # Elliot's features
        "is_utility_elliot": is_utility_bill_elliot(transaction),
        "is_always_recurring_elliot": get_is_always_recurring_elliot(transaction),
        "is_auto_pay_elliot": is_auto_pay_elliot(transaction),
        "is_membership_elliot": is_membership_elliot(transaction),
        "is_near_same_amount_elliot": get_is_near_same_amount_elliot(transaction, all_transactions),
        "is_recurring_based_on_99_elliot": is_recurring_based_on_99_elliot(transaction, all_transactions),
        "transaction_similarity_elliot": get_transaction_similarity_elliot(transaction, all_transactions),
        "is_weekday_transaction_elliot": is_weekday_transaction_elliot(transaction),
        "is_split_transaction_elliot": is_split_transaction_elliot(transaction, all_transactions),
        "is_price_trending_5pct_elliot": is_price_trending_elliot(transaction, all_transactions, 5),
        "is_price_trending_10pct_elliot": is_price_trending_elliot(transaction, all_transactions, 10),
        # Freedom's features
        "day_of_week_freedom": get_day_of_week_freedom(transaction),
        "days_until_next_transaction_freedom": get_days_until_next_transaction_freedom(transaction, all_transactions),
        "periodicity_confidence_30d_freedom": get_periodicity_confidence_freedom(transaction, all_transactions, 30),
        "periodicity_confidence_7d_freedom": get_periodicity_confidence_freedom(transaction, all_transactions, 7),
        "recurrence_streak_freedom": get_recurrence_streak_freedom(transaction, all_transactions),
        # Tife's features
        "transaction_frequency_tife": get_transaction_frequency_tife(all_transactions),
        "interval_consistency_tife": get_interval_consistency_tife(all_transactions),
        "amount_variability_tife": get_amount_variability_tife(all_transactions),
        "amount_range_tife": get_amount_range_tife(all_transactions),
        "transaction_count_tife": get_transaction_count_tife(all_transactions),
        "interval_mode_tife": get_interval_mode_tife(all_transactions),
        "normalized_interval_consistency_tife": get_normalized_interval_consistency_tife(all_transactions),
        "days_since_last_same_amount_tife": get_days_since_last_same_amount_tife(transaction, all_transactions),
        "amount_relative_change_tife": get_amount_relative_change_tife(transaction, all_transactions),
        "merchant_name_frequency_tife": get_merchant_name_frequency_tife(transaction, all_transactions),
        "amount_stability_score_tife": get_amount_stability_score_tife(all_transactions),
        "dominant_interval_strength_tife": get_dominant_interval_strength_tife(all_transactions),
        "near_amount_consistency_tife": get_near_amount_consistency_tife(transaction, all_transactions),
        "merchant_amount_signature_tife": get_merchant_amount_signature_tife(transaction, all_transactions),
        "amount_cluster_count_tife": get_amount_cluster_count_tife(transaction, all_transactions),
        "transaction_density_tife": get_transaction_density_tife(all_transactions),
        "biweekly_interval_tife": histogram["biweekly"],
        "monthly_interval_tife": histogram["monthly"],
        # Bassey's features
        "is_subscription_bassey": get_is_subscription_bassey(transaction),
        "is_streaming_service_bassey": get_is_streaming_service_bassey(transaction),
        "is_gym_membership_bassey": get_is_gym_membership_bassey(transaction),
        "is_recurring_apple_bassey": get_is_recurring_apple_bassey(transaction, all_transactions),
        "is_weekly_recurring_apple_bassey": get_is_weekly_recurring_apple_bassey(transaction, all_transactions),
        "is_high_value_transaction_bassey": get_is_high_value_transaction_bassey(transaction),
        "is_frequent_merchant_bassey": get_is_frequent_merchant_bassey(transaction, all_transactions),
        "is_weekend_transaction_bassey": get_is_weekend_transaction_bassey(transaction),
        "monthly_spending_average_bassey": get_monthly_spending_average_bassey(transaction, all_transactions),
        "is_merchant_recurring_bassey": get_is_merchant_recurring_bassey(transaction, all_transactions),
        "days_since_last_transaction_bassey": get_days_since_last_transaction_bassey(transaction, all_transactions),
        "is_same_day_multiple_transactions_bassey": get_is_same_day_multiple_transactions_bassey(
            transaction, all_transactions
        ),
        # Raphael's features
        "same_day_exact_raphael": get_n_transactions_same_day_raphael(transaction, all_transactions, 0),
        "pct_transactions_same_day_raphael": get_pct_transactions_same_day_raphael(transaction, all_transactions, 0),
        "same_day_off_by_1_raphael": get_n_transactions_same_day_raphael(transaction, all_transactions, 1),
        "same_day_off_by_2_raphael": get_n_transactions_same_day_raphael(transaction, all_transactions, 2),
        "14_days_apart_exact_raphael": get_n_transactions_days_apart_raphael(transaction, all_transactions, 14, 0),
        "pct_14_days_apart_exact_raphael": get_pct_transactions_days_apart_raphael(
            transaction, all_transactions, 14, 0
        ),
        "14_days_apart_off_by_1_raphael": get_n_transactions_days_apart_raphael(transaction, all_transactions, 14, 1),
        "pct_14_days_apart_off_by_1_raphael": get_pct_transactions_days_apart_raphael(
            transaction, all_transactions, 14, 1
        ),
        "7_days_apart_exact_raphael": get_n_transactions_days_apart_raphael(transaction, all_transactions, 7, 0),
        "pct_7_days_apart_exact_raphael": get_pct_transactions_days_apart_raphael(transaction, all_transactions, 7, 0),
        "7_days_apart_off_by_1_raphael": get_n_transactions_days_apart_raphael(transaction, all_transactions, 7, 1),
        "pct_7_days_apart_off_by_1_raphael": get_pct_transactions_days_apart_raphael(
            transaction, all_transactions, 7, 1
        ),
        "is_common_subscription_amount_raphael": get_is_common_subscription_amount_raphael(transaction),
        "occurs_same_week_raphael": get_occurs_same_week_raphael(transaction, all_transactions),
        "is_similar_name_raphael": get_is_similar_name_raphael(transaction, all_transactions),
        "is_fixed_interval_raphael": get_is_fixed_interval_raphael(transaction, all_transactions),
        "has_irregular_spike_raphael": get_has_irregular_spike_raphael(transaction, all_transactions),
        "is_first_of_month_raphael": get_is_first_of_month_raphael(transaction),
        # Ernest's features
        "is_weekly_ernest": get_is_weekly_ernest(transaction, all_transactions),
        "is_monthly_ernest": get_is_monthly_ernest(transaction, all_transactions),
        "is_biweekly_ernest": get_is_biweekly_ernest(transaction, all_transactions),
        "vendor_transaction_count_ernest": get_vendor_transaction_count_ernest(transaction, all_transactions),
        "vendor_amount_variance_ernest": get_vendor_amount_variance_ernest(transaction, all_transactions),
        "is_round_amount_ernest": get_is_round_amount_ernest(transaction),
        "is_small_amount_ernest": get_is_small_amount_ernest(transaction),
        "transaction_gap_mean_ernest": get_transaction_gap_stats_ernest(transaction, all_transactions)[0],
        "transaction_frequency_ernest": get_transaction_frequency_ernest(transaction, all_transactions),
        "is_recurring_vendor_ernest": get_is_recurring_vendor_ernest(transaction),
        "is_fixed_amount_ernest": get_is_fixed_amount_ernest(transaction, all_transactions),
        "recurring_interval_score_ernest": get_recurring_interval_score_ernest(transaction, all_transactions),
        "is_weekend_transaction_ernest": get_is_weekend_transaction_ernest(transaction),
        "is_high_frequency_vendor_ernest": get_is_high_frequency_vendor_ernest(transaction, all_transactions),
        "is_same_day_of_month_ernest": get_is_same_day_of_month_ernest(transaction, all_transactions),
        "is_quarterly_ernest": get_is_quarterly_ernest(transaction, all_transactions),
        "average_transaction_amount_ernest": get_average_transaction_amount_ernest(transaction, all_transactions),
        "is_subscription_based_ernest": get_is_subscription_based_ernest(transaction),
        # Efehi's features
        "transaction_time_of_month_efehi": get_transaction_time_of_month_efehi(transaction),
        "transaction_amount_stability_efehi": get_transaction_amount_stability_efehi(transaction, all_transactions),
        "time_between_transactions_efehi": get_time_between_transactions_efehi(transaction, all_transactions),
        "transaction_frequency_efehi": get_transaction_frequency_efehi(transaction, all_transactions),
        "n_same_name_transactions_efehi": get_n_same_name_transactions_efehi(transaction, all_transactions),
        "irregular_periodicity_efehi": get_irregular_periodicity_efehi(transaction, all_transactions),
        "irregular_periodicity_with_tolerance_efehi": get_irregular_periodicity_with_tolerance_efehi(
            transaction, all_transactions
        ),
        "user_transaction_frequency_efehi": get_user_transaction_frequency_efehi(transaction.user_id, all_transactions),
        "vendor_recurring_ratio_efehi": get_vendor_recurring_ratio_efehi(transaction, all_transactions),
        "vendor_recurrence_consistency_efehi": get_vendor_recurrence_consistency_efehi(transaction, all_transactions),
        # Adedotun's features
        "percent_transactions_same_amount_tolerant_at_adedotun": get_percent_transactions_same_amount_tolerant_adedotun(
            transaction, vendor_txns
        ),
        "is_always_recurring_at_adedotun": get_is_always_recurring_adedotun(transaction),
        "is_communication_or_energy_at_adedotun": get_is_communication_or_energy_adedotun(transaction),
        "is_recurring_monthly_at_adedotun": is_recurring_core_adedotun(
            transaction, vendor_txns, preprocessed, 30, 4, 2
        ),
        "is_recurring_weekly_at_adedotun": is_recurring_core_adedotun(transaction, vendor_txns, preprocessed, 7, 2, 2),
        "is_recurring_user_vendor_at_adedotun": is_recurring_core_adedotun(
            transaction, user_vendor_txns, preprocessed, 30, 4, 2
        ),
        "day_consistency_adedotun": sum(
            1 for t in vendor_txns if abs(date_obj.day - preprocessed["date_objects"][t].day) <= 2
        )
        / total_txns
        if total_txns
        else 0.0,
        "amount_stability_adedotun": (sum((t.amount - transaction.amount) ** 2 for t in vendor_txns) / total_txns)
        ** 0.5
        / transaction.amount
        if total_txns and transaction.amount
        else 0.0,
        "is_recurring_allowance_at_adedotun": is_recurring_allowance_adedotun(transaction, all_transactions, 30, 2, 2),
        "is_known_recurring_adedotun": get_is_always_recurring_adedotun(transaction),
        "is_one_time_vendor_adedotun": get_is_one_time_vendor_adedotun(transaction),
        "is_utility_adedotun": get_is_utility_adedotun(transaction),
        "is_insurance_adedotun": get_is_insurance_adedotun(transaction),
        "is_phone_adedotun": get_is_phone_adedotun(transaction),
        # Vendor characteristics
        "vendor_name_length_adedotun": len(transaction.name),
        "vendor_name_entropy_adedotun": get_vendor_name_entropy_adedotun(transaction),
        # Transaction frequency
        "vendor_occurrence_count_adedotun": get_vendor_occurrence_count_adedotun(transaction, all_transactions),
        "user_vendor_occurrence_count_adedotun": get_user_vendor_occurrence_count_adedotun(
            transaction, all_transactions
        ),
        "days_since_last_occurrence_adedotun": get_days_since_last_occurrence_adedotun(transaction, all_transactions),
        # Amount patterns
        "same_amount_count_adedotun": get_same_amount_count_adedotun(transaction, all_transactions),
        "similar_amount_count_adedotun": get_similar_amount_count_adedotun(transaction, all_transactions),
        "amount_uniqueness_score_adedotun": get_amount_uniqueness_score_adedotun(transaction, all_transactions),
        # Transaction context
        "is_weekend_adedotun": get_is_weekend_adedotun(transaction),
        "is_month_end_adedotun": get_is_month_end_adedotun(transaction),
        # Recurring check _adedotun(for reference)
        "is_recurring_allowance_adedotun": is_recurring_allowance_adedotun(transaction, all_transactions),
        "is_entertainment_adedotun": get_is_entertainment_adedotun(transaction),
        "is_food_dining_adedotun": get_is_food_dining_adedotun(transaction),
        "is_gambling_adedotun": get_is_gambling_adedotun(transaction),
        "is_gaming_adedotun": get_is_gaming_adedotun(transaction),
        "is_retail_adedotun": get_is_retail_adedotun(transaction),
        "is_travel_adedotun": get_is_travel_adedotun(transaction),
        "has_nonrecurring_keywords_adedotun": get_contains_common_nonrecurring_keywords_adedotun(transaction),
        "is_recurring_based_on_99_at_adedotun": is_recurring_based_on_99_adedotun(transaction, all_transactions),
        "get_interval_variance_coefficient_refine_adedotun": get_interval_variance_coefficient_adedotun(
            transaction, all_transactions
        ),
        "amount_variability_score_refine_adedotun": amount_variability_score_adedotun(
            all_transactions, transaction.name
        ),
        "is_known_recurring_company_refine_adedotun": is_known_recurring_company_adedotun(
            transaction, all_transactions
        ),
        "is_price_trendin_refine_adedotun": is_price_trending_adedotun(transaction, all_transactions),
        "get_percent_transactions_same_amount_adedotun": get_percent_transactions_same_amount_adedotun(
            transaction, all_transactions, transaction.name
        ),
        "get_n_transactions_same_amount_adedotun": get_n_transactions_same_amount_adedotun(
            transaction, all_transactions, transaction.name
        ),
        "get_interval_histogram_refine_adedotun": get_interval_histogram_adedotun(transaction, all_transactions),
        # Segun's features
        "total_transaction_amount_segun": get_total_transaction_amount_segun(all_transactions),
        "average_transaction_amount_segun": get_average_transaction_amount_segun(all_transactions),
        "max_transaction_amount_segun": get_max_transaction_amount_segun(all_transactions),
        "min_transaction_amount_segun": get_min_transaction_amount_segun(all_transactions),
        "transaction_amount_std_segun": get_transaction_amount_std_segun(all_transactions),
        "transaction_amount_median_segun": get_transaction_amount_median_segun(all_transactions),
        "transaction_amount_range_segun": get_transaction_amount_range_segun(all_transactions),
        "unique_transaction_amount_count_segun": get_unique_transaction_amount_count_segun(all_transactions),
        "transaction_amount_frequency_segun": get_transaction_amount_frequency_segun(transaction, all_transactions),
        "transaction_day_of_week_segun": get_transaction_day_of_week_segun(transaction),
        "transaction_time_of_day_segun": get_transaction_time_of_day_segun(transaction),
        "average_transaction_interval_segun": get_average_transaction_interval_segun(all_transactions),
        # Victor's features
        "avg_days_between_victor": get_avg_days_between_victor(all_transactions),
        # Emmanuel Eze's features
        "is_recurring_emmanuel_eze": get_is_recurring_emmanuel_eze(transaction, all_transactions),
        "recurring_transaction_confidence_emmanuel_eze": get_recurring_transaction_confidence_emmanuel_eze(
            transaction, all_transactions
        ),
        "sequence_confidence_emmanuel_eze": sequence_features["sequence_confidence"],
        "is_sequence_weekly_emmanuel_eze": 1.0 if sequence_features["sequence_pattern"] == "weekly" else 0.0,
        "is_sequence_monthly_emmanuel_eze": 1.0 if sequence_features["sequence_pattern"] == "monthly" else 0.0,
        "sequence_length_emmanuel_eze": sequence_features["sequence_length"],
        # Naomi's features
        "is_monthly_recurring_naomi": float(get_is_monthly_recurring_naomi(transaction, all_transactions)),
        "is_similar_amount_naomi": float(get_is_similar_amount_naomi(transaction, all_transactions)),
        "transaction_interval_consistency_naomi": get_transaction_interval_consistency_naomi(
            transaction, all_transactions
        ),
        "cluster_label_naomi": float(get_cluster_label_naomi(transaction, all_transactions)),
        "subscription_keyword_score_naomi": get_subscription_keyword_score_naomi(transaction),
        "recurring_confidence_score_naomi": get_recurring_confidence_score_naomi(transaction, all_transactions),
        "time_regularity_score_naomi": get_time_regularity_score_naomi(transaction, all_transactions),
        "outlier_score_naomi": get_outlier_score_naomi(transaction, all_transactions),
        # Yoloye's features
        "delayed_weekly_yoloye": get_delayed_weekly_yoloye(transaction, all_transactions),
        "delayed_fortnightly_yoloye": get_delayed_fortnightly_yoloye(transaction, all_transactions),
        "delayed_monthly_yoloye": get_delayed_monthly_yoloye(transaction, all_transactions),
        "delayed_quarterly_yoloye": get_delayed_quarterly_yoloye(transaction, all_transactions),
        "delayed_semi_annual_yoloye": get_delayed_semi_annual_yoloye(transaction, all_transactions),
        "delayed_annual_yoloye": get_delayed_annual_yoloye(transaction, all_transactions),
        "early_weekly_yoloye": get_early_weekly_yoloye(transaction, all_transactions),
        "early_fortnightly_yoloye": get_early_fortnightly_yoloye(transaction, all_transactions),
        "early_monthly_yoloye": get_early_monthly_yoloye(transaction, all_transactions),
        "early_quarterly_yoloye": get_early_quarterly_yoloye(transaction, all_transactions),
        "early_semi_annual_yoloye": get_early_semi_annual_yoloye(transaction, all_transactions),
        "early_annual_yoloye": get_early_annual_yoloye(transaction, all_transactions),
        # Gideon's features
        "is_microsoft_xbox_same_or_near_day_gideon": is_microsoft_xbox_same_or_near_day_gideon(
            transaction, all_transactions
        ),
    }
