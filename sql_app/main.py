from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .datavalidation import DataValidation

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------<Course>----------------

@app.post("/CreateCourse/")
def create_course(course: schemas.Course, db: Session = Depends(get_db)):
    DataValidation.cid_check(course.cid)
    DataValidation.cid_duplicate_check(db, course.cid)
    db_course = crud.get_course(db, cid=course.cid)
    if db_course:
        raise HTTPException(status_code=400, detail="Course already registered")
    DataValidation.cname_check(course.cname)
    DataValidation.department_check(course.department)
    DataValidation.credit_check(course.credit)
    return crud.create_course(db=db, course=course)


@app.get("/GetCourse/{cid}", response_model=schemas.Course)
def read_course(cid: str, db: Session = Depends(get_db)):
    DataValidation.cid_exists(db, cid)
    db_course = crud.get_course(db, cid=cid)
    if db_course is None:
        raise HTTPException(status_code=404, detail="course not found")
    return db_course


@app.delete("/DeleteCourse/{cid}")
def delete_course(cid: str, db: Session = Depends(get_db)):
    DataValidation.cid_exists(db, cid)
    return crud.delete_course(db, cid=cid)


@app.patch("/UpdateCourse/{cid}")
def update_course(cid: str, course_update: schemas.Course, db: Session = Depends(get_db)):
    DataValidation.cid_exists(db, cid)
    return crud.patch_course(db, cid=cid, updated_course=course_update)


# ---------------Lecturer-----------------

@app.post("/CreateLecturer/")
def create_lecturer(lecturer: schemas.Lecturer, db: Session = Depends(get_db)):
    DataValidation.lid_check(lecturer.lid)
    DataValidation.lid_duplicate_check(db, lecturer.lid)
    db_lecturer = crud.get_lecturer(db, lid=lecturer.lid)
    if db_lecturer:
        raise HTTPException(status_code=400, detail="lecturer already registered")
    DataValidation.fname_check(lecturer.fname)
    DataValidation.lname_check(lecturer.lname)
    DataValidation.check_codemelli(lecturer.id)
    DataValidation.ldepartment(lecturer.department)
    DataValidation.check_Lecturer_major(lecturer.major)
    DataValidation.valid_lecturer_birth(lecturer.birth)
    DataValidation.valid_lecturer_borncity(lecturer.borncity)
    DataValidation.lecturer_address(lecturer.address)
    DataValidation.lecturer_postalcode(lecturer.postalcode)
    DataValidation.lecturer_mphone(lecturer.mphone)
    DataValidation.lecturer_telephone(lecturer.tphone)
    DataValidation.lcourseid_check(db, lecturer.lcourseid)
    return crud.create_lecturer(db=db, lecturer=lecturer)


@app.get("/GetLecturer/{lid}")
def read_lecturer(lid: str, db: Session = Depends(get_db)):
    DataValidation.lid_exists(db, lid)
    db_lecturer = crud.get_lecturer(db, lid=lid)
    if db_lecturer is None:
        raise HTTPException(status_code=404, detail="lecturer not found")
    return db_lecturer


@app.delete("/DeleteLecturer/{lid}")
def delete_lecturer(lid: str, db: Session = Depends(get_db)):
    DataValidation.lid_exists(db, lid)
    return crud.delete_lecturer(db, lid=lid)


@app.patch("/UpdateLecturer/{lid}")
def update_lecturer(lid: str, lecturer_update: schemas.Lecturer, db: Session = Depends(get_db)):
    DataValidation.lid_exists(db, lid)
    return crud.patch_lecturer(db, lid=lid, updated_lecturer=lecturer_update)


# ---------------Student-----------------

@app.post("/CreateStudent/")
def create_student(student: schemas.Student, db: Session = Depends(get_db)):
    DataValidation.check_stid(student.stid)
    DataValidation.stid_duplicate_check(db, student.stid)
    db_student = crud.get_student(db, stid=student.stid)
    if db_student:
        raise HTTPException(status_code=400, detail="student already registered")
    DataValidation.sfname_check(student.sfname)
    DataValidation.slname_check(student.slname)
    DataValidation.sfather_check(student.sfather)
    DataValidation.valid_student_birth(student.sbirth)
    DataValidation.serial_number(student.ids)
    DataValidation.valid_student_borncity(student.sborncity)
    DataValidation.student_address(student.saddress)
    DataValidation.student_postalcode(student.spostalcode)
    DataValidation.student_mphone(student.smphone)
    DataValidation.student_telephone(student.stphone)
    DataValidation.sdepartment(student.sdepartment)
    DataValidation.check_student_major(student.smajor)
    DataValidation.marital(student.married)
    DataValidation.check_student_id(student.sid)
    DataValidation.scourseid_check(db, student.scourseid)
    DataValidation.lids_check(db, student.lids)
    return crud.create_student(db=db, student=student)


@app.get("/GetStudent/{stid}")
def read_student(stid: str, db: Session = Depends(get_db)):
    DataValidation.stid_exists(db, stid)
    db_student = crud.get_student(db, stid=stid)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.delete("/DeleteStudent/{stid}")
def delete_student(stid: str, db: Session = Depends(get_db)):
    DataValidation.stid_exists(db, stid)
    return crud.delete_student(db, stid=stid)


@app.patch("/UpdateStudent/{stid}")
def update_student(stid: str, student_update: schemas.Student, db: Session = Depends(get_db)):
    DataValidation.stid_exists(db, stid)
    return crud.patch_student(db, stid=stid, updated_student=student_update)
