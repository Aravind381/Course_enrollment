import os
import random
import datetime

from flask import Flask,request,session,render_template,redirect

import pymysql
from Mail import send_email

conn = pymysql.connect(host="localhost",db="CourseEnrollment",user="root",password='root')
cursor = conn.cursor()

app = Flask(__name__)
app.secret_key ="Course Enrollment"


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
Professor_files_path = APP_ROOT + "/static/files/professor_files"
Course_files_path = APP_ROOT + "/static/files/course_files"
Material_pdf_files_path = APP_ROOT + "/static/files/material_pdf_files"
Assignments_pdf_files_path = APP_ROOT + "/static/files/assignments"
Student_assignments_files_path = APP_ROOT + "/static/files/student_assignments"

admin_username = "admin"
admin_password = "admin"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")


@app.route("/professor_login")
def professor_login():
    return render_template("professor_login.html")


@app.route("/student_login")
def student_login():
    return render_template("student_login.html")


@app.route("/professor_home")
def professor_home():
    return render_template("professor_home.html")

@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")


@app.route("/student_registration")
def student_registration():
    return render_template("student_registration.html")


@app.route("/student_registration_action", methods=['post'])
def student_registration_action():
    otp = request.form.get("otp")
    otp2 = request.form.get("otp2")
    if otp != otp2:
        return render_template("message.html", message="Invalid Otp! Plz Try Again")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    ssn = request.form.get("ssn")
    password = request.form.get("password")
    address = request.form.get("address")
    state = request.form.get("state")
    city = request.form.get("city")
    zipcode = request.form.get("zipcode")
    level = request.form.get("level")
    count = cursor.execute("select * from student where ssn ='" + str(ssn) + "' ")
    if count > 0:
        return render_template("message.html", message="Duplicate SSN !")
    count = cursor.execute("select * from student where email ='" + str(email) + "' ")
    if count > 0:
        return render_template("message.html", message="Duplicate Email !")
    count = cursor.execute("select * from student where phone = '" + str(phone) + "' ")
    if count > 0:
        return render_template("message.html", message="Duplicate Phone Number")
    cursor.execute("insert into student(first_name,last_name,email,phone,password,ssn,address,state,city,zipcode,level)values('"+str(first_name)+"','"+str(last_name)+"','"+str(email)+"','"+str(phone)+"','"+str(password)+"','"+str(ssn)+"','"+str(address)+"','"+str(state)+"','"+str(city)+"','"+str(zipcode)+"','"+str(level)+"')")
    conn.commit()
    return render_template("message.html", message="Student Registration Successfully")


@app.route("/mail_verification")
def mail_verification():
    return render_template("mail_verification.html")


@app.route("/mail_verification_action", methods=['post'])
def mail_verification_action():
    email = request.form.get("email")
    otp = random.randint(1000,10000)
    print(otp)
    count = cursor.execute("select * from student where email='"+str(email)+"' ")
    if count > 0:
        send_email("OTP For Login ","OTP For Login Verification :  "+str(otp)+"",email)
        return render_template("/otp_with_login.html",email=email,otp=otp)
    else:
        send_email("OTP For Registration ", "Use This " + str(otp) + " To Register Your Account", email)
        return render_template("/student_registration.html", email=email,otp=otp)


@app.route("/otp_with_login")
def otp_with_login():
    return render_template("otp_with_login.html")


@app.route("/otp_with_login_action", methods=['post'])
def otp_with_login_action():
    otp = request.form.get("otp")
    otp2 = request.form.get("otp2")
    if otp != otp2:
        return render_template("message.html",message="Invalid Otp! Plz Try Again")
    else:
        email = request.form.get("email")
        cursor.execute("select * from student where email='"+str(email)+"'")
    student = cursor.fetchone()
    session['student_id'] = student[0]
    session['role'] = 'student'
    return redirect("/student_home")


@app.route("/student_home")
def student_home():
    cursor.execute("select * from student where student_id='"+str(session['student_id'])+"' ")
    student = cursor.fetchone()
    return render_template("student_home.html",student=student)


