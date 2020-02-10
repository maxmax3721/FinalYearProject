from flask import Flask
from flask import render_template
from datetime import time
import pandas as pd
import numpy
import os

app = Flask(__name__)

@app.route("/IV")
def IV():
    #read csv datafile and convert to dataframe
    Data = pd.read_csv (os.getcwd()+('\\data.csv'))
    # sort dataframe into accending voltage values
    Data = Data.sort_values(by=['Voltage'])
    #convert dataframe to separate lists
    Currents= Data['Current'].to_numpy()
    Voltages= Data['Voltage'].to_numpy()
    title= 'IV'
    #Converts lists to json format to be used in template
    xyData = [{'x': int(Voltages[i]), 'z': int(Currents[i])} for i in range(len(Voltages))]
    xyDatastring = str(xyData).replace('z', 'y')
    xyDatastring = str(xyDatastring).replace('\'', '')
    return render_template('IV.html', xydata= xyDatastring , title=title)

if __name__ == "__main__":
    app.run(debug=True)
