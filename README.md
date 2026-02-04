# PF2E Kingdom Manager

A free-form kingdom turn tracker for Pathfinder 2E Kingmaker. Players log
activities and GMs configure kingdom state without enforced phase order. The
system models Paizo's kingdom rules as persistent game state rather than an
automated turn engine.

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