@app.route("/admin_login_action", methods=['post'])
def admin_login_action():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == admin_username and password == admin_password:
        count = cursor.execute("select * from admin")
        if count==0:
            cursor.execute("insert into admin(username,password)values('"+str(username)+"','"+str(password)+"')")
            conn.commit()
        session['role'] = 'admin'
        return redirect("/admin_home")
    else:
        return render_template("message.html", message="Invalid Login Credentials..!")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/professor")
def professor():
    keyword = request.args.get("keyword")
    if keyword == None:
        keyword =""
    if keyword == "":
        cursor.execute("select * from professor")
    else:
        cursor.execute("select * from professor where first_name like '%"+str(keyword)+"%' or last_name like '%"+str(keyword)+"%' or email like '%"+str(keyword)+"%' or designation like '%"+str(keyword)+"%'   ")
    professors = cursor.fetchall()
    return render_template("professor.html", professors=professors)


@app.route("/add_professor")
def add_professor():
    return render_template("add_professor.html")


@app.route("/add_professor_action", methods=['post'])
def add_professor_action():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    designation = request.form.get("designation")
    ssn = request.form.get("ssn")
    picture = request.files.get("picture")
    path = Professor_files_path + "/" + picture.filename
    picture.save(path)
    count = cursor.execute("select * from professor where ssn ='" + str(ssn) + "' ")
    if count > 0:
        return render_template("admin_message.html", message="Duplicate SSN !")
    count = cursor.execute("select * from professor where email ='"+str(email)+"' ")
    if count > 0:
        return render_template("admin_message.html", message="Duplicate Email !")
    count = cursor.execute("select * from professor where phone = '"+str(phone)+"' ")
    if count > 0:
        return render_template("admin_message.html", message="Duplicate Phone Number")
    cursor.execute("insert into professor(first_name,last_name,email,phone,password,designation,ssn,picture,login_status) values('"+str(first_name)+"','"+str(last_name)+"','"+str(email)+"','"+str(phone)+"','"+str(password)+"','"+str(designation)+"','"+str(ssn)+"','"+str(picture.filename)+"', '"+str(False)+"') ")
    conn.commit()
    return redirect("/professor")


@app.route("/professor_login_action", methods=['post'])
def professor_login_action():
    email = request.form.get("email")
    password = request.form.get("password")
    count = cursor.execute("select * from professor where email= '" + str(email) + "' and password = '" + str(password) + "' ")
    if count > 0:
        professor = cursor.fetchall()
        if str(professor[0][9]) == str("True"):
            session['professor_id'] = str(professor[0][0])
            session['role'] = 'professor'
            return redirect("/professor_home")
        else:
            session['professor_id'] = str(professor[0][0])
            session['role'] = 'professor'
            return render_template("change_professor_password.html")
    else:
        return render_template("message.html", message="Invalid Email and Password")


@app.route("/edit_professor_profile")
def edit_professor_profile():
    professor_id = request.args.get("professor_id")
    cursor.execute("select * from professor where professor_id='"+str(professor_id)+"' ")
    professor=cursor.fetchone()
    return render_template("edit_professor_profile.html",professor=professor)


@app.route("/edit_professor_profile_action",methods=['post'])
def edit_professor_profile_action():
    professor_id = request.form.get("professor_id")
    ssn = request.form.get("ssn")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    designation = request.form.get("designation")
    cursor.execute("update professor set first_name='"+str(first_name)+"',last_name='"+str(last_name)+"',email='"+str(email)+"', phone='"+str(phone)+"',designation='"+str(designation)+"',ssn='"+str(ssn)+"' where professor_id='"+str(professor_id)+"' ")
    conn.commit()
    return redirect("/professor")

