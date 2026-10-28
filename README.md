# Workers' compensation MCP

A [FastMCP](https://gofastmcp.com/) server over the OKF wiki in `state-by-state-research`. It returns each jurisdiction's reimbursement JSON and, when a publisher URL is cataloged, the text of that official page.

## Tools

- `list_jurisdictions` lists the 50 states and the District of Columbia. `regulation_coverage` is `act`, `chapter`, `section`, or `rules`. `regulation_retrieval` is `live` or `stored`.
- `get_jurisdiction` returns the agency, the primary-law citation, and the regulation catalog. Each catalog entry includes `coverage` and `retrieval`.
- `get_reimbursement` returns the stored JSON. `benefits` holds the weekly maximum, weekly minimum, wage-replacement rate, and temporary-total week cap. `claimcalc` holds ClaimCalc's injury-level settlement. `figures_from` becomes `official` only when a rate notice states all four benefit fields.
- `get_regulations` fetches one cataloged official URL and returns its text. The default document is the statute when rules are also cataloged. `section` returns the passage that starts at a citation. Some jurisdictions return text saved from the official page when that host blocks the server. A failed live fetch returns `fetch_error`. A state with no cataloged URL returns `status: uncatalogued`.

`benefits` holds weekly benefit limits from [ClaimCalc](https://claimcalc.app/workers-comp/settlement-chart). A field is replaced only when an official rate notice states a different number, and `figures_from` becomes `official` only when that notice states all four benefit fields. `claimcalc` holds that source's injury-level settlement amount.

## Run locally

```bash
uv sync
uv run fastmcp run server.py:mcp
```

That uses stdio. For HTTP, the endpoint is `http://localhost:8000/mcp`:

```bash
uv run fastmcp run server.py:mcp --transport http --host 0.0.0.0 --port 8000
```

## Docker

```bash
docker build -t workers-comp-mcp .
docker run --rm -p 8000:8000 workers-comp-mcp
```

## Chat dashboard

A Streamlit chat drives the MCP server with the local Ollama model `gemma4`. The model calls `list_jurisdictions`, `get_jurisdiction`, `get_reimbursement`, and `get_regulations` through the FastMCP client.

```bash
uv sync --group dashboard
uv run --group dashboard streamlit run dashboard.py
```

Ollama must already be running and `gemma4` must appear in `ollama list`. The dashboard is at http://localhost:8501.

## Tests

```bash
uv run pytest
```
