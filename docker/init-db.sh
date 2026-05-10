#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE authentication_db;
    CREATE DATABASE vehicles_db;
    CREATE DATABASE operation_db;
EOSQL
