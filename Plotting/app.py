#REFERENCES
#The files from this tutorial were initially used as an initial template.
#http://www.patricksoftwareblog.com/flask-tutorial/ 
#this gave starting point code for plotting a single dataset using chart.js and flask
#Functions to get new data from arduino and load new datasets to urls were writed
#by Max Bowker

from flask import Flask, render_template, jsonify
from datetime import time
import pandas as pd
import numpy
import os
import json
import sys
import serial
import keyboard
import time

IVapp = Flask(__name__)


#specify number of datapoints- must match number of datapoints measured by data aquisition arduino
global datapoints
datapoints=23

#Route URL
@IVapp.route("/")
def index():
    #Open serial connection with arduino when website is loaded
    global ser
    ser = serial.Serial('COM3', baudrate=9600)
    #wait for serial port to open
    time.sleep(1)
    #returns IV.html for browser to create website
    return render_template('IV.html')

@IVapp.route("/IVData", methods = ['GET'])
def GetIVData():
    #call GetCharacteristic to get new data from arduino
    GetCharacteristic()
    #read data from CSV into arrays
    Voltages, Currents, Vop = ReadCsv()
    #Converts lists to json format to be used in template
    xyData = [{'x': Voltages[i], 'y': Currents[i]} for i in range(datapoints-1)]
    #return IV data as JSON object
    return jsonify(xyData)

@IVapp.route("/PVData", methods = ['GET'])
def GetPVData():
    Voltages, Currents, Vop = ReadCsv()
    #Converts lists to json format to be used in template
    xyData = [{'x': Voltages[i], 'y': Currents[i]*Voltages[i]} for i in range(datapoints-1)]
    #return PV data as JSON object
    return jsonify(xyData)

@IVapp.route("/CurrentOpPoint", methods = ['GET'])
def GetCurrentOpPoint():
    Voltages, Currents, Vop= ReadCsv()
    #interpolate voltage values to find operating current
    I=numpy.interp(Vop,Voltages,Currents)
    #return operating current and voltage as JSON object
    return jsonify(x=Vop,y=I)

@IVapp.route("/PowerOpPoint", methods = ['GET'])
def GetPowerOpPoint():
    #Read data from CSV into arrays
    Voltages, Currents, Vop = ReadCsv()
    Powers=Voltages*Currents
    #interpolate voltage values to find operating power
    P=numpy.interp(Vop,Voltages,Powers)
    #return operating power and voltage as JSON object
    return jsonify(x=Vop,y=P)

def ReadCsv():
    data = pd.read_csv (os.getcwd()+('\\data.csv'))
    #Extract operating voltage from data (last entry in voltage column)
    Vop = data.at[(datapoints-1),'Voltage']
    data = data.drop((datapoints-1), axis=0)
    # sort dataframe into accending voltage values
    data = data.sort_values(by=['Voltage'])
    #convert dataframe to separate lists
    Currents= data['Current'].to_numpy()
    Voltages= data['Voltage'].to_numpy()
    return Voltages, Currents, Vop

def GetCharacteristic():
    
    if os.path.exists('data.csv'):
        os.remove('data.csv')
    
    # remove old data while the application was not running
    ser.flushInput()
    #tell arduino to send data
    ser.write('s')

    #Write column Headings in CSV
    file = open('data.csv', 'ab')
    file.write('Voltage,Current\n')
    file.close()

    i=1
    while i<=datapoints:
        # check if bytes received
        dataWaiting = ser.inWaiting()
        if(dataWaiting > 0):
            #Write 'I,V' line to CSV
            serBytes = ser.readline()
            print(serBytes)
            file = open('data.csv', 'ab')
            file.write(serBytes)
            file.close()
            i=i+1
    i=1
    

if __name__ == "__main__":
    #make program single threaded so csv isnt read while being written to
    IVapp.run(debug=True,threaded=False)
    # IVapp.run(host= '0.0.0.0',debug=True,threaded=False) #run on local network
