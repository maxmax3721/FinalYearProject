import pandas as pd
import numpy
import json


Data = pd.read_csv (r'C:\Users\maxbo\OneDrive - University of Bristol\Documents\Year 3\Project\Python\Chart Example edited\data.csv')
Currents= Data['Current'].to_numpy()
Voltages= Data['Voltage'].to_numpy()
title= 'IV'
xyData = [{'x': int(Voltages[i]), 'z': int(Currents[i])} for i in range(len(Voltages))]
xyDatastring = str(xyData).replace('z', 'y')
xyDatastring = str(xyDatastring).replace('\'', '')
print(xyDatastring)


scales: {xAxes: [{ type: 'linear', position: 'bottom'}]}