@app.route("/change_professor_password_action", methods=['post'])
def change_professor_password_action():
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")
    professor = cursor.execute("select * from professor where professor_id='" + str(session['professor_id']) + "'")
    professor = cursor.fetchall()
    if str(new_password) != str(confirm_password):
        return render_template("professor_message.html", message="Invalid  confirm password")
    cursor.execute("update professor set password= '" + str(new_password) + "', login_status= '" + str(True) + "' where professor_id='" + str(session['professor_id']) + "' ")
    conn.commit()
    session['professor_id'] = str(professor[0][0])
    session['role'] = 'professor'
    return redirect("/professor_home")


@app.route("/department")
def department():
    message = request.args.get("message")
    if message == None:
        message = ""
    cursor.execute("select * from department ")
    departments=cursor.fetchall()
    return render_template("department.html",departments=departments,message=message)


@app.route("/edit_department")
def edit_department():
    department_id = request.args.get("department_id")
    cursor.execute("select * from department where department_id='"+str(department_id)+"' ")
    department=cursor.fetchone()
    return render_template("edit_department.html",department=department)


@app.route("/edit_department_action",methods=['post'])
def edit_department_action():
    department_id = request.form.get("department_id")
    department_name = request.form.get("department_name")
    cursor.execute("update department set department_name='"+str(department_name)+"' where department_id='"+str(department_id)+"' ")
    conn.commit()
    return redirect("/department")


@app.route("/add_department_action",methods=['post'])
def add_department_action():
    department_name = request.form.get("department_name")
    count = cursor.execute("select * from department where department_name='"+str(department_name)+"' ")
    if count > 0:
        return redirect("department?message=This Department Name Already Exist..!")
    else:
        cursor.execute("insert into department(department_name)values('"+str(department_name)+"')")
        conn.commit()
        return redirect("department?message=Department Added Successfully..")


@app.route("/course")
def course():
    if session['role']=="professor":
        cursor.execute("select * from course where course_id in(select section_id from section where  professor_id='"+str(session['professor_id'])+"')")
    keyword = request.args.get("keyword")
    if keyword == None:
        keyword = ""
    if keyword == "":
        cursor.execute("select * from course")
    else:
        cursor.execute("select * from course where course_code like '%" + str(keyword) + "%' or course_name like '%" + str(keyword) + "%'   ")
    courses=cursor.fetchall()
    return render_template("course.html",courses=courses)


@app.route("/add_course")
def add_course():
    message= request.args.get("message")
    if message== None:
        message =""
    return render_template("add_course.html",message=message)


@app.route("/add_course_action",methods=['post'])
def add_course_action():
    course_code = request.form.get("course_code")
    course_name = request.form.get("course_name")
    credits = request.form.get("credits")
    description = request.form.get("description")
    course_picture = request.files.get("course_picture")
    path = Course_files_path + "/" + course_picture.filename
    course_picture.save(path)
    count = cursor.execute("select * from course where course_code='" + str(course_code) + "' ")
    if count > 0:
        return redirect("add_course?message=This Course Code Already Exist..!")
    count = cursor.execute("select * from course where course_name='"+str(course_name)+"' ")
    if count > 0:
        return redirect("add_course?message=This Course Name Already Exist..!")
    else:
        cursor.execute("insert into course(course_code,course_name,description,course_picture,credits)values('"+str(course_code)+"','"+str(course_name)+"','"+str(description)+"','"+str(course_picture.filename)+"','"+str(credits)+"')")
        conn.commit()
        return redirect("course?message=Course Added Successfully..")


@app.route("/edit_course")
def edit_course():
    course_id = request.args.get("course_id")
    cursor.execute("select * from course where course_id='"+str(course_id)+"' ")
    course = cursor.fetchone()
    return render_template("edit_course.html",course=course)


@app.route("/edit_course_action", methods=['post'])
def edit_course_action():
    course_id= request.form.get("course_id")
    course_code = request.form.get("course_code")
    course_name = request.form.get("course_name")
    credits = request.form.get("credits")
    description = request.form.get("description")
    cursor.execute("update course set course_code='"+str(course_code)+"',course_name='"+str(course_name)+"',credits='"+str(credits)+"',description='"+str(description)+"' where course_id='"+str(course_id)+"' ")
    conn.commit()
    return redirect("/course")



