# Todo App

Todo App: A modern, full-stack application for managing tasks and to-dos. Supports both local and cloud deployments, with a FastAPI backend, PostgreSQL database, Docker Compose setup, and secure credential management via `.env`.

---

## Features
- FastAPI backend for RESTful API
- PostgreSQL integration via SQLAlchemy & asyncpg
- Alembic migrations for schema management
- Docker Compose for local/cloud deployment
- Centralized credential management with `.env`

---

## Tech Stack
- **Python 3.11+**
- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **asyncpg**
- **PostgreSQL 14+**
- **Docker & Docker Compose**


---

## Getting Started

### 1. Clone the Repository
```sh
git clone https://github.com/vishalbuilds/py-postgres-utils.git
cd py-postgres-utils
```

### 2. Create a `.env` File
Centralize all credentials and configuration in a `.env` file at the project root. Example:

```env
# PostgreSQL configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=tododb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123

```

#### For Cloud Deployment
Set your cloud database credentials in `.env`:
```env
POSTGRES_HOST=your-cloud-host
POSTGRES_PORT=5432
POSTGRES_DB=your-cloud-db
POSTGRES_USER=your-cloud-user
POSTGRES_PASSWORD=your-cloud-password
```

---

## Installation

### Local Development
1. Install Python dependencies:
  ```sh
  pip install -r requirements.txt
  ```
2. (Optional) Set up a virtual environment:
  ```sh
  python -m venv .venv
  .venv\Scripts\activate  # Windows
  source .venv/bin/activate  # Linux/Mac
  ```


### Docker Compose
Set `.env` values and Run the stack locally or in the cloud:

#### Local
```sh
docker-compose -f Dockerfile.postgres up
```

#### Cloud

```sh
docker-compose -f Dockerfile.postgres up
```

---

## Running the Application

---

## Notes
- All credentials and configuration are managed via `.env` for security and portability.
- For cloud deployments, ensure your database is accessible from your server/container.

---

## License
MIT
