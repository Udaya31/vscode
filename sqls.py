import mysql.connector
from sqlalchemy import create_engine
import pandas as pd

# mydb=mysql.connector.connect(host='localhost',user='root',password='SQL180822udemy',database='vscode')
# c=mydb.cursor()
# c.execute("drop table if exists lite")
# c.execute('''create table lite(application varchar(20),dates datetime,amount float,load_date varchar(20))''')
# sqs=pd.read_csv('lake1.txt')
# sqs.to_sql('lite',mydb,index=False,if_exists='replace')
# # c.execute('''select * from lite''')
# # for row in c:
# #     print(row)
# print(c.fetchall())
# c.commit()
# c.close()

hostname="localhost"
dbname="vscode"
uname="root"
pwd="SQL180822udemy"

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
				.format(host=hostname, db=dbname, user=uname, pw=pwd))
c=engine.connect()
c.execute("drop table if exists lite")
c.execute('''create table lite(application varchar(20),dates datetime,amount float,load_date datetime)''')
def insert_d(file):
	df=pd.read_csv(file)
	df.to_sql('lite', engine, index=False,if_exists='replace')
	print('File uploaded to MYSql')
	# cursor = c.cursor()
	# query = "SELECT * from history_table"
	# cursor.execute(query)
	# cursor.fetchall()
c.close()


