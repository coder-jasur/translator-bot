FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY pyproject.toml /app/
COPY uv.lock /app/
COPY . /app/

RUN cat /app/pyproject.toml

RUN uv pip install -r uv.lock --system

CMD ["python", "-m", "src.app.main"]