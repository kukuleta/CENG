CREATE TABLE Suppliers 
(sid INTEGER PRIMARY KEY,
sname varchar(24),
adress varchar(24));

CREATE TABLE Parts 
(pid INTEGER PRIMARY KEY,
pname varchar(24),
color varchar(24));

CREATE TABLE Catalog 
(sid INTEGER REFERENCES Suppliers,
pid INTEGER REFERENCES Parts,
cost real,
PRIMARY KEY(sid,pid));
 
INSERT INTO Catalog VALUES (1,1,1.3);
INSERT INTO Catalog VALUES (2,2,1.4);
INSERT INTO Catalog VALUES (4,2,1.3);
INSERT INTO Catalog VALUES (2,3,1.3);
-- 1. Find the pnames of parts for which there is some supplier 

SELECT P.pname
FROM Parts P
WHERE EXISTS (SELECT * FROM Catalog C WHERE P.pid = C.pid);

-- 2. Find the snames of suppliers who supply every part 

SELECT S.sname
FROM Suppliers S
WHERE NOT EXISTS (
(SELECT P.pid FROM Parts P
EXCEPT
SELECT C1.pid FROM Catalog C1,Parts P1 WHERE S.sid = C1.sid and C1.pid = P1.pid);

-- 3. Find the snames of suppliers who supply every red part. 

SELECT S.sname
FROM Suppliers S
WHERE EXISTS
(SELECT P.pnames FROM Parts P WHERE P.color = "red"
EXCEPT
(SELECT P1.pnames FROM Parts P1,Catalog C1 WHERE S.sid = C1.sid and P1.pid = C1.pid

-- 4.Find the pnames of parts supplied by Acme Widget Suppliers and no one else 

SELECT P.pname
FROM Parts P
WHERE P.pid in
(SELECT C.pid
FROM Catalog C,Suppliers S
WHERE S.sname = "Acme Widget Suppliers" and S.sid = C.sid and 
NOT EXISTS (SELECT C.pid FROM Catalog C1 WHERE S.sid != C1.sid and C.pid = C1.pid)); 

/* 5. Find the sids of suppliers who charge more for some part than the average cost of
that part (averaged over all the suppliers who supply that part) */

SELECT S.sname, P.pname , C.cost
FROM Suppliers S,Parts P,Catalog C
WHERE S.sid = C.sid and P.pid = C.pid and C.cost >=
(SELECT AVG(C.cost)
FROM Catalog C
WHERE P.pid = C.pid
);

-- 6- For each part, ﬁnd the sname of the supplier who charges the most for that part 

SELECT S.sname,P.pname
FROM Suppliers S,Parts P,Catalog C
WHERE S.sid = C.sid and P.pid = C.pid and C.cost >=(
SELECT max(C.cost)
FROM Catalog C1
WHERE P.pid = C1.pid);

-- 7-Find the sids of suppliers who supply only red parts 

SELECT S.sid,S.sname
FROM Suppliers S,Parts P,Catalog C
WHERE S.sid = C.sid and P.pid = C.pid and P.pid not in
(SELECT C1.pid
FROM Catalog C1
WHERE S.sid = C1.sid and C1.pid in (SELECT P.pid FROM Parts P WHERE P.color <> "red"));

-- 8. Find the sids of suppliers who supply a red part and a green part. 

SELECT S.sid
FROM Suppliers S
WHERE S.sid in 
(
SELECT C.sid
FROM Catalog C,Parts P
WHERE C.pid = P.pid and P.color = "red"
INTERSECT
SELECT C.sid
FROM Catalog C,Parts P
WHERE C.pid = P.pid and P.color = "green"
);

-- 9. Find the sids of supplier s who supply a red part or a green part 


SELECT S.sid
FROM Suppliers S
WHERE S.sid in 
(
SELECT C.sid
FROM Catalog C,Parts P
WHERE C.pid = P.pid and P.color = "red"
UNION
SELECT C.sid
FROM Catalog C,Parts P
WHERE C.pid = P.pid and P.color = "green"
); 

/* 10. For every supplier that only supplies green parts, print the name of the supplier
and the total number of parts that she supplies. */

SELECT S.sname,count(*)
FROM Suppliers S,Parts P,Catalog C
WHERE S.sid = C.sid and P.pid = C.pid and C.pid not in
(SELECT C1.pid
FROM Catalog C1
WHERE S.sid = C1.sid and C1.pid in (SELECT P.pid FROM Parts P WHERE P.color <> "green"))
GROUP BY S.sid;
