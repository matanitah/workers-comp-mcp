---
type: Jurisdiction
title: Illinois
description: "Illinois workers' compensation agency and primary law. Open average reimbursement by injury is not yet available."
resource: "http://www.iwcc.il.gov/"
tags: [workers-compensation, il, reimbursement, regulations]
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
    resource: "http://www.iwcc.il.gov/"
    title: "Illinois Workers' Compensation Commission"
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/illinois"
    title: "ClaimCalc workers' compensation figures for Illinois"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "Illinois Workers' Compensation Act"
    resource: "https://www.ilga.gov/Legislation/ILCS/Articles?ActID=2430&ChapterID=68&Print=True"
    publisher: "Illinois General Assembly"
    coverage: "act"
    text_file: "statutes/illinois.txt"
    retrieved_at: "2026-10-28T16:40:00Z"
---

# Agency

Illinois Workers' Compensation Commission administers workers' compensation for Illinois.[^dol-directory]

- Address: Cook County Office Building, 69 W. Washington Street, Suite 900, Chicago, IL 60602
- Phone: (312) 814-6500
- Web: http://www.iwcc.il.gov/
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

Illinois Workers' Compensation Act, 820 ILCS 305.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The reimbursement record is [Illinois reimbursement](/reimbursement/illinois.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
