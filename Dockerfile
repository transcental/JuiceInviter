FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN uv sync

EXPOSE 3000

CMD ["juiceinviter"]