"""Compare ClaimCalc benefit figures with the linked official page."""

from __future__ import annotations

import re
from decimal import Decimal

CHECKED_FIELDS = (
    "maximum_weekly_benefit_usd",
    "minimum_weekly_benefit_usd",
    "wage_replacement_rate",
    "max_ttd_weeks",
)

_MAX_LABEL = re.compile(
    r"maximum(?:\s+\S+){0,3}\s+rate|maximum weekly(?:\s+(?:benefit|compensation|payment))?|weekly maximum|maximum compensation rate",
    re.I,
)
_PRIOR_AMOUNT = re.compile(
    r"\b(?:19|20)\d{2}\b.{0,60}?\b(?:through|to)\b\s+(?:[A-Za-z]+\.?\s+\d{1,2},?\s+)?2026\s*[:\-]?\s*\$\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.\d{2})?|[0-9]+(?:\.\d{2})?)",
    re.I,
)
_DATED_TTD = (
    re.compile(
        r"(?:January|July)\s+1,\s*2026.{0,180}?(?:temporary total|\bTTD\b).{0,80}?\$\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.\d{2})?)",
        re.I,
    ),
    re.compile(
        r"\$\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.\d{2})?).{0,80}?(?:temporary total|\bTTD\b).{0,100}?(?:January|July)\s+1,\s*2026",
        re.I,
    ),
)
_WC_MAXIMUM = re.compile(
    r"maximum weekly workers['’] compensation benefit rate.{0,240}?\$\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.\d{2})?)",
    re.I,
)
_MIN_LABEL = re.compile(
    r"minimum weekly(?:\s+(?:benefit|compensation|rate|payment))?|weekly minimum|minimum compensation rate",
    re.I,
)
_MONEY = re.compile(r"\$\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.\d{2})?|[0-9]+(?:\.\d{2})?)")
_WEEKS = re.compile(r"\b(\d{2,4})\s+weeks\b", re.I)
_NO_LIMIT = re.compile(
    r"no (?:statutory |weekly )?limit|unlimited|duration of (?:the )?disability",
    re.I,
)
_TTD = re.compile(r"temporary total|\bTTD\b", re.I)
_RATE_WORD = re.compile(r"two[-\s]thirds|\b2/3\b|66\s*2/3", re.I)
_PERCENT = re.compile(r"(\d{2}(?:\.\d+)?)\s*(?:%|percent)\b", re.I)
_WAGE_CONTEXT = re.compile(r"average weekly wage|\bAWW\b|weekly benefit|weekly compensation", re.I)
_CURRENT_YEAR = re.compile(r"\b2026\b")


def sentences(text: str) -> list[str]:
    flat = re.sub(r"\s+", " ", text).strip()
    if not flat:
        return []
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", flat) if part.strip()]


def _money(raw: str) -> int | float:
    amount = Decimal(raw.replace(",", ""))
    if amount == amount.to_integral():
        return int(amount)
    return float(amount)


def _normalize_spaced_money(text: str) -> str:
    """Join digits a PDF text layer split, such as '$ 1,27 7.99'."""

    def fix(match: re.Match[str]) -> str:
        return "$" + re.sub(r"\s+", "", match.group(1))

    return re.sub(
        r"\$\s*([0-9](?:[0-9,\s]{0,16})?(?:\.[0-9\s]{2,4})?)",
        fix,
        text,
    )


def _prior_amounts(text: str) -> list:
    return [_money(match.group(1)) for match in _PRIOR_AMOUNT.finditer(text)]


def _without_prior(text: str, amounts: list) -> list:
    prior = {float(amount) for amount in _prior_amounts(text)}
    return [amount for amount in amounts if float(amount) not in prior]


def _in_range(text: str, low: float, high: float) -> list:
    found = []
    for match in _MONEY.finditer(text):
        amount = _money(match.group(1))
        if low <= float(amount) <= high:
            found.append(amount)
    return found


