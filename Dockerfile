FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY server.py wiki.py regulations.py claimcalc.py ./
COPY state-by-state-research ./state-by-state-research
EXPOSE 8000
CMD ["uv", "run", "fastmcp", "run", "server.py:mcp", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
