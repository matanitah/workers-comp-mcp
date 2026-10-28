---
type: Jurisdiction
title: New York
description: "New York workers' compensation agency and primary law. Open average reimbursement by injury is not yet available."
resource: "http://www.wcb.ny.gov/"
tags: [workers-compensation, ny, reimbursement, regulations]
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
    resource: "http://www.wcb.ny.gov/"
    title: "Workers' Compensation Board"
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/new-york"
    title: "ClaimCalc workers' compensation figures for New York"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "New York Workers' Compensation Law section 1"
    resource: "https://www.nysenate.gov/legislation/laws/WKC/1"
    publisher: "New York State Senate"
    coverage: "section"
    text_file: "statutes/new-york.txt"
    retrieved_at: "2026-10-28T16:45:00Z"
---

# Agency

Workers' Compensation Board administers workers' compensation for New York.[^dol-directory]

- Address: 328 State Street, Schenectady, NY 12305; mailing P.O. Box 5205, Binghamton, NY 13902-5205
- Phone: (877) 632-4996
- Web: http://www.wcb.ny.gov/
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

New York Workers' Compensation Law.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The reimbursement record is [New York reimbursement](/reimbursement/new-york.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
