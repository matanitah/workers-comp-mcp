"""Parse ClaimCalc workers' compensation pages into reimbursement JSON."""

from __future__ import annotations

import re
from decimal import Decimal
from pathlib import Path

CHART_URL = "https://claimcalc.app/workers-comp/settlement-chart"
STATE_URL = "https://claimcalc.app/workers-comp/{slug}"

_CHART_ROW = re.compile(
    r"<tr>\s*<td><strong>(?P<state>[^<]+)</strong></td>\s*"
    r"<td class=\"num\">\$(?P<max>[0-9,]+\.\d{2})</td>\s*"
    r"<td class=\"num\">(?P<formula>[^<]+)</td>\s*"
    r"<td class=\"num\">(?P<weeks>[^<]+)</td>\s*"
    r"<td[^>]*>\s*<a href=\"(?P<href>[^\"]+)\"[^>]*>(?P<label>[^<]+)</a>",
    re.S,
)
_GLANCE_ROW = re.compile(
    r"<tr><td><strong>(?P<label>.*?)</strong></td><td[^>]*>(?P<value>.*?)</td></tr>",
    re.S,
)
_VERIFIED = re.compile(
    r"Last verified (?P<verified>\d{4}-\d{2}-\d{2}).*?href=\"(?P<href>[^\"]+)\"",
    re.S,
)
_YEAR = re.compile(r"key figures \((\d{4})\)")
_MONEY = re.compile(r"\$([0-9,]+(?:\.\d+)?)")
_PERCENT = re.compile(r"([0-9]+(?:\.[0-9]+)?)%")
_NO_LIMIT = re.compile(r"no (statutory )?limit", re.I)


def _money(value: str) -> int | float:
    amount = Decimal(value.replace(",", "").replace("$", ""))
    if amount == amount.to_integral():
        return int(amount)
    return float(amount)


def _rate(formula: str) -> float:
    match = _PERCENT.search(formula)
    if not match:
        raise ValueError(f"No wage-replacement percent in {formula!r}")
    rate = Decimal(match.group(1)) / Decimal("100")
    return float(rate)


def _weeks(value: str) -> int | None:
    if _NO_LIMIT.search(value):
        return None
    match = re.search(r"\d+", value)
    if not match:
        raise ValueError(f"No TTD week count in {value!r}")
    return int(match.group(0))


def _average(value: str | None) -> tuple[int | float | None, str | None]:
    if not value:
        return None, None
    wording = " ".join(value.split())
    match = _MONEY.search(wording)
    if not match:
        return None, wording
    return _money(match.group(0)), wording


def parse_chart(html: str, *, expect: int | None = 50) -> dict[str, dict]:
    found = {}
    for match in _CHART_ROW.finditer(html):
        formula = " ".join(match.group("formula").split())
        weeks = " ".join(match.group("weeks").split())
        found[match.group("state").strip()] = {
            "kind": "indemnity_benefit_parameters",
            "rate_year": 2025,
            "verified": "2025-01",
            "resource": CHART_URL,
            "chart_resource": CHART_URL,
            "maximum_weekly_benefit_usd": _money(match.group("max")),
            "minimum_weekly_benefit_usd": None,
            "wage_replacement_rate": _rate(formula),
            "wage_replacement_basis": formula,
            "max_ttd_weeks": _weeks(weeks),
            "max_ttd_wording": weeks,
            "statute_of_limitations": None,
            "average_settlement_usd": None,
            "approximate": False,
            "average_settlement_wording": None,
            "official_source_label": " ".join(match.group("label").split()),
            "official_source_resource": match.group("href"),
        }
    if expect is not None and len(found) != expect:
        raise ValueError(f"ClaimCalc chart parsed {len(found)} states, expected {expect}")
    return found


def parse_state_page(html: str, slug: str) -> dict:
    rows = {
        " ".join(match.group("label").split()): " ".join(match.group("value").split())
        for match in _GLANCE_ROW.finditer(html)
    }
    if "Maximum weekly benefit" not in rows:
        raise ValueError(f"{slug} page has no benefit table")
    year = _YEAR.search(html)
    verified = _VERIFIED.search(html)
    average, wording = _average(rows.get("Average settlement"))
    formula = rows["Benefit formula"]
    weeks = rows["Max weeks (TTD)"]
    return {
        "kind": "indemnity_benefit_parameters",
        "rate_year": int(year.group(1)) if year else None,
        "verified": verified.group("verified") if verified else None,
        "resource": STATE_URL.format(slug=slug),
        "chart_resource": CHART_URL,
        "maximum_weekly_benefit_usd": _money(rows["Maximum weekly benefit"]),
        "minimum_weekly_benefit_usd": _money(rows["Minimum weekly benefit"])
        if rows.get("Minimum weekly benefit")
        else None,
        "wage_replacement_rate": _rate(formula),
        "wage_replacement_basis": formula,
        "max_ttd_weeks": _weeks(weeks),
        "max_ttd_wording": weeks,
        "statute_of_limitations": rows.get("Statute of limitations"),
        "average_settlement_usd": average,
        "approximate": bool(wording and wording.startswith("~")),
        "average_settlement_wording": wording,
        "official_source_label": rows.get("Official source"),
        "official_source_resource": verified.group("href") if verified else None,
    }


