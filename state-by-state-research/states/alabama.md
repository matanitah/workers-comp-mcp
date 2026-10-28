---
type: Jurisdiction
title: Alabama
description: "Alabama workers' compensation agency and primary law. Injury averages are unpublished here; the 2025 fee-schedule index is linked and not copied."
resource: "http://labor.alabama.gov/wc"
tags: [workers-compensation, al, reimbursement, regulations]
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
    resource: "http://labor.alabama.gov/wc"
    title: "Department of Labor, Workers' Compensation Division"
    author: process:state-agency

  - id: fee-schedule
    resource: https://labor.alabama.gov/wc/2025FeeSchedules.aspx
    title: Alabama medical fee schedule source cited in the JSON
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/settlement-chart"
    title: "ClaimCalc workers' compensation figures for Alabama"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "Code of Alabama section 25-5-1"
    resource: "https://alison.legislature.state.al.us/code-of-alabama?section=25-5-1"
    publisher: "Alabama Legislature"
    coverage: "section"
    text_file: "statutes/alabama.txt"
    retrieved_at: "2026-10-28T16:45:00Z"
---

# Agency

Department of Labor, Workers' Compensation Division administers workers' compensation for Alabama.[^dol-directory]

- Address: 649 Monroe Street, Montgomery, AL 36131
- Phone: (334) 956-4044 or (800) 528-5166
- Web: http://labor.alabama.gov/wc
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

Alabama Workers' Compensation Act, Ala. Code § 25-5-1 et seq.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The `medical_fee_schedule` object is a procedure maximum, or a pointer to one.[^fee-schedule]

The reimbursement record is [Alabama reimbursement](/reimbursement/alabama.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
[^fee-schedule]: Medical fee schedule source cited in frontmatter
