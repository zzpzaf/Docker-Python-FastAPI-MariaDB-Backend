
# FastAPI Backend – app1

Please, also refer to the `The Python - FastAPI Backend Project - app1.docx` document into the myDocs folder

## Overview

`app1` is a FastAPI-based REST backend service that provides read-only access to a MariaDB database (`bookstore1`).

The service is part of a Docker Compose multi-service stack and runs under a profile-based configuration.  
It follows a clean layered backend architecture and currently implements GET endpoints using pure SQL (PyMySQL).

---

## Technology Stack

- Python 3.12
- FastAPI
- PyMySQL (pure SQL, no ORM)
- MariaDB 11
- Pydantic v2
- Docker Compose (profile-based setup)

---

## Architecture

The backend follows a layered structure to maintain separation of concerns:

```

Client
↓
Routers (HTTP layer)
↓
Services (SQL / business logic)
↓
Database Connection Layer
↓
MariaDB (bookstore1)

```

### Layer Responsibilities

| Layer | Responsibility |
|--------|----------------|
| `main.py` | Application entry point |
| `routers/` | Defines HTTP endpoints |
| `services/` | Contains SQL queries |
| `core/` | DB connection & configuration |
| `schemas/` | Response validation models |

---

## Project Structure

```
workspace/app1/
.
|-- README.md
`-- app
    |-- __init__.py
    |-- core
    |   |-- __init__.py
    |   |-- config.py
    |   `-- database.py
    |-- main.py
    |-- models
    |   |-- __init__.py
    |   |-- category.py
    |   |-- category_item.py
    |   `-- item.py
    |-- routers
    |   |-- __init__.py
    |   |-- public			<-- indicates exposed/public endpoints
    |   |   |-- __init__.py
    |   |   |-- catalog.py
    |   |   |-- health.py
    |   |   `-- import_books.py
    |   `-- internal			<-- indicates endpoints for internal (‘private’) use
    |       `-- __init__.py
    |-- schemas
    |   |-- __init__.py
    |   |-- category.py
    |   `-- item.py
    `-- services
        |-- __init__.py
        |-- db				<-- indicates services accessing local db
        |   |-- __init__.py
        |   |-- catalog.py
        |   `-- items_sql.py
        `-- external
            |-- __init__.py
            `-- external_books.py	<-- indicates services that access external APIs
```

---

## Database Schema

The service connects to the MariaDB database:

```

bookstore1

```

Tables:

- `categories`
- `items`
- `categoryitems` (junction table for many-to-many relationship)

Primary keys are `INT UNSIGNED AUTO_INCREMENT`.

---

## API Endpoints


# health


GET
/health
Health


GET
/api/health
Health

# catalog


GET
/api/categories
Get Categories


POST
/api/categories
Create Category


GET
/api/categories/{category_id}
Get Category


PUT
/api/categories/{category_id}
Put Category


PATCH
/api/categories/{category_id}
Patch Category


DELETE
/api/categories/{category_id}
Delete Category


GET
/api/items
Get Items


POST
/api/items
Create Item


GET
/api/items/{item_id}
Get Item


PUT
/api/items/{item_id}
Put Item


PATCH
/api/items/{item_id}
Patch Item


DELETE
/api/items/{item_id}
Delete Item


GET
/api/categories/{category_id}/items
Get Items For Category


GET
/api/items/{item_id}/categories
Get Categories For Item

# import


POST
/api/import/book
Import Book



---

## Example Response (Category)

```json
{
  "categoryId": 1,
  "categoryName": "Mountain Bikes",
  "categoryStatusId": 1,
  "categoryCrUUID": "5b8a6c2e-1c3d-4b8e-9a5e-123456789abc",
  "categoryCrTimestamp": "2024-01-10T12:00:00",
  "categoryClientUUID": null
}
```

---
## Day-by-day maintanence

1) Start using Docker profile:
```bash
docker compose --profile app1 up -d
```
2) Rebuild the app1 image (dev target)
```bash
docker compose --profile app1 build --no-cache app1
```
3) Recreate the container (so it uses the new image)
```bash
docker compose --profile app1 up -d --force-recreate app1
```
4) Confirm the package (e.g. tenacity) is installed inside the container
```bash
docker compose --profile app1 exec app1 bash -lc "python -c 'import tenacity; print(tenacity.__version__)'"
```

When we just make changes to our Python code, in most of cases, we just need to restart the container
```bash
docker compose --profile app1 restart app1   
```
or
```bash
docker compose --profile app1 up -d --force-recreate app1
```



Access API:

```
http://localhost:8000/api/categories
```

API documentation:

```
http://localhost:8000/docs
```

---

## Configuration

Environment variables are defined in `.env`:

```
DB_HOST=mariadb
DB_PORT=3306
DB_NAME=bookstore1
DB_USER=appuser
DB_PASSWORD=apppass
```

---

## Design Principles

* Clean layered architecture
* No ORM (pure SQL for transparency)
* Strong response validation via Pydantic
* Docker-ready
* Profile-based multi-service environment
* Easily extensible to full CRUD

---

## Current Status

✔ Database integration complete
✔ Environment configuration resolved
✔ Permissions configured
✔ GET endpoints operational
✔ Response validation implemented

---

## Next Steps

* Implement POST (Create)
* Implement PUT/PATCH (Update)
* Implement DELETE
* Add pagination & filtering
* Add centralized error handling
* Optional migration to SQLAlchemy ORM

---



