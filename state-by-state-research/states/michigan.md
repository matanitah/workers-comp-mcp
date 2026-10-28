---
type: Jurisdiction
title: Michigan
description: "Michigan workers' compensation agency and primary law. Injury averages are unpublished here; a cited medical fee schedule is recorded separately."
resource: "http://www.michigan.gov/wca"
tags: [workers-compensation, mi, reimbursement, regulations]
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
    resource: "http://www.michigan.gov/wca"
    title: "Department of Licensing and Regulatory Affairs, Workers' Compensation Agency"
    author: process:state-agency

  - id: fee-schedule
    resource: https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WDCA-HEALTHCARE/2025/RBRVS/RBRVS-methodology.pdf
    title: Michigan medical fee schedule source cited in the JSON
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/michigan"
    title: "ClaimCalc workers' compensation figures for Michigan"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "Michigan Compiled Laws Act 317 of 1969"
    resource: "https://www.legislature.mi.gov/documents/mcl/pdf/mcl-Act-317-of-1969.pdf"
    publisher: "Michigan Legislature"
    coverage: "act"
---

# Agency

Department of Licensing and Regulatory Affairs, Workers' Compensation Agency administers workers' compensation for Michigan.[^dol-directory]

- Address: 2501 Woodlake Circle, Suite 115, Okemos, MI 48864; mailing P.O. Box 30016, Lansing, MI 48909
- Phone: (888) 396-5041
- Web: http://www.michigan.gov/wca
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

Michigan Worker's Disability Compensation Act, MCL 418.101 et seq.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The `medical_fee_schedule` object is a procedure maximum, or a pointer to one.[^fee-schedule]

The reimbursement record is [Michigan reimbursement](/reimbursement/michigan.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
[^fee-schedule]: Medical fee schedule source cited in frontmatter
