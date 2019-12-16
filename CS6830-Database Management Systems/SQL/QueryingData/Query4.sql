CREATE TABLE Employee(eid integer PRIMARY KEY,ename varchar(24),age integer,salary real);
CREATE TABLE Works(eid integer REFERENCES Employee,did integer REFERENCES Department,pct_time integer,PRIMARY KEY(eid,did));
CREATE TABLE Departmen(did integer PRIMARY KEY,dname varchar(24),budget real,managerid integer);

/* 1. Print the names and ages of each employee who works in both the Hardware
department and the Software department*/

SELECT E.ename, E.age
FROM Employee E
WHERE EXISTS 
(SELECT * FROM Works W WHERE E.eid = W.eid 
and W.did in(SELECT D.did FROM Departmen D WHERE D.dname="HARDWARE")
and W.did in (SELECT D1.did FROM Departmen D1 WHERE D1.dname="HARDWARE"));

/* 2. For each department with more than 20 full-time-equivalent employees (i.e., where the
part-time and full-time employees add up to at least that many full-time employees),
print the did together with the number of employees that work in that department. */

SELECT D.did,count(*) as numOfEmployees
FROM Works W,Departmen D
WHERE W.did = D.did
GROUP BY(W.did)
HAVING SUM(W.pct_time) >= 100;

/* 3. Print the name of each employee whose salary exceeds the budget of all of the departments
that he or she works in.*/

SELECT E.ename
FROM Employee E
WHERE E.salary > (SELECT Sum(D.budget) 
FROM Works W,Departmen D 
WHERE E.eid = W.eid and W.did = D.did);

/* 4. Find the managerids of managers who manage only departments with budgets greater
than $1.000.000*/

SELECT D.managerid
FROM Departmen D
WHERE NOT EXISTS
(SELECT * 
FROM Departmen D2 
WHERE D.managerid = D2.managerid and D2.budget < 1000000);

/* 
5. Find the enames of managers who manage the departments with the largest budget.
*/

SELECT E.ename
FROM Employee E,Departmen D
WHERE E.eid = D.managerid and D.budget >= ALL (SELECT D2.budget FROM Departmen D2);

/* 6. If a manager manages more than one department, he or she controls the sum of all the
budgets for those departments. Find the managerids of managers who control more than
$5,000,000.
*/

SELECT D.managerid
FROM Departmen D
GROUP BY(D.managerid)
HAVING SUM(D.budget) > 5000000;

-- 7. Find the managerids of managers who control the largest amount.

SELECT Temp.managerid,MAX(totalBudget) as maxBudget
FROM
(SELECT D.managerid,SUM(D.budget) as totalBudget
FROM Departmen D
GROUP BY(D.managerid)) as Temp;

