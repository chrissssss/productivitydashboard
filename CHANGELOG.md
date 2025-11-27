# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-27

### Added
- Creation of a fully automated monitoring stack consisting of PostgreSQL, Python, and Grafana.
- Implementation of a Python service that periodically generates sample data and inserts it into the PostgreSQL database.
- Automatic provisioning of a Grafana data source and a dashboard to visualize the generated data.
- Configuration of the entire stack via `docker-compose.yml` for a single-command start (`docker-compose up`).