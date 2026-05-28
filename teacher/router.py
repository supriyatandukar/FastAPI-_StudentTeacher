from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from databases import get_db
from .schemas import TeacherProfile
from .models import TeacherModel

# Create a router instance
router = APIRouter(
    prefix="/teacher",
    tags=["teacher"],
    responses={404: {"description": "Not found"}},
)


@router.get("/dashboard")
async def read_teacher_dashboard():
    return {"username": "teacher", "access": "full"}


@router.get("/teachers")
async def teachers(db: Session = Depends(get_db)):

    teachers = db.query(TeacherModel).all()

    return {"all_teachers": teachers, "access": "full"}


@router.post("/create-teacher")
def create_teacher(
    teacher: TeacherProfile,
    db: Session = Depends(get_db)
):
    new_teacher = TeacherModel(
        id=teacher.id,
        username=teacher.username,
        email=teacher.email,
        age=teacher.age,
        is_active=teacher.is_active,
        bio=teacher.bio,
        full_name=teacher.full_name,
        address=teacher.address,
        subject=teacher.subject,
        qualification=teacher.qualification,
        experience_years=teacher.experience_years,
        salary=teacher.salary
    )

    db.add(new_teacher)      # stage the object
    db.commit()              # save to DB
    db.refresh(new_teacher)  # get generated ID

    return {"new_teacher":new_teacher}


   
test_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Add Teacher</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        body {
            background: #f4f6f9;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            background: white;
            width: 100%;
            max-width: 700px;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        h2 {
            text-align: center;
            margin-bottom: 25px;
            color: #333;
        }

        .form-group {
            margin-bottom: 18px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #444;
        }

        input,
        textarea,
        select {
            width: 100%;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 15px;
        }

        textarea {
            resize: vertical;
            min-height: 100px;
        }

        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .checkbox-group input {
            width: auto;
        }

        button {
            width: 100%;
            background: #007bff;
            color: white;
            border: none;
            padding: 14px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
        }

        button:hover {
            background: #0056b3;
        }

        .row {
            display: flex;
            gap: 15px;
        }

        .row .form-group {
            flex: 1;
        }

        @media (max-width: 600px) {
            .row {
                flex-direction: column;
            }
        }
    </style>
</head>

<body>

<div class="container">
    <h2>Add Teacher</h2>

<form id="teacherForm">

    <!-- Username -->
    <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" name="username" required />
    </div>

    <!-- Email -->
    <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" required />
    </div>

    <!-- Full Name -->
    <div class="form-group">
        <label for="full_name">Full Name</label>
        <input type="text" id="full_name" name="full_name" required />
    </div>

    <!-- Age and Subject -->
    <div class="row">
        <div class="form-group">
            <label for="age">Age</label>
            <input type="number" id="age" name="age" min="18" required />
        </div>

        <div class="form-group">
            <label for="subject">Subject</label>
            <input type="text" id="subject" name="subject" required />
        </div>
    </div>

    <!-- Qualification -->
    <div class="form-group">
        <label for="qualification">Qualification</label>
        <input type="text" id="qualification" name="qualification" required />
    </div>

    <!-- Experience and Salary -->
    <div class="row">
        <div class="form-group">
            <label for="experience_years">Experience (Years)</label>
            <input
                type="number"
                id="experience_years"
                name="experience_years"
                min="0"
                required
            />
        </div>

        <div class="form-group">
            <label for="salary">Salary</label>
            <input
                type="number"
                step="0.01"
                id="salary"
                name="salary"
                required
            />
        </div>
    </div>

    <!-- Address -->
    <div class="form-group">
        <label for="address">Address</label>
        <textarea id="address" name="address" required></textarea>
    </div>

    <!-- Bio -->
    <div class="form-group">
        <label for="bio">Bio</label>
        <textarea
            id="bio"
            name="bio"
            placeholder="Optional teacher bio..."
        ></textarea>
    </div>

    <!-- Active Status -->
    <div class="form-group checkbox-group">
        <input
            type="checkbox"
            id="is_active"
            name="is_active"
            checked
        />
        <label for="is_active">Active Teacher</label>
    </div>

    <button type="submit">Add Teacher</button>

</form>

<p>
    <a href="/teacher/view-teachers">View All Teachers</a>
    </p>
    

<script>
document
    .getElementById("teacherForm")
    .addEventListener("submit", async function (e) {

        e.preventDefault();

        const teacherData = {
            id: Date.now(),  // Simple unique ID generation
            username: document.getElementById("username").value,
            email: document.getElementById("email").value,
            age: parseInt(document.getElementById("age").value),
            is_active: document.getElementById("is_active").checked,
            bio: document.getElementById("bio").value,
            full_name: document.getElementById("full_name").value,
            address: document.getElementById("address").value,
            subject: document.getElementById("subject").value,
            qualification: document.getElementById("qualification").value,
            experience_years: parseInt(
                document.getElementById("experience_years").value
            ),
            salary: parseFloat(document.getElementById("salary").value)
        };

        try {

            const response = await fetch(
                "/teacher/create-teacher",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(teacherData)  #python ma load garya jastai ho, js lai json ma covert gareko
                }
            );

            const result = await response.json();

            if (response.ok) {
                alert("Teacher added successfully!");

                console.log(result);

                document.getElementById("teacherForm").reset();
            }
            else {
                alert("Error creating teacher");
                console.log(result);  #python ko print jastai ho, js ma console.log le print garcha
            }

        }
        catch (error) {

            console.error(error);

            alert("Something went wrong!");
        }
    });
