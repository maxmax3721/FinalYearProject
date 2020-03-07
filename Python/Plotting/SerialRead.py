import sys
import os
import serial
import keyboard
import time

print("modules start")
print(keyboard.__file__)
print(serial.__file__)
print("modules end")

if os.path.exists('data.csv'):
    os.remove('data.csv')

# open the serial port once (arduino will reset when serial port is opened)
ser = serial.Serial('COM3', baudrate=9600)
time.sleep(2)
# remove old data while the application was not running
ser.flushInput()
#tell arduino to send data
ser.write('s')

file = open('data.csv', 'ab')
file.write('Voltage,Current\n')
file.close()

i=0
while i<21:
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

# close serial port
ser.flushOutput()
ser.write('f')
