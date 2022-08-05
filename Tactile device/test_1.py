import csv
import keyboard
import string
import sys
import time

import numpy as np
import matplotlib.pyplot as plt

import serial
# from sys import version_info
# https://maker.pro/pic/tutorial/introduction-to-python-serial-ports
# serialPort = serial.Serial(port = "/dev/ttyACM0", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialPort = serial.Serial(port = "COM5", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

'''
@serial commands
open() – This will open the serial port
close() – This will close the serial port
readline() – This will read a string from the serial port
read(size) – This will read n number of bytes from the serial port
write(data) – This will write the data passed to the function to the serial port
in_waiting – This variable holds the number of bytes in the buffer
'''

serialString = ""   # Used to hold data coming over UART

i = 0

while(1):

    # print("ONE POINT TWENTY-ONE GIGAWATTS?!")

    t = time.time()

    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        # print("The pressure sensed (PSI) is:")

        # # Print the contents of the serial data
        # print(serialString.decode('Ascii'))

        pressure_value = serialString.decode('Ascii')

        i += 1

        if i < 20:
            number = str(3100)
            serialPort.write(number.encode('utf-8'))
        elif i >= 20 and i <= 40:
            number = str(1)
            serialPort.write(number.encode('utf-8'))
        elif i >= 40 and i <= 60:
            number = str(0)
            serialPort.write(number.encode('utf-8'))
        elif i >= 60 and i <= 80:
            number = str(1)
            serialPort.write(number.encode('utf-8'))
        elif i >= 80 and i <= 100:
            number = str(0)
            serialPort.write(number.encode('utf-8'))
        elif i >= 120 and i <= 140:
            number = str(1)
            serialPort.write(number.encode('utf-8'))
        elif i >= 140 and i <= 160:
            number = str(0)
            serialPort.write(number.encode('utf-8'))
        elif i >= 160 and i <= 180:
            number = str(1)
            serialPort.write(number.encode('utf-8'))
        elif i >= 180 and i <= 200:
            number = str(0)
            serialPort.write(number.encode('utf-8'))
        elif i >= 200 and i <= 220:
            number = str(1)
            serialPort.write(number.encode('utf-8'))

        print(pressure_value)
