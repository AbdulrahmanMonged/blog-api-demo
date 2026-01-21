# FastAPI Blog API

A RESTful blog API built with FastAPI, SQLAlchemy, and PostgreSQL. This project serves as a hands-on learning experience for mastering FastAPI fundamentals, covering everything from basic CRUD operations to database relationships and password security.

## Features

- **User Management** - Registration, authentication, profile updates, and account deletion
- **Blog Posts CRUD** - Full create, read, update, and delete functionality
- **Password Security** - Bcrypt hashing with Passlib for secure credential storage
- **Database Migrations** - Version-controlled schema changes with Alembic
- **ORM Relationships** - One-to-many relationship between users and posts with cascade deletion
- **Auto-generated Docs** - Interactive Swagger UI with dark theme

## Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | Web framework with automatic OpenAPI docs |
| SQLAlchemy | ORM with modern `Mapped` type annotations |
| PostgreSQL | Relational database |
| Alembic | Database migrations |
| Passlib + Bcrypt | Password hashing |
| Pydantic | Request/response validation |

## Project Structure

```
fastapi-playground/
├── main.py              # Application entry point
├── schemas.py           # Pydantic request/response models
├── requirements.txt     # Dependencies
├── alembic.ini          # Migration configuration
├── db/
│   ├── database.py      # Database connection & session dependency
│   ├── models.py        # SQLAlchemy ORM models
│   ├── hash.py          # Password hashing utilities
│   ├── user_db.py       # User database operations
│   └── posts_db.py      # Post database operations
├── routers/
│   ├── user.py          # User endpoints
│   └── posts.py         # Post endpoints
└── migrations/
    └── versions/        # Migration history
```

## Database Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| username | String(50) | Indexed for fast lookups |
| password | String(255) | Bcrypt hashed |
| email | String(50) | User email |

### Posts Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| title | String(50) | Post title |
| content | Text | Post body |
| published | Boolean | Default: True |
| user_id | Integer | Foreign Key → users.id (indexed) |

**Relationship:** Users have many Posts. Deleting a user cascades to delete all their posts.

## API Endpoints

### User Endpoints `/user`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/user/` | Create new user |
| `POST` | `/user/login` | Authenticate user |
| `GET` | `/user/` | Get all users |
| `PUT` | `/user/` | Update user details |
| `DELETE` | `/user/` | Delete user account |

### Post Endpoints `/posts`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/posts/` | Create new post |
| `GET` | `/posts/{user_id}` | Get all posts by user |
| `GET` | `/posts/post/{post_id}` | Get specific post |
| `PUT` | `/posts/post/{post_id}` | Update post |
| `DELETE` | `/posts/post/{post_id}` | Delete post |

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/fastapi-playground.git
   cd fastapi-playground
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**

   Create a `.env` file:
   ```env
   DB_URI=postgresql+psycopg2://username:password@localhost:5432/blog
   ```

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the server**
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

## API Documentation

Once running, access the interactive docs:

- **Swagger UI (Dark Theme)**: http://localhost:8000/docs

## Usage Examples

### Create a User

```bash
curl -X POST "http://localhost:8000/user/" \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "secret123", "email": "john@example.com"}'
```

### Login

```bash
curl -X POST "http://localhost:8000/user/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "secret123"}'
```

### Create a Post

```bash
curl -X POST "http://localhost:8000/posts/" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "Hello World!", "user_id": 1}'
```

### Get User's Posts

```bash
curl -X GET "http://localhost:8000/posts/1"
```

## Key Learnings

This project covers several important FastAPI and SQLAlchemy concepts:

- **Dependency Injection** - Using `Depends(get_db)` for database session management
- **Modern SQLAlchemy** - Using `Mapped` and `mapped_column` for type-safe models
- **Pydantic Models** - Separating request models from response models to control data exposure
- **Password Security** - Never storing plain passwords, using bcrypt for hashing
- **Database Relationships** - Configuring one-to-many relationships with cascade behavior
- **Response Models** - Using `response_model` to automatically filter sensitive data like passwords

## Roadmap

Planned improvements:

- [ ] JWT token-based authentication
- [ ] Role-based access control
- [ ] Post categories and tags
- [ ] Pagination for list endpoints
- [ ] Unit and integration tests
- [ ] Docker containerization

## License

This project is open source and available under the [MIT License](LICENSE).

---

*A learning project for practicing FastAPI fundamentals*