@app.route("/section")
def section():
    course_id = request.args.get("course_id")
    if session['role']=='professor':
        if course_id is None:
            cursor.execute("select * from section where professor_id='" + str(session['professor_id']) + "'   ")
        else:
            cursor.execute("select * from section where professor_id='" + str(session['professor_id']) + "' and course_id='" + str(course_id) + "' ")
    elif session['role']=='admin':
        if course_id is None:
            cursor.execute("select * from section ")
        else:
            cursor.execute("select * from section where course_id='" + str(course_id) + "' ")
    elif session['role'] == 'student':
        if course_id is None:
            cursor.execute("select * from section ")
        else:
            cursor.execute("select * from section where course_id='" + str(course_id) + "' ")
    sections = cursor.fetchall()
    return render_template("section.html", sections=sections,get_professor_by_professor_id=get_professor_by_professor_id,get_course_by_course_id=get_course_by_course_id,get_department_by_department_id=get_department_by_department_id,get_is_enrollment_expired=get_is_enrollment_expired,get_enrollment_by_enrollment_id=get_enrollment_by_enrollment_id)


@app.route("/add_section")
def add_section():
    cursor.execute("select * from course")
    courses = cursor.fetchall()
    cursor.execute("select * from professor")
    professors = cursor.fetchall()
    cursor.execute("select * from department")
    departments = cursor.fetchall()
    return render_template("add_section.html", courses=courses, professors=professors,departments=departments)


@app.route("/add_section_action", methods=['post'])
def add_section_action():
    section_title = request.form.get("section_title")
    number_of_students = request.form.get("number_of_students")
    crn = request.form.get("crn")
    course_id = request.form.get("course_id")
    professor_id = request.form.get("professor_id")
    department_id = request.form.get("department_id")
    enrollment_start_date = request.form.get("enrollment_start_date")
    enrollment_end_date = request.form.get("enrollment_end_date")
    day = request.form.get("day")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    enrollment_start_date2 = datetime.datetime.strptime(enrollment_start_date, "%Y-%m-%d")
    enrollment_end_date2 = datetime.datetime.strptime(enrollment_end_date, "%Y-%m-%d")
    start_time2 = datetime.datetime.strptime(start_time,'%H:%M')
    start_time2 = start_time2.strftime("%H:%M")
    end_time2 = datetime.datetime.strptime(end_time, '%H:%M')
    end_time2 = end_time2.strftime("%H:%M")
    count = cursor.execute("select * from section where day='"+str(day)+"' and professor_id='"+str(professor_id)+"' and ((start_time >= '"+str(start_time2)+"' and start_time<= '"+str(end_time2)+"' and end_time >='"+str(start_time2)+"' and end_time >= '"+str(end_time2)+"') or (start_time <= '"+str(start_time2)+"' and start_time <= '"+str(end_time2)+"' and end_time >= '"+str(start_time2)+"' and end_time <= '"+str(end_time2)+"') or (start_time <= '"+str(start_time2)+"' and start_time <= '"+str(end_time2)+"' and end_time >= '"+str(start_time2)+"' and end_time >= '"+str(end_time2)+"') or (start_time <= '"+str(end_time2)+"' and start_time <= '"+str(end_time2)+"' and end_time <= '"+str(start_time2)+"' and end_time >= '"+str(end_time2)+"'))")
    if count == 0:
        count = cursor.execute("select * from section where crn = '"+str(crn)+"' ")
        if count == 0:
            if session["role"]=="admin":
                cursor.execute("insert into section(section_title,crn,course_id,professor_id,department_id,enrollment_start_date,enrollment_end_date,day,start_time,end_time,number_of_students) values('"+str(section_title)+"','"+str(crn)+"','"+str(course_id)+"','"+str(professor_id)+"','"+str(department_id)+"','"+str(enrollment_start_date)+"','"+str(enrollment_end_date)+"','"+str(day)+"','"+str(start_time2)+"','"+str(end_time2)+"','"+str(number_of_students)+"')")
            else:
                cursor.execute("insert into section(section_title,crn,course_id,professor_id,department_id,enrollment_start_date,enrollment_end_date,day,start_time,end_time,number_of_students) values('"+str(section_title)+"','"+str(crn)+"','"+str(course_id)+"','"+str(session['professor_id'])+"','"+str(department_id)+"','"+str(enrollment_start_date)+"','"+str(enrollment_end_date)+"','"+str(day)+"','"+str(start_time2)+"','"+str(end_time2)+"','"+str(number_of_students)+"')")
            conn.commit()
            return redirect("/section")
        return render_template("admin_message.html", message="This CRN Already Exist")
    else:
        return render_template("admin_message.html", message="There is a Time Collision For Section! ")



