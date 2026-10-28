---
type: Jurisdiction
title: Arizona
description: "Arizona workers' compensation agency and primary law. Open average reimbursement by injury is not yet available."
resource: "https://www.azica.gov/claims-division"
tags: [workers-compensation, az, reimbursement, regulations]
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
    resource: "https://www.azica.gov/claims-division"
    title: "Industrial Commission of Arizona, Claims Division"
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/settlement-chart"
    title: "ClaimCalc workers' compensation figures for Arizona"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "Arizona Revised Statutes section 23-901"
    resource: "https://www.azleg.gov/ars/23/00901.htm"
    publisher: "Arizona State Legislature"
    coverage: "section"
---

# Agency

Industrial Commission of Arizona, Claims Division administers workers' compensation for Arizona.[^dol-directory]

- Address: 800 West Washington Street, Phoenix, AZ 85007; mailing P.O. Box 19070, Phoenix, AZ 85005
- Phone: (602) 542-4661
- Web: https://www.azica.gov/claims-division
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

Arizona Workers' Compensation Act, A.R.S. § 23-901 et seq.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The reimbursement record is [Arizona reimbursement](/reimbursement/arizona.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
