# FastAPI Blog API

A RESTful blog API built with FastAPI, SQLAlchemy, and PostgreSQL. This project serves as a hands-on learning experience for mastering FastAPI fundamentals, covering everything from basic CRUD operations to JWT authentication, WebSockets, and template rendering.

## Features

- **User Management** - Registration, authentication, profile updates, and account deletion
- **Blog Posts CRUD** - Full create, read, update, and delete functionality
- **JWT Authentication** - Token-based auth with OAuth2 password flow
- **Password Security** - Bcrypt hashing with Passlib for secure credential storage
- **WebSocket Chat** - Real-time bidirectional communication
- **File Upload/Download** - Handle file uploads and serve downloads
- **Jinja2 Templates** - Server-side HTML rendering with static files
- **Database Migrations** - Version-controlled schema changes with Alembic
- **ORM Relationships** - One-to-many relationship between users and posts with cascade deletion
- **Custom Middleware** - Request timing and custom headers
- **Custom Exception Handling** - Application-specific exceptions with custom HTTP responses
- **CORS Middleware** - Cross-Origin Resource Sharing configuration
- **Multiple Response Types** - JSON, HTML, and PlainText responses
- **Dependency Injection** - Class-based and multi-level dependencies
- **Unit Tests** - TestClient-based endpoint testing

## Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | Web framework with automatic OpenAPI docs |
| SQLAlchemy | ORM with modern `Mapped` type annotations |
| PostgreSQL | Relational database |
| Alembic | Database migrations |
| Passlib + Bcrypt | Password hashing |
| python-jose | JWT token encoding/decoding |
| Jinja2 | Template engine |
| Pydantic | Request/response validation |
| pytest | Testing framework |

## Project Structure

```
fastapi-playground/
├── main.py              # Application entry point, middleware, WebSocket
├── schemas.py           # Pydantic request/response models
├── exceptions.py        # Custom exception classes
├── client.py            # WebSocket chat HTML client
├── test_main.py         # Unit tests
├── requirements.txt     # Dependencies
├── alembic.ini          # Migration configuration
├── auth/
│   ├── authentication.py   # Token endpoint
│   └── oauth2.py           # JWT creation & validation
├── db/
│   ├── database.py      # Database connection & session dependency
│   ├── models.py        # SQLAlchemy ORM models
│   ├── hash.py          # Password hashing utilities
│   ├── user_db.py       # User database operations
│   └── posts_db.py      # Post database operations
├── routers/
│   ├── user.py          # User endpoints
│   ├── posts.py         # Post endpoints
│   ├── product.py       # Product endpoints (response types demo)
│   ├── files.py         # File upload/download endpoints
│   └── dependencies.py  # Dependency injection examples
├── templates/
│   ├── templates.py     # Template router
│   ├── product.html     # Jinja2 template
│   └── static/          # CSS/JS static files
├── files/               # Uploaded files directory
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

### Authentication `/auth`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/token` | Get JWT access token (OAuth2 password flow) |

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

### File Endpoints `/file`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/file/upload` | Upload file as bytes |
| `POST` | `/file/uploadfile` | Upload file using UploadFile |
| `GET` | `/file/download/{name}` | Download a file |

### Template Endpoints `/templates`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/templates/product/{id}` | Render product HTML template |

### Dependency Examples `/dependency`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/dependency/` | Demo: query params & headers extraction |
| `GET` | `/dependency/new` | Demo: nested dependencies |
| `GET` | `/dependency/user` | Demo: class-based dependency |

### Product Endpoints `/product`

| Method | Endpoint | Description | Response Type |
|--------|----------|-------------|---------------|
| `GET` | `/product/all` | Get all products | Plain Text |
| `GET` | `/product/withheader` | Get products with custom headers | JSON |
| `GET` | `/product/set_cookie` | Set and read cookies | JSON |
| `GET` | `/product/{id}` | Get product by ID | HTML or Plain Text |

### WebSocket

| Endpoint | Description |
|----------|-------------|
| `ws://localhost:8000/chat` | Real-time chat WebSocket |

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/AbdulrahmanMonged/fastapi-playground.git
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

- **Swagger UI**: http://localhost:8000/docs

## Usage Examples

### Get JWT Token

```bash
curl -X POST "http://localhost:8000/auth/token" \
  -d "username=john&password=secret123"
```

### Create a User

```bash
curl -X POST "http://localhost:8000/user/" \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "secret123", "email": "john@example.com"}'
```

### Create a Post

```bash
curl -X POST "http://localhost:8000/posts/" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "Hello World!", "user_id": 1}'
```

### Upload a File

```bash
curl -X POST "http://localhost:8000/file/uploadfile" \
  -F "file=@myfile.txt"
```

### Download a File

```bash
curl -X GET "http://localhost:8000/file/download/myfile.txt" -o myfile.txt
```

## Running Tests

```bash
pytest test_main.py -v
```

## Key Learnings

This project covers several important FastAPI and SQLAlchemy concepts:

- **Dependency Injection** - Using `Depends(get_db)` for database session management
- **Modern SQLAlchemy** - Using `Mapped` and `mapped_column` for type-safe models
- **Pydantic Models** - Separating request models from response models to control data exposure
- **Password Security** - Never storing plain passwords, using bcrypt for hashing
- **Database Relationships** - Configuring one-to-many relationships with cascade behavior
- **Response Models** - Using `response_model` to automatically filter sensitive data like passwords
- **Custom Exception Handling** - Creating custom exceptions and registering handlers with `@app.exception_handler()`
- **CORS Middleware** - Configuring cross-origin resource sharing for frontend integration
- **HTTP Middleware** - Adding request timing with `@app.middleware("http")`
- **Multiple Response Types** - Returning `HTMLResponse`, `PlainTextResponse`, and `JSONResponse`
- **Cookies & Headers** - Using `Cookie()` and `Header()` parameters for reading, and `Response` for setting
- **OpenAPI Response Documentation** - Using `responses={}` parameter to document multiple response types
- **JWT Authentication** - Creating and validating tokens with `python-jose`, OAuth2PasswordBearer flow
- **WebSockets** - Real-time bidirectional communication for chat functionality
- **File Handling** - Upload with `File()` and `UploadFile`, download with `FileResponse`
- **Static Files** - Mounting directories with `StaticFiles`
- **Jinja2 Templates** - Server-side rendering with `Jinja2Templates` and `TemplateResponse`
- **Class-based Dependencies** - Using classes as dependencies with automatic parameter injection
- **Multi-level Dependencies** - Dependencies that depend on other dependencies
- **Testing** - Using `TestClient` for endpoint testing with pytest

## Roadmap

Planned improvements:

- [x] JWT token-based authentication
- [x] Unit and integration tests
- [ ] Role-based access control
- [ ] Post categories and tags
- [ ] Pagination for list endpoints
- [ ] Docker containerization

## License

This project is open source and available under the [MIT License](LICENSE).

---

*A learning project for practicing FastAPI fundamentals*
