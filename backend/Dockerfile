FROM alpine

RUN apk add --no-cache\
    python3 py3-uv ffmpeg

WORKDIR /app

EXPOSE 8080

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY src/ ./src/

CMD ["uv", "run", "src/main.py"]
