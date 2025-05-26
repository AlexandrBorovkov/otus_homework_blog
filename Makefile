install:
	uv sync

start:
	uv run my_blog

lint:
	uv run ruff check