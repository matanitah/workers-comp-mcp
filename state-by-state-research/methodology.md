---
type: Reference
title: Methodology
description: How this bundle treats official regulations, benefit caps, and ClaimCalc injury settlements.
tags: [workers-compensation, methodology, regulations, reimbursement]
status: draft
stale_after: "2027-04-01T00:00:00Z"
generated: { by: cursor-agent/grok-4.7, at: "2026-10-28T15:00:00Z" }
sources:
  - id: okf
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
    title: Open Knowledge Format v0.2
    author: process:okf-spec
  - id: dol-directory
    resource: https://www.dol.gov/agencies/owcp/wc
    title: State Workers' Compensation Officials
    author: process:us-dol-owcp
    last_modified: "2026-10-28T15:00:00Z"
  - id: ncci-asb-terms
    resource: https://www.ncci.com/asb/editionlist/2025/Annual%20Statistical%20Bulletin.pdf
    title: NCCI Annual Statistical Bulletin, 2025 edition, terms of use
    author: process:ncci
  - id: claimcalc
    resource: https://claimcalc.app/workers-comp/settlement-chart
    title: "ClaimCalc workers' compensation settlement chart"
    author: process:claimcalc
---

# Purpose

The server this research supports should, for a state, return the current workers' compensation regulations word for word and the average reimbursement by injury. This bundle records what can be cited today and leaves an explicit hole where a number cannot.

# Regulations

"Word for word" means the official act and the agency rules that govern compensability, benefits, and medical payment, taken from the state publisher.

Each jurisdiction concept names the primary law and the agency page listed by the U.S. Department of Labor on 2026-10-28.[^dol-directory] `get_regulations` returns one cataloged publisher document. A URL is cataloged when that single response contains the statute: the citation appears in the text, the text is longer than a navigation shell, and the body is not a JavaScript prompt or an access-denied page. Annotated commercial codes are not the source. Connecticut General Statutes chapter 568 and the Illinois Workers' Compensation Act are saved under `statutes/` because those publisher hosts fail the server's TLS check. The catalog still names the official URL.

On 2026-10-28 a later pass added Colorado's 2026 Workers' Compensation Act PDF, Connecticut General Statutes chapter 568, Florida Statutes section 440.02, the Illinois Workers' Compensation Act, Indiana Code title 22 article 3 chapter 2, Montana Code Annotated section 39-71-101, the New Jersey Division of Workers' Compensation compilation of Title 34 chapter 15, New Mexico Statutes chapter 52, South Dakota Codified Laws section 62-1-1, and the Texas Department of Insurance compilation of the Workers' Compensation Act through the 89th Legislature. Earlier entries remain: Alaska Statutes title 23, Arizona Revised Statutes section 23-901, D.C. Code section 32-1501, Delaware Code title 19 chapter 23 subchapter I, Idaho Code title 72 chapter 1, Iowa Code section 85.1, Kansas Statutes section 44-501, Kentucky Revised Statutes section 342.0011, Louisiana Revised Statutes section 23:1021, Maine Revised Statutes title 39-A, Maryland Code Labor and Employment article, Massachusetts General Laws chapter 152 section 1, Michigan Compiled Laws Act 317 of 1969, Minnesota Statutes section 176.011, Missouri Revised Statutes section 287.020, Nebraska Revised Statutes section 48-101, Nevada Revised Statutes chapter 616A, New Hampshire RSA chapter 281-A, North Carolina General Statutes chapter 97, North Dakota Century Code chapter 65-01, Ohio Revised Code section 4123.01, Oklahoma Statutes title 85A, Oregon Revised Statutes chapter 656, the Pennsylvania Workers' Compensation Act, Rhode Island General Laws section 28-33-1, South Carolina Code title 42 chapter 1, Utah Code title 34A chapter 2, Vermont Statutes title 21 section 601, the Code of Virginia title 65.2, Revised Code of Washington 51.04.010, Wisconsin Statutes section 102.03, West Virginia Code section 23-1-1, and Wyoming Statutes title 27. Alaska's file is title 23, Maryland's file is the Labor and Employment article, and Wyoming's file is title 27. Each of those contains the workers' compensation law and other chapters. Oklahoma's file is the Senate's May 2022 compilation of title 85A. New Jersey's file is the Division's December 15, 2025 compilation, and the Division says the Revised Statutes control. Where the publisher does not serve the whole act as one document, the entry title names the section or chapter that the URL actually contains.

Every state and the District of Columbia now has a cataloged document. `coverage` is `act` when that document is the workers' compensation statute or the chapter that is that statute, `chapter` when it is a multi-section piece of the act, `section` when it is one section, and `rules` when the code is published through Lexis and the catalog holds the official agency rules instead. `get_regulations` returns the act when both are cataloged, and `source_id` `agency-rules` returns the rules. `section` returns the passage that starts at a citation. A live fetch that fails returns `fetch_error`.

Florida Statutes chapter 440, Iowa Code chapter 85, Minnesota Statutes chapter 176, Ohio Revised Code chapter 4123, and Wisconsin Statutes chapter 102 are the whole chapter. Alabama section 25-5-1, California Labor Code division 4 part 1 chapter 1, and New York Workers' Compensation Law section 1 are saved under `statutes/` because those official pages do not return the statute to the server's HTTP client. Hawaii Revised Statutes section 386-1 is fetched from the legislature's statute archive. Connecticut chapter 568 and the Illinois Workers' Compensation Act are saved for the same TLS reason.

