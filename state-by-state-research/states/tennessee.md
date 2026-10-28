---
type: Jurisdiction
title: Tennessee
description: "Tennessee workers' compensation agency and primary law. Injury averages are unpublished here; a cited medical fee schedule is recorded separately."
resource: "https://www.tn.gov/workforce/injuries-at-work.html"
tags: [workers-compensation, tn, reimbursement, regulations]
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
    resource: "https://www.tn.gov/workforce/injuries-at-work.html"
    title: "Department of Labor and Workforce Development, Division of Workers' Compensation"
    author: process:state-agency

  - id: fee-schedule
    resource: https://www.tn.gov/workforce/injuries-at-work/bureau-services/bureau-services/medical-fee-schedule/handbook/medical-fee-schedule-handbook-april-2025.html
    title: Tennessee medical fee schedule source cited in the JSON
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/tennessee"
    title: "ClaimCalc workers' compensation figures for Tennessee"
    author: process:claimcalc
regulations:
  - id: agency-rules
    title: "Tennessee Rules chapter 0800-02-01"
    resource: "https://publications.tnsosfiles.com/rules/0800/0800-02/0800-02-01.20180531.pdf"
    publisher: "Tennessee Secretary of State"
    coverage: "rules"
---

# Agency

Department of Labor and Workforce Development, Division of Workers' Compensation administers workers' compensation for Tennessee.[^dol-directory]

- Address: 220 French Landing Drive, Nashville, TN 37243-1002
- Phone: (844) 224-5818
- Web: https://www.tn.gov/workforce/injuries-at-work.html
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

Tennessee Workers' Compensation Law, Tenn. Code Ann. § 50-6-101 et seq.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The `medical_fee_schedule` object is a procedure maximum, or a pointer to one.[^fee-schedule]

The reimbursement record is [Tennessee reimbursement](/reimbursement/tennessee.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
[^fee-schedule]: Medical fee schedule source cited in frontmatter
