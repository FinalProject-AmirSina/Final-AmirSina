from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from re import search

from . import crud, models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# -----------------Necessary Lists & Datas:--------------------

def is_persian(input_string: str):

    pattern = r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]"
    if search(pattern, input_string):
        return True
    return False


def special_char(text: str):

    special_ch = any(chr.isdigit() or (not chr.isalnum()) and chr != '-' and chr != ' ' for chr in text)
    if special_ch:
        return True
    else:
        return False


# --------------------------------------------------------------

valid_city = ["تبریز", "ارومیه", "اردبیل", "اصفهان", "البرز", "ایلام", "بجنورد", "بندرعباس", "بوشهر", "بیرجند", "تبریز",
              "تهران", "خرم آباد", "رشت", "زاهدان", "زنجان", "ساری", "سمنان", "سنندج", "شهرکرد", "شیراز", "قزوین", "قم",
              "کرج", "کرمان", "کرمانشاه", "گرگان", "مشهد", "همدان", "یاسوج", " یزد"]

code_number = ["041", "044", "045", "031", "026", "084", "077", "021", "038", "056", "051", "058", "061", "024", "023",
               "054", " 071", "028", "025", "087", "034", "083", "074", "017", "013", "066", "011", "086", "076", "081",
               "035"]

code_number2 = ["33", "32", "34", "42", "43", "44", "52", "53", "54", "50", "40", "30", "36"]

valid_department = ["علوم انسانی", "فنی و مهندسی", "علوم پایه", "دامپزشکی", "اقتصاد", "کشاورزی", "منابع طبیعی"]

valid_major = ["مهندسی عمران", "مهندسی هوافضا", "مهندسی صنایع", "مهندسی مکانیک",
               "مهندسی نفت", "مهندسی کامپیوتر", "مهندسی معماری", "مهندسی برق"]

valid_input = "مجرد  متاهل"

# --------------------------------------------------------------


