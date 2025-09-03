FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY pyproject.toml /app/
COPY uv.lock /app/
COPY . /app/

RUN uv pip install -r uv.lock --system || uv pip install -r pyproject.toml --system

CMD ["python", "-m", "src.app.main"]