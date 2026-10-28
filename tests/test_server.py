import asyncio

from server import mcp


def test_server_exposes_the_four_tools():
    tools = asyncio.run(mcp.list_tools())
    names = sorted(tool.name for tool in tools)
    assert names == [
        "get_jurisdiction",
        "get_regulations",
        "get_reimbursement",
        "list_jurisdictions",
    ]


def test_list_jurisdictions_reports_coverage_and_retrieval():
    from server import list_jurisdictions

    rows = {row["postal"]: row for row in list_jurisdictions()}
    assert rows["FL"]["regulation_coverage"] == "act"
    assert rows["FL"]["regulation_retrieval"] == "live"
    assert rows["IA"]["regulation_coverage"] == "act"
    assert rows["AL"]["regulation_coverage"] == "section"
    assert rows["AL"]["regulation_retrieval"] == "stored"
    assert rows["AR"]["regulation_coverage"] == "rules"
    assert rows["ID"]["regulation_coverage"] == "chapter"
    for postal in ("DC", "DE", "IN", "VT", "WA", "WV"):
        assert rows[postal]["regulation_coverage"] == "act"
        assert rows[postal]["regulation_retrieval"] == "live"
