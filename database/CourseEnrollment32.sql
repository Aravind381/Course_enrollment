drop database CourseEnrollment;
create database CourseEnrollment;
use CourseEnrollment;

create table admin(
username VARCHAR(255),
password VARCHAR(255)
);

create table professor(
	professor_id int auto_increment primary key,
	first_name VARCHAR(255) not null, 
    last_name VARCHAR(255) not null, 
	email  VARCHAR(255) not null unique,
	phone  VARCHAR(255) not null unique,
	password VARCHAR(255) not null,
    designation  VARCHAR(255) not null,
    ssn  VARCHAR(255) not null,
    picture VARCHAR(255) not null,
	login_status VARCHAR(255)
);


create table department(
department_id int auto_increment primary key,
department_name VARCHAR(255)
);

create table student(
student_id  int auto_increment primary key,
first_name varchar(255) not null,
last_name varchar(255) not null,
email varchar(255) not null unique,
phone varchar (255)  not null unique,
password varchar(255)not null,
address varchar(255)not null,
state varchar(255)not null,
city varchar(255)not null,
zipcode varchar(255)not null,
ssn varchar(255)not null,
level varchar(255)not null
);

create table course(
course_id  int auto_increment primary key,
course_code varchar(255)not null,
course_name varchar(255) not null,
description varchar(255)not null,
course_picture varchar(255)not null,
credits varchar(255)not null
);


create table section(
section_id  int auto_increment primary key,
section_title varchar(255)not null,
crn varchar(255) not null unique,
start_time varchar(255)not null,
end_time varchar(255)not null,
enrollment_start_date datetime not null,
enrollment_end_date datetime  not null,
number_of_students varchar(255)not null,
day varchar(255)not null,
course_id int,
professor_id int,
department_id int,
foreign key (course_id) references course(course_id),
foreign key (professor_id) references professor(professor_id),
foreign key (department_id) references department(department_id)
);

create table course_material(
course_material_id  int auto_increment primary key,
course_material_name varchar(255) not null,
material_pdf varchar(255) not null,
description varchar(255)not null,
section_id int,
foreign key (section_id) references section(section_id)
);


create table enrollment(
enrollment_id  int auto_increment primary key,
grade varchar(255),
date varchar(255),
status varchar(255),
section_id int,
student_id int,
foreign key (section_id) references section(section_id),
foreign key (student_id) references student(student_id)
);






create table assignment(
assignment_id int auto_increment primary key,
assignment_title varchar(255),
assignment_pdf varchar(255),
date varchar(255),
submission_date varchar(255),
description varchar(255) not null,
status varchar(255),
section_id int,
foreign key (section_id) references section(section_id)
);






create table submissions(
submission_id int auto_increment primary key,
date varchar(255)  not null,
status varchar(255),
assignment_pdf varchar(255),
enrollment_id int,
assignment_id int,
foreign key (enrollment_id) references enrollment(enrollment_id),
foreign key (assignment_id) references assignment(assignment_id)
);











