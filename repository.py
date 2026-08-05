import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


def get_connection():
    return psycopg.connect(DATABASE_URL)


def initialize_database():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                )
            """)

            cursor.execute("SELECT COUNT(*) FROM tasks")
            count = cursor.fetchone()[0]

            if count == 0:
                cursor.executemany(
                    """
                    INSERT INTO tasks (title, done)
                    VALUES (%s, %s)
                    """,
                    [
                        ("Study FastAPI", False),
                        ("Buy groceries", True),
                        ("Go to the gym", False),
                    ],
                )
def get_all_tasks(done=None, search=None):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            query = "SELECT id, title, done FROM tasks"
            conditions = []
            values = []

            if done is not None:
                conditions.append("done = %s")
                values.append(done)

            if search is not None:
                conditions.append("title ILIKE %s")
                values.append(f"%{search}%")

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY id"

            cursor.execute(query, values)
            rows = cursor.fetchall()

            return [
                {"id": row[0], "title": row[1], "done": row[2]}
                for row in rows
            ]


def get_task_by_id(task_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, done FROM tasks WHERE id = %s",
                (task_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "id": row[0],
                "title": row[1],
                "done": row[2],
            }