def _amount_after(sentence: str, label: re.Pattern[str], low: float, high: float) -> int | float | None:
    """Return the amount stated with the label.

    Money that precedes the label belongs to the previous sentence fragment.
    A label that names both the maximum and the minimum is the statewide
    average wage, not the benefit. The amount has to sit in the first 45
    characters after the label so a later benefit in the same sentence is
    not picked up early.
    """
    found = []
    for match in label.finditer(sentence):
        if re.search(r"and minimum", match.group(), re.I):
            continue
        tail = _bounded(sentence, match.end(), match.end() + 45)
        if _prior_amounts(tail):
            continue
        near = _without_prior(tail, _unique(_in_range(tail, low, high)))
        if len(near) != 1:
            continue
        year_window = _bounded(sentence, match.start() - 40, match.end() + 45)
        sentence_amounts = _unique(_in_range(sentence, low, high))
        if _CURRENT_YEAR.search(year_window) or len(sentence_amounts) == 1 or not _CURRENT_YEAR.search(sentence):
            found.append(near[0])
    unique = _unique(found)
    if len(unique) == 1:
        return unique[0]
    return None


def _unique(values: list) -> list:
    seen = []
    for value in values:
        if value not in seen:
            seen.append(value)
    return seen


def _bounded(text: str, start: int, end: int) -> str:
    """Slice without cutting a dollar amount in half."""
    start = max(0, start)
    end = min(len(text), end)
    while end < len(text) and text[end] not in " \t\n":
        end += 1
    return text[start:end]


def _quote(sentence: str) -> str:
    sentence = " ".join(sentence.split())
    if len(sentence) <= 500:
        return sentence
    return sentence[:497] + "..."


def _pick_labeled(text: str, label: re.Pattern[str], low: float, high: float):
    found = []
    for sentence in sentences(text):
        amount = _amount_after(sentence, label, low, high)
        if amount is not None:
            found.append((amount, sentence))
    unique = _unique([amount for amount, _ in found])
    if len(unique) == 1:
        sentence = next(sentence for amount, sentence in found if amount == unique[0])
        # A page that also prints the current year is a rate history. The one
        # labeled amount is the current rate only when that sentence is the
        # current year, or when the page states no other in-range amount.
        others = _unique(_in_range(text, low, high))
        if len(others) > 1 and _CURRENT_YEAR.search(text) and not _CURRENT_YEAR.search(sentence):
            return _pick_current_window(text, label, low, high)
        return unique[0], _quote(sentence)
    current = [(amount, sentence) for amount, sentence in found if _CURRENT_YEAR.search(sentence)]
    chosen = _one(current) or _one(_temporary(current))
    if chosen is not None:
        return chosen
    return _pick_current_window(text, label, low, high)


def _temporary(found: list) -> list:
    return [
        (amount, sentence)
        for amount, sentence in found
        if re.search(r"temporary total|\bTTD\b|temporary benefit", sentence, re.I)
    ]


def _one(found: list):
    unique = _unique([amount for amount, _ in found])
    if len(unique) != 1:
        return None
    sentence = next(sentence for amount, sentence in found if amount == unique[0])
    return unique[0], _quote(sentence)


def _pick_current_window(text: str, label: re.Pattern[str], low: float, high: float):
    flat = re.sub(r"\s+", " ", text)
    found = []
    for match in label.finditer(flat):
        if re.search(r"and minimum", match.group(), re.I):
            continue
        window = _bounded(flat, match.end(), match.end() + 120)
        period = window.find(". ")
        if period != -1:
            window = window[: period + 1]
        if not _CURRENT_YEAR.search(_bounded(flat, match.start() - 40, match.end() + 120)):
            continue
        amounts = _without_prior(window, _unique(_in_range(window, low, high)))
        if len(amounts) == 1:
            found.append((amounts[0], window))
    unique = _unique([amount for amount, _ in found])
    if len(unique) != 1:
        return None, None
    window = next(window for amount, window in found if amount == unique[0])
    return unique[0], _quote(window)


def _dated_maximum(text: str) -> tuple[int | float | None, str | None]:
    flat = re.sub(r"\s+", " ", text)
    found = []
    for pattern in _DATED_TTD:
        for match in pattern.finditer(flat):
            if re.search(r"lower of|minimum", match.group(0), re.I):
                continue
            amount = _money(match.group(1))
            if 400 <= float(amount) <= 3500 and not _prior_amounts(match.group(0)):
                found.append((amount, match.group(0)))
    return _one(found) or (None, None)


