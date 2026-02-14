
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
app/
main.py
core/
config.py
database.py
routers/
health.py
catalog.py
services/
catalog.py
schemas/
category.py
item.py

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

All endpoints are prefixed with:

```

/api

```

### Health

```

GET /api/health

```

Returns service status.

---

### Categories

```

GET /api/categories
GET /api/categories/{category_id}
GET /api/categories/{category_id}/items

```

---

### Items

```

GET /api/items
GET /api/items/{item_id}
GET /api/items/{item_id}/categories

````

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
````

---

## Running the Service

Start using Docker profile:

```bash
docker compose --profile app1 up -d
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



