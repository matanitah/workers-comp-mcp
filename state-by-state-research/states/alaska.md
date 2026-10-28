---
type: Jurisdiction
title: Alaska
description: "Alaska workers' compensation agency and primary law. Injury averages are unpublished here; a cited medical fee schedule is recorded separately."
resource: "http://labor.alaska.gov/wc/"
tags: [workers-compensation, ak, reimbursement, regulations]
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
    resource: "http://labor.alaska.gov/wc/"
    title: "Department of Labor & Workforce Development, Division of Workers' Compensation"
    author: process:state-agency

  - id: fee-schedule
    resource: https://labor.state.ak.us/wc/forms/2025_Alaska_Medical_Fee_Schedule.pdf
    title: Alaska medical fee schedule source cited in the JSON
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/settlement-chart"
    title: "ClaimCalc workers' compensation figures for Alaska"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "Alaska Statutes title 23"
    resource: "https://www.akleg.gov/statutesPDF/Title-23.pdf"
    publisher: "Alaska Legislature"
    coverage: "act"
---

# Agency

Department of Labor & Workforce Development, Division of Workers' Compensation administers workers' compensation for Alaska.[^dol-directory]

- Address: 1111 West 8th Street, Room 305, P.O. Box 115512, Juneau, AK 99801
- Phone: (907) 465-2790
- Web: http://labor.alaska.gov/wc/
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

Alaska Workers' Compensation Act, AS 23.30.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The `medical_fee_schedule` object is a procedure maximum, or a pointer to one.[^fee-schedule]

The reimbursement record is [Alaska reimbursement](/reimbursement/alaska.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
[^fee-schedule]: Medical fee schedule source cited in frontmatter
