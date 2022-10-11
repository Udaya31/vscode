import pandas as pd


def create_f(how):
    a='lake'
    for i in range(1,how+1):
        b=str(i)
        a+=b
        file=open(f"{a}.txt", "w")
        file.write("application,dates,amount,load_date")
        print(f'File {i} created')
        a=a.strip(b)