Arkansas, Georgia, Mississippi, and Tennessee publish the code through Lexis. That commercial text is not copied. Their catalog entries are the official agency rules instead: Code of Arkansas Rules title 11 part 25, the Georgia State Board of Workers' Compensation rules, the Mississippi Workers' Compensation Commission rules, and Tennessee Rules chapter 0800-02-01. Mississippi's rules page is a client-rendered shell, so that text is saved under `statutes/` as well.

# Reimbursement

The shape is defined in the [reimbursement record](/reimbursement-schema). A jurisdiction file holds two different kinds of number.

1. **Benefit caps.** The weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap live in `benefits`. A medical fee schedule, when one was read, lives in `medical_fee_schedule`. A fee schedule prices a procedure. It does not say what a fracture or a sprain costs.
2. **Injury-level settlements.** Those amounts are the `claimcalc` object. This bundle does not keep a nature-of-injury table.

# What was found

NCCI's Annual Statistical Bulletin reports average cost per case by injury type and by state. Its terms forbid copying the bulletin, preparing derivative works from it, and using it as input or output of an AI application.[^ncci-asb-terms] Those exhibits are not in this bundle. Injury-level amounts in a jurisdiction file come from ClaimCalc. The [countrywide claim costs](/countrywide-claim-costs) page records only the summary figures a separate public page states, and it says they are national.

Fee-schedule facts read from the agency's own page are on [Alabama](/states/alabama), [Alaska](/states/alaska), [Michigan](/states/michigan), [Tennessee](/states/tennessee), and [Utah](/states/utah). Alabama's entry points at the 2025 schedule index and does not copy the rate tables. California's 2024 CHSWC annual report states a few permanent-disability averages in prose. Those injury amounts are not copied into the reimbursement record.

# ClaimCalc

`benefits` is filled from the [ClaimCalc settlement chart](https://claimcalc.app/workers-comp/settlement-chart) and, where ClaimCalc publishes one, the state calculator page such as [California](https://claimcalc.app/workers-comp/california). The state page wins when it disagrees with the chart. `figures_from` stays `claimcalc` until an official page states a different number. The District of Columbia is absent from the chart, so its `benefits` object says so and stores no amount.

`claimcalc` keeps that source's injury-level settlement: the state page's approximate average, with `kind` set to `injury_settlement`. The chart does not print that average. The separate ClaimCalc averages guide attributes its state table to NCCI and WCRI, and its caps disagree with the state pages. That guide is not ingested.[^claimcalc]

The record itself is not inside the jurisdiction page. It is `/reimbursement/<slug>.json`, and the page links to that file. Countrywide figures are `/reimbursement/countrywide.json`.

On 2026-10-28 each state's `official_source_resource` was fetched once. Those links are agency homepages. The weekly maximum, weekly minimum, wage-replacement percent, and temporary-total week cap were replaced only when that page stated a different number, and the previous ClaimCalc value was kept on `verification` with a quotation. Pages that did not state a figure left the ClaimCalc value in place and marked the field `unchecked`. No fetched homepage stated one of those four figures, so no benefit number changed on that pass. The settlement average was not compared, because the homepages do not publish it. Twelve fetches did not return the agency page (HTTP 403, a certificate error, a host that did not resolve, an empty body, or a bot check); those fields are `unchecked` and the error is stored. The District of Columbia stayed `unlisted`.

A later pass pointed verification at the official rate notice where one was fetched. A figure changed only when that notice stated it. `figures_from` stays `claimcalc` unless the notice states all four benefit fields. California's benefit chart, Minnesota's compensation-rate PDF, North Carolina's maximum-rate table, Texas's maximum-and-minimum table, and Oregon Bulletin 111 were fetched. Minnesota's notice states a 2026 maximum of $1,594.08 and North Carolina's states $1,446. Iowa, Kentucky, Michigan, New Jersey, New York, Pennsylvania, South Carolina, and Wisconsin notices each state a 2026 weekly maximum, and Iowa and Kentucky also state a 2026 weekly minimum. Those stated numbers replaced the ClaimCalc values. California, Oregon, and Texas notices do not state one current weekly maximum, so those ClaimCalc numbers stayed and the fields remain `unchecked`. The other states still point at the agency homepage.

# Jurisdiction list

Fifty states and the District of Columbia. Territories are out of this pass. North Dakota, Ohio, Washington, and Wyoming are marked as exclusive state funds. Every other jurisdiction is marked as a private-carrier, self-insurance, or competitive-state-fund market.

Agency name, address, phone, and URL are the DOL directory entry retrieved on 2026-10-28. That directory can lag a rename or a move. Iowa's directory name is Iowa Workforce Development, and the URL DOL published is on dial.iowa.gov. Oklahoma's directory name is Workers' Compensation Court, and the URL DOL published is cec.ok.gov.

# Freshness

Concepts are `draft` until a person checks them against the live official page. `stale_after` is 2027-04-01, ahead of the usual spring fee-schedule revision. A null amount stays null until a new source is attached. Filling it from memory, or from the NCCI bulletin, is outside this method.

[^okf]: Open Knowledge Format v0.2
[^dol-directory]: State Workers' Compensation Officials, U.S. Department of Labor
[^ncci-asb-terms]: NCCI Annual Statistical Bulletin, 2025 edition, terms of use
[^claimcalc]: ClaimCalc workers' compensation settlement chart
