FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app


RUN apt-get update && apt-get install -y gcc libpq-dev python3-dev

COPY pyproject.toml uv.lock /app/

RUN uv sync --frozen --system --no-install-project
COPY . .

CMD ["python", "-m", "src.app.main"]