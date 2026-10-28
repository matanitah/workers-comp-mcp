---
type: Schema
title: Reimbursement record
description: JSON object for each jurisdiction. Benefit caps and fee-schedule maximums are the record. Injury-level settlement amounts are the ClaimCalc object.
tags: [workers-compensation, reimbursement, schema]
status: draft
stale_after: "2027-04-01T00:00:00Z"
generated: { by: cursor-agent/grok-4.7, at: "2026-10-28T15:00:00Z" }
sources:
  - id: methodology
    resource: /methodology
    title: Methodology
---

# Schema

Each jurisdiction record is a file under `/reimbursement/`, linked from the jurisdiction page. [Alabama](/states/alabama) points at [alabama.json](/reimbursement/alabama.json). `schema_version` is `"0.2"`. Amounts are US dollars. `null` means no cited figure, and it is not a zero.

The record stores official benefit limits and, when one was read, a medical fee schedule. Injury-level settlement amounts are the `claimcalc` object. This schema has no nature-of-injury table.

## benefits

Statutory indemnity limits: the weekly maximum, the weekly minimum, the wage-replacement rate, and the temporary-total week cap.

| Field | Meaning |
| --- | --- |
| `maximum_weekly_benefit_usd` | State maximum weekly indemnity benefit. |
| `minimum_weekly_benefit_usd` | State minimum, when a figure is on file. |
| `wage_replacement_rate` | Replacement percent as a fraction of 1. `0.6667` means 66.67 percent. |
| `wage_replacement_basis` | Formula wording that accompanies the rate. |
| `max_ttd_weeks` | Temporary-total week cap. `null` when the source says there is no limit. |
| `max_ttd_wording` | The week-cap phrase as printed. |
| `statute_of_limitations` | Present when a state page states one. |
| `rate_year` | Year the figures apply to. |
| `official_source_label` | Agency name printed beside the official link. |
| `official_source_resource` | Agency page linked as the official source. |
| `figures_from` | `claimcalc` while the stored numbers are ClaimCalc's snapshot. An official page replaces a number only when that page states a different figure. |
| `claimcalc_resource` | ClaimCalc page the snapshot was read from. |
| `verification` | Result of reading `official_source_resource`. `checked_at` is when that page was fetched. `fetch_status` is `ok` or `error`. Each of `maximum_weekly_benefit_usd`, `minimum_weekly_benefit_usd`, `wage_replacement_rate`, and `max_ttd_weeks` is `matched`, `corrected`, or `unchecked`. A correction also stores `claimcalc_value`, `official_value`, and a `quote` from the page. |

The District of Columbia is not on the ClaimCalc chart. Its `benefits` object is `status: unlisted` and a `reason`, with no weekly amounts. Its `verification.status` is `unlisted` because no official rate page was fetched.

On 2026-10-28 the linked agency pages did not state these four figures, so the stored numbers remain the ClaimCalc snapshot and each field is `unchecked`.

## medical_fee_schedule

Optional. `null` when this pass did not read a schedule. When present, it describes a procedure maximum or a link to one. It is not an injury settlement.

## claimcalc

Injury-level settlement amounts from [ClaimCalc](https://claimcalc.app/workers-comp/settlement-chart). `kind` is `injury_settlement`. A dedicated state page supplies `average_settlement_usd`, `approximate`, and `average_settlement_wording`. The settlement chart does not state that average, so chart-only states store `average_settlement_usd: null`. The state page wins when both exist.

| Field | Meaning |
| --- | --- |
| `average_settlement_usd` | The state page's approximate average settlement. |
| `approximate` | `true` when that average is printed with a tilde. |
| `average_settlement_wording` | The average as printed, such as `~$62,000`. |
| `resource` | State calculator page when one exists, otherwise the settlement chart. |
| `chart_resource` | The settlement chart. |
| `verified` | `YYYY-MM-DD` from a state page, or `YYYY-MM` when the chart only says January 2025. |
| `retrieved_at` | When this snapshot was written. |

The District of Columbia's `claimcalc` object is `status: unlisted` and the same reason, with no settlement amount.

The averages guide that attributes a state table to NCCI and WCRI is not ingested. Countrywide figures are a separate file, [countrywide.json](/reimbursement/countrywide.json), and they are not state rates.

## Example shape

```json
{
  "maximum_weekly_benefit_usd": 1112,
  "minimum_weekly_benefit_usd": null,
  "wage_replacement_rate": 0.6667,
  "max_ttd_weeks": 500,
  "figures_from": "claimcalc"
}
```

[^methodology]: Methodology
