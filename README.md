# projects-presenter-api

Software Engineer Exercise

## Table of Contents

- [About This Project](#about-this-project)
  - [Motivation](#motivation)
  - [Project structure](#project-structure)
- [Project Documentation](#project-documentation)
  - [Prerequisites](#prerequisites)
  - [Local Deployment](#local-deployment)
  - [TODO](#todo)

## About this project

### Motivation

This project is a simple REST API designed to manage a software portfolio. It allows users to track projects and their 
technology stacks (e.g., Python, Flask, PostgreSQL).

Features:
- CRUD for projects and their associated technologies.
- Automatic validation of incoming data using Pydantic.
- Prevents duplicate technologies.
- Includes Swagger/OpenAPI documentation.
- Run in Docker containers.

### Project structure

```text
.
├── docker/                         # Container configuration
│   ├── Dockerfile
│   └── entrypoint.sh
├── seed/
│   └── projects.json               # Initial dataset
├── src/
│   ├── application/                # [Layer] Business Logic & Use Cases
│   │   ├── interfaces.py           # Application service interface
│   │   └── services.py             # Service classes implementation
│   ├── commands/                   # CLI commands implementation
│   │   └── database.py
│   ├── core/                       # [Layer] Domain Models
│   │   ├── dto.py                  # Data Transfer Objects
│   │   ├── entities.py             # Pure domain entities
│   │   └── exceptions.py           # Custom domain exceptions
│   ├── infrastructure/             # [Layer] Adapters & Drivers
│   │   └── db/
│   │       └── postgres/
│   │           ├── migrations/     # Alembic migrations location
│   │           ├── models.py       # SQLAlchemy ORM models
│   │           ├── repositories.py # Repository implementation for Postgres
│   │           └── session.py      # Session management
│   ├── presentation/               # [Layer] API
│   │   └── api/
│   │       ├── endpoints.py        # API endpoints implementation for CRUD
│   │       ├── exception_handlers.py # Error mapping
│   │       ├── main.py             # App factory & initialization
│   │       ├── schemas.py          # Pydantic schemas for API requests and responses
│   │       └── swagger.py          # Spectree config for Swagger
│   ├── cli.py                      # CLI entry point
│   ├── log.py                      # Logging configuration
│   └── settings.py
├── alembic.ini                     # Alembic configuration
├── docker-compose.yaml
├── Makefile
└── requirements.txt
```

### Project documentation

#### Prerequisites

`docker` and `docker compose` should be installed.

#### Local Deployment

1. Run:
```bash
make build
```
2. Run:
```bash
cp .env.example .env
```
3. Set API tokens in `.env` file.
4. Run (default `ENVIRONMENT=dev`):
```bash
make up
```
5. Load seed into `Postgres`:
```bash
make load-seed
```
5. Go to [api docs link](http://localhost:8000/docs/swagger/).

#### TODO:
 - Add tests.
 - Add version validation.
 - Make tech names case-insensitive.
