from sqlalchemy.orm import Session
from . import models, schemas


# ---------------Course-----------------
def get_course(db: Session, cid: int):
    return db.query(models.Course).filter(models.Course.cid == cid).first()


def create_course(db: Session, course: schemas.Course):
    db_course = models.Course(cid=course.cid, cname=course.cname, department=course.department, credit=course.credit)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course(db: Session, cid: int):
    db_course = db.query(models.Course).filter(models.Course.cid == cid).first()
    if db_course:
        db.delete(db_course)
        db.commit()
        return "Successfully deleted"
    else:
        return "Course not found"


def patch_course(db: Session, cid: int, updated_course: schemas.Course):
    db_course = db.query(models.Course).filter(models.Course.cid == cid).first()
    if db_course:
        db_course.cname = updated_course.cname
        db_course.department = updated_course.department
        db_course.credit = updated_course.credit
        db.commit()
        db.refresh(db_course)
        return db_course
    else:
        return "Course not found"


# ---------------Lecturer-----------------
def get_lecturer(db: Session, lid: int):
    return db.query(models.Lecturer).filter(models.Lecturer.lid == lid).first()


def create_lecturer(db: Session, lecturer: schemas.Lecturer):
    db_lecturer = models.Lecturer(lid=lecturer.lid, fname=lecturer.fname, lname=lecturer.lname, id=lecturer.id,
                                  department=lecturer.department, major=lecturer.major, birth=lecturer.birth,
                                  borncity=lecturer.borncity, address=lecturer.address, postalcode=lecturer.postalcode,
                                  mphone=lecturer.mphone, tphone=lecturer.tphone, lcourseid=lecturer.lcourseid)
    db.add(db_lecturer)
    db.commit()
    db.refresh(db_lecturer)
    return db_lecturer


def delete_lecturer(db: Session, lid: int):
    db_lecturer = db.query(models.Lecturer).filter(models.Lecturer.lid == lid).first()
    if db_lecturer:
        db.delete(db_lecturer)
        db.commit()
        return "Successfully deleted"
    else:
        return "Lecturer ID not found"


def patch_lecturer(db: Session, lid: int, updated_lecturer: schemas.Lecturer):
    db_lecturer = db.query(models.Lecturer).filter(models.Lecturer.lid == lid).first()
    if db_lecturer:
        db_lecturer.fname = updated_lecturer.fname
        db_lecturer.lname = updated_lecturer.lname
        db_lecturer.id = updated_lecturer.id
        db_lecturer.department = updated_lecturer.department
        db_lecturer.major = updated_lecturer.major
        db_lecturer.birth = updated_lecturer.birth
        db_lecturer.borncity = updated_lecturer.borncity
        db_lecturer.address = updated_lecturer.address
        db_lecturer.postalcode = updated_lecturer.postalcode
        db_lecturer.mphone = updated_lecturer.mphone
        db_lecturer.tphone = updated_lecturer.tphone
        db_lecturer.lcourseid = updated_lecturer.lcourseid
        db.commit()
        db.refresh(db_lecturer)
        return db_lecturer
    else:
        return "Lecturer not found"


# ---------------Student-----------------
def get_student(db: Session, stid: int):
    return db.query(models.Student).filter(models.Student.stid == stid).first()


def create_student(db: Session, student: schemas.Student):
    db_student = models.Student(stid=student.stid, sfname=student.sfname, slname=student.slname, sfather=student.sfather,
                                sbirth=student.sbirth, ids=student.ids, sborncity=student.sborncity,
                                saddress=student.saddress, spostalcode=student.spostalcode, smphone=student.smphone,
                                stphone=student.stphone, sdepartment=student.sdepartment, smajor=student.smajor,
                                married=student.married, sid=student.sid, scourseid=student.scourseid, lids=student.lids)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, stid: int):
    db_student = db.query(models.Student).filter(models.Student.stid == stid).first()
    if db_student:
        db.delete(db_student)
        db.commit()
        return "Successfully deleted"
    else:
        return "Student ID not found"


def patch_student(db: Session, stid: int, updated_student: schemas.Student):
    db_student = db.query(models.Student).filter(models.Student.stid == stid).first()
    if db_student:
        db_student.sfname = updated_student.sfname
        db_student.slname = updated_student.slname
        db_student.sfather = updated_student.sfather
        db_student.sbirth = updated_student.sbirth
        db_student.ids = updated_student.ids
        db_student.sborncity = updated_student.sborncity
        db_student.saddress = updated_student.saddress
        db_student.spostalcode = updated_student.spostalcode
        db_student.smphone = updated_student.smphone
        db_student.stphone = updated_student.stphone
        db_student.sdepartment = updated_student.sdepartment
        db_student.smajor = updated_student.smajor
        db_student.married = updated_student.married
        db_student.sid = updated_student.sid
        db_student.scourseid = updated_student.scourseid
        db_student.lids = updated_student.lids
        db.commit()
        db.refresh(db_student)
        return db_student
    else:
        return "Student not found"
