FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY pyproject.toml /app/
COPY . /app/

RUN cat /app/pyproject.toml

RUN uv pip install -r pyproject.toml --system

CMD ["python", "-m", "src.app.main"]