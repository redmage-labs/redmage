import sqlite3
from dataclasses import dataclass
from typing import Optional

con = sqlite3.connect("todos.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, message TEXT, finished INTEGER)"
)


@dataclass
class Todo:
    id: Optional[int] = None
    message: Optional[str] = None
    finished: bool = False


def get_todo(id):
    cur.execute("SELECT * FROM todos WHERE id = ?", (id,))
    todo = Todo(*cur.fetchone())
    return todo


def get_todos():
    cur.execute("SELECT * FROM todos")
    todos = [Todo(*todo) for todo in cur.fetchall()]
    return todos


def create_todo(message, finished):
    cur.execute(
        "INSERT INTO todos (message, finished) VALUES (?, ?)", (message, finished)
    )
    con.commit()


def update_todo(id, message, finished):
    cur.execute(
        "UPDATE todos SET message = ?, finished = ? WHERE id = ?",
        (message, finished, id),
    )
    con.commit()


def delete_todo(id):
    cur.execute("DELETE FROM todos WHERE id = ?", (id,))
    con.commit()
