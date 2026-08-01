from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

app = FastAPI();

class Task(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    done: bool

def get_db_connection():
    return psycopg.connect(os.environ["DATABASE_URL"])

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM tasks")
    if cursor.fetchone()[0] == 0:
        sample_tasks = [
            ("Learn Postgres", False),
            ("Write API endpoints", True),
            ("Submit Week 1 Assignment", False)
        ]
        
        cursor.executemany("INSERT INTO tasks (title, done) VALUES (%s, %s)",    
            sample_tasks
        )
        
    conn.commit()
    conn.close()

init_db()

from fastapi import HTTPException, status
from psycopg.rows import dict_row

@app.get("/")
def root():
    return {"status": "online", "message": "backend is running"}

@app.get("/test/{item_id}")
def return_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "query_parameter": q}


@app.get("/tasks")
def get_tasks():
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()
            
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            task = cursor.fetchone()
            
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return task


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
        
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *", 
                (task.title, False)
            )
            new_task = cursor.fetchone()
        conn.commit()
        
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    if not task_update.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
        
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                "UPDATE tasks SET title=%s, done=%s WHERE id=%s RETURNING *", 
                (task_update.title, task_update.done, task_id)
            )
            updated_task = cursor.fetchone()
        conn.commit()
        
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return updated_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM tasks WHERE id=%s RETURNING id", (task_id,))
            deleted = cursor.fetchone()
        conn.commit()
        
    if deleted is None:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return None