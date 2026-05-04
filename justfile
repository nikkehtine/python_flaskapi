#!/usr/bin/env -S just --justfile
set windows-shell := ["pwsh", "-NoLogo", "-NoProfileLoadTime", "-Command"]

install:
    uv sync

dev:
    uv run flask --app main run --debug

lint:
    uv run ruff check . --fix

format:
    uv run ruff format .
