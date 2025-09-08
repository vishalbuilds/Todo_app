# py-postgres-utils

A collection of Python scripts and utilities to interact with PostgreSQL databases.  
This repository contains reusable code snippets, helper functions, and examples for connecting, querying, and managing PostgreSQL using Python.

---

## Features
- Connect to PostgreSQL using `psycopg2` and `SQLAlchemy`
- Run queries and fetch results
- Insert, update, and delete data
- Handle transactions and errors
- Example scripts for common use cases

---

## Tech Stack
- **Python 3.11+**
- **PostgreSQL 14+**
- **Libraries:** `psycopg2`, `SQLAlchemy`

---

## Getting Started

### Prerequisites
- Install Python (>=3.11)
- Install PostgreSQL (>=14)
- Create a `.env` file with your database credentials:
  ```env
  DB_HOST=localhost
  DB_PORT=5432
  DB_NAME=mydatabase
  DB_USER=myuser
  DB_PASSWORD=mypassword
