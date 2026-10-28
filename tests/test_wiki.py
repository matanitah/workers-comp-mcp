from pathlib import Path

import wiki

ROOT = Path(__file__).resolve().parents[1]
BENEFIT_FIELDS = (
    "maximum_weekly_benefit_usd",
    "minimum_weekly_benefit_usd",
    "wage_replacement_rate",
    "max_ttd_weeks",
)


def test_every_jurisdiction_stores_benefit_caps_and_a_claimcalc_settlement():
    items = wiki.load_jurisdictions(ROOT / "state-by-state-research")
    assert len(items) == 51
    postals = {item.postal for item in items}
    assert "DC" in postals
    assert len(postals) == 51
    for item in items:
        record = item.reimbursement
        assert record["schema_version"] == "0.2"
        assert "average_reimbursement_by_injury" not in record
        assert "benefits" in record
        assert record["claimcalc"]["kind"] == "injury_settlement"
        if item.postal == "DC":
            assert record["benefits"]["status"] == "unlisted"
            continue
        for field in BENEFIT_FIELDS:
            assert field in record["benefits"]
        assert record["benefits"]["figures_from"] == "claimcalc"


def test_resolve_accepts_postal_code_and_dc_name():
    root = ROOT / "state-by-state-research"
    assert wiki.resolve_jurisdiction("ca", root).postal == "CA"
    assert wiki.resolve_jurisdiction("District of Columbia", root).postal == "DC"
    assert wiki.resolve_jurisdiction("d.c.", root).postal == "DC"


def test_reimbursement_is_a_sidecar_file():
    root = ROOT / "state-by-state-research"
    for path in (root / "states").glob("*.md"):
        if path.name == "index.md":
            continue
        text = path.read_text(encoding="utf-8")
        assert "```json" not in text
        assert f"/reimbursement/{path.stem}.json" in text
        assert wiki.reimbursement_path(path.stem, root).is_file()
    countrywide = (root / "countrywide-claim-costs.md").read_text(encoding="utf-8")
    assert "```json" not in countrywide
    assert "/reimbursement/countrywide.json" in countrywide
    assert "```json" in (root / "reimbursement-schema.md").read_text(encoding="utf-8")


def test_california_official_page_left_benefit_caps_in_place():
    item = wiki.resolve_jurisdiction("California", ROOT / "state-by-state-research")
    benefits = item.reimbursement["benefits"]
    assert benefits["maximum_weekly_benefit_usd"] == 1619.15
    assert benefits["minimum_weekly_benefit_usd"] == 242.86
    assert benefits["wage_replacement_rate"] == 0.6667
    assert benefits["max_ttd_weeks"] == 104
    verification = benefits["verification"]
    assert verification["resource"] == "https://www.dir.ca.gov/dwc/workerscompensationbenefits.htm"
    assert verification["fetch_status"] == "ok"
    assert verification["fields"]["maximum_weekly_benefit_usd"]["status"] == "unchecked"
    settlement = item.reimbursement["claimcalc"]
    assert settlement["average_settlement_usd"] == 62000
    assert "maximum_weekly_benefit_usd" not in settlement
    district = wiki.resolve_jurisdiction("District of Columbia", ROOT / "state-by-state-research")
    assert district.reimbursement["benefits"]["verification"]["status"] == "unlisted"


def test_unknown_jurisdiction():
    try:
        wiki.resolve_jurisdiction("Atlantis", ROOT / "state-by-state-research")
    except ValueError as exc:
        assert "Atlantis" in str(exc)
    else:
        raise AssertionError("expected ValueError")
