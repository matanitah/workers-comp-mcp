"""Chat dashboard that drives the MCP server with a local Ollama model."""

from __future__ import annotations

import asyncio
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import server

OLLAMA_URL = "http://127.0.0.1:11434"
MODEL = "gemma4"
MODEL_LIMIT = 8000
DISPLAY_LIMIT = 12000
TOOL_ROUNDS = 4

SYSTEM = (
    "You test a workers' compensation MCP server by calling its tools. "
    "Use a tool for every fact about a state. Do not invent benefit amounts, "
    "settlements, or statute text. A postal code or a state name both work. "
    "When a tool result is truncated, say so and quote only the part that "
    "answers the question. If a tool returns an error, report that error."
)


def clip(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    omitted = len(text) - limit
    return f"{text[:limit]}\n\n[truncated, {omitted} characters omitted]"


def ollama_models(base_url: str = OLLAMA_URL) -> list[str]:
    request = Request(base_url.rstrip("/") + "/api/tags")
    with urlopen(request, timeout=3) as response:
        payload = json.loads(response.read().decode())
    return [item.get("name", "") for item in payload.get("models", [])]


def ollama_tools(mcp_tools: list[dict]) -> list[dict]:
    tools = []
    for tool in mcp_tools:
        parameters = tool.get("parameters") or {"type": "object", "properties": {}}
        parameters = json.loads(json.dumps(parameters))
        tools.append(
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool.get("description") or "",
                    "parameters": parameters,
                },
            }
        )
    return tools


async def _using_client(callback):
    from fastmcp import Client

    async with Client(server.mcp, timeout=180) as client:
        return await callback(client)


def list_mcp_tools() -> list[dict]:
    async def load(client):
        found = []
        for tool in await client.list_tools():
            schema = tool.input_schema
            if hasattr(schema, "model_dump"):
                schema = schema.model_dump(exclude_none=True)
            found.append(
                {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": schema,
                }
            )
        return found

    return asyncio.run(_using_client(load))


def call_mcp_tool(name: str, arguments: dict | None) -> tuple[str, bool]:
    cleaned = {key: value for key, value in (arguments or {}).items() if value is not None}

    async def run(client):
        return await client.call_tool(name, cleaned, raise_on_error=False)

    try:
        result = asyncio.run(_using_client(run))
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}", True
    if result.data is not None:
        text = json.dumps(result.data, indent=2, ensure_ascii=False, default=str)
    else:
        text = "\n".join(getattr(block, "text", str(block)) for block in result.content)
    if result.is_error:
        return f"Tool error:\n{text}", True
    return text, False


def _arguments(raw) -> dict:
    if raw is None:
        return {}
    if isinstance(raw, str):
        raw = json.loads(raw) if raw.strip() else {}
    if not isinstance(raw, dict):
        raise TypeError(f"Tool arguments must be an object, got {type(raw).__name__}")
    return raw


def stream_chat(base_url: str, model: str, messages: list[dict], tools: list[dict]):
    """Yield dicts with content, thinking, and any complete tool calls in that chunk."""
    body = {
        "model": model,
        "messages": messages,
        "tools": tools,
        "stream": True,
        "options": {"temperature": 0.1},
    }
    request = Request(
        base_url.rstrip("/") + "/api/chat",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        response = urlopen(request, timeout=600)
    except HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(f"Ollama returned HTTP {exc.code}: {detail[:500]}") from exc
    except URLError as exc:
        raise RuntimeError(f"Cannot reach Ollama at {base_url}: {exc.reason}") from exc
    with response:
        for raw in response:
            line = raw.decode().strip()
            if not line:
                continue
            event = json.loads(line)
            if event.get("error"):
                raise RuntimeError(event["error"])
            message = event.get("message") or {}
            yield {
                "content": message.get("content") or "",
                "thinking": message.get("thinking") or "",
                "tool_calls": message.get("tool_calls") or [],
            }
            if event.get("done"):
                break


def run_turn(base_url: str, model: str, history: list[dict], mcp_tools: list[dict], prompt: str):
    """Talk to Ollama, call MCP tools it requests, and return the assistant turn."""
    tools = ollama_tools(mcp_tools)
    messages = [{"role": "system", "content": SYSTEM}]
    for item in history:
        messages.append({"role": item["role"], "content": item["content"]})
    messages.append({"role": "user", "content": prompt})
    answer = []
    thinking = []
    used = []
    for _ in range(TOOL_ROUNDS):
        tool_calls = []
        for chunk in stream_chat(base_url, model, messages, tools):
            if chunk["content"]:
                answer.append(chunk["content"])
                yield {"type": "token", "text": chunk["content"]}
            if chunk["thinking"]:
                thinking.append(chunk["thinking"])
                yield {"type": "thinking", "text": chunk["thinking"]}
            tool_calls.extend(chunk["tool_calls"])
        if not tool_calls:
            break
        messages.append(
            {
                "role": "assistant",
                "content": "".join(answer),
                "tool_calls": tool_calls,
            }
        )
        for call in tool_calls:
            function = call.get("function") or {}
            name = function.get("name") or ""
            try:
                arguments = _arguments(function.get("arguments"))
            except (TypeError, json.JSONDecodeError) as exc:
                text, is_error = f"Could not read tool arguments: {exc}", True
                arguments = {}
            else:
                known = {tool["name"] for tool in mcp_tools}
                if name not in known:
                    text, is_error = f"Unknown tool {name!r}.", True
                else:
                    yield {"type": "tool_start", "name": name, "arguments": arguments}
                    text, is_error = call_mcp_tool(name, arguments)
            preview = clip(text, DISPLAY_LIMIT)
            used.append(
                {
                    "name": name,
                    "arguments": arguments,
                    "preview": preview,
                    "is_error": is_error,
                }
            )
            yield {"type": "tool_result", "name": name, "preview": preview, "is_error": is_error}
            messages.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "content": clip(text, MODEL_LIMIT),
                }
            )
        answer = []
    final = "".join(answer).strip()
    if not final and used:
        final = "The tools returned. Their results are shown with this reply."
    yield {
        "type": "done",
        "content": final,
        "thinking": "".join(thinking).strip(),
        "tools": used,
    }


