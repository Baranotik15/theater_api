# 🎭 Theater Service API

The **Theater Service** is a RESTful API built with Django REST Framework that manages a theater system — actors, genres, plays, halls, performances, and reservations. It supports **JWT authentication**, an **admin panel**, and **auto-generated Swagger documentation**. Everything runs inside Docker containers for easy deployment.

## 📦 Features

- 📑 Full CRUD for:
  - Theatre halls
  - Actors
  - Genres
  - Plays
  - Performances
- 🔐 JWT-based authentication
- 👤 Role-based access:
  - Admins: full access
  - Authenticated users: read-only access
- 🧑‍💼 Django Admin Panel
- 📄 Swagger/OpenAPI documentation via drf-spectacular
- 🐳 Docker support
- 📁 Modular structure: `users`, `theater`, `reservations`, `theater_service`

## Model diagram
![image-removebg-preview (3)](https://github.com/user-attachments/assets/d4bb7de3-4023-48f1-bd46-2d58ed514ca2)

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/theater-service.git
cd theater-service
```

### 2. Copy .env file

```bash
cp .env.sample .env
```
it should look like this
```bash
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
```

## 🐳 Run with docker

### 1. Build and run the project
```bash
docker-compose up --build
```

### 2. Apply migrations and create a superuser
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```
## 🧾 Register

To create a new user account:

**POST** `/api/users/register/`

**Request body:**

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

## 🔑 Authentication
This project uses JWT for user authentication.

### Obtain token:

**POST /api/users/token/**

Request body:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```
Response:
```json
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}
```
_____________________________
### Refresh token:

**POST /api/users/token/refresh/**

Request body:
```json
{
  "refresh": "your_refresh_token"
}
```
You can access the Swagger UI documentation at:

`/api/doc/swagger/`

## 🧾 Tech Stack

- Python 3.12
- Django 5.2.1
- Django REST Framework
- Simple JWT
- drf-spectacular
- PostgreSQL
- Docker & Docker Compose
