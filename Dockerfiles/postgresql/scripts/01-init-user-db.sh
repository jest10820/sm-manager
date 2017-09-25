#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER manager WITH PASSWORD '190689';
    CREATE DATABASE supermanager;
    GRANT ALL PRIVILEGES ON DATABASE supermanager TO manager;
EOSQL
