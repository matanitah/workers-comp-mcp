---
type: Jurisdiction
title: California
description: "California workers' compensation agency and primary law. Benefit caps are in the reimbursement file. Injury-level amounts are ClaimCalc's."
resource: "http://www.dir.ca.gov/dwc/dwc_home_page.htm"
tags: [workers-compensation, ca, reimbursement, regulations]
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
    resource: "http://www.dir.ca.gov/dwc/dwc_home_page.htm"
    title: "Department of Industrial Relations, Division of Workers' Compensation"
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/california"
    title: "ClaimCalc workers' compensation figures for California"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "California Labor Code division 4, part 1, chapter 1"
    resource: "https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?article=&chapter=1.&division=4.&lawCode=LAB&part=1.&title="
    publisher: "California Legislative Counsel"
    coverage: "section"
    text_file: "statutes/california.txt"
    retrieved_at: "2026-10-28T16:45:00Z"
---

# Agency

Department of Industrial Relations, Division of Workers' Compensation administers workers' compensation for California.[^dol-directory]

- Address: 455 Golden Gate Avenue, 2nd Floor, San Francisco, CA 94102-7014
- Phone: (415) 703-5020 or (800) 736-7401
- Web: http://www.dir.ca.gov/dwc/dwc_home_page.htm
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

California workers' compensation law, Labor Code § 3200 et seq.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The reimbursement record is [California reimbursement](/reimbursement/california.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
