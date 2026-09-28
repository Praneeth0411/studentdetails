# 🎓 Student Management API (FastAPI CRUD Assessment)

A high-performance, robust, and cleanly structured RESTful API built with **FastAPI** and **Pydantic v2** for managing student records.

---

## 📁 Project Structure

```text
├── main.py          # FastAPI application, routing, and business logic
├── schemas.py       # Pydantic data models & request/response validation
├── test_main.py     # Automated test suite (pytest)
├── test_suite.py    # Standard unittest test suite
└── README.md        # API documentation and Interview Q&A
```

---

## 🚀 Quick Start & How to Run

### 1. Install Dependencies
```bash
pip install fastapi uvicorn email-validator pytest httpx
```

### 2. Start the FastAPI Server
```bash
python -m uvicorn main:app --reload --port 8000
```
Or directly:
```bash
python main.py
```

- 🌐 **API Base URL**: `http://127.0.0.1:8000`
- 📖 **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`
- 📚 **Redoc Documentation**: `http://127.0.0.1:8000/redoc`

### 3. Run Automated Tests
```bash
python -m pytest -v test_main.py
```

---

## 📡 API Endpoints Specification

| Method | Endpoint | Description | Status Code | Error Codes |
|---|---|---|---|---|
| `POST` | `/students` | Create a new student record | `201 Created` | `400`, `422` |
| `GET` | `/students` | Retrieve all student records | `200 OK` | - |
| `GET` | `/students/search?course=...` | Search students by course name | `200 OK` | `422` |
| `GET` | `/students/{student_id}` | Retrieve a student by ID | `200 OK` | `404` |
| `PUT` | `/students/{student_id}` | Update an existing student | `200 OK` | `400`, `404`, `422` |
| `DELETE` | `/students/{student_id}` | Delete a student by ID | `200 OK` | `404` |

---

## 📝 Request & Response Examples

### 1. Create Student (`POST /students`)
**Request Body:**
```json
{
  "name": "Rahul",
  "email": "rahul@gmail.com",
  "course": "Python Full Stack",
  "age": 22
}
```
**Response (`201 Created`):**
```json
{
  "id": 1,
  "name": "Rahul",
  "email": "rahul@gmail.com",
  "course": "Python Full Stack",
  "age": 22
}
```

### 2. Get All Students (`GET /students`)
**Response (`200 OK`):**
```json
[
  {
    "id": 1,
    "name": "Rahul",
    "email": "rahul@gmail.com",
    "course": "Python Full Stack",
    "age": 22
  }
]
```

### 3. Search Students by Course (`GET /students/search?course=Python`)
*(Case-insensitive partial matching)*
**Response (`200 OK`):**
```json
[
  {
    "id": 1,
    "name": "Rahul",
    "email": "rahul@gmail.com",
    "course": "Python Full Stack",
    "age": 22
  }
]
```

### 4. Error Handling: Student Not Found (`GET /students/999`)
**Response (`404 Not Found`):**
```json
{
  "detail": "Student not found"
}
```

### 5. Error Handling: Student Already Exists (`POST /students`)
**Response (`400 Bad Request`):**
```json
{
  "detail": "Student already exists."
}
```

---

## 🎤 Interview Follow-up Questions & Answers

### 1. Why did you use a Pydantic model?
- **Type Safety & Data Parsing**: Pydantic validates incoming payload types (string, int, email) and coerces compatible types automatically.
- **Automated Documentation**: FastAPI leverages Pydantic schemas to generate OpenAPI/Swagger JSON schemas seamlessly.
- **Sanitization & Error Messages**: It delivers clear, standardized `422 Unprocessable Entity` responses when client data fails validation rules (such as missing required fields, non-positive age, or malformed email).

### 2. Why is POST used for creating a student?
- According to RESTful architectural guidelines, `POST` is designed for non-idempotent operations where the server creates a new subordinate resource and assigns its identifier (e.g. `id: 1`). Calling `POST` multiple times will create multiple distinct records.

### 3. What is the difference between PUT and PATCH?
- **`PUT` (Full Replacement)**: Replaces the entire resource state. The client must supply all required fields; missing fields are overwritten or reset.
- **`PATCH` (Partial Update)**: Updates only the specific fields provided in the request payload, leaving unmodified fields untouched.

### 4. How are you handling a student that does not exist?
- When querying, updating, or deleting by `student_id`, the system checks if the key exists in the database.
- If absent, an `HTTPException(status_code=404, detail="Student not found")` is raised, adhering to REST standards and FastAPI error formatting.

### 5. Where is validation happening?
- **Request Level (Pydantic & FastAPI)**:
  - `name`: Must be a non-empty string (`min_length=1`).
  - `email`: Validated by `EmailStr` conforming to RFC email format specifications.
  - `age`: Must be an integer within acceptable range (`gt=0, le=120`).
  - `course`: Must be non-empty (`min_length=1`).
- **Business Logic Level**:
  - Uniqueness check for email addresses before creating or updating records to prevent duplicates.
  - Route ordering: `/students/search` is declared before `/students/{student_id}` to prevent path conflict.

### 6. How would you replace the in-memory data with MongoDB or PostgreSQL?
- **PostgreSQL (Relational via SQLAlchemy / SQLModel)**:
  1. Define a database model using `SQLAlchemy` declarative base.
  2. Create an `engine` and `sessionmaker`.
  3. Inject `db: Session = Depends(get_db)` into FastAPI route handlers.
  4. Perform CRUD using `db.query(Student).filter(...)`, `db.add()`, and `db.commit()`.
- **MongoDB (Document-based via Motor / Beanie / PyMongo)**:
  1. Initialize `AsyncIOMotorClient(MONGODB_URI)`.
  2. Map Pydantic models to MongoDB documents using `_id` to `id` serialization.
  3. Execute async queries: `await collection.find_one({"_id": ObjectId(student_id)})`.

### 7. How would you connect this API to a React frontend?
1. **Enable CORS**: `CORSMiddleware` is configured in `main.py` allowing origins (e.g., `http://localhost:3000` or `http://localhost:5173`).
2. **Frontend Service (Axios / Fetch)**:
   ```javascript
   import axios from 'axios';

   const API = axios.create({ baseURL: 'http://127.0.0.1:8000' });

   export const getStudents = () => API.get('/students');
   export const createStudent = (data) => API.post('/students', data);
   export const updateStudent = (id, data) => API.put(`/students/${id}`, data);
   export const deleteStudent = (id) => API.delete(`/students/${id}`);
   export const searchStudents = (course) => API.get(`/students/search?course=${course}`);
   ```
3. **State Management**: Use React Hooks (`useState`, `useEffect`) or React Query / TanStack Query to fetch data, handle loading states, and update the UI dynamically.
