import pandas as pd
import numpy
import os
import random
import time

while True:
    Data = pd.read_csv(os.getcwd()+('\\data.csv'))
    for i in range(24):
        Data['Current'][i]=Data['Current'][i]+0.1
    time.sleep(1)
    os.remove('data.csv')
    Data.to_csv(os.getcwd()+('\\data.csv'),index=False)
    for i in range(24):
        Data['Current'][i]=Data['Current'][i]-0.1
    time.sleep(1)
    os.remove('data.csv')
    Data.to_csv(os.getcwd()+('\\data.csv'),index=False)




