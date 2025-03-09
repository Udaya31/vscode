/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [OrderID]
      ,[CustomerName]
      ,[OrderDate]
      ,[TotalAmount]
  FROM [hvr_db].[Stage].[Orders]

  INSERT INTO [hvr_db].[Stage].orders 
VALUES 
(5, 'test1', getdate(), 100),
(6, 'test2', getdate(), 200);


BEGIN TRANSACTION;

-- Acquire an exclusive lock on the table
SELECT * FROM hvr_db.Stage.Orders WITH (TABLOCKX);

-- 3 Insert statements
INSERT INTO hvr_db.Stage.Orders (OrderID, CustomerName, OrderDate, TotalAmount)
VALUES (1034, 'New Customer 1', GETDATE(), 150.00);

INSERT INTO hvr_db.Stage.Orders (OrderID, CustomerName, OrderDate, TotalAmount)
VALUES (1065, 'New Customer 2', GETDATE(), 200.00);

INSERT INTO hvr_db.Stage.Orders (OrderID, CustomerName, OrderDate, TotalAmount)
VALUES (1055, 'New Customer 3', GETDATE(), 120.00);

-- 2 Update statements
UPDATE hvr_db.Stage.Orders 
SET TotalAmount = 250.00 
WHERE OrderID = 1;

UPDATE hvr_db.Stage.Orders 
SET CustomerName = 'Updated Customer' 
WHERE OrderID = 2;

-- 1 Delete statement
DELETE FROM hvr_db.Stage.Orders WHERE OrderID = 1000;

-- Wait for 5 minutes (optional)
WAITFOR DELAY '00:05:00'; 

-- Commit the transaction (this will release the lock)
COMMIT TRANSACTION;

BEGIN TRANSACTION;

-- Acquire a shared lock on the table
SELECT * FROM hvr_db.Stage.Orders WITH (TABLOCK);

-- 3 Insert statements with new values
INSERT INTO hvr_db.Stage.Orders (OrderID, CustomerName, OrderDate, TotalAmount)
VALUES (2001, 'New Customer A', GETDATE(), 350.00);

INSERT INTO hvr_db.Stage.Orders (OrderID, CustomerName, OrderDate, TotalAmount)
VALUES (2002, 'New Customer B', GETDATE(), 180.00);

INSERT INTO hvr_db.Stage.Orders (OrderID, CustomerName, OrderDate, TotalAmount)
VALUES (2003, 'New Customer C', GETDATE(), 220.00);

-- 2 Update statements with new values
UPDATE hvr_db.Stage.Orders 
SET TotalAmount = 150.00 
WHERE OrderID = 3;

UPDATE hvr_db.Stage.Orders 
SET CustomerName = 'Updated Customer Name' 
WHERE OrderID = 4;

-- 1 Delete statement with a new value
DELETE FROM hvr_db.Stage.Orders WHERE OrderID = 2000;

-- Wait for 5 minutes (optional)
WAITFOR DELAY '00:05:00'; 

-- Commit the transaction (this will release the lock)
COMMIT TRANSACTION;
