CREATE TABLE Flights(
flno INTEGER PRIMARY KEY,
f_from varchar(24),
f_to varchar(24),
distane INTEGER,
departs TIME,
arrives TIME,
price INTEGER);

CREATE TABLE Aircraft(
aid INTEGER PRIMARY KEY,
aname varchar(24),
cruisinrange INTEGER);

CREATE TABLE Certified(
eid INTEGER REFERENCES Employees,
aid INTEGER REFERENCES Aircraft,
PRIMARY KEY (eid,aid));

CREATE TABLE Employees(
eid INTEGER PRIMARY KEY,
ename varchar(24),
salary INTEGER);

/* 1. Find the names of aircraft such that all pilots certified to operate them earn more than
80,000. */


SELECT A.aname
FROM Aircraft A
WHERE EXISTS 
(SELECT * FROM Certified C WHERE C.aid = A.aid and NOT EXISTS
(SELECT * FROM Employees E WHERE E.eid = C.eid and E.salary <= 80000));

/*2. For each pilot who is certified for more than three aircraft, 
find the eid and the maximum
cruisingrange of the aircraft that he (or she) is certified for. */

SELECT CE.eid,max(A.cruisinrange) as maxRange
FROM Certified CE,Aircraft A
WHERE CE.aid = A.aid 
GROUP BY C.eid
HAVING count(*) > 3;


/* 3. Find the names of pilots whose salary is less than the price of the cheapest route from
Los Angeles to Honolulu.
*/
SELECT E.ename
FROM Employees E
WHERE E.salary < (SELECT F1.price
FROM Flights F1
WHERE F1.f_from = "Los Angeles" and F1.f_to = "Honolulu" and F1.price < ALL (SELECT F.price
FROM Flights F
WHERE F.f_from = "Los Angeles" and F.f_to = "Honolulu"));

/* 4. For all aircraft with cruisingrange over 1,000 miles,find the name of the aircraft and the
average salary of all pilots certified for this aircraft. */

SELECT A.aname,AVG(E.salary)
FROM Certified C,Employees E,Aircraft A
WHERE C.eid = E.eid and C.aid in (SELECT A.aid
FROM Aircraft A
WHERE A.cruisinrange > 1000)
GROUP BY C.aid;

/* 5. Find the names of pilots certified for some Boeing aircraft. */

SELECT E.ename
FROM Employees E
WHERE EXISTS 
(SELECT * FROM Certified C
WHERE E.eid = C.eid
and C.aid in (SELECT A.aid FROM Aircraft A WHERE A.aname lIKE "Boeing%"));

/* 6. Find the aids of all aircraft that can be used on routes from Los Angeles to Chicago. */

SELECT A.aid
FROM Aircraft A
WHERE A.cruisinrange > 
(SELECT DISTINCT F.distane FROM Flights F 
WHERE F.f_from = "Los Angeles" and F.f_to="Chicago");

/* 7. Identify the flights that can be piloted by every pilot who makes more than $100,000.
(Hint: The pilot must be certified for at least one plane with a sufficiently large cruising
range.) */
SELECT *
FROM Flights
WHERE distane > (SELECT max(A.cruisinrange)
FROM Employees E,Certified C,Aircraft A
WHERE E.salary < 100000 and E.eid = C.eid and A.aid = C.aid);


/* 8. Print the enames of pilots who can operate planes with cruisingrange greater than 
3000 miles , but are not certified on any Boeing aircraft */

SELECT E.ename
FROM Employees E
WHERE EXISTS 
(SELECT * FROM Certified C,Aircraft A 
WHERE E.eid = C.eid and C.aid = A.aid and A.cruisinrange > 3000
and C.aid not in (SELECT A1.aid FROM Aircraft A1 WHERE A.aname="Boeing"));

/* 9. A customer wants to travel from Madison to New York with no more than two changes
of flight. List the choice of departure times from Madison if the customer wants to arrive
in New York by 6 p.m. */

SELECT F.departs
FROM Flights F
WHERE F.ﬂno IN ((SELECT F0.ﬂno
FROM Flights F0
WHERE F0.from = "Madison" AND F0.to = 'New York'
AND F0.arrives < "18:00" )
UNION
( SELECT F0.ﬂno
FROM Flights F0, Flights F1
WHERE F0.from = "Madison" AND F0.to <> "New York"
AND F0.to = F1.from AND F1.to = "New York"
AND F1.departs > F0.arrives
AND F1.arrives < "18:00" )
UNION
( SELECT F0.ﬂno
FROM Flights F0, Flights F1, Flights F2
WHERE F0.from = "Madison"
AND F0.to = F1.from
AND F1.to = F2.from
AND F2.to = "New York"
AND F0.to <> "New York"
AND F1.to <> "New York"
AND F1.departs > F0.arrives
AND F2.departs > F1.arrives
AND F2.arrives < "18:00" ))