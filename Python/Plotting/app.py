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
    
    title= 'IV'

    return render_template('IV.html', title=title)

@app.route("/Data", methods = ['GET'])
def Data():

    Data = pd.read_csv (os.getcwd()+('\\data.csv'))
    # sort dataframe into accending voltage values
    Data = Data.sort_values(by=['Voltage'])
    #convert dataframe to separate lists
    rand=random.randint(1,100)
    Currents= Data['Current'].to_numpy()
    Voltages= Data['Voltage'].to_numpy()
    title= 'IV'
    #Converts lists to json format to be used in template
    xyData = [{'x': Voltages[i], 'y': Currents[i]+50*random.random()} for i in range(len(Voltages))]
    xyDatastring = str(xyData).replace('z', 'y')
    xyDatastring = str(xyDatastring).replace('\'','')
    
    return jsonify(xyData)


if __name__ == "__main__":
    app.run(debug=True)
