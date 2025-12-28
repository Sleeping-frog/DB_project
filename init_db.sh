#!/usr/bin/env bash
set -e

DB_NAME="zoo_db"
DB_USER="postgres"
DB_PASSWORD="1234"
DB_HOST="localhost"

export PGPASSWORD="$DB_PASSWORD"

echo "Dropping database $DB_NAME (if exists)..."
psql -h "$DB_HOST" -U "$DB_USER" -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"

echo "Creating database $DB_NAME..."
psql -h "$DB_HOST" -U "$DB_USER" -d postgres -c "CREATE DATABASE $DB_NAME;"

echo "Creating tables..."
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" <<'EOF'

CREATE TABLE IF NOT EXISTS species (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    family TEXT NOT NULL,
    habitat TEXT NOT NULL,
    lifespan_years INTEGER CHECK (lifespan_years > 0)
);

CREATE TABLE IF NOT EXISTS enclosure (
    id SERIAL PRIMARY KEY,
    room_number INTEGER NOT NULL UNIQUE,
    complex_name TEXT NOT NULL,
    has_pond BOOLEAN NOT NULL DEFAULT FALSE,
    area NUMERIC(10,2) CHECK (area > 0)
);

CREATE TABLE IF NOT EXISTS placement (
    id SERIAL PRIMARY KEY,
    species_id INTEGER NOT NULL REFERENCES species(id) ON DELETE CASCADE,
    enclosure_id INTEGER NOT NULL REFERENCES enclosure(id) ON DELETE CASCADE,
    animals_count INTEGER NOT NULL CHECK (animals_count >= 0),
    CONSTRAINT unique_species_enclosure UNIQUE (species_id, enclosure_id)
);

EOF

echo "Done ✅"
