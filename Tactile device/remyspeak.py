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
serialPort = serial.Serial(port = "/dev/ttyUSB0", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

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

# with open('logpsi.csv', mode='w') as logpsi:
with open('/home/nckmlb/finpro/Experiment-Monitor-Py/logpsi.csv', mode='w') as logpsi:
    # preslog = csv.writer(logpsi, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    preslog = csv.writer(logpsi)
    t_0 = time.time()

    while(1):

        # print("ONE POINT TWENTY-ONE GIGAWATTS?!")

        t = time.time()
        t_x = t - t_0

        # Wait until there is data waiting in the serial buffer
        if(serialPort.in_waiting > 0):

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()

            print("The pressure sensed (PSI) is:")

            # Print the contents of the serial data
            print(serialString.decode('Ascii'))

            tolog = serialString.decode('Ascii')
            preslog.writerow([tolog[:-2]])  #trim end to get rid of newline

            # # Tell the device connected over the serial port that we recevied the data!
            # # The b at the beginning is used to indicate bytes!
            # serialPort.write(b"Thank you for sending data \r\n")

            if t_x > 1:
                plt.axis([0, 10, 0, 10])

                # for i in range(10):
                #     y = np.random.random()
                #     plt.scatter(i, y)
                #     plt.pause(0.05)
                plt.scatter(t_x, float(tolog[:-2]))

                # plt.show()
                
                # # press 'q' to exit (print plot)
                # if key == keyboard.Key.esc:
                #     sys.exit(1)
    plt.show()


# while(1):

#     # print("ONE POINT TWENTY-ONE GIGAWATTS?!")

#     # Wait until there is data waiting in the serial buffer
#     if(serialPort.in_waiting > 0):

#         # Read data out of the buffer until a carraige return / new line is found
#         serialString = serialPort.readline()

#         print("reverse the polarity of the neutron flow!")

#         # Print the contents of the serial data
#         print(serialString.decode('Ascii'))

#         tolog = serialString.decode('Ascii')
#         # preslog.writerow([tolog])

#         # # Tell the device connected over the serial port that we recevied the data!
#         # # The b at the beginning is used to indicate bytes!
#         # serialPort.write(b"Thank you for sending data \r\n")