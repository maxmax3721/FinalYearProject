import pandas as pd
import numpy

D = pd.read_csv (r'C:\Users\maxbo\OneDrive - University of Bristol\Documents\Year 3\Project\Python\Chart Example edited\data.csv')
print(D)

V= D['Voltage'].to_numpy()
C= D['Current'].to_numpy()

print(V,C)

