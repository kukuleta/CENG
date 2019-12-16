CREATE TABLE Student 
(snum INTEGER,
sname VARCHAR(24),
major VARCHAR(24),
t_level VARCHAR(24),
age INTEGER,
PRIMARY KEY (snum));

CREATE TABLE Class
(class_name VARCHAR(24),
meets_at time,
room varchar(24),
fid integer REFERENCES Faculty,
PRIMARY KEY (class_name));

CREATE TABLE Enrolled 
(snum integer REFERENCES Student,
cname varchar(24) REFERENCES Class,
PRIMARY KEY (snum,cname)
);

CREATE TABLE Faculty
(fid integer,
fname varchar(24),
deptid integer,
 PRIMARY KEY (fid));

/* Q1/Find the names of all Juniors (Level = JR) who are enrolled in a class
taught by I. Teach. */

SELECT S.sname
FROM Student S,Enrolled E,Faculty F,Class C
WHERE S.snum = E.snum and E.cname = C.class_name 
and C.fid = F.fid and F.fname = "I.Teach" and S.t_level="JR";

/* 2. Find the age of the oldest student who is either a History major or is enrolled in a course
taught by I. Teach. */

SELECT Temp.sname, MAX(Temp.age) as maximumAge
FROM 
(SELECT S.sname,S.age
FROM Student S
WHERE (S.major = "History") -- S.age >= ALL (SELECT S1.age FROM Student S1) and -- (S.major = "History")
UNION
SELECT S.sname,S.age
FROM Student S,Enrolled E,Faculty F,Class C
WHERE S.snum = E.snum and E.cname = C.class_name 
and C.fid = F.fid and F.fname = "I.Teach") as Temp;

/* Find the names of all classes that either meet in room R128 
or have five or more students enrolled. */

SELECT C.class_name
FROM Class C
WHERE C.room = "R128" or C.cname IN 
(Select E.cname FROM Enrolled E
WHERE E.cname
GROUP BY E.cname
HAVING Count(*) >= 5);

/*4. Find the names of all students who are enrolled
 in two classes that meet at the same time. */

SELECT DISTINCT S.sname
FROM Enrolled E,Student S,Class C
WHERE S.snum = E.snum and C.class_name = E.cname and
EXISTS 
(SELECT * 
FROM Class C1 
WHERE C.class_name <> C1.class_name and C.meets_at = C1.meets_at and E.cname = C1.class_name);

/* 5. Find the names of faculty members who teach
 in every room in which some class is taught */

SELECT DISTINCT F.fname
FROM Faculty F
WHERE NOT EXISTS (( SELECT *
FROM Class C )
EXCEPT
(SELECT C1.room
FROM Class C1
WHERE C1.ﬁd = F.ﬁd ));

/* 6. Find the names of faculty members for whom the combined enrollment of the courses
that they teach is less than five */

SELECT TemporaryTable.fid,TemporaryTable.fname
FROM (SELECT F.fid,F.fname,count(*) as enrollmentCount
	FROM Enrolled E,Class C,Faculty F 
	WHERE F.fid = C.fid and E.cname = C.class_name 
	GROUP BY F.fid) as TemporaryTable
WHERE TemporaryTable.enrollmentCount > 5;

-- 7. Print the Level and the average age of students for that Level, for each level 

SELECT S.t_level, avg(S.t_level)
FROM Student S
GROUP BY t_level;


-- 8. Print the Level and the average age of students for that Level, for all Levels except JR 

SELECT S.t_level, avg(S.t_level)
FROM Student S
WHERE S.t_level <> "JR"
GROUP BY S.t_level;

-- 9. Find the names of students who are enrolled in the maximum number of classes 

SELECT DISTINCT sname, max(enrollmentCount)
FROM (SELECT S1.sname,count(*) as enrollmentCount 
		FROM Student S1,Enrolled E1,Class C1 
		WHERE S1.snum = E1.snum and E1.cname = C1.class_name
		GROUP BY S1.snum) AS temp;

-- 10. Find the names of students who are not enrolled in any classes 

SELECT DISTINCT S.sname
FROM Student S
WHERE S.snum not in (SELECT E.snum FROM Enrolled E);

/* 11. For each age value that appears in Students,Find the level value that appears most often.
For example, if there are more FR level students aged 18 than SR, JR, or SO students
aged 18, you should print the pair (18,FR) */

SELECT S.age, S.t_level
FROM Student S
GROUP BY S.age, S.t_level
HAVING S.t_level IN 
(SELECT S1.t_level
FROM Student S1
WHERE S1.age = S.age
GROUP BY S1.t_level, S1.age
HAVING COUNT (*) >= ALL (SELECT COUNT (*)
FROM Student S2
WHERE s1.age = S2.age
GROUP BY S2.t_level, S2.age));