def main() -> None:
    import streamlit as st

    st.set_page_config(page_title="Workers' compensation MCP", layout="wide")
    st.title("Workers' compensation MCP")
    st.caption("Chat with local Ollama model gemma4. The model calls the MCP server's tools.")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "mcp_tools" not in st.session_state:
        try:
            st.session_state.mcp_tools = list_mcp_tools()
            st.session_state.mcp_error = ""
        except Exception as exc:
            st.session_state.mcp_tools = []
            st.session_state.mcp_error = f"{type(exc).__name__}: {exc}"

    with st.sidebar:
        st.header("Ollama")
        base_url = st.text_input("Server", OLLAMA_URL)
        model = st.text_input("Model", MODEL)
        try:
            names = ollama_models(base_url)
        except Exception as exc:
            st.error(f"Ollama is not reachable. {exc}")
            names = []
        else:
            ready = any(name == model or name.startswith(model + ":") for name in names)
            if ready:
                st.success(f"{model} is installed.")
            else:
                st.warning(f"{model} is not in `ollama list`.")
        st.header("MCP tools")
        if st.session_state.mcp_error:
            st.error(st.session_state.mcp_error)
        for tool in st.session_state.mcp_tools:
            st.markdown(f"**{tool['name']}**")
            st.caption((tool["description"] or "").split("\n", 1)[0])
        if st.button("Clear chat"):
            st.session_state.messages = []
            st.rerun()

    prompts = {
        "California maximum": "What is California's maximum weekly workers' compensation benefit? Use the reimbursement tool.",
        "Section-only states": "Which jurisdictions have regulation coverage of section? Use list_jurisdictions.",
        "Ohio statute section": "Fetch Ohio regulations and return the passage for section 4123.56.",
    }
    chosen = st.columns(len(prompts))
    pending = st.session_state.pop("pending", None)
    for column, (label, text) in zip(chosen, prompts.items()):
        with column:
            if st.button(label, use_container_width=True):
                pending = text

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message.get("thinking"):
                with st.expander("Model thinking"):
                    st.text(message["thinking"])
            for tool in message.get("tools") or []:
                title = f"Tool {tool['name']}" + (" failed" if tool["is_error"] else "")
                with st.expander(title):
                    st.code(json.dumps(tool["arguments"], indent=2), language="json")
                    st.text(tool["preview"])
            st.markdown(message["content"])

    typed = st.chat_input("Ask about a state's benefits or statute")
    prompt = pending or typed
    if not prompt:
        return
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        thinking_box = st.empty()
        tool_box = st.container()
        reply = st.empty()
        shown = ""
        thinking_shown = ""
        final = None
        try:
            for event in run_turn(
                base_url,
                model,
                st.session_state.messages[:-1],
                st.session_state.mcp_tools,
                prompt,
            ):
                if event["type"] == "token":
                    shown += event["text"]
                    reply.markdown(shown)
                elif event["type"] == "thinking" and event["text"]:
                    thinking_shown += event["text"]
                    with thinking_box.container():
                        with st.expander("Model thinking"):
                            st.text(clip(thinking_shown, 4000))
                elif event["type"] == "tool_result":
                    title = f"Tool {event['name']}" + (" failed" if event["is_error"] else "")
                    with tool_box.expander(title, expanded=True):
                        st.text(event["preview"])
                elif event["type"] == "done":
                    final = event
        except Exception as exc:
            final = {
                "content": f"The chat stopped: {exc}",
                "thinking": thinking_shown.strip(),
                "tools": [],
            }
            reply.markdown(final["content"])
        if final is None:
            final = {"content": shown.strip(), "thinking": thinking_shown.strip(), "tools": []}
        if final["content"]:
            reply.markdown(final["content"])
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": final["content"],
                "thinking": final.get("thinking") or "",
                "tools": final.get("tools") or [],
            }
        )


if __name__ == "__main__":
    main()
