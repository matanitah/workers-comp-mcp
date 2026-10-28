---
type: Jurisdiction
title: Virginia
description: "Virginia workers' compensation agency and primary law. Open average reimbursement by injury is not yet available."
resource: "https://workcomp.virginia.gov"
tags: [workers-compensation, va, reimbursement, regulations]
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
    resource: "https://workcomp.virginia.gov"
    title: "Workers' Compensation Commission"
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/virginia"
    title: "ClaimCalc workers' compensation figures for Virginia"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "Code of Virginia title 65.2"
    resource: "https://law.lis.virginia.gov/vacodefull/title65.2/"
    publisher: "Virginia Legislative Information System"
    coverage: "act"
---

# Agency

Workers' Compensation Commission administers workers' compensation for Virginia.[^dol-directory]

- Address: 333 E. Franklin Street, Richmond, VA 23219
- Phone: (877) 664-2566
- Web: https://workcomp.virginia.gov
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

Virginia Workers' Compensation Act, Va. Code Ann. Title 65.2.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The reimbursement record is [Virginia reimbursement](/reimbursement/virginia.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
