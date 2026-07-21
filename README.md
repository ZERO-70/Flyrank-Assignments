# FlyRank Backend Track - Week 3 Assignment A2

This project upgrades our previous in-memory CRUD API to use a real SQLite database. The API endpoints behave exactly the same, but now the data persists and survives server restarts.

## Running the Project

To run this project, you only need one command. Ensure you have `uv` installed, then run:

`uv run uvicorn main:app --reload`

The application requires zero manual setup. When you run the command above, the `tasks.db` database file and the `tasks` table are created automatically. If the table is empty, it will also automatically seed three example tasks.

## Database Storage: Why SQLite?

For this assignment, we chose SQLite because it is a serverless, zero-configuration database that lives entirely in a single file[cite: 1]. It requires no separate background server processes to run or manage. This allows our data to survive server restarts easily while keeping the developer experience incredibly simple[cite: 1]. 

The database file lives in the root directory of the project and is named `tasks.db`[cite: 1]. It is created automatically the first time the application runs[cite: 1]. (Note: `tasks.db` is usually added to `.gitignore` so that every new clone starts with a fresh database[cite: 1]).

## DB Browser Exploration (Stage 4)

As part of testing the database directly, I explored the `tasks.db` file using DB Browser for SQLite. 

**Example SQL Query Executed:**
```sql
SELECT * FROM tasks WHERE done = 1;