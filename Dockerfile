FROM ghcr.io/astral-sh/uv:latest

ADD . /app

WORKDIR /app

RUN uv sync --frozen

EXPOSE 3000

CMD ["juiceinviter"]