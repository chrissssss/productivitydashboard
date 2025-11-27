# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-11-27

### Changed
- Re-architected the data pipeline from a polling model (Postgres/InfluxDB) to a push model using Grafana Live for true real-time updates.
- The middleware now pushes data directly to Grafana via a WebSocket, enabling live dashboard updates without a time-series database.

### Removed
- Removed the InfluxDB service and its related configurations from the `docker-compose.yml` file to simplify the technology stack.
- Eliminated the data transfer mechanism between PostgreSQL and InfluxDB, as it is no longer needed.

## [1.0.0] - 2025-11-27

### Added
- Creation of a fully automated monitoring stack consisting of PostgreSQL, Python, and Grafana.
- Implementation of a Python service that periodically generates sample data and inserts it into the PostgreSQL database.
- Automatic provisioning of a Grafana data source and a dashboard to visualize the generated data.
- Configuration of the entire stack via `docker-compose.yml` for a single-command start (`docker-compose up`).