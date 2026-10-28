from pathlib import Path

import claimcalc
import wiki

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_california_page_fixture():
    html = (FIXTURES / "claimcalc-california.html").read_text(encoding="utf-8")
    page = claimcalc.parse_state_page(html, "california")
    assert page["maximum_weekly_benefit_usd"] == 1619.15
    assert page["minimum_weekly_benefit_usd"] == 242.86
    assert page["wage_replacement_rate"] == 0.6667
    assert page["wage_replacement_basis"] == "66.67% of average weekly wage"
    assert page["max_ttd_weeks"] == 104
    assert page["statute_of_limitations"] == (
        "1 year from injury or knowledge of work-related injury"
    )
    assert page["average_settlement_usd"] == 62000
    assert page["approximate"] is True
    assert page["average_settlement_wording"] == "~$62,000"
    assert page["verified"] == "2025-01-15"
    assert page["rate_year"] == 2025
    assert page["official_source_resource"] == "https://www.dir.ca.gov/dwc/"
    assert page["resource"] == "https://claimcalc.app/workers-comp/california"


def test_state_page_overrides_a_rounded_chart_maximum():
    chart = claimcalc.parse_chart(
        (FIXTURES / "claimcalc-chart.html").read_text(encoding="utf-8"),
        expect=3,
    )
    page = claimcalc.parse_state_page(
        (FIXTURES / "claimcalc-california.html").read_text(encoding="utf-8"),
        "california",
    )
    merged = claimcalc.merge_claimcalc(chart["California"], page)
    assert chart["California"]["maximum_weekly_benefit_usd"] == 1619
    assert merged["maximum_weekly_benefit_usd"] == 1619.15
    assert merged["chart_resource"] == claimcalc.CHART_URL
    assert chart["Arizona"]["max_ttd_weeks"] is None
    assert chart["Alabama"]["maximum_weekly_benefit_usd"] == 1112
    assert chart["Alabama"]["max_ttd_weeks"] == 500


def test_ingested_california_splits_caps_from_the_settlement():
    item = wiki.resolve_jurisdiction("CA", ROOT / "state-by-state-research")
    benefits = item.reimbursement["benefits"]
    settlement = item.reimbursement["claimcalc"]
    assert benefits["maximum_weekly_benefit_usd"] == 1619.15
    assert benefits["minimum_weekly_benefit_usd"] == 242.86
    assert settlement["average_settlement_usd"] == 62000
    assert settlement["approximate"] is True
    assert settlement["kind"] == "injury_settlement"
    assert settlement["resource"] == "https://claimcalc.app/workers-comp/california"
    assert "maximum_weekly_benefit_usd" not in settlement
    assert item.reimbursement["medical_fee_schedule"] is None


def test_split_snapshot_keeps_the_week_cap_out_of_the_settlement():
    benefits, injury = claimcalc.split_snapshot(
        {
            "maximum_weekly_benefit_usd": 1112,
            "max_ttd_weeks": 500,
            "average_settlement_usd": 40000,
            "resource": "https://claimcalc.app/workers-comp/alabama",
        }
    )
    assert benefits["maximum_weekly_benefit_usd"] == 1112
    assert benefits["max_ttd_weeks"] == 500
    assert injury["average_settlement_usd"] == 40000
    assert "maximum_weekly_benefit_usd" not in injury


def test_district_of_columbia_is_unlisted():
    item = wiki.resolve_jurisdiction("DC", ROOT / "state-by-state-research")
    benefits = item.reimbursement["benefits"]
    settlement = item.reimbursement["claimcalc"]
    assert benefits["status"] == "unlisted"
    assert settlement["status"] == "unlisted"
    assert "District of Columbia" in benefits["reason"]
    assert "maximum_weekly_benefit_usd" not in benefits
    assert "average_settlement_usd" not in settlement
