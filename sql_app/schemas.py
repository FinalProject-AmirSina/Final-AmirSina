from pydantic import BaseModel


class Course(BaseModel):
    cid: str
    cname: str
    department: str
    credit: int


class Lecturer(BaseModel):
    lid: str
    fname: str
    lname: str
    id: int
    department: str
    major: str
    birth: str
    borncity: str
    address: str
    postalcode: int
    mphone: str
    tphone: str
    lcourseid: str


class Student(BaseModel):
    stid: str
    sfname: str
    slname: str
    sfather: str
    sbirth: str
    ids: str
    sborncity: str
    saddress: str
    spostalcode: int
    smphone: str
    stphone: str
    sdepartment: str
    smajor: str
    married: str
    sid: int
    scourseid: str
    lids: str
