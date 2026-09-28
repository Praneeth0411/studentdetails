from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional


class StudentBase(BaseModel):
    """Base schema with common attributes and validation rules."""
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Full name of the student (cannot be empty)",
        examples=["Rahul"]
    )
    email: EmailStr = Field(
        ...,
        description="Valid email address of the student",
        examples=["rahul@gmail.com"]
    )
    course: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Enrolled course name (cannot be empty)",
        examples=["Python Full Stack"]
    )
    age: int = Field(
        ...,
        gt=0,
        le=120,
        description="Age of the student (must be a positive integer)",
        examples=[22]
    )


class StudentCreate(StudentBase):
    """Schema for creating a new student (POST request payload)."""
    pass


class StudentUpdate(StudentBase):
    """Schema for full update of an existing student (PUT request payload)."""
    pass


class StudentResponse(StudentBase):
    """Schema for response payload returned by API endpoints."""
    id: int = Field(..., description="Unique auto-incremented identifier", examples=[1])

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    """Generic message response schema."""
    message: str
