CREATE TABLE Employee
(eid integer PRIMARY KEY,
ename varchar(24),
age integer,
salary real,
CONSTRAINT must_be_greater_than_10000 CHECK (salary > 10000));

CREATE TABLE Works
(eid integer,
did integer,
pct_time integer,
PRIMARY KEY(eid,did),
FOREIGN KEY (eid) REFERENCES Employee(eid) ON DELETE CASCADE,
FOREIGN KEY (did) REFERENCES Departmen(did) ON DELETE CASCADE);

CREATE TABLE Departmen
(did integer PRIMARY KEY,
dname varchar(24),
budget real,
managerid integer ,
FOREIGN KEY (managerid) REFERENCES Employee(eid) ON DELETE SET NULL);

ALTER TABLE Departmen ADD CONSTRAINT must_be_older_than_30
CHECK ((SELECT E.age FROM Employee E, Departmen D WHERE E.eid = D.managerid) > 30);

/*3. Define an assertion on Dept that will ensure that all managers have age > 30. Compare
this assertion with the equivalent table constraint. Explain which is better.
*/

CREATE ASSERTION must_be_older_than_30 as CHECK 
((SELECT E.age FROM Emp E, Dept D WHERE E.eid = D.managerid) > 30));

/* 4. Write SQL statements to delete all information about employees whose salaries exceed
that of the manager of one or more departments that they work in. Be sure to ensure
that all the relevant integrity constraints are satisfied after your updates.*/

DELETE FROM Employee E
WHERE E.salary > ANY (SELECT E1.salary 
FROM Employee E1,Departmen D1
WHERE E1.eid = D1.managerid and D1.did in 
(SELECT W.did FROM Works W WHERE W.eid = E.eid));



