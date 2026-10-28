import json

import dashboard


def test_tool_schema_is_an_ollama_function():
    tools = dashboard.ollama_tools(
        [
            {
                "name": "get_reimbursement",
                "description": "Return the stored reimbursement JSON.",
                "parameters": {
                    "type": "object",
                    "properties": {"state": {"type": "string"}},
                    "required": ["state"],
                },
            }
        ]
    )
    assert tools[0]["type"] == "function"
    assert tools[0]["function"]["name"] == "get_reimbursement"
    assert tools[0]["function"]["parameters"]["required"] == ["state"]
    json.dumps(tools)


def test_long_tool_text_is_clipped():
    text = "a" * (dashboard.MODEL_LIMIT + 25)
    clipped = dashboard.clip(text, dashboard.MODEL_LIMIT)
    assert clipped.startswith("a" * dashboard.MODEL_LIMIT)
    assert "truncated" in clipped
    assert "truncated, 25 characters omitted" in clipped


def test_mcp_client_lists_the_four_tools_and_reads_california():
    names = [tool["name"] for tool in dashboard.list_mcp_tools()]
    assert names == [
        "list_jurisdictions",
        "get_jurisdiction",
        "get_reimbursement",
        "get_regulations",
    ]
    text, is_error = dashboard.call_mcp_tool("get_jurisdiction", {"state": "CA"})
    assert not is_error
    assert '"postal": "CA"' in text
