import warnings
import time

import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Queue
import serial
import re


class Tactile_Control:
    def __init__(self, stream_rate=100):
        self.serialPort = serial.Serial(port = "COM6", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        self.intended_stream_rate = 1 / stream_rate
        self.prev_time = time.perf_counter()

    def read_samples(self):
        serialString = ""

        # Read data out of the buffer until a carraige return / new line is found
        serialString = self.serialPort.readline()
        pressure_value = serialString.decode('Ascii')


        data = re.findall(r"\d+\.?\d*",pressure_value)


        if data:
            data = str(data[0])
            # pressure_data = float(data[0][:9])
            # solenoid_value = int(data[0][9])

        samples = [[data]]

        next_time = time.perf_counter()
        time_delta = (time.perf_counter() - self.prev_time) / len(samples[0])
        
        samples.append(
            [self.prev_time + (time_delta * i) for i in range(len(samples[0]))]
        )

        transposed = [[C[i] for C in samples] for i in range(len(samples[0]))]

        self.prev_time = next_time

        return transposed
    
    def write_actuator(self, number):
        # the number will be input to the PIC microcontroller
        number = str(number)
        self.serialPort.write(number.encode('utf-8'))
    
    def safe_exit(self):
        self.serialPort.close()


def main():
    tactile_control = Tactile_Control()

    running = True

    sample_cache = []

    prev_time = time.perf_counter()

    delete_first_data = 0

    while running:
        if(tactile_control.serialPort.in_waiting > 0):
            samples = tactile_control.read_samples()
            
            delete_first_data += 1
            if delete_first_data >= 2 and len(samples[0][0]) != 0:
                samples[0].insert(0, int(samples[0][0][9]))
                samples[0].insert(0, (int(samples[0][1][0:3])))
                samples[0].insert(0, (int(samples[0][2][4:9])))
                samples[0].pop(3)

                print(samples[0])

        tactile_control.write_actuator(16000)

if __name__ == "__main__":
    main()


def data_sender(
    sample_delay, send_queue: Queue = None, communication_queue: Queue = None
):
    tactile_control = Tactile_Control()

    running = True

    sample_cache = []

    prev_time = time.perf_counter()

    delete_first_data = 0

    i = 0
    sum_data = 0
    pressure_val = 1000

    while running:
        if(tactile_control.serialPort.in_waiting > 0):
            samples = tactile_control.read_samples()
            
            delete_first_data += 1
            if delete_first_data >= 2 and len(samples[0][0]) != 0:
                samples[0].insert(0, int(samples[0][0][9]))
                samples[0].insert(0, (int(samples[0][1][0:3])))
                samples[0].insert(0, (int(samples[0][2][4:9])))
                samples[0].pop(3)
                    
                sample_cache.extend(samples)
                prev_time += sample_delay

                if not send_queue.full() and sample_cache:
                    send_queue.put_nowait(sample_cache)
                    sample_cache = []

            tactile_control.write_actuator(pressure_val)
            while not communication_queue.empty():
                val = communication_queue.get_nowait()

                pressure_val = val
                
                if val == "EXIT":
                    tactile_control.safe_exit()
                    running = False
