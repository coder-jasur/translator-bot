FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY . /app
RUN uv pip compile pyproject.toml > requirement.txt
RUN uv pip install -r requirement.txt --system

CMD ["python", "-m", "src.app.main"]