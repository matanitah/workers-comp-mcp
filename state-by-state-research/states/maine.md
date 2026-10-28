---
type: Jurisdiction
title: Maine
description: "Maine workers' compensation agency and primary law. Open average reimbursement by injury is not yet available."
resource: "http://maine.gov/wcb/"
tags: [workers-compensation, me, reimbursement, regulations]
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
    resource: "http://maine.gov/wcb/"
    title: "Workers' Compensation Board"
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/settlement-chart"
    title: "ClaimCalc workers' compensation figures for Maine"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "Maine Revised Statutes title 39-A"
    resource: "https://legislature.maine.gov/statutes/39-A/title39-A.pdf"
    publisher: "Maine Legislature"
    coverage: "act"
---

# Agency

Workers' Compensation Board administers workers' compensation for Maine.[^dol-directory]

- Address: 442 Civil Center Drive, Suite 100, Augusta, ME 04330-8572; mailing 27 State House Station, Augusta, ME 04333-0027
- Phone: (207) 287-3751
- Web: http://maine.gov/wcb/
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

Maine Workers' Compensation Act, 39-A M.R.S. § 101 et seq.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The reimbursement record is [Maine reimbursement](/reimbursement/maine.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
