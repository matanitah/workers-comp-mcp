"""FastMCP server over the workers' compensation research wiki."""

from __future__ import annotations

from fastmcp import FastMCP

import regulations
import wiki

mcp = FastMCP("Workers' compensation")


@mcp.tool
def list_jurisdictions() -> list[dict]:
    """List the 50 states and the District of Columbia in the research wiki.

    Each row includes the postal code, the jurisdiction name, whether a
    cataloged official regulation URL is on file, whether that document is
    the act, a chapter, a section, or agency rules, whether the text is fetched
    live or read from a saved file, and whether a medical fee schedule object
    is stored.
    """
    rows = []
    for item in wiki.load_jurisdictions():
        primary = regulations.choose_entry(item.regulations, None) if item.regulations else None
        rows.append(
            {
                "postal": item.postal,
                "name": item.name,
                "has_regulation_url": item.has_regulation_url,
                "regulation_coverage": primary.get("coverage") if primary else None,
                "regulation_retrieval": (
                    ("stored" if primary.get("text_file") else "live") if primary else None
                ),
                "regulation_ids": [entry.get("id") for entry in item.regulations],
                "has_fee_schedule": item.has_fee_schedule,
            }
        )
    return rows


@mcp.tool
def get_jurisdiction(state: str) -> dict:
    """Return the agency, primary-law citation, and regulation catalog for a state.

    `state` is a postal code or jurisdiction name, such as CA or California.
    Each catalog entry includes `coverage` (`act`, `chapter`, `section`, or
    `rules`) and `retrieval` (`live` or `stored`).
    """
    item = wiki.resolve_jurisdiction(state)
    regulations_out = []
    for entry in item.regulations:
        row = dict(entry)
        row["retrieval"] = "stored" if entry.get("text_file") else "live"
        regulations_out.append(row)
    return {
        "postal": item.postal,
        "name": item.name,
        "agency": item.agency,
        "primary_law": item.primary_law,
        "regulations": regulations_out,
    }


@mcp.tool
def get_reimbursement(state: str) -> dict:
    """Return the stored reimbursement JSON for a state.

    `benefits` holds the weekly maximum, weekly minimum, wage-replacement rate,
    and temporary-total week cap. `claimcalc` is ClaimCalc's injury-level
    settlement figure. `state` is a postal code or name.
    """
    return wiki.resolve_jurisdiction(state).reimbursement


@mcp.tool
def get_regulations(state: str, source_id: str | None = None, section: str | None = None) -> dict:
    """Fetch one cataloged official regulation and return its text.

    The URL comes from that jurisdiction's catalog. This tool does not accept
    an arbitrary URL and does not summarize the document. When several
    documents are cataloged, the default is `primary-statute`; pass `source_id`
    for another, such as `agency-rules`. A catalog entry that names a saved
    text file returns that file. `section` returns the passage that starts at
    that citation. A failed live fetch returns status `fetch_error`. When no
    official URL is cataloged, the result is status `uncatalogued` with the
    citation and agency link already recorded in the wiki.
    """
    item = wiki.resolve_jurisdiction(state)
    return regulations.regulation_response(item, source_id=source_id, section=section)


if __name__ == "__main__":
    mcp.run()
