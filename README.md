# PF2E Kingdom Manager

A free-form kingdom turn tracker for Pathfinder 2E Kingmaker. Players log
activities and GMs configure kingdom state without enforced phase order. The
system models Paizo's kingdom rules as persistent game state rather than an
automated turn engine.

<p align="center">
  <a href="https://github.com/DavidMiserak/pf2e-kingdom-manager/actions/workflows/test.yml">
    <img src="https://github.com/DavidMiserak/pf2e-kingdom-manager/actions/workflows/test.yml/badge.svg" alt="Tests" />
  </a>
  <a href="https://codecov.io/gh/DavidMiserak/pf2e-kingdom-manager">
    <img src="https://codecov.io/gh/DavidMiserak/pf2e-kingdom-manager/branch/main/graph/badge.svg" alt="codecov" />
  </a>
  <img src="https://img.shields.io/badge/python-3.13+-blue.svg" alt="Python 3.13+" />
  <img src="https://img.shields.io/badge/django-6.0-green.svg" alt="Django 6.0" />
  <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black" />
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit" alt="pre-commit" />
  </a>
</p>

## Features

- Kingdom statistics tracking (ability scores, skills, ruin, unrest, XP/level)
- Leadership role assignment and investment
- Free-form activity logging with optional roll tracking
- Settlement and hex territory management
- Commodity stockpile and Resource Point tracking
- Turn-by-turn state snapshots
- GM and player permission model

## Requirements

- Python 3.13+
- PostgreSQL 14+
- Podman (or Docker)
- Bootstrap 5 (for frontend styling)

## Quick Start

```bash
# Build the container image and start services
make run

# Run database migrations
make migrate
```

The app will be available at `http://localhost:8000`.

## Development

```bash
# Install pre-commit hooks
make pre-commit-setup

# Run tests inside the container
make test

# Run tests locally (uses SQLite)
make test-local

# Generate HTML coverage report
make coverage-html

# View container logs
make logs

# Stop services
make stop
```

## License

<!-- Add license information -->
