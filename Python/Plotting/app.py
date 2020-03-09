from flask import Flask, render_template, jsonify
from datetime import time
import pandas as pd
import numpy
import os
import random
import json
import sys
import serial
import keyboard
import time

app = Flask(__name__)

global datapoints
datapoints=25

@app.route("/")
def index():
    global ser
    ser = serial.Serial('COM3', baudrate=9600)
    time.sleep(1)
    return render_template('IV.html')

@app.route("/IVData", methods = ['GET'])
def GetIVData():
    GetCharacteristic()
    Voltages, Currents, Vop = ReadCsv()
    #Converts lists to json format to be used in template
    xyData = [{'x': Voltages[i], 'y': Currents[i]} for i in range(datapoints)]
    
    return jsonify(xyData)

@app.route("/PVData", methods = ['GET'])
def GetPVData():
    Voltages, Currents, Vop = ReadCsv()
    #Converts lists to json format to be used in template
    xyData = [{'x': Voltages[i], 'y': Currents[i]*Voltages[i]} for i in range(datapoints)]
    return jsonify(xyData)


@app.route("/CurrentOpPoint", methods = ['GET'])
def GetCurrent():
    Voltages, Currents, Vop = ReadCsv()
    #interpolate voltage values to find current value 
    I=numpy.interp(Vop,Voltages,Currents)
    return jsonify(x=Vop,y=I)

@app.route("/PowerOpPoint", methods = ['GET'])
def GetPower():
    Voltages, Currents, Vop = ReadCsv()
    Powers=Voltages*Currents
    #interpolate voltage values to find current value 
    P=numpy.interp(Vop,Voltages,Powers)
    return jsonify(x=Vop,y=P)

def ReadCsv():
    data = pd.read_csv (os.getcwd()+('\\data.csv'))
    # sort dataframe into accending voltage values
    Vop = data.at[datapoints,'Voltage']
    data = data.drop(datapoints, axis=0)
    data = data.sort_values(by=['Voltage'])
    #convert dataframe to separate lists
    Currents= data['Current'].to_numpy()
    Voltages= data['Voltage'].to_numpy()
    return Voltages, Currents, Vop

def GetCharacteristic():

    if os.path.exists('data.csv'):
        os.remove('data.csv')

    # open the serial port once (arduino will reset when serial port is opened)
    
    # remove old data while the application was not running
    ser.flushInput()
    #tell arduino to send data
    ser.write('s')

    file = open('data.csv', 'ab')
    file.write('Voltage,Current\n')
    file.close()

    i=0
    while i<datapoints+1:
        # check if bytes received
        numBytes = ser.inWaiting()
        if(numBytes > 0):
            serBytes = ser.readline()
            print(serBytes)
            # open file for binary (!) appending; not using binary results in
            # 1) error telling you 'must be str, not bytes'
            # 2) convering using str(ser_bytes) results in unwanted quotation marks in the file (as shown in the result of above print)
            file = open('data.csv', 'ab')
            file.write(serBytes)
            file.close()
            i=i+1

if __name__ == "__main__":
    app.run(debug=True,threaded=False)#made single threaded so csv isnt read while being written
