from pydantic import BaseModel
from typing import Optional

class StudentProfile(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    age: int
    is_active: bool = True
    full_name: str
    phone_number: str
    address: str
    grade: str
    course: str
    gpa: float