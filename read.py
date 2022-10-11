import pandas as pd
import numpy as np

def read_f(re):
    for i in range(1,re+1):
        s=input(f'Enter your {i} file name:')
        file_read=pd.read_csv(s)
        st_date=input('Enter Starting date:')
        file_read['dates']= pd.Series(pd.date_range(start=st_date, end='2020-10-01 ', freq ='H'))
        file_read['load_date']='2020-10-01'
        file_read['application']='Lake'
        file_read['amount']=np.random.randint(5,10,size=(len(file_read['dates']))).astype(float)
        
        file_read.to_csv(s,index=False)
        print(f'File {i} updated!')