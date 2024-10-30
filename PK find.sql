/*
Select count(*) from lyn_appointment(NOLOCK);
SELECT UPPER(COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='lyn_appointment' ORDER BY ORDINAL_POSITION;

SELECT C.COLUMN_NAME,T.CONSTRAIN_TYPE FROM 
INFORMATION_SCHEMA.TABLE_CONSTRAINTS T
JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE C
ON C.CONSTRAINT_NAME=T.CONSTRAINT_NAME
WHERE
C.TABLE_NAME='lyn_appointment'
AND T.CONSTRAINT_TYPE IN('PRIMARY KEY','UNIQUE')
*/

SET NOCOUNT ON
DECLARE @SQL NVARCHAR(3000),
	@ColumnNames NVARCHAR(3000),
	@GuessPrimaryKey NVARCHAR(3000),
	@LoopColumnName NVARCHAR(500),
	@StrKeyColumns NVARCHAR(500),
	@ALL_COUNT int,@KEY_COUNT int,
	@TableName NVARCHAR(500),
	@KeyColumns NVARCHAR(3000)

SET @TableName='APPOINTMENT'
SET @KeyColumns='ID,P_ID,D_ID'

IF OBJECT_ID('tempdb..#tempcolumns') IS NOT NULL
DROP TABLE #tempcolumns
SELECT UPPER(COLUMN_NAME) AS COLUMN_NAME,0 AS VERIFIED INTO #tempcolumns FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=@TableName
AND @KeyColumns NOT LIKE '%'+COLUMN_NAME+'%' 
SELECT @ColumnNames=STUFF((SELECT ',', UPPER(COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=@TableName AND @KeyColumns NOT LIKE '%'+COLUMN_NAME+'%'
ORDER BY ORDINAL_POSITION FOR XML PATH('')),1, 1, '')

IF OBJECT_ID('tempdb..#temp') IS NOT NULL
DROP TABLE ##temp
CREATE TABLE ##temp
(
	TABLE_NAME NVARCHAR(500),
	PRIMARY_KEYS NVARCHAR(3000),
	ALL_COUNT INT,
	KEY_COUNT INT
)

IF OBJECT_ID('tempdb..##temp_all_count') IS NOT NULL
DROP TABLE ##temp_all_count
CREATE TABLE ##temp_all_count
(
	TABLE_NAME NVARCHAR(500),
	ALL_COUNT int
)
SET @SQL='INSERT INTO ##temp_all_count SELECT '''+@TableName+''' AS TABLE_NAME,COUNT(1) AS ALL_COUNT FROM '+@TableName+'(NOLOCK);'
exec sp_executesql @SQL
SELECT @ALL_COUNT=ALL_COUNT FROM ##temp_all_count

IF OBJECT_ID('tempdb.##temp_key_count') IS NOT NULL
DROP TABLE ##temp_key_count
CREATE TABLE ##temp_key_count
(
	TABLE_NAME NVARCHAR(500),
	KEY_COUNT int
)
IF @KeyColumns LIKE '%,%'
	SET @StrKeyColumns='CONCAT('+@KeyColumns+')'
ELSE
	SET @StrKeyColumns=@KeyColumns

SET @SQL='INSERT INTO ##temp_key_count SELECT '''+@TableName+''' AS TABLE_NAME,COUNT(DISTINCT '+@StrKeyColumns+') AS KEY_COUNT FROM '+@TableName+'(NOLOCK);'
exec sp_executesql @SQL
SELECT @KEY_COUNT=KEY_COUNT FROM ##temp_key_count

IF @ALL_COUNT=@KEY_COUNT
BEGIN
	SELECT 'THIS IS THE PRIMARY KEY' AS MESSAGE,@TableName AS TableName,@KeyColumns AS KeyColumns,@ALL_COUNT AS ALL_COUNT,@KEY_COUNT AS KEY_COUNT FROM ##temp_key_count
	GOTO DOWN
END

WHILE EXISTS(SELECT 1 FROM #tempcolumns WHERE VERIFIED=0)
BEGIN
	SELECT TOP 1 @LoopColumnName=COLUMN_NAME FROM #tempcolumns WHERE VERIFIED=0
	SET @GuessPrimaryKey=@KeyColumns+','+@LoopColumnName
	SET @SQL='INSERT INTO ##temp SELECT '''+@TableName+''' AS TABLE_NAME,'''+GuessPrimaryKey+''' AS PRIMARY_KEYS, '+convert(NVARCHAR,@ALL_COUNT)' AS ALL_COUNT, COUNT(DISTINCT CONCAT('+@GuessPrimaryKey+')) AS KEY_COUNT FROM '+@TableName+'(NOOLOCk);'
	exec sp_executesql @SQL
	UPDATE #tempcolumns SET VERIFIED=1 WHERE COLUMN_NAME=@LoopColumnName
END

SELECT * FROM ##temp where ALL_COUNT=KEY_COUNT
SELECT * FROM ##temp WHERE ALL_COUNT<>KEY_COUNT ORDER BY ALL_COUNT,KEY_COUNT DESC
DOWN;