FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY pyproject.toml /app/
COPY . /app/

RUN cat /app/pyproject.toml

RUN uv pip compile /app/pyproject.toml > /app/requirement.txt

RUN uv pip install -r /app/requirement.txt --system

CMD ["python", "-m", "src.app.main"]