class DataValidation(BaseModel):
    # ------------------Course validation-----------------------

    # Course Id
    def cid_exists(db: Session, cid: str):
        course_exists = db.query(models.Course).filter(models.Course.cid == cid).first()
        if not course_exists:
            raise HTTPException(status_code=404, detail="Course not found")

    def cid_check(cid: str):
        if not len(cid) == 5:
            raise HTTPException(status_code=400, detail="Invalid Course Id. Cid must be 5 digits")

    def cid_duplicate_check(db: Session, cid: str):
        duplicate_cid_exists = db.query(models.Course).filter(models.Course.cid == cid).first()
        if duplicate_cid_exists:
            raise HTTPException(status_code=409, detail=f"Duplicate Course Id, cid: {cid} already exists")

    # Course Name
    def cname_check(cname: str):
        if len(cname) > 25:
            raise HTTPException(status_code=400, detail="Invalid CName. cname must be Maximum 25 digits")
        if is_persian(cname) == False:
            raise HTTPException(status_code=400, detail="Invalid CName. cname must be persian!")
        if special_char(cname) == True:
            raise HTTPException(status_code=400, detail="Invalid CName. cname must don't have any special characters")

    # Department
    def department_check(department: str):
        if department not in valid_department:
            raise HTTPException(status_code=400, detail="Invalid department.")

    # Credit
    def credit_check(credit: int):
        if not 1 <= credit < 4:
            raise HTTPException(status_code=400, detail="Invalid credit. Must be between 1 and 4")

    # ------------------Lecturer validation-----------------------

    # Lecturer Id
    def lid_exists(db: Session, lid: str):
        lid_exists = db.query(models.Lecturer).filter(models.Lecturer.lid == lid).first()
        if not lid_exists:
            raise HTTPException(status_code=404, detail="lid not found")

    def lid_check(lid: str):
        if not len(lid) == 6:
            raise HTTPException(status_code=400, detail="Invalid Lecturer Id. lid must be 6 digits")

    def lid_duplicate_check(db: Session, lid: str):
        duplicate_lid_exists = db.query(models.Lecturer).filter(models.Lecturer.lid == lid).first()
        if duplicate_lid_exists:
            raise HTTPException(status_code=409, detail=f"Duplicate Lecturer Id, lid: {lid} already exists")

    # Lecturer First Name
    def fname_check(fname: str):
        if len(fname) > 10:
            raise HTTPException(status_code=400, detail="Invalid fname. fname must be Maximum 10 digits")
        if is_persian(fname) == False:
            raise HTTPException(status_code=400, detail="Invalid fname. fname must be persian!")
        if special_char(fname) == True:
            raise HTTPException(status_code=400, detail="Invalid fname. fname must don't have any special characters")

    # Lecturer Last Name
    def lname_check(lname: str):
        if len(lname) > 10:
            raise HTTPException(status_code=400, detail="Invalid lname. lname must be Maximum 10 digits")
        if is_persian(lname) == False:
            raise HTTPException(status_code=400, detail="Invalid lname. lname must be persian!")
        if special_char(lname) == True:
            raise HTTPException(status_code=400, detail="Invalid lname. lname must don't have any special characters")

    # Lecturer Code Melli
    def check_codemelli(id: int):
        if not id:
            raise HTTPException(status_code=400, detail="Lecturer not found")

        if not str(id).isdigit() or len(str(id)) != 10:
            raise HTTPException(status_code=400, detail="Id must be a number and have 10 digits")

        if str(id).count(str(id)[0]) == len(str(id)):
            raise HTTPException(status_code=400, detail="Invalid id")

        total = sum(int(str(id)[i]) * (10 - i) for i in range(9))
        remainder = total % 11
        check_digit = int(str(id)[9])

        if remainder < 2 and check_digit == remainder:
            return {"message": "Code melli is valid"}
        elif str(id) == "0123456789":
            return {"message": "Code melli is invalid!"}
        elif remainder >= 2 and check_digit == 11 - remainder:
            return {"message": "Code melli is valid"}
        else:
            raise HTTPException(status_code=400, detail="Invalid id")

    # Lecturer Department
    def ldepartment(department: str):
        if department not in valid_department:
            raise HTTPException(status_code=400, detail="department is not valid")
        else:
            return {"message": f"department is valid:{department}"}

    # Lecturer Major
    def check_Lecturer_major(major: str):
        if major not in valid_major:
            raise HTTPException(status_code=400, detail="Major is not valid")
        else:
            return {"message": f"Major is valid:{major}"}

    # Lecturer Birthdate
    def kabise(year: int, month: int, day: int):
        days_in_month = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]

        if (year % 33 == 1 or year % 33 == 5 or year % 33 == 9 or
                year % 33 == 13 or year % 33 == 17 or year % 33 == 22 or
                year % 33 == 26 or year % 33 == 30):  # بررسی کبیسه بودن سال مورد نظر
            days_in_month[11] = 30  # در سال کبیسه اسفند ماه 30 روز دارد

        if 1 <= month <= 12 and 1 <= day <= days_in_month[month - 1]:
            return True
        return False

    def valid_lecturer_birth(birth: str):
        if len(birth) == 10 and birth[4] == '/' and birth[7] == '/':
            year, month, day = birth.split('/')
            if year.isdigit() and month.isdigit() and day.isdigit():
                return {"message": f"Birth date is valid: {birth}"}
        else:
            raise HTTPException(status_code=400, detail="Invalid birthdate format!")

    # Lecturer born city
    def valid_lecturer_borncity(borncity: str):
        if borncity not in valid_city:
            raise HTTPException(status_code=400, detail="city name is not valid")
        else:
            return {"message": f"City name is valid:{borncity}"}

    # Lecturer Address
    def lecturer_address(address: str):
        if not address:
            raise HTTPException(status_code=400, detail="Inter an address.")
        if len(address) > 100:
            raise HTTPException(status_code=400, detail="Address too long. Its must be less than 100 digits.")
        if len(address) < 10:
            raise HTTPException(status_code=400, detail="Address too short. Its must be more than 10 digits.")
        else:
            return {"message": "your address is valid"}

    # Lecturer Postalcode
    def lecturer_postalcode(postalcode: int):
        if not str(postalcode).isdigit() or len(str(postalcode)) != 10:
            raise HTTPException(status_code=400, detail="postal code invalid. Its must be numbers and be 10 digits.")
        else:
            return {"message": "your postal code is valid"}

    # Lecturer Mobile Phone
    def lecturer_mphone(mphone: str):
        if len(mphone) != 13:
            raise HTTPException(status_code=400, detail="Phone number must be equal to 13 digits.")
        if not mphone[:3] == "098":
            raise HTTPException(status_code=400, detail="The 1st part of number must start with 098.")

        region_number1 = mphone[3:6]  # اولین عدد سه رقمی(پیش شماره)
        region_number2 = mphone[6:9]  # دومین عدد سه رقمی(اعداد میانی)
        unique_number = mphone[9:]  # چهار رقم آخر

        if not region_number1.isnumeric() or not "900" <= region_number1 <= "999":
            raise HTTPException(status_code=400, detail="The 2nd part of number must be between 900 and 999.")
        if not region_number2.isnumeric() or not "000" <= region_number2 <= "999":
            raise HTTPException(status_code=400, detail="The 3rd part of number must be between 100 and 999.")
        if not unique_number.isnumeric() or not "0000" <= unique_number <= "9999":
            raise HTTPException(status_code=400, detail="The last 4 digits of number must be between 1000 and 9999.")
        return {"message": "Your phone number is valid"}

    # Lecturer Telephone
    def lecturer_telephone(tphone: str):
        if len(tphone) != 11:
            raise HTTPException(status_code=400, detail="TelePhone number must be equal to 11 digits.")
        if tphone[:3] not in code_number:
            raise HTTPException(status_code=400, detail="The 1st part of Telephone number must be in code numbers.")

        region_number1 = tphone[3:5]  # اولین عدد دو رقمی(کد شهر)
        region_number2 = tphone[5:7]  # دومین عدد دو رقمی
        unique_number = tphone[7:]  # چهار رقم آخر

        if not region_number1.isdigit() or not region_number1 in code_number2:
            raise HTTPException(status_code=400, detail="The 2nd part of Tphone must be in valid coded.")
        if not region_number2.isdigit() or not 10 <= int(region_number2) <= 99:
            raise HTTPException(status_code=400, detail="The 3rd part of Tphone must be between 10 and 99.")
        if not unique_number.isdigit() or not 0000 <= int(unique_number) <= 9999:
            raise HTTPException(status_code=400, detail="The  last 4 digits of Tphone must be between 1000 and 9999.")
        else:
            return {"message": "Your telephone is valid"}

    # Lecturer Course ID
    def lcourseid_check(db: Session, lcourseid: str):
        cid = lcourseid.split("-")
        for cid in cid:
            scid = crud.get_course(db, cid)
            if scid is None:
                raise HTTPException(status_code=400, detail="scourseid not found! (separate scourseid with '-')")

    # ------------------Student validation-----------------------

    # Student Number
    def stid_exists(db: Session, stid: str):
        stid_exists = db.query(models.Student).filter(models.Student.stid == stid).first()
        if not stid_exists:
            raise HTTPException(status_code=404, detail="stid not found")

    def check_stid(stid: str):
        if len(stid) != 11:
            raise HTTPException(status_code=400, detail="Student number must be equal to 11 digits.")

        if not (400 <= int(stid[:3]) <= 402):
            raise HTTPException(status_code=400, detail="The first three digits must be between 400 and 402.")

        if int(stid[3:9]) != 114150:
            raise HTTPException(status_code=400, detail="The middle digits must be 114150.")

        if not (1 <= int(stid[9:]) <= 99):
            raise HTTPException(status_code=400, detail="The last two digits must be between 01 and 99.")
        return {"message": "student number is valid"}

    def stid_duplicate_check(db: Session, stid: str):
        duplicate_stid_exists = db.query(models.Student).filter(models.Student.stid == stid).first()
        if duplicate_stid_exists:
            raise HTTPException(status_code=409, detail=f"Duplicate Student Id, stid: {stid} already exists")

    # Student first Name
    def sfname_check(sfname: str):
        if len(sfname) > 10:
            raise HTTPException(status_code=400, detail="Invalid sfname. sfname must be Maximum 10 digits")
        if is_persian(sfname) == False:
            raise HTTPException(status_code=400, detail="Invalid sfname. sfname must be persian!")
        if special_char(sfname) == True:
            raise HTTPException(status_code=400, detail="Invalid sfname. sfname must don't have any special characters")

    # Student Last Name
    def slname_check(slname: str):
        if len(slname) > 10:
            raise HTTPException(status_code=400, detail="Invalid slname. slname must be Maximum 10 digits")
        if is_persian(slname) == False:
            raise HTTPException(status_code=400, detail="Invalid slname. slname must be persian!")
        if special_char(slname) == True:
            raise HTTPException(status_code=400, detail="Invalid slname. slname must don't have any special characters")

    # Student Father Name
    def sfather_check(sfather: str):
        if len(sfather) > 10:
            raise HTTPException(status_code=400, detail="Invalid sfather. sfather must be Maximum 10 digits")
        if is_persian(sfather) == False:
            raise HTTPException(status_code=400, detail="Invalid sfather. sfather must be persian!")
        if special_char(sfather) == True:
            raise HTTPException(status_code=400, detail="Invalid sfather. sfather must don't have special characters")

    # Student Birthdate
    def valid_student_birth(sbirth: str):
        if len(sbirth) == 10 and sbirth[4] == '/' and sbirth[7] == '/':
            year, month, day = sbirth.split('/')
            if year.isdigit() and month.isdigit() and day.isdigit():
                return {"message": f"Birth date is valid: {sbirth}"}
        else:
            raise HTTPException(status_code=400, detail="Invalid birthdate format!")

    # Student Serial ID
    def serial_number(ids: str):
        if len(ids) != 10:
            raise HTTPException(status_code=400, detail="Serial number must be equal to 10 digits.")
        first_digit = ids[0]
        if is_persian(first_digit) == False:
            raise HTTPException(status_code=400, detail="The 1st digit must be a Persian letter.")

        region_code = ids[1:3]  # یک عدد دو رقمی
        unique_number = ids[4:]  # یک عدد شش رقمی

        if ids[3] != "/":
            raise HTTPException(detail="invalid parameter. 4th digit must be /.", status_code=400)

        if not region_code.isdigit() or not (1 <= int(region_code) <= 99):
            raise HTTPException(status_code=400, detail="The 2nd and 3rd digits must be number between 01 and 99.")

        if not unique_number.isdigit() or not (1 <= int(unique_number) <= 999999):
            raise HTTPException(status_code=400, detail="The last 6 digits must be number between 000001 and 999999.")
        return {"message": f"student number is valid: {ids}"}

    # Student born city
    def valid_student_borncity(sborncity: str):
        if sborncity not in valid_city:
            raise HTTPException(status_code=400, detail="city name is not valid")
        else:
            return {"message": f"City name is valid:{sborncity}"}

    # Student Address
    def student_address(saddress: str):
        if not saddress:
            raise HTTPException(status_code=400, detail="Inter an address.")
        if len(saddress) > 100:
            raise HTTPException(status_code=400, detail="Address too long. Its must be less than 100 digits.")
        if len(saddress) < 10:
            raise HTTPException(status_code=400, detail="Address too short. Its must be more than 10 digits.")
        else:
            return {"message": "your address is valid"}

    # Student Postalcode
    def student_postalcode(spostalcode: int):
        if not str(spostalcode).isdigit() or len(str(spostalcode)) != 10:
            raise HTTPException(status_code=400, detail="postal code invalid. Its must be numbers and be 10 digits.")
        else:
            return {"message": "your postal code is valid"}

    # Student Mobile Phone
    def student_mphone(smphone: str):
        if len(smphone) != 13:
            raise HTTPException(detail="Phone number must be equal to 13 digits.",
                                status_code=400)
        if smphone[:3] != "098":
            raise HTTPException(detail="The 1st part of number must be 098.", status_code=400)

        region_number1 = smphone[3:6]  # اولین عدد سه رقمی(پیش شماره)
        region_number2 = smphone[6:9]  # دومین عدد سه رقمی(اعداد میانی)
        unique_number = smphone[9:]  # چهار رقم آخر

        if not region_number1.isdigit() or not 900 <= int(region_number1) <= 999:
            raise HTTPException(status_code=400, detail="The 2nd part of number must be between 900 and 999.")
        if not region_number2.isdigit() or not 000 <= int(region_number2) <= 999:
            raise HTTPException(status_code=400, detail="The 3rd part of number must be between 100 and 999.")
        if not unique_number.isdigit() or not 0000 <= int(unique_number) <= 9999:
            raise HTTPException(status_code=400, detail="The  last 4 digits of number must be between 1000 and 9999.")
        else:
            return {"message": "Your phone number is valid"}

    # Student Telephone
    def student_telephone(stphone: str):
        if len(stphone) != 11:
            raise HTTPException(status_code=400, detail="TelePhone number must be equal to 11 digits.")
        if stphone[:3] not in code_number:
            raise HTTPException(status_code=400, detail="The 1st part of Telephone number must be in code numbers.")

        region_number1 = stphone[3:5]  # اولین عدد دو رقمی(کد شهر)
        region_number2 = stphone[5:7]  # دومین عدد دو رقمی
        unique_number = stphone[7:]  # چهار رقم آخر

        if not region_number1.isdigit() or not region_number1 in code_number2:
            raise HTTPException(status_code=400, detail="The 2nd part of Tphone must be in valid coded.")
        if not region_number2.isdigit() or not 10 <= int(region_number2) <= 99:
            raise HTTPException(status_code=400, detail="The 3rd part of Tphone must be between 10 and 99.")
        if not unique_number.isdigit() or not 0000 <= int(unique_number) <= 9999:
            raise HTTPException(status_code=400, detail="The  last 4 digits of Tphone must be between 1000 and 9999.")
        else:
            return {"message": "Your telephone is valid"}

    # Student Department
    def sdepartment(sdepartment: str):
        if sdepartment not in valid_department:
            raise HTTPException(status_code=400, detail="department is not valid")
        else:
            return {"message": f"student department is valid:{sdepartment}"}

    # Student Major
    def check_student_major(smajor: str):
        if smajor not in valid_major:
            raise HTTPException(status_code=400, detail="Major is not valid")
        else:
            return {"message": f"Major is valid:{smajor}"}

    # Student Marital
    def marital(married: str):
        if not married:
            raise HTTPException(detail="Please inter your Marital.", status_code=400)
        if married not in valid_input:
            raise HTTPException(detail="Marital is invalid", status_code=400)
        else:
            return {f" Marital is valid: {married}"}

    # Student CodeMelli
    def check_student_id(sid: int):
        if not str(sid).isdigit() or len(str(sid)) != 10:
            raise HTTPException(status_code=400, detail="Student Code melli must be a number and have 10 digits")

        if str(sid).count(str(sid)[0]) == len(str(sid)):
            raise HTTPException(status_code=400, detail="Invalid student Code melli")

        total = sum(int(str(sid)[i]) * (10 - i) for i in range(9))
        remainder = total % 11
        check_digit = int(str(sid)[9])

        if remainder < 2 and check_digit == remainder:
            return {"message": "Student Code melli is valid"}
        if str(sid) == "0123456789":
            raise HTTPException(status_code=400, detail="Invalid Student Code melli")
        elif remainder >= 2 and check_digit == 11 - remainder:
            return {"message": "Student Code melli is valid"}
        else:
            raise HTTPException(status_code=400, detail="Invalid Student Code melli")

    # Student's Course ID
    def scourseid_check(db: Session, scourseid: str):
        cid = scourseid.split("-")
        for cid in cid:
            scid = crud.get_course(db, cid=cid)
            if scid is None:
                raise HTTPException(status_code=400, detail="scourseid not found! (separate scourseid with '-')")

    # Student's Lecturer ID
    def lids_check(db: Session, lids: str):
        lid_list = lids.split("-")
        for lid in lid_list:
            lecturer = crud.get_lecturer(db, lid=lid)
            if lecturer is None:
                raise HTTPException(status_code=400, detail="lid not found! (separate lids with '-')")