def _workers_comp_maximum(text: str) -> tuple[int | float | None, str | None]:
    flat = re.sub(r"\s+", " ", text)
    found = []
    for match in _WC_MAXIMUM.finditer(flat):
        start = max(0, match.start() - 400)
        if not _CURRENT_YEAR.search(flat[start : match.end()]):
            continue
        amount = _money(match.group(1))
        if 400 <= float(amount) <= 3500:
            found.append((amount, match.group(0)))
    return _one(found) or (None, None)


def _explicit_maximum(text: str):
    flat = re.sub(r"\s+", " ", text)
    pattern = re.compile(
        r"the 2026 maximum weekly compensation rate is \$([0-9,]+\.\d{2}|[0-9,]+)",
        re.I,
    )
    found = []
    for match in pattern.finditer(flat):
        amount = _money(match.group(1))
        if 400 <= float(amount) <= 3500:
            found.append((amount, match.group(0)))
    return _one(found)


def _year_row_maximum(text: str):
    """A rate table that prints 2026 beside one maximum, with the label elsewhere on the page."""
    flat = re.sub(r"\s+", " ", text)
    if not _MAX_LABEL.search(flat):
        return None
    found = []
    pattern = re.compile(r"\b2026\b[^$]{0,24}\$\s*([0-9,]+\.\d{2}|[0-9,]+)")
    for match in pattern.finditer(flat):
        nearby = flat[max(0, match.start() - 120) : match.end()]
        if not _MAX_LABEL.search(nearby):
            continue
        amount = _money(match.group(1))
        if 400 <= float(amount) <= 3500 and not _prior_amounts(match.group(0)):
            found.append((amount, match.group(0)))
    return _one(found)


def find_maximum(text: str) -> tuple[int | float | None, str | None]:
    text = _normalize_spaced_money(text)
    explicit = _explicit_maximum(text)
    if explicit is not None:
        return explicit
    labeled_amount, labeled_quote = _pick_labeled(text, _MAX_LABEL, 400, 3500)
    dated_amount, dated_quote = _dated_maximum(text)
    if dated_amount is not None and not _same(dated_amount, labeled_amount):
        return dated_amount, dated_quote
    if labeled_amount is not None:
        return labeled_amount, labeled_quote
    stated = _workers_comp_maximum(text)
    if stated[0] is not None:
        return stated
    return _year_row_maximum(text) or (None, None)


_DATED_MINIMUM = re.compile(
    r"(?:January|July)\s+1,\s*2026.{0,120}?(?:minimum weekly|lower of)\s*\$\s*([0-9,]+\.\d{2})",
    re.I,
)


def _dated_minimum(text: str):
    flat = re.sub(r"\s+", " ", text)
    found = []
    for match in _DATED_MINIMUM.finditer(flat):
        amount = _money(match.group(1))
        if 20 <= float(amount) <= 1500:
            found.append((amount, match.group(0)))
    return _one(found)


def find_minimum(text: str) -> tuple[int | float | None, str | None]:
    text = _normalize_spaced_money(text)
    labeled_amount, labeled_quote = _pick_labeled(text, _MIN_LABEL, 20, 1500)
    dated = _dated_minimum(text)
    if dated is not None and not _same(dated[0], labeled_amount):
        return dated
    return labeled_amount, labeled_quote


def _rates(sentence: str) -> list[float]:
    found = []
    if _RATE_WORD.search(sentence):
        found.append(0.6667)
    for match in _PERCENT.finditer(sentence):
        rate = round(float(match.group(1)) / 100, 4)
        if 0.5 <= rate <= 0.9:
            found.append(rate)
    return _unique(found)


def find_rate(text: str) -> tuple[float | None, str | None]:
    text = _normalize_spaced_money(text)
    found = []
    for sentence in sentences(text):
        if len(sentence) > 400 or not _WAGE_CONTEXT.search(sentence):
            continue
        rates = _rates(sentence)
        if len(rates) == 1:
            found.append((rates[0], sentence))
    unique = _unique([rate for rate, _ in found])
    if len(unique) != 1:
        return None, None
    sentence = next(sentence for rate, sentence in found if rate == unique[0])
    return unique[0], _quote(sentence)


