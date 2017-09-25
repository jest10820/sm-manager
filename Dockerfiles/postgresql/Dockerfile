FROM postgres:9.6.5
MAINTAINER jest10820

ARG INIT_DB_DIR=/docker-entrypoint-initdb.d/

ENV POSTGRES_USER user
ENV POSTGRES_PASSWORD 1234

RUN mkdir -p ${INIT_DB_DIR}
COPY ./scripts/* ${INIT_DB_DIR}
RUN chmod +x ${INIT_DB_DIR}*.sh
