PORT ?= 8000

install:
	uv sync

lint:
	uv run ruff check

start:
	uv run uvicorn my_blog:app --host 0.0.0.0 --port $(PORT) --reload