def find_ttd_weeks(text: str) -> tuple[int | None, str | None, bool]:
    """Return (weeks, quote, found). weeks is None when the page says there is no limit."""
    found: list[tuple[int | None, str]] = []
    for sentence in sentences(text):
        if not _TTD.search(sentence):
            continue
        weeks = [int(value) for value in _WEEKS.findall(sentence) if int(value) >= 90]
        no_limit = _NO_LIMIT.search(sentence) is not None
        if no_limit and weeks:
            continue
        if no_limit:
            found.append((None, sentence))
        elif len(_unique(weeks)) == 1:
            found.append((weeks[0], sentence))
    if not found:
        return None, None, False
    unique = _unique([value for value, _ in found])
    if len(unique) != 1:
        return None, None, False
    sentence = next(sentence for value, sentence in found if value == unique[0])
    return unique[0], _quote(sentence), True


def _same(left, right) -> bool:
    if left is None and right is None:
        return True
    if left is None or right is None:
        return False
    return abs(float(left) - float(right)) < 0.001


def attach_verification(block: dict, text: str, url: str, checked_at: str) -> dict:
    updated, fields = assess(block, text)
    stated = all(fields[name]["status"] in {"matched", "corrected"} for name in CHECKED_FIELDS)
    if stated:
        updated["figures_from"] = "official"
    updated["verification"] = {
        "checked_at": checked_at,
        "resource": url,
        "fetch_status": "ok",
        "fields": fields,
    }
    return updated


def unchecked_verification(block: dict, url: str, checked_at: str, error: str) -> dict:
    updated = dict(block)
    updated["verification"] = {
        "checked_at": checked_at,
        "resource": url,
        "fetch_status": "error",
        "error": error,
        "fields": {name: {"status": "unchecked"} for name in CHECKED_FIELDS},
    }
    return updated


def _field(status: str, quote: str | None = None, previous=None, official=None) -> dict:
    record = {"status": status}
    if quote:
        record["quote"] = quote
    if status == "corrected":
        record["claimcalc_value"] = previous
        record["official_value"] = official
    return record


def assess(block: dict, text: str) -> tuple[dict, dict]:
    """Return an updated claimcalc object. Unstated official figures stay as ClaimCalc published them."""
    updated = dict(block)
    fields = {}

    maximum, max_quote = find_maximum(text)
    if maximum is None:
        fields["maximum_weekly_benefit_usd"] = _field("unchecked")
    elif _same(maximum, block.get("maximum_weekly_benefit_usd")):
        fields["maximum_weekly_benefit_usd"] = _field("matched", max_quote)
    else:
        fields["maximum_weekly_benefit_usd"] = _field(
            "corrected",
            max_quote,
            block.get("maximum_weekly_benefit_usd"),
            maximum,
        )
        updated["maximum_weekly_benefit_usd"] = maximum

    minimum, min_quote = find_minimum(text)
    if minimum is None:
        fields["minimum_weekly_benefit_usd"] = _field("unchecked")
    elif _same(minimum, block.get("minimum_weekly_benefit_usd")):
        fields["minimum_weekly_benefit_usd"] = _field("matched", min_quote)
    else:
        fields["minimum_weekly_benefit_usd"] = _field(
            "corrected",
            min_quote,
            block.get("minimum_weekly_benefit_usd"),
            minimum,
        )
        updated["minimum_weekly_benefit_usd"] = minimum

    rate, rate_quote = find_rate(text)
    if rate is None:
        fields["wage_replacement_rate"] = _field("unchecked")
    elif _same(rate, block.get("wage_replacement_rate")):
        fields["wage_replacement_rate"] = _field("matched", rate_quote)
    else:
        fields["wage_replacement_rate"] = _field(
            "corrected",
            rate_quote,
            block.get("wage_replacement_rate"),
            rate,
        )
        updated["wage_replacement_rate"] = rate

    weeks, weeks_quote, found_weeks = find_ttd_weeks(text)
    if not found_weeks:
        fields["max_ttd_weeks"] = _field("unchecked")
    elif _same(weeks, block.get("max_ttd_weeks")):
        fields["max_ttd_weeks"] = _field("matched", weeks_quote)
    else:
        fields["max_ttd_weeks"] = _field(
            "corrected",
            weeks_quote,
            block.get("max_ttd_weeks"),
            weeks,
        )
        updated["max_ttd_weeks"] = weeks
        updated["max_ttd_wording"] = "no limit" if weeks is None else f"{weeks} weeks"

    return updated, fields


