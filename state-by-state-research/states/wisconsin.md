---
type: Jurisdiction
title: Wisconsin
description: "Wisconsin workers' compensation agency and primary law. Open average reimbursement by injury is not yet available."
resource: "https://dwd.wisconsin.gov/wc/"
tags: [workers-compensation, wi, reimbursement, regulations]
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
    resource: "https://dwd.wisconsin.gov/wc/"
    title: "Department of Workforce Development, Workers' Compensation Division"
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/settlement-chart"
    title: "ClaimCalc workers' compensation figures for Wisconsin"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "Wisconsin Statutes chapter 102"
    resource: "https://docs.legis.wisconsin.gov/statutes/statutes/102.pdf"
    publisher: "Wisconsin Legislature"
    coverage: "act"
---

# Agency

Department of Workforce Development, Workers' Compensation Division administers workers' compensation for Wisconsin.[^dol-directory]

- Address: 201 East Washington Avenue, P.O. Box 7946, Madison, WI 53707
- Phone: (608) 266-3131
- Web: https://dwd.wisconsin.gov/wc/
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

Wisconsin Worker's Compensation Act, Wis. Stat. Chapter 102.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The reimbursement record is [Wisconsin reimbursement](/reimbursement/wisconsin.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
