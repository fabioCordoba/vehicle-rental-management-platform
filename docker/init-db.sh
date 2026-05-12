#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    SELECT 'CREATE DATABASE authentication_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'authentication_db')\gexec
    SELECT 'CREATE DATABASE vehicles_db'       WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'vehicles_db')\gexec
    SELECT 'CREATE DATABASE operation_db'      WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'operation_db')\gexec
EOSQL
