FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apt-get update --allow-insecure-repositories && \
    apt-get install -y \
    gcc git make && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

COPY . .

FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PORT=5400

RUN apt-get update --allow-insecure-repositories && \
    apt-get install -y \
    libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY --from=builder /app /app

RUN useradd --create-home sse && \
    chown -R sse:sse /app
USER sse

EXPOSE ${PORT}

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]