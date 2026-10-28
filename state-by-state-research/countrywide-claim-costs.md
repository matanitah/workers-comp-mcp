---
type: Metric
title: Countrywide claim costs
description: National workers' compensation claim-cost highlights for 2023-2024. They are not a state reimbursement rate and they are not a complete injury table.
tags: [workers-compensation, reimbursement, countrywide]
status: draft
stale_after: "2027-04-01T00:00:00Z"
generated: { by: cursor-agent/grok-4.7, at: "2026-10-28T15:00:00Z" }
sources:
  - id: nsc-injury-facts
    resource: https://injuryfacts.nsc.org/work/costs/workers-compensation-costs/
    title: Workers' Compensation Costs, NSC Injury Facts
    author: process:national-safety-council
---

# Scope

These figures are countrywide. They do not belong on a state reimbursement object. The page attributes them to NCCI's Workers Compensation Statistical Plan, valued at the latest report available to NCCI as of 2026-10-15, for accidents in 2023 and 2024.[^nsc-injury-facts]

The page's prose states an all-claims average and then the lost-time categories that sit above that average, by cause, nature, and part of body. Categories at or below the average are on the page's charts and are not copied here, because this pass did not read a complete data table. A direct refetch of the HTML on 2026-10-28 returned HTTP 403, so the amounts below are the figures that retrieval had already quoted from the page. Re-check the page before treating them as current.

State-level NCCI exhibits are excluded. See [methodology](/methodology).

# Figures

The figures are in [countrywide claim costs](/reimbursement/countrywide.json).

[^nsc-injury-facts]: Workers' Compensation Costs, NSC Injury Facts
