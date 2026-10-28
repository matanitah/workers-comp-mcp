---
type: Jurisdiction
title: Maryland
description: "Maryland workers' compensation agency and primary law. Open average reimbursement by injury is not yet available."
resource: "http://www.wcc.state.md.us/"
tags: [workers-compensation, md, reimbursement, regulations]
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
    resource: "http://www.wcc.state.md.us/"
    title: "Workers' Compensation Commission"
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/maryland"
    title: "ClaimCalc workers' compensation figures for Maryland"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "Maryland Code, Labor and Employment article"
    resource: "https://mgaleg.maryland.gov/2026RS/Statute_Web/GLE/GLE.pdf"
    publisher: "Maryland General Assembly"
    coverage: "act"
---

# Agency

Workers' Compensation Commission administers workers' compensation for Maryland.[^dol-directory]

- Address: 10 East Baltimore Street, 4th Floor, Baltimore, MD 21202
- Phone: (410) 864-5100
- Web: http://www.wcc.state.md.us/
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

Maryland Workers' Compensation Act, Md. Code, Lab. & Empl. § 9-101 et seq.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The reimbursement record is [Maryland reimbursement](/reimbursement/maryland.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
