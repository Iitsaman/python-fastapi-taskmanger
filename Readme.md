



# Task Manager API + React Frontend

## Project Overview

This project is a **scalable REST API with  role-based access,JWT authentication and a simple frontend UI** built with:

- **Backend:** FastAPI, SQLite, JWT authentication, role-based access, CRUD APIs for tasks.
- **Frontend:** React + Vite, Axios for API calls, JWT storage.
- **Deployment:** Dockerized backend and frontend for easy setup.

---

## Features

### Backend
- User registration & login with hashed passwords and JWT tokens
- Role-based access control (user vs admin)
- CRUD APIs for `tasks` entity
- API versioning (`/api/v1`)
- Input validation with Pydantic
- Error handling with proper HTTP status codes
- API documentation via Swagger UI (`/docs`)
- Database schema management SQLite 

### Frontend
- Register & log in users
- JWT-protected 
- CRUD operations for tasks
- Display success and error messages from backend responses

### Security & Scalability
- Secure JWT token handling
- Input sanitization & validation
- Modular project structure for adding new modules


---

## Project Structure


---

# Run with Docker Compose
````markdown
🚀 Run with Docker Compose

docker-compose up --build

docker-compose down

````

---

## 🌐 Access the Services

* **Backend API:** [http://localhost:8000](http://localhost:8000)
* **Swagger docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Frontend (Vite dev server):** [http://localhost:5173](http://localhost:5173)

---

## 📝 Backend API Endpoints

| Method | Endpoint                   | Description                 |
| ------ | -------------------------- | --------------------------- |
| POST   | `/api/v1/auth/register`    | Register new user           |
| POST   | `/api/v1/auth/login`       | Login and get JWT           |
| GET    | `/api/v1/auth/me`          | Get current user info       |
| GET    | `/api/v1/tasks/tasks/`     | List tasks for current user |
| POST   | `/api/v1/tasks/tasks/`     | Create a task               |
| GET    | `/api/v1/tasks/tasks/{id}` | Get task by ID              |
| PUT    | `/api/v1/tasks/tasks/{id}` | Update a task               |
| DELETE | `/api/v1/tasks/tasks/{id}` | Delete a task               |
| GET    | `/api/v1/tasks/tasks/all`  | Admin: list all tasks       |

> **Note:** All task endpoints require a JWT token. Admin-only routes require proper role.

---

## 🖥️ Frontend Usage

- JWT is stored in **localStorage** & attached via Axios (`src/api/api.js`)  
- **Components:**  
  - `Auth.jsx` → Register/Login  
  - `Tasks.jsx` → CRUD tasks for regular users  
  - `AdminTasks.jsx` → Admin-only task management  


---

## 🐳 Docker Notes

* Backend exposes **port 8000**
* Frontend exposes **port 5173** (Vite dev server)
* Volumes for application:

  * Backend: `./backend:/app`
  * Frontend: `./frontend:/app`



---




