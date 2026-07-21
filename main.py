from fastapi import FastAPI, HTTPException, status
import sqlite3
from pydantic import BaseModel

app = FastAPI();

class Task(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    done: bool

def get_db_connection():
    conn = sqlite3.connect("task3.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM tasks")
    if cursor.fetchone()[0] == 0:
        sample_tasks = [
            ("Learn SQLite", 0),
            ("Write API endpoints", 1),
            ("Submit Week 3 Assignment", 0)
        ]
        cursor.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)",    
            sample_tasks
        )
    conn.commit()
    conn.close()

init_db()
