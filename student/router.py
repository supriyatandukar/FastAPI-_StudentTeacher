from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from databases import get_db
from .schemas import StudentProfile
from .models import StudentModel


# Create a router instance
router = APIRouter(
    prefix="/student",
    tags=["student"],
    responses={404: {"description": "Not found"}},
)


@router.get("/dashboard")
async def read_student_dashboard():
    return {"username": "student", "access": "full"}

@router.get("/students")
async def students(db: Session = Depends(get_db)):

    students = db.query(StudentModel).all()

    return {"all_students": students, "access": "full"}


@router.post("/create-student")
def create_student(
    student: StudentProfile,
    db: Session = Depends(get_db)
):
    new_student = StudentModel(
        username=student.username,
        email=student.email,
        age=student.age,
        is_active=student.is_active,
        full_name=student.full_name,
        phone_number=student.phone_number,
        address=student.address,
        grade=student.grade,
        course=student.course,
        gpa=student.gpa
    )

    db.add(new_student)      # stage the object
    db.commit()              # save to DB
    db.refresh(new_student)  # get generated ID

    return {"new_student":new_student}

