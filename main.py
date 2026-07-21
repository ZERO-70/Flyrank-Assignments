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

