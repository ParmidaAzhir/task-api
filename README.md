# Task API

A REST API built with **FastAPI**, **PostgreSQL**, and **Docker** for managing tasks.

This project demonstrates the fundamental CRUD (Create, Read, Update, Delete) operations using PostgreSQL for persistent storage. The entire application runs with Docker Compose and provides automatically generated interactive documentation using Swagger UI.
---

# Features

- Create a new task
- Get all tasks
- Get a task by ID
- Update a task
- Delete a task
- Filter tasks by completion status
- Search tasks by title
- Store tasks permanently using PostgreSQL
- Run the entire application with Docker Compose
- Interactive Swagger UI documentation

---
# Authentication

This API uses **Supabase Auth** for user authentication.

Users can sign up and log in with email and password. After login, Supabase returns an **access token (JWT)** and a **refresh token**.

Protected routes require the access token in the Authorization header:

```text
Authorization: Bearer <access_token>
```

FastAPI verifies the token with Supabase before allowing access.


# Technologies

- Python
- FastAPI
- Uvicorn
- PostgreSQL
- Docker
- Docker Compose
- Psycopg
- Supabase Auth
- JWT
- python-dotenv

---

# Database

This project uses **PostgreSQL** running inside a Docker container.

The application automatically:

- Connects to PostgreSQL using the `DATABASE_URL` environment variable
- Creates the `tasks` table if it does not exist
- Inserts the three example tasks only when the table is empty

Database data is stored in a Docker volume, so tasks remain available even after restarting the containers.
---

# Installation

Clone the repository:

```bash
git clone https://github.com/ParmidaAzhir/task-api.git
```

Go into the project folder:

```bash
cd task-api
```

Copy the example environment file:

```bash
cp .env.example .env
```

Start the application:

```bash
docker compose up --build
```

---
# Environment Variables

Create a `.env` file using `.env.example`.

Example:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/tasks
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_publishable_key
```

The real `.env` file is ignored by Git and must not be committed.


# API URLs

API:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Get API information |
| GET | `/health` | Check API health |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks?done=true` | Filter completed tasks |
| GET | `/tasks?search=text` | Search tasks by title |
| GET | `/tasks/{id}` | Get a task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

---
## Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/auth/signup` | Create a new user | No |
| POST | `/auth/login` | Log in and receive tokens | No |
| POST | `/auth/logout` | Log out | Yes |
| GET | `/public/info` | Public information | No |
| GET | `/protected/profile` | Get authenticated user profile | Yes |
| GET | `/protected/dashboard` | Example protected route | Yes |

# Example Request

Create a task:

```http
POST /tasks
```

Request body:

```json
{
  "title": "Study FastAPI"
}
```

Response:

```json
{
  "id": 4,
  "title": "Study FastAPI",
  "done": false
}
```

Status code:

```text
201 Created
```

---

# Example SQL Query

Return all tasks:

```sql
SELECT * FROM tasks;
```

This query can be executed using:

- psql
- pgAdmin
- TablePlus
- DBeaver

---

# Database Screenshot

The PostgreSQL database was inspected after running the application with Docker Compose.

## Database Screenshot

<img width="524" height="109" alt="image" src="https://github.com/user-attachments/assets/aa01bc21-1732-41fa-8772-dd0003fc99e1" />

---

# Swagger UI

FastAPI automatically generates interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Every endpoint can be tested directly from the browser using the **Try it out** button.

# Swagger Screenshot

![Swagger UI](swagger.png.png)

---
## Swagger Authentication

Protected routes show a lock icon in Swagger UI.

To test them:

1. Run `POST /auth/login`.
2. Copy the `access_token`.
3. Click **Authorize** at the top of Swagger.
4. Paste the token.
5. Run `GET /protected/profile` or `GET /protected/dashboard`.

A valid token returns `200`. An invalid or tampered token returns `401`.


# Project Structure

```text
task-api/
│
├── main.py
├── repository.py
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

---

# Assignment Progress

## Assignment 1

- Built a REST API using FastAPI
- Implemented CRUD operations
- Added filtering and search
- Added Swagger UI documentation

## Assignment 2

- Replaced the in-memory task list with SQLite
- Created the database automatically
- Created the table automatically
- Inserted example tasks only on the first run
- Replaced CRUD operations with SQL queries
- Executed SQL queries manually using DB Browser for SQLite

---
## Assignment 3

- Migrated the API from SQLite to PostgreSQL
- Connected FastAPI to PostgreSQL using Psycopg
- Stored the connection string in a `.env` file
- Moved database logic into `repository.py`
- Containerized the application with Docker
- Used Docker Compose to run the API and PostgreSQL together
- Added persistent storage using Docker volumes

  ## Assignment 4

- Added Supabase authentication
- Added signup and login endpoints
- Returned JWT access and refresh tokens
- Added public and protected routes
- Verified JWT tokens with Supabase
- Added reusable authentication dependency
- Added protected dashboard route
- Added logout endpoint
- Added Swagger Bearer authorization
- Tested valid and tampered tokens

# Author

**Parmida Azhir**
