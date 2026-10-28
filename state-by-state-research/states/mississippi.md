---
type: Jurisdiction
title: Mississippi
description: "Mississippi workers' compensation agency and primary law. Open average reimbursement by injury is not yet available."
resource: "https://mwcc.ms.gov/"
tags: [workers-compensation, ms, reimbursement, regulations]
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
    resource: "https://mwcc.ms.gov/"
    title: "Workers' Compensation Commission"
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/settlement-chart"
    title: "ClaimCalc workers' compensation figures for Mississippi"
    author: process:claimcalc
regulations:
  - id: agency-rules
    title: "Rules of the Mississippi Workers' Compensation Commission"
    resource: "https://www.mwcc.ms.gov/#/generalAndProceduralRules"
    publisher: "Mississippi Workers' Compensation Commission"
    coverage: "rules"
    text_file: "statutes/mississippi.txt"
    retrieved_at: "2026-10-28T16:45:00Z"
---

# Agency

Workers' Compensation Commission administers workers' compensation for Mississippi.[^dol-directory]

- Address: 301 N. Lamar Street, Jackson, MS 39201
- Phone: (601) 987-4200 or (866) 473-6922
- Web: https://mwcc.ms.gov/
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

Mississippi Workers' Compensation Law, Miss. Code Ann. § 71-3-1 et seq.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The reimbursement record is [Mississippi reimbursement](/reimbursement/mississippi.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
