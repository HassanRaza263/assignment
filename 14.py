from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int
    grade: str

students_db = {}
student_id_counter = 0

@app.get("/students")
async def get_students():
    return students_db

@app.get("/students/{student_id}")
async def get_student(student_id: int):
    student = students_db.get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post("/students")
async def create_student(student: Student):
    global student_id_counter
    student_id_counter += 1
    students_db[student_id_counter] = student.dict()
    return {"message": "Student created successfully", "student_id": student_id_counter}

@app.put("/students/{student_id}")
async def update_student(student_id: int, updated_student: Student):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    students_db[student_id] = updated_student.dict()
    return {"message": "Student updated successfully"}

@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    del students_db[student_id]
    return {"message": "Student deleted successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
