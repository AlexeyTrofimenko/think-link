FROM postgres:17

ARG PG_MAJOR=17

ARG PGVECTOR_VERSION=v0.8.1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    ca-certificates \
    postgresql-server-dev-${PG_MAJOR}

RUN git clone --branch ${PGVECTOR_VERSION} https://github.com/pgvector/pgvector.git /tmp/pgvector \
    && make -C /tmp/pgvector \
    && make -C /tmp/pgvector install

RUN apt-get remove -y build-essential git postgresql-server-dev-${PG_MAJOR} \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
