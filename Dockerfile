FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /otus_homework_blog

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ADD . /otus_homework_blog

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "my_blog:app", "--host", "0.0.0.0", "--port", "8000"]