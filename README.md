# Crypto Data Engineering Sprint: End-to-End Pipeline

**Developer:** YOUR NAME

---

## Overview

This project implements a production-grade ELT pipeline that extracts live cryptocurrency data from the CoinGecko API, validates it using data contracts, and transforms it into analytics-ready models using modern cloud-native tooling.

## Developer & Stack

- **Developer:** YOUR NAME
- **Stack:** Python, dlt, dbt, MotherDuck, Pydantic, uv

## Configuration & Credentials

To run this pipeline, access to **MotherDuck** must be configured.

### dlt Secrets (Ingestion)

Create the file `.dlt/secrets.toml` in the project root:

```toml
[destination.motherduck.credentials]
database = "crypto_db"
password = "YOUR_MOTHERDUCK_SERVICE_TOKEN"
```

### dbt Profile (Transformation)

Update your local `~/.dbt/profiles.yml`:

```yaml
brahim:
  target: duck
  outputs:
    duck:
      type: duckdb
      path: 'md:crypto_db'
      motherduck_token: "YOUR_MOTHERDUCK_SERVICE_TOKEN"
      threads: 4
```

## Running the Pipeline

Execute the ELT workflow in sequence.

### Step 1: Ingest Raw Data

- Fetches live cryptocurrency data from CoinGecko
- Validates payloads using Pydantic
- Loads raw tables into MotherDuck

```bash
uv run python ingest.py
```

### Step 2: Transform Data

- Builds staging models
- Produces analytics-ready marts

```bash
cd analytics
uv run dbt run
```

## Architecture & Design Decisions

- **Data Contracts (Pydantic):** Enforces schema validation before data reaches the warehouse, preventing silent corruption.
- **Schema Evolution (dlt):** Automatically handles upstream API schema changes and column drift.
- **Cloud-Native Analytics (MotherDuck):** Combines DuckDB performance with cloud scalability.
- **Modern Dependency Management (uv):** Ensures fast, reproducible, and deterministic environments.

## Project Structure

```
.
├── .dlt/
│   └── secrets.toml
├── analytics/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── dbt_project.yml
├── ingest.py
├── models.py
├── pyproject.toml
└── README.md
```

## Summary

This project demonstrates a complete, production-ready ELT pipeline featuring strong data contracts, schema-safe ingestion, cloud-native analytics, and modern Python tooling suitable for real-world data engineering workflows.
