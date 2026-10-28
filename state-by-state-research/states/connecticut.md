---
type: Jurisdiction
title: Connecticut
description: "Connecticut workers' compensation agency and primary law. Open average reimbursement by injury is not yet available."
resource: "https://portal.ct.gov/WCC"
tags: [workers-compensation, ct, reimbursement, regulations]
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
    resource: "https://portal.ct.gov/WCC"
    title: "Workers' Compensation Commission"
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/settlement-chart"
    title: "ClaimCalc workers' compensation figures for Connecticut"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "Connecticut General Statutes chapter 568"
    resource: "https://www.cga.ct.gov/current/pub/chap_568.htm"
    publisher: "Connecticut General Assembly"
    coverage: "act"
    text_file: "statutes/connecticut.txt"
    retrieved_at: "2026-10-28T16:40:00Z"
---

# Agency

Workers' Compensation Commission administers workers' compensation for Connecticut.[^dol-directory]

- Address: Capitol Place, 21 Oak Street, 4th Floor, Hartford, CT 06106
- Phone: (860) 493-1500 or (800) 223-9675
- Web: https://portal.ct.gov/WCC
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

Connecticut Workers' Compensation Act, Conn. Gen. Stat. Chapter 568.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The reimbursement record is [Connecticut reimbursement](/reimbursement/connecticut.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
