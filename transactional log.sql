SELECT * FROM fn_dblog(NULL, NULL);

SELECT 
    [Transaction ID], 
    [Transaction Name], 
    [Operation], 
    [Context], 
    [AllocUnitName], 
    [Transaction SID],
    [Begin Time], 
    [End Time]
FROM fn_dblog(NULL, NULL)
WHERE [Operation] = 'LOP_DELETE_ROWS';


SELECT distinct
    [AllocUnitName]
FROM fn_dblog(NULL, NULL)

--log checking

WHERE [Operation] = 'LOP_DELETE_ROWS';

SELECT * 
FROM sys.partitions p
JOIN sys.allocation_units a ON p.hobt_id = a.container_id
WHERE a.allocation_unit_id = 'dbo.hvr_stats.hvr_stats__time';

SELECT 
    a.allocation_unit_id, 
    a.type_desc AS AllocationType, 
    OBJECT_NAME(p.object_id) AS TableName
FROM sys.allocation_units a
JOIN sys.partitions p ON a.container_id = p.hobt_id
WHERE ISNUMERIC('<AllocUnitName>') = 1  -- Ensure it's a number
AND a.allocation_unit_id = CAST('<AllocUnitName>' AS BIGINT);


SELECT 
    OBJECT_NAME(object_id) AS TableName,
    name AS IndexName
FROM sys.indexes
WHERE name = 'PK__hvr_stat__E616048D2CE76019';


SELECT name, recovery_model_desc FROM sys.databases WHERE name = 'hvr_db';
SELECT name, last_log_backup_lsn 
FROM sys.databases 
WHERE name = 'hvr_db';

select * from staGE.orders;
delete from stage.orders where orderid=2;


--Log stored location
SELECT name, physical_name 
FROM sys.master_files 
WHERE type_desc = 'LOG'

USE YourDatabaseName;
EXEC sp_helpfile;


---list of login available
SELECT name, type_desc, create_date FROM sys.server_principals
WHERE type IN ('S', 'U', 'G', 'E', 'X')
ORDER BY create_date DESC;
