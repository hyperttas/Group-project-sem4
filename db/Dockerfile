FROM mysql:9

WORKDIR /db
COPY ./init-src.sql /docker-entrypoint-initdb.d/

EXPOSE 3306