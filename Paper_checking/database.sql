CREATE DATABASE checking;

USE checking;

CREATE TABLE paper(
subject_code varchar(20),
question_no varchar(10),
marks varchar(10)
);

INSERT INTO paper VALUES ("10135","5","2");

CREATE TABLE result(
Roll_no varchar(20),
Subject_code varchar(20),
marks varchar(10)
);

INSERT INTO result VALUES ("103","10135","2");

CREATE TABLE student_sheet(
subject_code varchar(20),
Answer varchar(5000),
roll_no varchar(10),
Name varchar(50)
);

INSERT INTO student_sheet VALUES ("10135","","103","Nisahd");

CREATE TABLE teacher_login(
username varchar(20),
password varchar(20)
);

INSERT INTO teacher_login VALUES ("Tec101","12345");

CREATE TABLE teacher_paper(
subject_code varchar(20),
Answer varchar(5000)
);

INSERT INTO teacher_paper VALUES ("10135","");

