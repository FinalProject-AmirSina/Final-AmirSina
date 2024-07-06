from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from .database import Base


class Course(Base):
    __tablename__ = "course"

    cid = Column(String, primary_key=True)
    cname = Column(String)
    department = Column(String)
    credit = Column(Integer)


class Lecturer(Base):
    __tablename__ = "lecturer"

    lid = Column(String, primary_key=True)
    fname = Column(String)
    lname = Column(String)
    id = Column(Integer)
    department = Column(String)
    major = Column(String)
    birth = Column(String)
    borncity = Column(String)
    address = Column(String)
    postalcode = Column(Integer)
    mphone = Column(String)
    tphone = Column(String)
    lcourseid = Column(String)


class Student(Base):
    __tablename__ = "student"

    stid = Column(String, primary_key=True)
    sfname = Column(String)
    slname = Column(String)
    sfather = Column(String)
    sbirth = Column(String)
    ids = Column(String)
    sborncity = Column(String)
    saddress = Column(String)
    spostalcode = Column(Integer)
    smphone = Column(String)
    stphone = Column(String)
    sdepartment = Column(String)
    smajor = Column(String)
    married = Column(String)
    sid = Column(Integer)
    scourseid = Column(String)
    lids = Column(String)
