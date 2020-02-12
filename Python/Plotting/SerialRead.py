import sys
import os
import serial
import keyboard

print("modules start")
print(keyboard.__file__)
print(serial.__file__)
print("modules end")

if os.path.exists('data.csv'):
    os.remove('data.csv')


try:
    # open the serial port once (arduino will reset when serial port is opened)
    ser = serial.Serial('COM3', baudrate=57600)
    # remove old data while the application was not running
    # not sure yet if it's 100% reliable; robin's approach is probably safer
    ser.flushInput()

    while True:
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

            # check if <esc> was pressed; stop if so
        if keyboard.is_pressed('esc'):
            break;

    # close serial port
    ser.close
except:
    print("Unexpected error:", sys.exc_info()[0])
    print("Unexpected error:", sys.exc_info()[1])

    # maybe todo: close serial port; this might need a little rework of above code moving 'ser = serial.Serial('COM4', baudrate=57600)' to outside the try

