from cmath import pi
from multiprocessing import Process, Queue
from pickle import TRUE
from data_intake import data_sender
from Saver import data_saver
from GUI import launchGUI as gui_run
from dataclasses import dataclass, field
from typing import List
from collections import deque
from plotter import animation_control
from threading import Timer
import numpy as np
from numpy import *
import math


@dataclass
class MainExperiment:
    # Experimental state and control
    experiment_mode: str = "DEFAULT"
    mode_state: str = "DEFAULT"
    current_trial: str = "Prepare"
    current_status: str = "Prepare"
    task: str = "DEFAULT"
    mode_status: str = "Prepare"
    program_start: int = 0

    # pressure
    pressure_value: float = 1
    pressure_down: float = 1
    voltage_value: float = 1
    solenoid_value: int = 0
    BNC_value: int = 0
    BNC_logic: int = 0

    target_pressure: int = 1000
    target_solenoid: str = "DEFAULT"
    duty_cycle: float = 1

    pressure_low: int = 1
    pressure_medium: int = 1
    pressure_high: int = 1

    # Info about the participants
    subject_number: float = 0
    participant_age: float = 0
    participant_gender: str = "UNSPECIFIED"
    participant_years_since_stroke: int = 0
    participant_dominant_arm: str = "DEFAULT"
    participant_weight: float = 0
    
    shoulder_aduction_angle: float = 0
    elbow_flexion_angle: float = 0
    arm_length: float = 0
    midloadcell_to_elbowjoint: float = 0


    timestep: float = 0



