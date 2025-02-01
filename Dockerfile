FROM ghcr.io/astral-sh/uv:alpine

ADD . /app

WORKDIR /app

RUN uv sync --frozen

EXPOSE 3000

CMD ["juiceinviter"]