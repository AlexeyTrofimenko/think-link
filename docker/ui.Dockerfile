FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.8.15 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --group ui

CMD ["uv", "run", "streamlit", "run", "ui/ui_main.py", "--server.address", "0.0.0.0"]
