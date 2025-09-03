FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY . /app/

RUN uv pip install -r /app/requirements.txt

CMD ["python", "-m", "src.app.main"]