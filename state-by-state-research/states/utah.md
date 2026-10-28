---
type: Jurisdiction
title: Utah
description: "Utah workers' compensation agency and primary law. Injury averages are unpublished here; a cited medical fee schedule is recorded separately."
resource: "https://laborcommission.utah.gov/divisions/industrial-accidents/injured-workers/"
tags: [workers-compensation, ut, reimbursement, regulations]
status: draft
stale_after: "2027-04-01T00:00:00Z"
generated: { by: cursor-agent/grok-4.7, at: "2026-10-28T15:00:00Z" }
sources:
  - id: dol-directory
    resource: https://www.dol.gov/agencies/owcp/wc
    title: State Workers' Compensation Officials
    author: process:us-dol-owcp
    last_modified: "2026-10-28T15:00:00Z"
  - id: agency
    resource: "https://laborcommission.utah.gov/divisions/industrial-accidents/injured-workers/"
    title: "Labor Commission, Division of Industrial Accidents"
    author: process:state-agency

  - id: fee-schedule
    resource: https://laborcommission.utah.gov/wp-content/uploads/2025-Medical-Fee-Schedule-3.pdf
    title: Utah medical fee schedule source cited in the JSON
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/settlement-chart"
    title: "ClaimCalc workers' compensation figures for Utah"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "Utah Code title 34A, chapter 2"
    resource: "https://le.utah.gov/xcode/Title34A/Chapter2/C34A-2_1800010118000101.pdf"
    publisher: "Utah State Legislature"
    coverage: "act"
---

# Agency

Labor Commission, Division of Industrial Accidents administers workers' compensation for Utah.[^dol-directory]

- Address: 160 East 300 South, 3rd Floor, Salt Lake City, UT 84114-6610
- Phone: (801) 530-6800
- Web: https://laborcommission.utah.gov/divisions/industrial-accidents/injured-workers/
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

Utah Workers' Compensation Act, Utah Code Title 34A, Chapter 2. Occupational disease is Title 34A, Chapter 3.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The `medical_fee_schedule` object is a procedure maximum, or a pointer to one.[^fee-schedule]

The reimbursement record is [Utah reimbursement](/reimbursement/utah.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
[^fee-schedule]: Medical fee schedule source cited in frontmatter
