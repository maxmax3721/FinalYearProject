from flask import Flask, render_template, jsonify
from datetime import time
import pandas as pd
import numpy
import os
import random
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('IV.html')

@app.route("/IVData", methods = ['GET'])
def GetIVData():

    Voltages, Currents = ReadCsv()
    #Converts lists to json format to be used in template
    xyData = [{'x': Voltages[i], 'y': Currents[i]} for i in range(len(Voltages))]
    
    return jsonify(xyData)

@app.route("/PVData", methods = ['GET'])
def GetPVData():

    Voltages, Currents = ReadCsv()
    #Converts lists to json format to be used in template
    xyData = [{'x': Voltages[i], 'y': Currents[i]*Voltages[i]} for i in range(len(Voltages))]
    return jsonify(xyData)

def ReadCsv():
    data = pd.read_csv (os.getcwd()+('\\data.csv'))
    # sort dataframe into accending voltage values
    data = data.sort_values(by=['Voltage'])
    #convert dataframe to separate lists
    rand=random.randint(1,100)
    Currents= data['Current'].to_numpy()
    Voltages= data['Voltage'].to_numpy()
    return Voltages, Currents

@app.route("/OpPoint", methods = ['GET'])
def GetVoltage():
    Voltages, Currents = ReadCsv()
    #arduino read voltage
    V=12+random.random()*6
    #interpolate voltage values to find current value 
    I=numpy.interp(V,Voltages,Currents)
    return jsonify(x=V,y=I)


if __name__ == "__main__":
    app.run(debug=True,threaded=False)#made single threaded so csv isnt read while being written
