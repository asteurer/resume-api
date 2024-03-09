FROM postgres

VOLUME pgdata

WORKDIR /docker-entrypoint-initdb.d/

COPY ./SQL/main.sql /docker-entrypoint-initdb.d/