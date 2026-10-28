from pathlib import Path

import regulations
import verify_official

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_official_page_replaces_a_different_weekly_maximum():
    html = (FIXTURES / "official-maximum.html").read_text(encoding="utf-8")
    text = regulations.html_to_text(html)
    block = {
        "maximum_weekly_benefit_usd": 1619.15,
        "minimum_weekly_benefit_usd": 242.86,
        "wage_replacement_rate": 0.6667,
        "max_ttd_weeks": 500,
        "max_ttd_wording": "500",
        "average_settlement_usd": 62000,
    }
    updated, fields = verify_official.assess(block, text)
    assert updated["maximum_weekly_benefit_usd"] == 2000
    assert fields["maximum_weekly_benefit_usd"]["status"] == "corrected"
    assert fields["maximum_weekly_benefit_usd"]["claimcalc_value"] == 1619.15
    assert "$2,000.00" in fields["maximum_weekly_benefit_usd"]["quote"]
    assert updated["minimum_weekly_benefit_usd"] == 50
    assert fields["minimum_weekly_benefit_usd"]["status"] == "corrected"
    assert fields["wage_replacement_rate"]["status"] == "matched"
    assert updated["wage_replacement_rate"] == 0.6667
    assert updated["max_ttd_weeks"] == 104
    assert fields["max_ttd_weeks"]["claimcalc_value"] == 500
    assert updated["average_settlement_usd"] == 62000


def test_figures_from_becomes_official_only_when_every_field_is_stated():
    html = (FIXTURES / "official-maximum.html").read_text(encoding="utf-8")
    text = regulations.html_to_text(html)
    block = {
        "maximum_weekly_benefit_usd": 1619.15,
        "minimum_weekly_benefit_usd": 242.86,
        "wage_replacement_rate": 0.6667,
        "max_ttd_weeks": 500,
        "figures_from": "claimcalc",
    }
    updated = verify_official.attach_verification(block, text, "https://example.test/rates", "2026-10-28T16:45:00Z")
    assert updated["figures_from"] == "official"
    assert updated["verification"]["resource"] == "https://example.test/rates"
    partial = verify_official.attach_verification(
        block,
        "The maximum weekly benefit is $2,000.00.",
        "https://example.test/rates",
        "2026-10-28T16:45:00Z",
    )
    assert partial["maximum_weekly_benefit_usd"] == 2000
    assert partial["figures_from"] == "claimcalc"


def test_a_rate_history_uses_the_2026_amount():
    text = (
        "The maximum weekly benefit for 2024 is $1,000.00. "
        "The maximum weekly benefit for 2026 is $1,500.00. "
        "The minimum weekly benefit for 2024 is $40.00. "
        "The minimum weekly benefit for 2026 is $80.00."
    )
    assert verify_official.find_maximum(text)[0] == 1500
    assert verify_official.find_minimum(text)[0] == 80


def test_two_current_maxima_stay_unstated():
    text = (
        "The maximum weekly benefit for 2026 is $1,488.30. "
        "The maximum weekly benefit for 2026 is $1,353.00."
    )
    assert verify_official.find_maximum(text)[0] is None


def test_temporary_maximum_is_used_when_the_page_states_both():
    text = (
        "The maximum weekly benefit for temporary benefits in 2026 is $1,488.30. "
        "The maximum weekly benefit for permanent benefits in 2026 is $1,353.00."
    )
    assert verify_official.find_maximum(text)[0] == 1488.3


def test_a_period_that_ends_in_2026_is_not_the_current_rate():
    text = (
        "For injuries from July 1, 2025, through June 30, 2026: $1,174.98. "
        "Maximum weekly rate. For injuries from July 1, 2026, through June 30, 2027: "
        "TTD, HP, PTD, and death benefits: $2,431.00. PPD benefits: $2,237.00."
    )
    assert verify_official.find_maximum(text)[0] == 2431


def test_temporary_total_rate_beats_the_permanent_partial_rate():
    text = (
        "Wisconsin's maximum Worker's Compensation rate will increase to $1,375 per week "
        "for temporary total disability, permanent total disability and death benefits "
        "for injuries occurring on or after January 1, 2026. "
        "The maximum weekly indemnity rate for permanent partial disability remains "
        "$446 for injuries occurring on or after January 1, 2026."
    )
    assert verify_official.find_maximum(text)[0] == 1375


def test_spaced_pdf_money_is_read():
    text = (
        "The maximum weekly indemnity benefit for calendar year 2026 for total "
        "disability shall be $ 1,27 7.99."
    )
    assert verify_official.find_maximum(text)[0] == 1277.99


def test_a_single_2026_row_is_the_maximum():
    text = "Maximum weekly compensation rates. 2025 $1,000.00. 2026 $1,446.00. 2024 $900.00."
    assert verify_official.find_maximum(text)[0] == 1446


def test_the_statewide_average_wage_is_not_the_weekly_maximum():
    text = "Year SAWW increase 2026 $1,789.00 4.9%. Mileage is $0.76."
    assert verify_official.find_maximum(text)[0] is None


def test_workers_compensation_rate_is_not_the_unemployment_rate():
    text = (
        "Each of these changes will take effect on January 1, 2026. "
        "The maximum weekly benefit rate for Unemployment Insurance claims will increase to $905, from $875. "
        "The maximum weekly Workers' Compensation benefit rate for temporary disability rises to $1,199, from $1,159."
    )
    assert verify_official.find_maximum(text)[0] == 1199


def test_unstated_figures_stay_unchecked():
    updated, fields = verify_official.assess(
        {"maximum_weekly_benefit_usd": 1112, "minimum_weekly_benefit_usd": None, "wage_replacement_rate": 0.6667, "max_ttd_weeks": 500},
        "Welcome to the workers' compensation agency.",
    )
    assert updated["maximum_weekly_benefit_usd"] == 1112
    assert all(item["status"] == "unchecked" for item in fields.values())
