
# Docker-Python-FastAPI-MariaDB-Backend
## A Docker stack that allows you to start working with a FastAPI-based, Python Backend apps
#### 260213-14


## Repository purpose

This repository provides a Docker Compose environment for running multiple FastAPI projects (`app1`, `app2`, `app3`, …) that share a MariaDB database and optional phpMyAdmin UI. It supports dev and prod modes via profiles, keeps DB data persistent via a named volume, and uses an Ubuntu-based FastAPI image with a Python venv and curated OS tools.

---

## Top-level folder structure and what each part is for

```
fastapi-mariadb-env/
├─ docker-compose.yml
├─ Dockerfile.ubuntu
├─ .env
├─ .gitignore
├─ README.md
├─ requirements/
├─ workspace/
├─ shared/
├─ db/
└─ myDocs/
```

### `docker-compose.yml`

Defines the full stack:

* Infrastructure: `mariadb`, `phpmyadmin`
* FastAPI apps in dev: `app1`, `app2`, `app3` (profile-scoped)
* FastAPI apps in prod: `app1-prod`, `app2-prod`, `app3-prod` (profile-scoped)

### `Dockerfile.ubuntu`

Build definition for the FastAPI containers (Ubuntu 24.04 base) including:

* OS tools (wget, curl, lsof, net-tools, git, etc.)
* Python 3 + venv to avoid Ubuntu 24.04 PEP 668 “externally managed environment” issue
* Dependency installation via `requirements/` with BuildKit caching
* Separate targets for `dev-runtime` and `prod-runtime`

### `.env`

Central place for configuration and secrets:

* `COMPOSE_PROJECT_NAME` (namespaces container/network/volume names)
* Ports for each app
* MariaDB credentials and ports
* Optional prod concurrency variable

### `.gitignore`

Keeps secrets and caches out of git (especially `.env`, python caches, IDE folders).

### `README.md`

Human documentation for setup, usage, build/run/stop commands.

---

## Project subfolders


### `requirements/`

Dependency strategy split into files:

* `base.txt` – runtime dependencies shared by dev/prod
* `dev.txt` – dev + test tooling layered on top of base
* `prod.txt` – production runtime additions layered on top of base

These files control what gets installed into the container venv depending on the Docker build target.

---

### `workspace/`

This is where the actual FastAPI project(s) live.

```
workspace/
  app1/
    app/
      __init__.py
      main.py
    tests/
  app2/
  app3/
```

Each `appX` is a separate FastAPI project folder.
Inside each project, the `app/` folder is a Python package so that the Compose uvicorn command works:

* `uvicorn app.main:app`

Meaning:

* first `app` = package folder `app/`
* `main` = `main.py`
* second `app` = `app = FastAPI()` variable in `main.py`

---

### `shared/`

A folder mounted into **all containers** at `/shared`.

Use it for:

* quick file exchange between host ↔ containers
* temporary exports/imports
* logs or generated artifacts you want to inspect easily from the host

It is bind-mounted, so changes are visible instantly on the host.

---

### `db/`  (MariaDB init/update SQL scripts)

This folder is intended for SQL scripts that can be executed by MariaDB.

Recommended structure:

```
db/
  init/
    001_schema.sql
    002_seed.sql
  migrations/
    2026-02-13_add_table_x.sql
```

#### How the `db/init/` is commonly used with MariaDB in Docker

MariaDB’s official Docker image supports automatic execution of `.sql` scripts placed in db/init/, such as:
  *  001_schema.sql
  *  002_seed.sql

The 1st is used to define database schemas, tables, etc.,     
The 2nd inserts initial (demo) data into tables

So, the `db/init/` → is used for placing first-time initialization scripts. MariaDB will run those scripts **only the first time** the database volume is created (i.e., on initial initialization).

In order to fire the initial execution process of the scripts, the following line should be included in the mariadb volumes section, in docker-compose.yml under mariadb: volumes:  

```
    - ./db/init:/docker-entrypoint-initdb.d:ro
```

* Later, schema changes are handled by a migration tool (e.g. Alembic) or by manually running scripts (e.g., via phpMyAdmin)



---

### `myDocs/`

Local project documentation, notes, diagrams, or internal references.

Typical usage:

* architecture notes
* decisions log
* snippets / runbooks
* environment notes

It does not affect the Docker stack directly; it’s informational for humans.

---

## Stack behavior and profiles

* `mariadb` and `phpmyadmin` have **no profiles** → considered default infrastructure services
* `app1/app2/app3` are dev services behind profiles → start only when profile enabled
* `app1-prod/app2-prod/app3-prod` are prod services behind profiles

Profiles are expected to require explicit activation (normal behavior everywhere).

---

## Start/stop/build usage (summary)

### Build the full stack, all dev apps at once

```bash
docker compose --profile app1 --profile app2 --profile app3 build
```

<br>

### Create all containers and start the full stack, all dev apps at once


```bash
docker compose --profile app1 --profile app2 --profile app3 up -d
```

Or


### Create and start infrastructure containers, only 

```bash
docker compose up -d mariadb phpmyadmin
```

### Start only app3 dev container

```bash
docker compose --profile app3 up -d app3
```  

<br>


### Stop all containers (keep DB data persistent)

```bash
docker compose --profile app1 --profile app2 --profile app3 stop
```

### Start all containers at aonce

```bash
docker compose --profile app1 --profile app2 --profile app3 start
```

<br>


### Remove containers (keep DB data)

```bash
 docker compose --profile app1 --profile app2 --profile app3 down 
```


### Remove all containers <u>AND</u> DB data

```bash
 docker compose --profile app1 --profile app2 --profile app3 down --volumes
```


---

## Where to check in browser

* phpMyAdmin: `http://localhost:${PHPMYADMIN_PORT}`, e.g.: http://localhost:8080/

<br>

* FastAPI Entry points:

  * app1 docs: `http://localhost:${FASTAPI_PORT_APP1}/`, e.g.:  http://localhost:8000/
  * app2 docs: `http://localhost:${FASTAPI_PORT_APP2}/`, e.g.:  http://localhost:8001/
  * app3 docs: `http://localhost:${FASTAPI_PORT_APP3}/`, e.g.:  http://localhost:8002/

<br>

* FastAPI testing initial 'health' route:

  * app1 docs: `http://localhost:${FASTAPI_PORT_APP1}/docs`, e.g.:  http://localhost:8000/health
  * app2 docs: `http://localhost:${FASTAPI_PORT_APP2}/docs`, e.g.:  http://localhost:8001/health
  * app3 docs: `http://localhost:${FASTAPI_PORT_APP3}/docs`, e.g.:  http://localhost:8002/health

<br>

* FastAPI Swagger auto-generated UI (per app)::

  * app1 docs: `http://localhost:${FASTAPI_PORT_APP1}/docs`, e.g.:  http://localhost:8000/docs
  * app2 docs: `http://localhost:${FASTAPI_PORT_APP2}/docs`, e.g.:  http://localhost:8001/docs
  * app3 docs: `http://localhost:${FASTAPI_PORT_APP3}/docs`, e.g.:  http://localhost:8002/docs