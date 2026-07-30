FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /uvx /usr/local/bin/

WORKDIR /app

COPY input.txt /app/input.txt
