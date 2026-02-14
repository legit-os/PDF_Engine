FROM python:3.12-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN uv venv

RUN uv pip install --no-cache-dir paddlepaddle==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/

RUN uv pip install --no-cache-dir paddleocr

RUN uv pip install --no-cache-dir pillow



FROM python:3.12-slim-bookworm


WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p io/input_path
RUN mkdir -p io/output_path

COPY --from=builder /app/.venv /app/.venv

COPY main.py ./

ENV PATH="/app/.venv/bin:$PATH"


CMD ["python", "main.py"]