def main():
    # Emonitor section, delegating the subprocess and connection
    QUEUES = []
    # Process and queues for the GUI

    gui_queue = Queue()
    gui_out_queue = Queue()
    QUEUES.append(gui_queue)
    QUEUES.append(gui_out_queue)

    gui_p = Process(target=gui_run, args=(gui_queue, gui_out_queue))
    gui_p.start()

    # Initialize data collection
    HZ = 100

    data_intake_queue = Queue()
    data_intake_comm_queue = Queue()
    QUEUES.append(data_intake_queue)
    QUEUES.append(data_intake_comm_queue)
    data_intake_p = Process(
        target=data_sender, args=(1 / HZ, data_intake_queue, data_intake_comm_queue)
    )
    data_intake_p.start()

    # Initialize plotting
    plotting_comm_queue = Queue()
    QUEUES.append(plotting_comm_queue)
    plotting_p = Process(target=animation_control, args=(plotting_comm_queue,))
    plotting_p.start()

    # Initialize the experiment dataclass
    experiment = MainExperiment()
    
    data_buffer = deque()

    is_saved_folder = False
    is_saved = False

    is_saved_trial1 = True
    is_saved_trial2 = True
    is_saved_trial3 = True

    is_ending_trial1 = False
    is_ending_trial2 = False
    is_ending_trial3 = False

    is_BNC_start = False
    save_happen = True

    running = True

    while running:

        data = None

        while not data_intake_queue.empty():
            data_seq = data_intake_queue.get()
            for point in data_seq:
                data_buffer.append(point)

        if data_buffer:
            data = data_buffer.popleft()
            experiment.BNC_value, experiment.voltage_value, experiment.solenoid_value, experiment.timestep= data
            experiment.voltage_value = experiment.voltage_value*(3.3/1024)
            experiment.BNC_value = experiment.BNC_value*(3.3/1024)
            experiment.pressure_value = experiment.voltage_value*0.1095

            if experiment.BNC_value > 1.5:
                experiment.BNC_logic = 1
            else:
                experiment.BNC_logic = 0


            if experiment.solenoid_value == 0:
                experiment.solenoid_value = 1
            elif experiment.solenoid_value == 1:
                experiment.solenoid_value = 0

        # Get the data from the remote controls
        while not gui_queue.empty():
            header, gui_data = gui_queue.get()

            if header == "Task0_save":
                experiment.task = "Task0_save"
                # Subject information
                experiment.subject_number = gui_data["Subject Number"]
                experiment.participant_age = gui_data["Age"]
                experiment.participant_gender = gui_data["Gender"]
                experiment.participant_weight = gui_data["Weight(lb)"]
                experiment.participant_dominant_arm = gui_data["Dominant Arm"]

                # save the data
                is_saved_folder = True
                if int(experiment.subject_number) < 10:
                    subject_saver = data_saver(experiment.participant_gender+"0"+str(int(experiment.subject_number))+"/")
                elif int(experiment.subject_number) < 0 and int(experiment.subject_number) > 99:
                    print("It is an Error")
                else:
                    subject_saver = data_saver(experiment.participant_gender+"0"+str(int(experiment.subject_number))+"/")

                subject_saver.add_header(
                    [
                        "Subject Number",
                        "Age",
                        "Gender",
                        "Weight(lb)",
                        "Dominant Arm",
                    ]
                )   

                # add data in the subject file
                subject_saver.add_data(
                    [
                        experiment.subject_number,
                        experiment.participant_age,
                        experiment.participant_gender,
                        experiment.participant_weight,
                        experiment.participant_dominant_arm,
                    ]
                )
                subject_saver.save_data("Subject_Information", "Sub")
                subject_saver.clear()

                # Create 2 files to save data for 2 tasks
                saver_trial1 = data_saver(experiment.participant_gender+"0"+str(int(experiment.subject_number))+"/")
                saver_trial2 = data_saver(experiment.participant_gender+"0"+str(int(experiment.subject_number))+"/")
                saver_trial3 = data_saver(experiment.participant_gender+"0"+str(int(experiment.subject_number))+"/")

                saver_matrix = [saver_trial1, saver_trial2, saver_trial3]
                for i in range(3):
                    saver_matrix[i].add_header(
                        [
                            "Time",
                            "Pressure value (MPa)",
                            "Voltage value (V)",
                            "Solenoid Value (O or 1)",
                            "BNC cable voltage (V)",
                            "Program start (0 or 1)"
                        ]
                    )

            elif header == "Task0_control":
                # At present, the task is Trial 0_control, it will be used to control the device manually
                experiment.task = "Task0_control"

                # set the target pressure value and the solenoid data
                experiment.target_pressure = gui_data["Pressure regulator value"]
                experiment.target_solenoid = gui_data["Solenoid value"]

            elif header == "Task1":
                # At present, the task is Trial 1 MAX Measurement
                experiment.task = "Task1"

                # get the experiment mode Left Right
                experiment.mode_state = gui_data["Experiment Status"]

                # get the start time when the trial 1 is starting
                initial_time_trial1 = experiment.timestep

                # if the data in trial 1 has been saved, then delete the old data
                if is_saved:
                    saver_trial1.clear()
                
                is_saved_trial1 = False

            elif header == "Task2":
                # At present, the task is Trial 1 MAX Measurement
                experiment.task = "Task2"

                # get the experiment mode Left Right
                experiment.mode_state = gui_data["Experiment Status"]

                # get the start time when the trial 1 is starting
                initial_time_trial1 = experiment.timestep

                print("program start time: %f"%initial_time_trial1)
                print("Voltage start time: %f"%Voltage_time)
                print(initial_time_trial1 - Voltage_time)

                # if the data in trial 1 has been saved, then delete the old data
                if is_saved:
                    saver_trial1.clear()
                
                is_saved_trial1 = False


            elif header == "Task3":
                experiment.task = "Task3"

                # Mode: Automatic, Up direction, In direction, Up and In direction
                experiment.mode_state = gui_data["Experiment Mode"]

                # get the start time when the trial 2 is starting
                initial_time_trial3 = experiment.timestep

                if is_saved:
                    saver_trial3.clear()
                
                is_saved_trial3 = False

            elif header == "Stop":
                experiment.program_start = 0
                experiment.task = "Stop"
                save_happen = False
            
            elif header == "Start":
                experiment.program_start = 1

            elif header == "Close":
                gui_p.terminate()
                running = False

        if not data:
            continue

        # start to save the data
        if is_saved_folder:
            for i in range(3):
                saver_matrix[i].add_data(
                    [
                        experiment.timestep,
                        experiment.pressure_value,
                        experiment.voltage_value,
                        experiment.solenoid_value,
                        experiment.BNC_value,
                        experiment.program_start,
                    ]
                )
        
        ##########################################
        # 101 piston push down
        # pressure+0 piston push up, pressure range (1500 - 3100)

        # if get 5 V, start the program
        gui_out_queue.put(experiment.BNC_logic)


        if experiment.BNC_logic == 1 and is_BNC_start == False:
            Voltage_time = experiment.timestep
            is_BNC_start = TRUE

        if experiment.task == "DEFAULT":
            experiment.target_pressure = 1000
            data_intake_comm_queue.put(23001)

        if experiment.task == "Stop":
            experiment.target_pressure = 1000
            data_intake_comm_queue.put(23001)

        if save_happen == False:
            saver_trial2.save_data("Functional Localizer Scan", experiment.mode_state)
            saver_trial3.save_data("Functional Scan", experiment.mode_state)
            save_happen = True

        if experiment.task == "Task0_control":
            if experiment.target_solenoid == "Up":
                data_intake_comm_queue.put(int(str(experiment.target_pressure)+'0'))
            elif experiment.target_solenoid == "Down":
                data_intake_comm_queue.put(int(str(experiment.target_pressure)+'1'))

        # -------- ------------------------------------------------Trial Type 1: MAX Measurement-------------------------------------------------
        if experiment.task == "Task1" or experiment.task == "Task2" :
            
            # 101 piston push down
            # pressure+0 piston push up, pressure range (1500 - 3100)  0 -1500 0 V to 2.0V    1.5v
            # get the time in the trail 1
            trial1_time = experiment.timestep - initial_time_trial1

            time_duration = 0.5
            
            experiment.target_pressure = 3000

            # push up the piston
            if trial1_time <= 1.5:
                data_intake_comm_queue.put(int(str(experiment.target_pressure)+'0'))
            elif trial1_time > 1.5 and trial1_time <= 3:
                data_intake_comm_queue.put(25001)
            
            elif trial1_time > 3 and trial1_time <= 4.5:
                data_intake_comm_queue.put(int(str(experiment.target_pressure)+'0'))
            elif trial1_time > 4.5 and trial1_time <= 6:
                data_intake_comm_queue.put(25001)
            
            elif trial1_time > 6 and trial1_time <= 7.5:
                data_intake_comm_queue.put(int(str(experiment.target_pressure)+'0'))
            elif trial1_time > 7.5 and trial1_time <= 9:
                data_intake_comm_queue.put(25001)

            elif trial1_time > 9 and trial1_time <= 10.5:
                data_intake_comm_queue.put(int(str(experiment.target_pressure)+'0'))
            elif trial1_time > 10.5 and trial1_time <= 12:
                data_intake_comm_queue.put(25001)

            elif trial1_time > 12 and trial1_time <= 13.5:
                data_intake_comm_queue.put(int(str(experiment.target_pressure)+'0'))
            elif trial1_time > 13.5 and trial1_time <= 15:
                data_intake_comm_queue.put(25001)

            elif trial1_time > 15 and trial1_time <= 16.5:
                data_intake_comm_queue.put(int(str(experiment.target_pressure)+'0'))
            elif trial1_time > 16.5 and trial1_time <= 18:
                data_intake_comm_queue.put(25001)

            elif trial1_time > 18 and trial1_time <= 19.5:
                data_intake_comm_queue.put(int(str(experiment.target_pressure)+'0'))
            elif trial1_time > 19.5 and trial1_time <= 21:
                data_intake_comm_queue.put(25001)
            

            elif trial1_time > 21 and trial1_time <= 22.5:
                data_intake_comm_queue.put(int(str(experiment.target_pressure)+'0'))
            elif trial1_time > 22.5 and trial1_time <= 24:
                data_intake_comm_queue.put(25001)
            
            elif trial1_time > 24 and trial1_time <= 25.5:
                data_intake_comm_queue.put(int(str(experiment.target_pressure)+'0'))
            elif trial1_time > 25.5 and trial1_time <= 27:
                data_intake_comm_queue.put(25001)

            elif trial1_time > 27 and trial1_time <= 28.5:
                data_intake_comm_queue.put(int(str(experiment.target_pressure)+'0'))
            elif trial1_time > 28.5 and trial1_time <= 30:
                data_intake_comm_queue.put(23001)

            elif trial1_time > 31:
                is_ending_trial1 = True
           
            if is_ending_trial1 and is_saved_trial1 == False:
                if experiment.task == "Task1":
                    saver_trial1.save_data("Phantom Scan", experiment.mode_state)
                else:
                    saver_trial1.save_data("Functional Localizer Scan", experiment.mode_state)
                is_saved_trial1 = True
                is_ending_trial1 = False


        # --------------------------------------------------------Trial Type 3: Stimulation Task-------------------------------------------------
        if experiment.task == "Task3":

            task3_time = experiment.timestep - initial_time_trial3
            # Assume low medium high
            experiment.pressure_low = 100
            experiment.pressure_medium = 1350
            experiment.pressure_high = 3000

            experiment.pressure_down = 28001

            if experiment.mode_state == "Trial 1":
                # [high + 9 + low + 6 + medium + 7 + low + 10 + medium + 8]
                rest_list = [9, 6, 7, 10, 8]
                force_list = [experiment.pressure_high, experiment.pressure_low, experiment.pressure_medium,
                              experiment.pressure_low, experiment.pressure_medium]
                
                # medium on
                in_1 = 1.5
                out_1 = in_1+rest_list[0] # off

                in_2 = out_1+1.5
                out_2 = in_2+rest_list[1] # off

                in_3 = out_2+1.5
                out_3 = in_3+rest_list[2] # off

                in_4 = out_3+1.5
                out_4 = in_4+rest_list[3] # off

                in_5 = out_4+1.5
                out_5 = in_5+rest_list[4] # off

                stop_time = out_5+0.1

                # high
                if task3_time < in_1:
                    data_intake_comm_queue.put(int(str(force_list[0])+'0'))
                elif task3_time >= in_1 and task3_time < out_1:
                    data_intake_comm_queue.put(23001)

                # low
                elif task3_time >= out_1 and task3_time < in_2:
                    data_intake_comm_queue.put(int(str(force_list[1])+'0'))
                elif task3_time >= in_2 and task3_time < out_2:
                    data_intake_comm_queue.put(experiment.pressure_down)
                
                # medium
                elif task3_time >= out_2 and task3_time < in_3:
                    data_intake_comm_queue.put(int(str(force_list[2])+'0'))
                elif task3_time >= in_3 and task3_time < out_3:
                    data_intake_comm_queue.put(23001)

                # low 
                elif task3_time >= out_3 and task3_time < in_4:
                    data_intake_comm_queue.put(int(str(force_list[3])+'0'))
                elif task3_time >= in_4 and task3_time < out_4:
                    data_intake_comm_queue.put(experiment.pressure_down)

                # medium
                elif task3_time >= out_4 and task3_time < in_5:
                    data_intake_comm_queue.put(int(str(force_list[4])+'0'))
                elif task3_time >= in_5 and task3_time < out_5:
                    data_intake_comm_queue.put(23001)
                
                elif task3_time >= stop_time:
                    is_ending_trial3 = True
            
            elif experiment.mode_state == "Trial 2":
                # [low + 6 + high + 8 + low + 10 + medium + 9 + medium + 7]
                rest_list = [6, 8, 10, 9, 7]
                force_list = [experiment.pressure_low, experiment.pressure_high, experiment.pressure_low,
                              experiment.pressure_medium, experiment.pressure_medium]
                
                # medium on
                in_1 = 1.5
                out_1 = in_1+rest_list[0] # off

                in_2 = out_1+1.5
                out_2 = in_2+rest_list[1] # off

                in_3 = out_2+1.5
                out_3 = in_3+rest_list[2] # off

                in_4 = out_3+1.5
                out_4 = in_4+rest_list[3] # off

                in_5 = out_4+1.5
                out_5 = in_5+rest_list[4] # off

                stop_time = out_5+0.1

                # low
                if task3_time < in_1:
                    data_intake_comm_queue.put(int(str(force_list[0])+'0'))
                elif task3_time >= in_1 and task3_time < out_1:
                    data_intake_comm_queue.put(experiment.pressure_down)

                # high
                elif task3_time >= out_1 and task3_time < in_2:
                    data_intake_comm_queue.put(int(str(force_list[1])+'0'))
                elif task3_time >= in_2 and task3_time < out_2:
                    data_intake_comm_queue.put(23001)
                
                # low
                elif task3_time >= out_2 and task3_time < in_3:
                    data_intake_comm_queue.put(int(str(force_list[2])+'0'))
                elif task3_time >= in_3 and task3_time < out_3:
                    data_intake_comm_queue.put(experiment.pressure_down)

                # medium on 9 off
                elif task3_time >= out_3 and task3_time < in_4:
                    data_intake_comm_queue.put(int(str(force_list[3])+'0'))
                elif task3_time >= in_4 and task3_time < out_4:
                    data_intake_comm_queue.put(experiment.pressure_down)

                # medium on 7 off
                elif task3_time >= out_4 and task3_time < in_5:
                    data_intake_comm_queue.put(int(str(force_list[4])+'0'))
                elif task3_time >= in_5 and task3_time < out_5:
                    data_intake_comm_queue.put(23001)
                
                elif task3_time >= stop_time:
                    is_ending_trial3 = True
            
            # elif experiment.mode_state == "Trial 2":
            #     # [high + 6 + low + 8 + high + 10 + low + 9 + medium + 7]
            #     rest_list = [2, 2, 2, 
            #                     2, 2, 2,
            #                     2, 2, 2,
            #                     2, 2, 2,
            #                     2, 2, 2,]
            #     force_list = [experiment.pressure_low, experiment.pressure_medium, experiment.pressure_high,
            #                     experiment.pressure_low, experiment.pressure_medium, experiment.pressure_high,
            #                     experiment.pressure_low, experiment.pressure_medium, experiment.pressure_high,
            #                     experiment.pressure_low, experiment.pressure_medium, experiment.pressure_high,
            #                     experiment.pressure_low, experiment.pressure_medium, experiment.pressure_high,]
                
            #     # medium on
            #     in_1 = 2
            #     out_1 = in_1+rest_list[0] # off

            #     in_2 = out_1+2
            #     out_2 = in_2+rest_list[1] # off

            #     in_3 = out_2+2
            #     out_3 = in_3+rest_list[2] # off

            #     in_4 = out_3+2
            #     out_4 = in_4+rest_list[3] # off

            #     in_5 = out_4+2
            #     out_5 = in_5+rest_list[4] # off

            #     in_6 = out_5+2
            #     out_6 = in_6+rest_list[5] # off

            #     in_7 = out_6+2
            #     out_7 = in_7+rest_list[6] # off

            #     in_8 = out_7+2
            #     out_8 = in_8+rest_list[7] # off

            #     in_9 = out_8+2
            #     out_9 = in_9+rest_list[8] # off

            #     in_10 = out_9+2
            #     out_10 = in_10+rest_list[9] # off

            #     in_11 = out_10+2
            #     out_11 = in_11+rest_list[10] # off

            #     in_12 = out_11+2
            #     out_12 = in_12+rest_list[11] # off

            #     in_13 = out_12+2
            #     out_13 = in_13+rest_list[12] # off

            #     in_14 = out_13+2
            #     out_14 = in_14+rest_list[13] # off

            #     in_15 = out_14+2
            #     out_15 = in_15+rest_list[14] # off

            #     stop_time = out_15+2

            #     # 1
            #     if task3_time < in_1:
            #         data_intake_comm_queue.put(int(str(force_list[0])+'0'))
            #     elif task3_time >= in_1 and task3_time < out_1:
            #         data_intake_comm_queue.put(experiment.pressure_down)

            #     # 2
            #     elif task3_time >= out_1 and task3_time < in_2:
            #         data_intake_comm_queue.put(int(str(force_list[1])+'0'))
            #     elif task3_time >= in_2 and task3_time < out_2:
            #         data_intake_comm_queue.put(experiment.pressure_down)
                
            #     # 3
            #     elif task3_time >= out_2 and task3_time < in_3:
            #         data_intake_comm_queue.put(int(str(force_list[2])+'0'))
            #     elif task3_time >= in_3 and task3_time < out_3:
            #         data_intake_comm_queue.put(23001)

            #     # 4
            #     elif task3_time >= out_3 and task3_time < in_4:
            #         data_intake_comm_queue.put(int(str(force_list[3])+'0'))
            #     elif task3_time >= in_4 and task3_time < out_4:
            #         data_intake_comm_queue.put(experiment.pressure_down)

            #     # 5
            #     elif task3_time >= out_4 and task3_time < in_5:
            #         data_intake_comm_queue.put(int(str(force_list[4])+'0'))
            #     elif task3_time >= in_5 and task3_time < out_5:
            #         data_intake_comm_queue.put(experiment.pressure_down)
                
            #     # 6
            #     elif task3_time >= out_5 and task3_time < in_6:
            #         data_intake_comm_queue.put(int(str(force_list[5])+'0'))
            #     elif task3_time >= in_6 and task3_time < out_6:
            #         data_intake_comm_queue.put(23001)
                
            #     # 7
            #     elif task3_time >= out_6 and task3_time < in_7:
            #         data_intake_comm_queue.put(int(str(force_list[6])+'0'))
            #     elif task3_time >= in_7 and task3_time < out_7:
            #         data_intake_comm_queue.put(experiment.pressure_down)
                
            #     # 8
            #     elif task3_time >= out_7 and task3_time < in_8:
            #         data_intake_comm_queue.put(int(str(force_list[7])+'0'))
            #     elif task3_time >= in_8 and task3_time < out_8:
            #         data_intake_comm_queue.put(experiment.pressure_down)
                
            #     # 9
            #     elif task3_time >= out_8 and task3_time < in_9:
            #         data_intake_comm_queue.put(int(str(force_list[8])+'0'))
            #     elif task3_time >= in_9 and task3_time < out_9:
            #         data_intake_comm_queue.put(23001)
                
            #     # 10
            #     elif task3_time >= out_9 and task3_time < in_10:
            #         data_intake_comm_queue.put(int(str(force_list[9])+'0'))
            #     elif task3_time >= in_10 and task3_time < out_10:
            #         data_intake_comm_queue.put(experiment.pressure_down)
                
            #     # 11
            #     elif task3_time >= out_10 and task3_time < in_11:
            #         data_intake_comm_queue.put(int(str(force_list[10])+'0'))
            #     elif task3_time >= in_11 and task3_time < out_11:
            #         data_intake_comm_queue.put(experiment.pressure_down)
                
            #     # 12
            #     elif task3_time >= out_11 and task3_time < in_12:
            #         data_intake_comm_queue.put(int(str(force_list[11])+'0'))
            #     elif task3_time >= in_12 and task3_time < out_12:
            #         data_intake_comm_queue.put(23001)
                
            #     # 13
            #     elif task3_time >= out_12 and task3_time < in_13:
            #         data_intake_comm_queue.put(int(str(force_list[12])+'0'))
            #     elif task3_time >= in_13 and task3_time < out_13:
            #         data_intake_comm_queue.put(experiment.pressure_down)
                
            #     # 14
            #     elif task3_time >= out_13 and task3_time < in_14:
            #         data_intake_comm_queue.put(int(str(force_list[13])+'0'))
            #     elif task3_time >= in_14 and task3_time < out_14:
            #         data_intake_comm_queue.put(experiment.pressure_down)
                
            #     # 15
            #     elif task3_time >= out_14 and task3_time < in_15:
            #         data_intake_comm_queue.put(int(str(force_list[14])+'0'))
            #     elif task3_time >= in_15 and task3_time < out_15:
            #         data_intake_comm_queue.put(23001)
                
            #     elif task3_time >= stop_time:
            #         is_ending_trial3 = True
            
            elif experiment.mode_state == "Trial 3":
                # [low + 7 + medium + 10 + medium + 6 + high + 8 + high + 9]
                rest_list = [7, 10, 6, 8, 9]
                force_list = [experiment.pressure_low, experiment.pressure_medium, experiment.pressure_medium,
                              experiment.pressure_high, experiment.pressure_high]
                
                # medium on
                in_1 = 1.5
                out_1 = in_1+rest_list[0] # off

                in_2 = out_1+1.5
                out_2 = in_2+rest_list[1] # off

                in_3 = out_2+1.5
                out_3 = in_3+rest_list[2] # off

                in_4 = out_3+1.5
                out_4 = in_4+rest_list[3] # off

                in_5 = out_4+1.5
                out_5 = in_5+rest_list[4] # off

                stop_time = out_5+0.1

                # low + 7
                if task3_time < in_1:
                    data_intake_comm_queue.put(int(str(force_list[0])+'0'))
                elif task3_time >= in_1 and task3_time < out_1:
                    data_intake_comm_queue.put(experiment.pressure_down)

                # medium + 10
                elif task3_time >= out_1 and task3_time < in_2:
                    data_intake_comm_queue.put(int(str(force_list[1])+'0'))
                elif task3_time >= in_2 and task3_time < out_2:
                    data_intake_comm_queue.put(experiment.pressure_down)
                
                # medium + 6
                elif task3_time >= out_2 and task3_time < in_3:
                    data_intake_comm_queue.put(int(str(force_list[2])+'0'))
                elif task3_time >= in_3 and task3_time < out_3:
                    data_intake_comm_queue.put(experiment.pressure_down)

                # high + 8
                elif task3_time >= out_3 and task3_time < in_4:
                    data_intake_comm_queue.put(int(str(force_list[3])+'0'))
                elif task3_time >= in_4 and task3_time < out_4:
                    data_intake_comm_queue.put(experiment.pressure_down)

                # high + 9
                elif task3_time >= out_4 and task3_time < in_5:
                    data_intake_comm_queue.put(int(str(force_list[4])+'0'))
                elif task3_time >= in_5 and task3_time < out_5:
                    data_intake_comm_queue.put(23001)
                
                elif task3_time >= stop_time:
                    is_ending_trial3 = True
            
            elif experiment.mode_state == "Trial 4":
                # [low + 10 + medium + 6 + high + 8 + high + 9 + low + 7]
                rest_list = [10, 6, 8, 9, 7]
                force_list = [experiment.pressure_low, experiment.pressure_medium, experiment.pressure_high,
                              experiment.pressure_high, experiment.pressure_low]
                
                # medium on
                in_1 = 1.5
                out_1 = in_1+rest_list[0] # off

                in_2 = out_1+1.5
                out_2 = in_2+rest_list[1] # off

                in_3 = out_2+1.5
                out_3 = in_3+rest_list[2] # off

                in_4 = out_3+1.5
                out_4 = in_4+rest_list[3] # off

                in_5 = out_4+1.5
                out_5 = in_5+rest_list[4] # off

                stop_time = out_5+0.1

                # low + 10
                if task3_time < in_1:
                    data_intake_comm_queue.put(int(str(force_list[0])+'0'))
                elif task3_time >= in_1 and task3_time < out_1:
                    data_intake_comm_queue.put(experiment.pressure_down)

                # medium + 6
                elif task3_time >= out_1 and task3_time < in_2:
                    data_intake_comm_queue.put(int(str(force_list[1])+'0'))
                elif task3_time >= in_2 and task3_time < out_2:
                    data_intake_comm_queue.put(experiment.pressure_down)
                
                # high + 8
                elif task3_time >= out_2 and task3_time < in_3:
                    data_intake_comm_queue.put(int(str(force_list[2])+'0'))
                elif task3_time >= in_3 and task3_time < out_3:
                    data_intake_comm_queue.put(experiment.pressure_down)

                # high + 9
                elif task3_time >= out_3 and task3_time < in_4:
                    data_intake_comm_queue.put(int(str(force_list[3])+'0'))
                elif task3_time >= in_4 and task3_time < out_4:
                    data_intake_comm_queue.put(23001)

                # low + 7
                elif task3_time >= out_4 and task3_time < in_5:
                    data_intake_comm_queue.put(int(str(force_list[4])+'0'))
                elif task3_time >= in_5 and task3_time < out_5:
                    data_intake_comm_queue.put(23001)
                
                elif task3_time >= stop_time:
                    is_ending_trial3 = True
            
            elif experiment.mode_state == "Trial 5":
                # [high + 8 + high + 7 + low + 9 + medium + 6 + high + 10]
                rest_list = [8, 7, 9, 6, 10]
                force_list = [experiment.pressure_high, experiment.pressure_high, experiment.pressure_low,
                              experiment.pressure_medium, experiment.pressure_high]
                
                # medium on
                in_1 = 1.5
                out_1 = in_1+rest_list[0] # off

                in_2 = out_1+1.5
                out_2 = in_2+rest_list[1] # off

                in_3 = out_2+1.5
                out_3 = in_3+rest_list[2] # off

                in_4 = out_3+1.5
                out_4 = in_4+rest_list[3] # off

                in_5 = out_4+1.5
                out_5 = in_5+rest_list[4] # off

                stop_time = out_5+0.1

                # high + 8
                if task3_time < in_1:
                    data_intake_comm_queue.put(int(str(force_list[0])+'0'))
                elif task3_time >= in_1 and task3_time < out_1:
                    data_intake_comm_queue.put(experiment.pressure_down)

                # high + 7
                elif task3_time >= out_1 and task3_time < in_2:
                    data_intake_comm_queue.put(int(str(force_list[1])+'0'))
                elif task3_time >= in_2 and task3_time < out_2:
                    data_intake_comm_queue.put(23001)
                
                # low + 9
                elif task3_time >= out_2 and task3_time < in_3:
                    data_intake_comm_queue.put(int(str(force_list[2])+'0'))
                elif task3_time >= in_3 and task3_time < out_3:
                    data_intake_comm_queue.put(experiment.pressure_down)

                # medium + 6
                elif task3_time >= out_3 and task3_time < in_4:
                    data_intake_comm_queue.put(int(str(force_list[3])+'0'))
                elif task3_time >= in_4 and task3_time < out_4:
                    data_intake_comm_queue.put(experiment.pressure_down)

                # high + 10
                elif task3_time >= out_4 and task3_time < in_5:
                    data_intake_comm_queue.put(int(str(force_list[4])+'0'))
                elif task3_time >= in_5 and task3_time < out_5:
                    data_intake_comm_queue.put(23001)
                
                elif task3_time >= stop_time:
                    is_ending_trial3 = True
            
            elif experiment.mode_state == "Trial 6":
                # [high + 8 + low + 10 + medium + 7 + medium + 6 + low + 9]
                rest_list = [8, 10, 7, 6, 9]
                force_list = [experiment.pressure_high, experiment.pressure_low, experiment.pressure_medium,
                              experiment.pressure_medium, experiment.pressure_low]
                
                # medium on
                in_1 = 1.5
                out_1 = in_1+rest_list[0] # off

                in_2 = out_1+1.5
                out_2 = in_2+rest_list[1] # off

                in_3 = out_2+1.5
                out_3 = in_3+rest_list[2] # off

                in_4 = out_3+1.5
                out_4 = in_4+rest_list[3] # off

                in_5 = out_4+1.5
                out_5 = in_5+rest_list[4] # off

                stop_time = out_5+0.1
                # high + 8
                if task3_time < in_1:
                    data_intake_comm_queue.put(int(str(force_list[0])+'0'))
                elif task3_time >= in_1 and task3_time < out_1:
                    data_intake_comm_queue.put(23001)

                # low + 10
                elif task3_time >= out_1 and task3_time < in_2:
                    data_intake_comm_queue.put(int(str(force_list[1])+'0'))
                elif task3_time >= in_2 and task3_time < out_2:
                    data_intake_comm_queue.put(experiment.pressure_down)
                
                # medium + 7
                elif task3_time >= out_2 and task3_time < in_3:
                    data_intake_comm_queue.put(int(str(force_list[2])+'0'))
                elif task3_time >= in_3 and task3_time < out_3:
                    data_intake_comm_queue.put(experiment.pressure_down)

                # medium + 6
                elif task3_time >= out_3 and task3_time < in_4:
                    data_intake_comm_queue.put(int(str(force_list[3])+'0'))
                elif task3_time >= in_4 and task3_time < out_4:
                    data_intake_comm_queue.put(23001)

                # low + 9
                elif task3_time >= out_4 and task3_time < in_5:
                    data_intake_comm_queue.put(int(str(force_list[4])+'0'))
                elif task3_time >= in_5 and task3_time < out_5:
                    data_intake_comm_queue.put(23001)
                
                elif task3_time >= stop_time:
                    is_ending_trial3 = True


            if is_ending_trial3 and is_saved_trial3 == False:
                saver_trial3.save_data("Functional Scan", experiment.mode_state)
                is_saved_trial3 = True
                is_ending_trial3 = False
                print("SAVE THE FILE")

        # -------- ------------------------------------------------Live plotting-------------------------------------------------
        if not plotting_comm_queue.full():
            # These are the values to be plotted. The first value MUST be the
            # timestep, but the rest may be changed
            graph_titles = [
                "Pressure value (MPa)",
                "Voltage value (V)",
                "Solenoid Value (O or 1)",
                "BNC cable voltage (V)"
            ]

            graph_data = [
                experiment.timestep,
                experiment.pressure_value,
                experiment.voltage_value,
                experiment.solenoid_value,
                experiment.BNC_value,
            ]
            plotting_comm_queue.put((graph_data, graph_titles))

    # Exit all processes

    # Exit the DAQ
    data_intake_comm_queue.put("EXIT")
    plotting_comm_queue.put("EXIT")
    data_intake_p.join()
    plotting_p.join()

    # Clear the queues
    for queue in QUEUES:
        while not queue.empty():
            queue.get_nowait()


if __name__ == "__main__":
    main()