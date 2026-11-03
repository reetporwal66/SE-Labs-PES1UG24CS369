import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge


def test_invalid_cohorts_and_volume():
    with pytest.raises(ValueError):
        process_donor_cohort("not a list", 450)
    with pytest.raises(ValueError):
        process_donor_cohort([], 0)


def test_unregistered_cohort_is_skipped():
    result = process_donor_cohort([{"clinic_registered": False, "donors": [{"age": 25, "weight_kg": 65, "hb": 14}]}], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_accepted_donor_and_fast_track():
    result = process_donor_cohort([{"clinic_registered": True, "fast_track": True, "donors": [{"age": 25, "weight_kg": 65, "hb": 14}]}], 450)
    assert result == {"collected_ml": 500, "status": "ACCEPTED"}


def test_age_and_weight_deferrals():
    cohorts = [{"clinic_registered": True, "donors": [
        {"age": 16, "weight_kg": 65, "hb": 14},
        {"age": 25, "weight_kg": 49, "hb": 14},
    ]}]
    result = process_donor_cohort(cohorts, 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_low_and_high_hemoglobin_deferrals():
    cohorts = [{"clinic_registered": True, "donors": [
        {"age": 25, "weight_kg": 65, "hb": 12.0},
        {"age": 25, "weight_kg": 65, "hb": 18.5},
    ]}]
    result = process_donor_cohort(cohorts, 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_altitude_low_hb_resets_yield_and_breaks_donor_loop():
    cohorts = [{"clinic_registered": True, "type": "high_altitude", "donors": [
        {"age": 25, "weight_kg": 65, "hb": 14},
        {"age": 25, "weight_kg": 65, "hb": 12},
        {"age": 25, "weight_kg": 65, "hb": 14},
    ]}]
    result = process_donor_cohort(cohorts, 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_deferral_status():
    donors = [{"age": 16, "weight_kg": 65, "hb": 14} for _ in range(5)]
    result = process_donor_cohort([{"clinic_registered": True, "donors": donors}], 450)
    assert result == {"collected_ml": 0, "status": "HIGH_DEFERRAL"}


def test_centrifuge_no_data_and_stable():
    assert verify_storage_centrifuge([]) == "NO_DATA"
    assert verify_storage_centrifuge([[3100, 2900, 3200]]) == "STABLE"


def test_centrifuge_aborts_after_two_consecutive_drops():
    assert verify_storage_centrifuge([[2900, 2800, 3200]]) == "ABORT_SPIN"


def test_centrifuge_resets_streak_after_normal_rpm():
    assert verify_storage_centrifuge([[2900, 3200, 2900]]) == "STABLE"