def get_professor_by_professor_id(professor_id):
    cursor.execute("select * from professor where professor_id = '"+str(professor_id)+"'")
    professors = cursor.fetchall()
    return professors[0]


def get_course_by_course_id(course_id):
    cursor.execute("select * from course where course_id= '"+str(course_id)+"'")
    courses = cursor.fetchall()
    return courses[0]


def get_department_by_department_id(department_id):
    cursor.execute("select * from department where department_id= '"+str(department_id)+"'")
    departments = cursor.fetchall()
    return departments[0]


def get_is_enrollment_expired(section_id,enrollment_start_date):
    c_date = datetime.date.today()
    count = cursor.execute("select * from section where section_id='"+str(section_id)+"' and '"+str(c_date)+"'>enrollment_start_date ")
    if count == 0:
        return True
    else:
        return False


@app.route("/course_material")
def course_material():
    section_id = request.args.get("section_id")
    cursor.execute("select * from section")
    sections = cursor.fetchall()
    return render_template("course_material.html", section_id=section_id, sections=sections)


@app.route("/course_material_action", methods=['post'])
def course_material_action():
    section_id = request.form.get("section_id")
    course_material_name = request.form.get("course_material_name")
    description = request.form.get("description")
    material_pdf = request.files.get("material_pdf")
    path = Material_pdf_files_path + "/" + material_pdf.filename
    material_pdf.save(path)
    cursor.execute("insert into course_material(section_id,course_material_name,description,material_pdf)values('"+str(section_id)+"','"+str(course_material_name)+"','"+str(description)+"','"+str(material_pdf.filename)+"') ")
    conn.commit()
    return render_template("professor_message.html", message="Course Material Added Successfully")


@app.route("/view_course_material")
def view_course_material():
    section_id = request.args.get("section_id")
    cursor.execute("select * from course_material where section_id= '"+str(section_id)+"' ")
    course_materials = cursor.fetchall()
    return render_template("view_course_material.html", section_id=section_id, course_materials=course_materials)


def get_enrollment_by_enrollment_id(enrollment_id):
    count = cursor.execute("select * from enrollment where section_id= '" + str(enrollment_id) + "' and student_id = '"+str(session['student_id'])+"' and status != 'Dropped' ")
    return count


