---
type: Jurisdiction
title: Indiana
description: "Indiana workers' compensation agency and primary law. Open average reimbursement by injury is not yet available."
resource: "http://www.in.gov/wcb/"
tags: [workers-compensation, in, reimbursement, regulations]
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
    resource: "http://www.in.gov/wcb/"
    title: "Workers' Compensation Board of Indiana"
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/indiana"
    title: "ClaimCalc workers' compensation figures for Indiana"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "Indiana Code title 22, article 3"
    resource: "https://iga.in.gov/ic/2026/Title_22/Article_3.pdf"
    publisher: "Indiana General Assembly"
    coverage: "act"
---

# Agency

Workers' Compensation Board of Indiana administers workers' compensation for Indiana.[^dol-directory]

- Address: 402 West Washington Street, Room W-196, Indianapolis, IN 46204
- Phone: (317) 232-3811
- Web: http://www.in.gov/wcb/
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

Indiana Worker's Compensation Act, Ind. Code § 22-3-1-1 et seq.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The reimbursement record is [Indiana reimbursement](/reimbursement/indiana.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
