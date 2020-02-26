from flask import Flask, render_template, jsonify
from datetime import time
import pandas as pd
import numpy
import os
import random

app = Flask(__name__)

@app.route("/")
def index():
    #read csv datafile and convert to dataframe
    Data = pd.read_csv (os.getcwd()+('\\data.csv'))
    # sort dataframe into accending voltage values
    Data = Data.sort_values(by=['Voltage'])
    #convert dataframe to separate lists
    Currents= Data['Current'].to_numpy()
    Voltages= Data['Voltage'].to_numpy()
    title= 'IV'
    #Converts lists to json format to be used in template
    xyData = [{'x': Voltages[i], 'z': Currents[i]} for i in range(len(Voltages))]
    xyDatastring = str(xyData).replace('z', 'y')
    xyDatastring = str(xyDatastring).replace('\'','')
    return render_template('IV.html', xydata= xyDatastring, title=title)

@app.route("/Stuff", methods = ['GET'])
def Stuff():

    Data = pd.read_csv (os.getcwd()+('\\data.csv'))
    # sort dataframe into accending voltage values
    Data = Data.sort_values(by=['Voltage'])
    #convert dataframe to separate lists
    rand=random.randint(1,100)
    Currents= Data['Current'].to_numpy()
    Voltages= Data['Voltage'].to_numpy()
    title= 'IV'
    #Converts lists to json format to be used in template
    xyData = [{'x': Voltages[i], 'z': Currents[i]+random.random()} for i in range(len(Voltages))]
    xyDatastring = str(xyData).replace('z', 'y')
    xyDatastring = str(xyDatastring).replace('\'','')
    
    return xyDatastring


if __name__ == "__main__":
    app.run(debug=True)