@app.route("/enroll")
def enroll():
    section_id = request.args.get("section_id")
    student_id = session['student_id']
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    day = request.args.get("day")
    current_date = datetime.datetime.today()
    enrolled_date = current_date.strftime('%d-%m-%Y %H:%M')
    start_time2 = datetime.datetime.strptime(start_time, '%H:%M')
    start_time2 = start_time2.strftime("%H:%M")
    end_time2 = datetime.datetime.strptime(end_time, '%H:%M')
    end_time2 = end_time2.strftime("%H:%M")
    count = cursor.execute("select * from section where day='" + str(
        day) + "' and section_id in(select section_id from enrollment where student_id = '" + str(
        student_id) + "' and status ='"+str("Enrolled")+"') and ((start_time >= '" + str(
        start_time2) + "' and start_time<= '" + str(
        start_time2) + "' and end_time >='" + str(
        start_time2) + "' and end_time >= '" + str(
        end_time2) + "') or (start_time <= '" + str(
        end_time2) + "' and start_time <= '" + str(
        end_time2) + "' and end_time >= '" + str(
        start_time2) + "' and end_time <= '" + str(
        end_time2) + "') or (start_time <= '" + str(
        start_time2) + "' and start_time <= '" + str(
        end_time2) + "' and end_time >= '" + str(
        start_time2) + "' and end_time >= '" + str(
        end_time2) + "') or (start_time <= '" + str(
        end_time2) + "' and start_time <= '" + str(
        end_time2) + "' and end_time <= '" + str(
        end_time2) + "' and end_time >= '" + str(end_time2) + "'))")
    if count == 0:
        cursor.execute("insert into enrollment(section_id,student_id,date,status) values('"+str(section_id)+"','"+str(session['student_id'])+"','"+str(enrolled_date)+"', 'Enrolled' )  ")
        conn.commit()
        return redirect("/section")
    else:
        return render_template("student_message.html", message="There Is a Time conflict with existing section..!")


@app.route("/view_enrollments")
def view_enrollments():
    if session['role'] == 'student':
        cursor.execute("select * from enrollment where (status = '" + str('Enrolled') + "' or status = '" + str('Assigned Grade') + "')  and student_id = '"+str(session['student_id'])+"' ")
    elif session['role'] == 'professor':
        cursor.execute("select * from enrollment where (status = '" + str('Enrolled') + "' or status = '" + str('Assigned Grade') + "') and section_id in(select section_id from section where professor_id='"+str(session['professor_id'])+"') ")
    enrollments = cursor.fetchall()
    return render_template("view_enrollments.html", enrollments=enrollments, get_section_by_section_id=get_section_by_section_id, get_course_by_course_id2=get_course_by_course_id2,get_section_by_professor_id=get_section_by_professor_id,get_student_id_by_enrollment=get_student_id_by_enrollment)


def get_section_by_section_id(section_id):
    cursor.execute("select * from section where section_id = '"+str(section_id)+"' ")
    section = cursor.fetchall()
    return section[0]


def get_course_by_course_id2(course_id):
    cursor.execute("select * from course where course_id = '"+str(course_id)+"' ")
    course = cursor.fetchall()
    return course[0]


def get_section_by_professor_id(professor_id):
    cursor.execute("select * from professor where professor_id = '"+str(professor_id)+"' ")
    professor = cursor.fetchall()
    return professor[0]


@app.route("/assignments")
def assignments():
    cursor.execute("select * from section ")
    sections = cursor.fetchall()

    # cursor.execute("select * from assignment")
    # assignments = cursor.fetchall()
    cursor.execute("select * from assignment where section_id in(select section_id from section where professor_id='" + str(session['professor_id']) + "') ")
    assignments = cursor.fetchall()

    return render_template("assignments.html",sections=sections,assignments=assignments,get_section_id_by_assignment=get_section_id_by_assignment)


@app.route("/drop_enrollment")
def drop_enrollment():
    section_id = request.args.get("section_id")
    cursor.execute("update enrollment set status = 'Dropped' where section_id = '" + str(section_id) + "' and student_id='"+str(session['student_id'])+"' ")
    conn.commit()
    return render_template("student_message.html", message="Your Course Dropped Successfully")


@app.route("/student_assignments")
def student_assignments():
    enrollment_id = request.args.get("enrollment_id")
    section_id = request.args.get("section_id")

    # if session['role']=="professor":
    #     cursor.execute("select * from assignment where section_id in(select section_id from section where professor_id='" + str(session['professor_id']) + "') ")
    # elif session['role']=="student":
    #     cursor.execute("select * from assignment where student_id='" + str(session['student_id']) + "') ")
    cursor.execute("select * from assignment where section_id = '" + str(section_id) + "' ")
    assignments = cursor.fetchall()
    print(assignments)
    return render_template("student_assignments.html",assignments=assignments,get_section_id_by_assignment=get_section_id_by_assignment,enrollment_id=enrollment_id)


