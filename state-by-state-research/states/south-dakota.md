---
type: Jurisdiction
title: South Dakota
description: "South Dakota workers' compensation agency and primary law. Open average reimbursement by injury is not yet available."
resource: "https://dlr.sd.gov/workers_compensation/"
tags: [workers-compensation, sd, reimbursement, regulations]
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
    resource: "https://dlr.sd.gov/workers_compensation/"
    title: "Department of Labor and Regulation, Division of Labor & Management"
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/settlement-chart"
    title: "ClaimCalc workers' compensation figures for South Dakota"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "South Dakota Codified Laws section 62-1-1"
    resource: "https://sdlegislature.gov/api/Statutes/Statute/62-1-1"
    publisher: "South Dakota Legislative Research Council"
    coverage: "section"
---

# Agency

Department of Labor and Regulation, Division of Labor & Management administers workers' compensation for South Dakota.[^dol-directory]

- Address: 123 W. Missouri Avenue, Pierre, SD 57501-2291
- Phone: (605) 773-3681
- Web: https://dlr.sd.gov/workers_compensation/
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

South Dakota workers' compensation law, SDCL Title 62.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The reimbursement record is [South Dakota reimbursement](/reimbursement/south-dakota.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