RATE_NOTICES = {
    "CA": (
        "https://www.dir.ca.gov/dwc/workerscompensationbenefits.htm",
        "California Division of Workers' Compensation benefit chart",
    ),
    "IA": (
        "https://dial.iowa.gov/hearings/workers-comp/rates",
        "Iowa workers' compensation rate information",
    ),
    "KY": (
        "https://elc.ky.gov/Workers-Compensation/Workers%20Compensation/2026%20Workers'%20Compensation%20Benefit%20Schedule.pdf",
        "Kentucky 2026 workers' compensation benefit schedule",
    ),
    "MI": (
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WDCA-Calculation-Program/wca_2026_Rate_Book.pdf",
        "Michigan 2026 weekly compensation rate book",
    ),
    "MN": (
        "https://www.dli.mn.gov/sites/default/files/pdf/comprates.pdf",
        "Minnesota compensation rates as of October 1, 2026",
    ),
    "NC": (
        "https://www.ic.nc.gov/workers-compensation-claims/maximum-weekly-compensation-rates",
        "North Carolina maximum weekly compensation rates",
    ),
    "NJ": (
        "https://www.nj.gov/labor/lwdhome/press/2025/20251229_newbenefitrates2026.shtml",
        "New Jersey 2026 benefit rates",
    ),
    "NY": (
        "https://www.wcb.ny.gov/content/main/Workers/ScheduleMaxWeeklyBenefit.jsp",
        "New York schedule of maximum weekly benefit",
    ),
    "OR": (
        "https://wcd.oregon.gov/Bulletins/bul_111.pdf",
        "Oregon Bulletin 111 benefit rates",
    ),
    "PA": (
        "https://www.pa.gov/agencies/dli/programs-services/workers-compensation/workers--compensation-claim/statewide-average-weekly-wage-saww",
        "Pennsylvania statewide average weekly wage",
    ),
    "SC": (
        "https://www.wcc.sc.gov/claims/compensation-rates",
        "South Carolina compensation rates",
    ),
    "TX": (
        "https://www.tdi.texas.gov/wc/employee/maxminbens.html",
        "Texas maximum and minimum weekly benefits",
    ),
    "WI": (
        "https://dwd.wisconsin.gov/wc/letters/insurance/ins-letter-549.htm",
        "Wisconsin 2026 maximum rates",
    ),
}

RATE_NOTICE_CHECKED_AT = "2026-10-28T17:15:00Z"


def apply_rate_notices(root=None, fetch=None) -> list[str]:
    """Point stored benefits at a fetched rate notice and keep a figure only when that page states it."""
    import regulations
    import wiki

    fetch = fetch or regulations.default_fetch
    notes = []
    for postal, (url, label) in RATE_NOTICES.items():
        item = wiki.resolve_jurisdiction(postal, root)
        record = item.reimbursement
        benefits = record.get("benefits") or {}
        if benefits.get("status") == "unlisted":
            continue
        try:
            data, content_type = fetch(url)
            text = regulations.document_from_response(data, content_type)["text"]
        except Exception as exc:
            record["benefits"] = unchecked_verification(
                benefits,
                url,
                RATE_NOTICE_CHECKED_AT,
                f"{type(exc).__name__}: {exc}",
            )
            wiki.write_reimbursement(item.path, record)
            notes.append(f"{postal} fetch failed")
            continue
        previous = benefits.get("maximum_weekly_benefit_usd")
        updated = attach_verification(benefits, text, url, RATE_NOTICE_CHECKED_AT)
        updated["official_source_resource"] = url
        updated["official_source_label"] = label
        maximum = updated["verification"]["fields"]["maximum_weekly_benefit_usd"]
        if maximum["status"] in {"matched", "corrected"}:
            updated["rate_year"] = 2026
        record["benefits"] = updated
        wiki.write_reimbursement(item.path, record)
        status = maximum["status"]
        current = updated.get("maximum_weekly_benefit_usd")
        notes.append(f"{postal} maximum {status}: {previous} -> {current}")
    return notes