</script>

</body>
</html>
"""

from fastapi.responses import HTMLResponse

@router.get("/test", response_class=HTMLResponse)
async def test():
    return test_html



from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi import Depends

@router.get("/view-teachers", response_class=HTMLResponse)  #yesle chai teachers list dekhauxa
def view_teachers(db: Session = Depends(get_db)):

    teachers = db.query(TeacherModel).all()  #yesma .filter() pani garna sakincha, jastai .filter(TeacherModel.is_active == 1) le active teachers matra dekhauxa

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Teachers List</title>

        <style>

            body {
                font-family: Arial, sans-serif;
                background: #f4f6f9;
                margin: 0;
                padding: 20px;
            }

            h1 {
                text-align: center;
                margin-bottom: 25px;
                color: #333;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                background: white;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                border-radius: 10px;
                overflow: hidden;
            }

            th {
                background: #007bff;
                color: white;
                padding: 14px;
                text-align: left;
            }

            td {
                padding: 12px;
                border-bottom: 1px solid #ddd;
            }

            tr:hover {
                background: #f1f1f1;
            }

            .active {
                color: green;
                font-weight: bold;
            }

            .inactive {
                color: red;
                font-weight: bold;
            }

        </style>

    </head>

    <body>

    <div>
    <p>
    <a href="/teacher/dashboard">Go to Dashboard</a> |
    <a href="/teacher/test">Add New Teacher</a>
    </p>
    </div>

        <h1>Teachers List</h1>

        <table>

            <thead>
                <tr>
                    <th>ID</th>
                    <th>Full Name</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Subject</th>
                    <th>Qualification</th>
                    <th>Experience</th>
                    <th>Salary</th>
                    <th>Status</th>
                </tr>
            </thead>

            <tbody>
    """
#python ko loop haru yeta aauxa, yo bichma aayo aba tala feri doclai continue garna += garya xa
    for teacher in teachers:

        status = (
            "<span class='active'>Active</span>"
            if teacher.is_active
            else "<span class='inactive'>Inactive</span>"
        )

        html_content += f"""
            <tr>
                <td>{teacher.id}</td>
                <td>{teacher.full_name}</td>
                <td>{teacher.username}</td>
                <td>{teacher.email}</td>
                <td>{teacher.subject}</td>
                <td>{teacher.qualification}</td>
                <td>{teacher.experience_years} Years</td>
                <td>${teacher.salary}</td>
                <td>{status}</td>
            </tr>
        """

    html_content += """
            </tbody>
        </table>

    </body>
    </html>
    """

    return html_content

#action button, CRUD garne