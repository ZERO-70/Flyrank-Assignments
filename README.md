# FlyRank Backend Track - Week 1 Assignment A3: Containerize your stack

This project runs the task CRUD API against a real PostgreSQL database, with the entire
stack (app + database) started by a single command via Docker Compose. This is the third
storage swap in this repo: in-memory (A1) -> SQLite file (A2) -> containerized Postgres (A3,
this one). The API endpoints and their behaviour are unchanged across all three.

## Running the project

You need Docker Desktop (or Podman) installed. From the project root:

```bash
cp .env.example .env
docker compose up
```

That's it — no manual database setup. `docker compose up` builds the API image, starts a
Postgres container, creates the `tasks` table if it doesn't exist, and seeds three example
tasks the first time the table is empty. The API is then available at `http://localhost:8000`.

To stop everything: `docker compose down` (your data stays put — it lives in the
`taskdata` Docker volume, not inside the container).

## Environment variables

Copy `.env.example` to `.env` and adjust if needed. The only variable required is:

| Variable | Meaning | Example |
|---|---|---|
| `DATABASE_URL` | Postgres connection string the app uses | `postgres://postgres:dev@localhost:5432/tasks` |

`.env` is git-ignored — the real value never gets committed. `.env.example` holds the same
key with a placeholder/dev value so anyone cloning the repo knows what to set.

Note: inside `compose.yaml`, the `api` service is given its own `DATABASE_URL` that points
at host `db` (the Postgres service name), not `localhost` — containers on the same Compose
network reach each other by service name.

## Endpoints

| Method | Path | Body | Success | Errors |
|---|---|---|---|---|
| GET | `/tasks` | — | `200` + array of tasks | — |
| GET | `/tasks/{id}` | — | `200` + task | `404` if id doesn't exist |
| POST | `/tasks` | `{"title": string}` | `201` + created task | `400` if title is empty |
| PUT | `/tasks/{id}` | `{"title": string, "done": bool}` | `200` + updated task | `400` empty title, `404` unknown id |
| DELETE | `/tasks/{id}` | — | `204` no content | `404` if id doesn't exist |

Example:

```bash
$ curl -i http://localhost:8000/tasks
HTTP/1.1 200 OK
content-type: application/json

[{"id":1,"title":"Learn Postgres","done":false},{"id":2,"title":"Write API endpoints","done":true},{"id":3,"title":"Submit Week 1 Assignment","done":false}]
```

## Running Postgres standalone (Stage 0, without Compose)

```bash
docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -p 5432:5432 -v taskdata:/var/lib/postgresql/data -d postgres
```

The `PGDATA` variable is a compatibility fix for Postgres 18+ images: a brand-new Docker
named volume gets a `lost+found` directory from the underlying filesystem, which the
Postgres 18 entrypoint mistakes for pre-existing data in the old (pre-18) layout and refuses
to start against. Pointing `PGDATA` at a subdirectory of the mount avoids the conflict. The
same fix is applied to the `db` service in `compose.yaml`.

## Database screenshot

![tasks table in psql](docs/db-screenshot.png)

## Storage evolution

| Assignment | Where tasks live | What runs it |
|---|---|---|
| A1 | a list in memory | the program itself |
| A2 | a `tasks.db` file | disk (SQLite) |
| A3 (this) | rows in Postgres | a container — a real database server |

The API on top never changed across any of these three swaps — only the small module that
talks to the database (`get_db_connection`, `init_db`, and the SQL in each route) did.
