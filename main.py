from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware

from schemas import StudentCreate, StudentUpdate, StudentResponse, MessageResponse

# Initialize FastAPI application with rich OpenAPI documentation metadata
app = FastAPI(
    title="Student Management API",
    description="A robust RESTful API built with FastAPI and Pydantic for managing student records.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for frontend integration (e.g., React, Vue, Angular)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-Memory Database Simulation
# Dictionary mapping: student_id (int) -> student_data (dict)
students_db: Dict[int, dict] = {}
id_counter: int = 1


@app.get("/", tags=["Health"])
def root():
    """Welcome endpoint providing health check and docs link."""
    return {
        "message": "Welcome to the Student Management API",
        "docs": "/docs",
        "total_students": len(students_db),
    }


# ==========================================
# 1. CREATE - POST /students
# ==========================================
@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new student",
    tags=["Students"],
)
def create_student(student: StudentCreate):
    """
    Create a new student record with auto-incremented ID.
    - **name**: Non-empty string
    - **email**: Valid email format
    - **course**: Non-empty course title
    - **age**: Positive integer
    Rejects the request if a student already exists with the same email.
    """
    global id_counter

    # Check if student already exists (by email)
    for existing_student in students_db.values():
        if existing_student["email"].lower() == student.email.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student already exists."
            )

    new_student = {
        "id": id_counter,
        "name": student.name.strip(),
        "email": student.email,
        "course": student.course.strip(),
        "age": student.age,
    }
    students_db[id_counter] = new_student
    id_counter += 1

    return new_student


# ==========================================
# 2. READ ALL - GET /students
# ==========================================
@app.get(
    "/students",
    response_model=List[StudentResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all students",
    tags=["Students"],
)
def get_all_students():
    """Retrieve all student records stored in the system."""
    return list(students_db.values())


# ==========================================
# BONUS: SEARCH - GET /students/search?course=...
# (Must be declared BEFORE /students/{student_id} to avoid route collision)
# ==========================================
@app.get(
    "/students/search",
    response_model=List[StudentResponse],
    status_code=status.HTTP_200_OK,
    summary="Search students by course",
    tags=["Students"],
)
def search_students_by_course(
    course: str = Query(..., min_length=1, description="Course name to filter by (case-insensitive partial match)")
):
    """
    Bonus Challenge: Search students by course name.
    Supports case-insensitive partial match (e.g. 'python' matches 'Python Full Stack').
    """
    search_term = course.lower().strip()
    matched_students = [
        student for student in students_db.values()
        if search_term in student["course"].lower()
    ]
    return matched_students


# ==========================================
# 3. READ BY ID - GET /students/{student_id}
# ==========================================
@app.get(
    "/students/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a student by ID",
    tags=["Students"],
)
def get_student_by_id(student_id: int):
    """
    Retrieve a specific student by their unique ID.
    Returns 404 if the student does not exist.
    """
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return students_db[student_id]


# ==========================================
# 4. UPDATE - PUT /students/{student_id}
# ==========================================
@app.put(
    "/students/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a student",
    tags=["Students"],
)
def update_student(student_id: int, updated_data: StudentUpdate):
    """
    Update all fields of an existing student.
    Returns 404 if the student does not exist.
    """
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Check for duplicate email across other students
    for other_id, existing_student in students_db.items():
        if other_id != student_id and existing_student["email"].lower() == updated_data.email.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another student with this email already exists."
            )

    updated_record = {
        "id": student_id,
        "name": updated_data.name.strip(),
        "email": updated_data.email,
        "course": updated_data.course.strip(),
        "age": updated_data.age,
    }
    students_db[student_id] = updated_record
    return updated_record


# ==========================================
# 5. DELETE - DELETE /students/{student_id}
# ==========================================
@app.delete(
    "/students/{student_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a student",
    tags=["Students"],
)
def delete_student(student_id: int):
    """
    Delete a student record by their ID.
    Returns 404 if the student does not exist.
    """
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    del students_db[student_id]
    return {"message": "Student deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