@app.route("/student_assignments_submission_action", methods=['post'])
def student_assignments_submission_action():
    enrollment_id = request.form.get("enrollment_id")
    assignment_id = request.form.get("assignment_id")
    assignment_pdf = request.files.get("assignment_pdf")
    path = Student_assignments_files_path + "/" + assignment_pdf.filename
    assignment_pdf.save(path)
    current_date = datetime.datetime.today()
    date = current_date.strftime('%d-%m-%Y %H:%M')
    print(date)
    cursor.execute("insert into submissions(assignment_id,date,assignment_pdf,status,enrollment_id)values('"+str(assignment_id)+"','"+str(date)+"','"+str(assignment_pdf.filename)+"','submitted','"+str(enrollment_id)+"') ")
    conn.commit()
    return redirect("/view_submission")


@app.route("/professor_assignment_action", methods=['post'])
def professor_assignment_action():
    section_id = request.form.get("section_id")
    assignment_title = request.form.get("assignment_title")
    assignment_pdf = request.files.get("assignment_pdf")
    description = request.form.get("description")
    path = Assignments_pdf_files_path + "/" + assignment_pdf.filename
    assignment_pdf.save(path)
    submission_date = request.form.get("submission_date")

    # submission_date2 = datetime.strptime(submission_date, '%Y-%m-%dT%H:%M')
    # formatted_date = submission_date2.strftime('%d-%m-%Y %H:%M')
    # print(formatted_date)

    current_date = datetime.datetime.today()
    date = current_date.strftime('%d-%m-%Y %H:%M')

    cursor.execute("insert into assignment(assignment_title,assignment_pdf,description,date,submission_date,section_id,status)values('"+str(assignment_title)+"','"+str(assignment_pdf.filename)+"','"+str(description)+"','"+str(date)+"','"+str(submission_date)+"','"+str(section_id)+"','Assignment Posted') ")
    conn.commit()
    return redirect("/assignments")

def get_section_id_by_assignment(section_id):
    cursor.execute("select * from section where section_id = '"+str(section_id)+"' ")
    section = cursor.fetchall()
    return section[0]


def get_assignment_id_by_submission(assignment_id):
    cursor.execute("select * from assignment where assignment_id = '"+str(assignment_id)+"' ")
    assignment = cursor.fetchall()
    return assignment[0]

def get_student_id_by_enrollment(student_id):
    cursor.execute("select * from student where student_id = '"+str(student_id)+"' ")
    student = cursor.fetchall()
    return student[0]


@app.route("/view_submission")
def view_submission():
    if session['role']=='student':
        cursor.execute("select * from submissions where enrollment_id in(select enrollment_id from enrollment where student_id='" + str(session['student_id']) + "') ")
    elif session['role']=='professor':
        cursor.execute("select * from submissions where enrollment_id in(select enrollment_id from enrollment where section_id in (select section_id from section where professor_id='"+str(session['professor_id'])+"') )")
    submissions=cursor.fetchall()
    return render_template("view_submission.html",submissions=submissions,get_assignment_id_by_submission=get_assignment_id_by_submission)



@app.route("/assign_grade")
def assign_grade():
    enrollment_id = request.args.get("enrollment_id")
    submission_id = request.args.get("submission_id")
    return render_template("assign_grade.html", enrollment_id=enrollment_id,submission_id=submission_id)


@app.route("/assign_grade_action", methods=['post'])
def assignGrade_action():
    enrollment_id = request.form.get("enrollment_id")
    submission_id = request.form.get("submission_id")
    grade = request.form.get("grade")
    cursor.execute("update enrollment set grade = '" + str(grade) + "',status = '" + str('Assigned Grade') + "' where enrollment_id = '"+str(enrollment_id)+"' ")
    conn.commit()
    cursor.execute("update submissions set status = '" + str('Assigned Grade') + "' where submission_id = '" + str(submission_id) + "' ")
    conn.commit()
    return render_template("professor_message.html", message="Grade Assigned Successfully")


app.run(debug=True)
