import create
import read
import compare
import sqls

#creating file
how=int(input('How many Files u want to create:'))
create.create_f(how)
#Reading file
re=int(input('How many files you want to read:'))
read.read_f(re)
#Comparing file
compare.comp(re)
#import to sql
sq=input('Enter the file name you want to insert in MYSql:')
sqls.insert_d(sq)


print('Program complete')