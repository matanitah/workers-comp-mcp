---
type: Jurisdiction
title: Massachusetts
description: "Massachusetts workers' compensation agency and primary law. Open average reimbursement by injury is not yet available."
resource: "http://www.mass.gov/lwd/workers-compensation/"
tags: [workers-compensation, ma, reimbursement, regulations]
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
    resource: "http://www.mass.gov/lwd/workers-compensation/"
    title: "Department of Industrial Accidents"
    author: process:state-agency
  - id: claimcalc
    resource: "https://claimcalc.app/workers-comp/settlement-chart"
    title: "ClaimCalc workers' compensation figures for Massachusetts"
    author: process:claimcalc
regulations:
  - id: primary-statute
    title: "Massachusetts General Laws chapter 152, section 1"
    resource: "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXXI/Chapter152/section1"
    publisher: "Massachusetts General Court"
    coverage: "section"
---

# Agency

Department of Industrial Accidents administers workers' compensation for Massachusetts.[^dol-directory]

- Address: Lafayette City Center, 2 Avenue de Lafeyette, Boston, MA 02111
- Phone: (617) 727-4900
- Web: http://www.mass.gov/lwd/workers-compensation/
- Insurance market: Private carriers, self-insurance, or a competitive state fund.

The U.S. Department of Labor directory was retrieved on 2026-10-28. Office names and street addresses on that page can lag a move. The linked page is the one DOL published for this jurisdiction.

# Primary law

Massachusetts Workers' Compensation Act, Mass. Gen. Laws ch. 152.

# Regulations

This concept does not yet contain the statute or regulations word for word. The text to mirror later is the official code named above, from the state publisher, together with the agency's adopted medical-fee and benefit rules. Commercial annotated codes are not the source.

# Reimbursement

The reimbursement record stores the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. Injury-level settlement amounts are the ClaimCalc object in that file.[^dol-directory]

The reimbursement record is [Massachusetts reimbursement](/reimbursement/massachusetts.json).

[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
