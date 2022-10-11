import pandas as pd

def comp(re):
    f1=input('Enter your First file to compare:')
    for i in range(2,re+1):
        file1=pd.read_csv(f1)
        f2=input(f"Enter your {i} file to compare:")
        file2=pd.read_csv(f2)
        file1=pd.concat([file1,file2[~file2.dates.isin(file1.dates)]])
        file1.sort_values(["dates"], axis=0, ascending=[True], inplace=True)
        file1.to_csv(f1,index=False)
        print(f'File {i} updated!')