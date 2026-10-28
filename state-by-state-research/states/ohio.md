---
type: Jurisdiction
title: Ohio
description: "Ohio workers' compensation agency and primary law. Open average reimbursement by injury is not yet available."
resource: "http://www.bwc.ohio.gov"
tags: [workers-compensation, oh, reimbursement, regulations]
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
    resource: "http://www.bwc.ohio.gov"
    title: "Bureau of Workers' Compensation"
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/ohio"
    title: "ClaimCalc workers' compensation figures for Ohio"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "Ohio Revised Code chapter 4123"
    resource: "https://codes.ohio.gov/ohio-revised-code/chapter-4123"
    publisher: "Ohio Legislative Service Commission"
    coverage: "act"
---

# Agency

Bureau of Workers' Compensation administers workers' compensation for Ohio.[^dol-directory]

- Address: 30 West Spring Street, Columbus, OH 43215-2256
- Phone: (800) 644-6292
- Web: http://www.bwc.ohio.gov
- Insurance market: Exclusive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

Ohio workers' compensation law, Ohio Rev. Code Chapter 4123.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The reimbursement record is [Ohio reimbursement](/reimbursement/ohio.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