def merge_claimcalc(chart_row: dict, state_page: dict | None) -> dict:
    """Prefer a dedicated state page over the settlement chart."""
    if state_page is None:
        return dict(chart_row)
    merged = dict(chart_row)
    merged.update(state_page)
    merged["chart_resource"] = CHART_URL
    return merged


def unlisted_district() -> dict:
    return {
        "status": "unlisted",
        "reason": (
            "The District of Columbia is absent from ClaimCalc's "
            "50-state settlement chart."
        ),
        "resource": CHART_URL,
    }


_BENEFIT_FIELDS = (
    "maximum_weekly_benefit_usd",
    "minimum_weekly_benefit_usd",
    "wage_replacement_rate",
    "wage_replacement_basis",
    "max_ttd_weeks",
    "max_ttd_wording",
    "statute_of_limitations",
    "rate_year",
    "official_source_label",
    "official_source_resource",
)
_INJURY_FIELDS = (
    "resource",
    "chart_resource",
    "verified",
    "retrieved_at",
    "average_settlement_usd",
    "approximate",
    "average_settlement_wording",
)


def split_snapshot(record: dict, verification: dict | None = None) -> tuple[dict, dict]:
    """Separate statutory benefit limits from ClaimCalc's injury-level settlement."""
    if verification is None and "verification" in record:
        verification = record["verification"]
    if record.get("status") == "unlisted":
        benefits = {"status": "unlisted", "reason": record.get("reason")}
        if verification is not None:
            benefits["verification"] = verification
        injury = {
            "kind": "injury_settlement",
            "status": "unlisted",
            "reason": record.get("reason"),
            "resource": record.get("resource"),
        }
        if record.get("retrieved_at"):
            injury["retrieved_at"] = record["retrieved_at"]
        return benefits, injury
    benefits = {key: record.get(key) for key in _BENEFIT_FIELDS}
    benefits["figures_from"] = "claimcalc"
    benefits["claimcalc_resource"] = record.get("resource")
    if verification is not None:
        benefits["verification"] = verification
    injury = {"kind": "injury_settlement"}
    for key in _INJURY_FIELDS:
        if key in record:
            injury[key] = record[key]
    return benefits, injury


def apply_snapshots(root, chart_html: str, state_pages: dict[str, str], retrieved_at: str) -> None:
    import wiki

    jurisdictions = wiki.load_jurisdictions(root)
    records = build_records(
        chart_html,
        state_pages,
        {item.slug: item.name for item in jurisdictions},
        retrieved_at,
    )
    for item in jurisdictions:
        payload = dict(item.reimbursement)
        payload.pop("average_reimbursement_by_injury", None)
        payload["schema_version"] = "0.2"
        existing = payload.get("benefits") or {}
        prior = payload.get("claimcalc") or {}
        verification = existing.get("verification") or prior.get("verification")
        benefits, injury = split_snapshot(records[item.slug], verification)
        payload["benefits"] = benefits
        payload["claimcalc"] = injury
        wiki.write_reimbursement(item.path, payload)
        wiki.append_source(
            item.path,
            {
                "id": "claimcalc",
                "resource": records[item.slug]["resource"],
                "title": f"ClaimCalc workers' compensation figures for {item.name}",
                "author": "process:claimcalc",
            },
        )


def snapshot(block: dict, retrieved_at: str) -> dict:
    recorded = dict(block)
    recorded["retrieved_at"] = retrieved_at
    return recorded


def build_records(
    chart_html: str,
    state_pages: dict[str, str],
    names_by_slug: dict[str, str],
    retrieved_at: str,
) -> dict[str, dict]:
    """Return slug -> claimcalc object. `names_by_slug` includes the District of Columbia."""
    chart = parse_chart(chart_html)
    pages = {
        slug: parse_state_page(html, slug) for slug, html in state_pages.items()
    }
    records = {}
    for slug, name in names_by_slug.items():
        if name == "District of Columbia":
            records[slug] = snapshot(unlisted_district(), retrieved_at)
            continue
        if name not in chart:
            raise ValueError(f"ClaimCalc chart has no row for {name}")
        records[slug] = snapshot(merge_claimcalc(chart[name], pages.get(slug)), retrieved_at)
    return records
