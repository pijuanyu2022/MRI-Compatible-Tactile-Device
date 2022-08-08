from multiprocessing import Process, Queue
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import time
import numpy as np

class GUI(ttk.Frame):
    def __init__(self, master, conn, in_conn=None):
        super().__init__(master)

        self.afterid_1 = ttk.StringVar()
        self.afterid_2 = ttk.StringVar()
        self.afterid_3 = ttk.StringVar()

        self.running = ttk.BooleanVar(value=False)
        self.running_1 = ttk.BooleanVar(value=False)
        self.running_2 = ttk.BooleanVar(value=False)
        self.is_trial3_auto = False
        self.is_trial3_block1 = False
        self.is_trial3_block2 = False
        self.is_trial3_block3 = False
        self.is_trial3_block4 = False
        self.is_trial3_block5 = False
        self.is_trial3_block6 = False
        self.is_label = False
        self.is_rest_bar = False
        self.Program_start = False

        self.is_trial3_status = False
        self.trial3_break = False
        self.trial1_break = False

        self.is_trial4_status = False
        self.trial4_break = False

        self.is_trial5_auto = False
        self.is_trial5_up = False
        self.is_trial5_in = False
        self.is_trial5_upin = False

        self.is_trial6_set1 = False
        self.is_trial6_set2 = False
        self.is_trial6_set3 = False
        self.is_trial6_set4 = False
        self.trial6_break = False

        self.pause_bar = False
        self.stop_bar = False
        self.has_started_bar = False
        self.trial_finish = False

        self.is_trial1_status = False
        self.is_trial1 = False
        self.is_trial2_status = False
        self.is_trial2 = False
        self.is_trial3_status = False

        # queues for multiprocessing
        self.data_queue = conn
        self.in_queue = in_conn

        self.master = master
        
        self.style = ttk.Style()
        self.style.configure('lefttab.TNotebook',tabposition='wn',
                tabmargins=[5, 5, 2, 5],padding= [0, 0],justify= "left",font=("Calibri", 15, "bold"),foreground='green')
                # tabposition='wn',
                # justify= "left",
                # padding= [20, 10],
                # font=("Calibri", "bold"))

        self.style.element_create('Plain.Notebook.tab', "from", 'default')
        self.style.layout("TNotebook.Tab",
            [('Plain.Notebook.tab', {'children':
                [('Notebook.padding', {'side': 'top', 'children':
                    [('Notebook.focus', {'side': 'top', 'children':
                        [('Notebook.label', {'side': 'top', 'sticky': ''})],
                    'sticky': 'nswe'})],
                'sticky': 'nswe'})],
            'sticky': 'nswe'})])

        self.style.configure('TNotebook.Tab', background='green', foreground='green')
        self.style.configure("TNotebook", background='#666666', foreground='green' )
        # self.style.map("TNotebook", background=[("selected", 'green')])
        self.notebk = ttk.Notebook(self.master, style='lefttab.TNotebook')

        # Tabs for each section
        self.frame0 = ttk.Frame(self.notebk, width = 400, height = 400, relief = ttk.SUNKEN)
        self.frame1 = ttk.Frame(self.notebk, width = 400, height = 400, relief = ttk.SUNKEN)
        self.frame2 = ttk.Frame(self.notebk, width = 400, height = 400, relief = ttk.SUNKEN)
        self.frame3 = ttk.Frame(self.notebk, width = 400, height = 400, relief = ttk.SUNKEN)


        self.notebk.add(self.frame0, text = 'Constant                           ')
        self.notebk.add(self.frame1, text = 'Phantom Scan                  ')
        self.notebk.add(self.frame2, text = 'Functional Localizer Scan')
        self.notebk.add(self.frame3, text = 'Functional Scan                ')
        self.notebk.pack(expand = 1, fill="both")

        self.set_frame0()
        self.set_frame1()
        self.set_frame2()
        self.set_frame3()

        # self.trial_iteration()
 
    # frame functions
    def set_frame0(self):
        # --------------------------- Frame 0 ----------------------------------------------
        self.title = ttk.Label(self.frame0, text="                                                      Constant Value", bootstyle=DARK, font=("Calibri", 15, "bold"), background="")
        self.title.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.trial0_row = 0

        ######################### Input Constant Information #######################
        self.sub_lf = ttk.Labelframe(self.frame0,text="Constant Information", bootstyle=INFO)
        self.sub_lf.place(x=40,y=50,width=400,height=450)

        self.subjectInfo = ['Subject Number', 'Age', 'Gender', 'Weight(lb)', 'Dominant Arm']

        self.subject_result = []

        # Text entry fields
        for i in range(len(self.subjectInfo)):
            ttk.Label(self.sub_lf, text=self.subjectInfo[i],font=("Calibri", 10)).grid(row=i+1, column=0, padx=5, pady=5)
            if self.subjectInfo[i] not in ['Gender','Dominant Arm']:
                e1 = ttk.Entry(self.sub_lf,show=None)
                e1.grid(row=i+1, column=1, padx=5, pady=5)
                self.subject_result.append(e1)


        # Option Menus
        self.subStringVars = ['Gender', 'Diabetes', 'Dominant Arm', 'Testing Arm']
        # Gender
        self.genders_StinngVar = ttk.StringVar(self.master)
        self.genders_First = 'Select a gender'
        self.genders_StinngVar.set(self.genders_First)
        self.genders_Type = ["Male", "Female", "Other"]
        self.genders_Menu = ttk.OptionMenu(self.sub_lf, self.genders_StinngVar, self.genders_Type[0], *self.genders_Type,)
        self.genders_Menu.grid(row=3, column=1, padx=5, pady=5)

        # Dominant Arm
        self.domArm_StinngVar = ttk.StringVar(self.master)
        self.domArm_First = 'Left/Right'
        self.domArm_StinngVar.set(self.domArm_First)
        self.domArm_Type = ['Right', 'Left']
        self.domArm_Menu = ttk.OptionMenu(self.sub_lf, self.domArm_StinngVar, self.domArm_Type[0], *self.domArm_Type)
        self.domArm_Menu.grid(row=5, column=1, padx=5, pady=5)

        # Submit constant information
        self.Constant_Sub = ttk.Button(self.sub_lf, text="Save", bootstyle=(INFO, OUTLINE), command=self.trial0_save)
        self.Constant_Sub.grid(row=9,column=1, padx=5, pady=5)

        ######################### Manual Control #######################
        self.trial0_exp_lf = ttk.Labelframe(self.frame0,text="Manual Control", bootstyle=INFO)
        self.trial0_exp_lf.place(x=470,y=50,width=370,height=450)


        self.trial0_info = ['This section will be used to control the solenoid', 'manually. If you do not want to control the ', 'device manualy, please ignore this part',' ','      Set the pressure value in range 1500 - 3100', 'Choose to open the solenoid']

        self.trial0_result = []

        for i in range(4):
            self.trial0_label = ttk.Label(self.trial0_exp_lf, text=self.trial0_info[i],font=("Calibri", 10)).grid(row=i, column=0, columnspan=2, padx=5, pady=5)

        self.trial0_label = ttk.Label(self.trial0_exp_lf, text=self.trial0_info[4],font=("Calibri", 10)).grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.trial0_label = ttk.Label(self.trial0_exp_lf, text=self.trial0_info[5],font=("Calibri", 10)).grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        e2 = ttk.Entry(self.trial0_exp_lf,show=None)
        e2.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        self.trial0_result.append(e2)


        self.trial0_start_StinngVar = ttk.StringVar(self.master)
        self.trial0_start_First = 'Select a task'
        self.trial0_start_StinngVar.set(self.trial0_start_First)
        self.trial0_start_Type = ["Up", "Down"]
        self.trial0_start_Menu = ttk.OptionMenu(self.trial0_exp_lf, self.trial0_start_StinngVar, self.trial0_start_Type[0], *self.trial0_start_Type,)
        self.trial0_start_Menu.grid(row=8,column=0, columnspan=2, padx=5, pady=5)

        self.trial0_button = ttk.Button(self.trial0_exp_lf, text="Start", command=self.trial0_start, bootstyle=DANGER)
        self.trial0_button.grid(row=9,column=0, columnspan=2, padx=5, pady=5)

        # End 
        self.End_lf = ttk.Frame(self.frame0)
        self.End_lf.place(x=700,y=700,width=100,height=50)

        self.quit = ttk.Button(self.End_lf, text='Exit', command=self.close, bootstyle=DANGER)
        self.quit.grid(row=0,column=0,padx=5, pady=5)

    def set_frame1(self):

        # Bool number
        self.is_trial1_EMG = False
        self.is_trial1_in = False
        self.is_trial1_out = False
        self.is_trial1_up = False

        self.is_start_trial1 = True

        self.title = ttk.Label(self.frame1, text="                                                      Phantom Scan", bootstyle=DARK, font=("Calibri", 15, "bold"), background="")
        self.title.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.trial1_row = 0

        ### Description
        # add preparation frame
        self.trial1_lf = ttk.Labelframe(self.frame1,text="Preparation", bootstyle=INFO)
        self.trial1_lf.place(x=10,y=50,width=830,height=200)

        # description
        self.description_2 = ttk.Label(self.trial1_lf, text="Phantom Scan will be used to verify the validation of the MRI compatible device. 8 trials. Each trial will",font=("Calibri", 11))
        self.description_2.grid(row=self.trial1_row+1, column=0, columnspan=4, padx=5, pady=5)

        self.description_2 = ttk.Label(self.trial1_lf, text=" push up the piston for 1.5 second and push down for 1.5 second. 30 second rest between each trail.",font=("Calibri", 11))
        self.description_2.grid(row=self.trial1_row+2, column=0,columnspan=4, padx=5, pady=5)

        # # INPUT MVT
        self.input_subj = ttk.Label(self.trial1_lf, text="Subject Number:  ",font=("Calibri", 10))
        self.input_subj.grid(row=self.trial1_row+3, column=0, padx=5, pady=5)

        self.input_subj = ttk.Label(self.trial1_lf, text="Age:  ",font=("Calibri", 10))
        self.input_subj.grid(row=self.trial1_row+3, column=2, padx=5, pady=5)

        self.input_subj = ttk.Label(self.trial1_lf, text="Gender:  ",font=("Calibri", 10))
        self.input_subj.grid(row=self.trial1_row+4, column=0, padx=5, pady=5)

        self.input_subj = ttk.Label(self.trial1_lf, text="Weight(lb):  ",font=("Calibri", 10))
        self.input_subj.grid(row=self.trial1_row+4, column=2, padx=5, pady=5)

        self.input_subj = ttk.Label(self.trial1_lf, text="Dominant arm:  ",font=("Calibri", 10))
        self.input_subj.grid(row=self.trial1_row+5, column=0, padx=5, pady=5)

        ### Experimental 
        # add trial1 experimental label frame
        self.trial1_exp_lf = ttk.Labelframe(self.frame1,text="Experimental", bootstyle=INFO)
        self.trial1_exp_lf.place(x=10,y=300,width=830,height=365)

        # # UP IN UP&IN
        self.title_1 = ttk.Label(self.trial1_exp_lf, text="Click to start",font=("Calibri", 12, "bold"), bootstyle=PRIMARY)
        self.title_1.grid(row=self.trial1_row+0, column=0, padx=5, pady=5)

        self.trial1_button = ttk.Button(self.trial1_exp_lf, text="Start", command=self.trial1_Start, bootstyle=DANGER)
        self.trial1_button.grid(row=self.trial1_row+0,column=1, padx=5, pady=5)

        self.trial1_button_2 = ttk.Button(self.trial1_exp_lf, text="Stop", command=self.trial1_stop, bootstyle=DANGER)
        self.trial1_button_2.grid(row=self.trial1_row+0,column=2, padx=5, pady=5)

        # Trial and Status
        self.title_1 = ttk.Label(self.trial1_exp_lf, text="Current Trial: ",font=("Calibri", 12, "bold"))
        self.title_1.grid(row=self.trial1_row+1, column=0, padx=5, pady=5)

        self.title_1 = ttk.Label(self.trial1_exp_lf, text="Current Status: ",font=("Calibri", 12, "bold"))
        self.title_1.grid(row=self.trial1_row+1, column=2, padx=5, pady=5)

        self.title_1 = ttk.Label(self.trial1_exp_lf, text="       ",font=("Calibri", 12, "bold"))
        self.title_1.grid(row=self.trial1_row+2, column=2, padx=5, pady=5) 


        # Starting 
        self.title_1 = ttk.Label(self.trial1_exp_lf, text="The Experimental Progress Bar",font=("Calibri", 12, "bold"), bootstyle=INFO)
        self.title_1.grid(row=self.trial1_row+4, column=0, columnspan=5, padx=5, pady=5)   

        self.title_1 = ttk.Label(self.trial1_exp_lf, text="       ",font=("Calibri", 12, "bold"))
        self.title_1.grid(row=self.trial1_row+5, column=0, padx=5, pady=5)   

        self.trial1_bar_max = 1000
        self.title_1_fg = ttk.Floodgauge(self.trial1_exp_lf, bootstyle=INFO, length=750, maximum=self.trial1_bar_max, font=("Calibri", 12, 'bold'),)
        self.title_1_fg.grid(row=self.trial1_row+6, column=0, columnspan=5, padx=5, pady=3)  

        self.add_trial1()
        # End 
        self.End_lf = ttk.Frame(self.frame1)
        self.End_lf.place(x=700,y=740,width=100,height=50)

        self.quit = ttk.Button(self.End_lf, text='Exit', command=self.close, bootstyle=DANGER)
        self.quit.grid(row=0,column=0,padx=5, pady=5)
    
    def set_frame2(self):
    
        # Bool number
        self.is_trial2_EMG = False
        self.is_trial2_in = False
        self.is_trial2_out = False
        self.is_trial2_up = False

        self.is_start_trial2 = True

        self.title = ttk.Label(self.frame2, text="                                                  Functional Localizer Scan", bootstyle=DARK, font=("Calibri", 15, "bold"), background="")
        self.title.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.trial2_row = 0

        ### Description
        # add preparation frame
        self.trial2_lf = ttk.Labelframe(self.frame2,text="Preparation", bootstyle=INFO)
        self.trial2_lf.place(x=10,y=50,width=830,height=200)

        # description
        self.description_2 = ttk.Label(self.trial2_lf, text="Localization Scan will be used to locate the signal changes in the brain. 8 trials. Each trial will",font=("Calibri", 11))
        self.description_2.grid(row=self.trial2_row+1, column=0, columnspan=4, padx=5, pady=5)

        self.description_2 = ttk.Label(self.trial2_lf, text=" push up the piston for 1.5 second and push down for 1.5 second. 30 second rest between each trail.",font=("Calibri", 11))
        self.description_2.grid(row=self.trial2_row+2, column=0,columnspan=4, padx=5, pady=5)

        # # INPUT MVT
        self.input_subj = ttk.Label(self.trial2_lf, text="Subject Number:  ",font=("Calibri", 10))
        self.input_subj.grid(row=self.trial2_row+3, column=0, padx=5, pady=5)

        self.input_subj = ttk.Label(self.trial2_lf, text="Age:  ",font=("Calibri", 10))
        self.input_subj.grid(row=self.trial2_row+3, column=2, padx=5, pady=5)

        self.input_subj = ttk.Label(self.trial2_lf, text="Gender:  ",font=("Calibri", 10))
        self.input_subj.grid(row=self.trial2_row+4, column=0, padx=5, pady=5)

        self.input_subj = ttk.Label(self.trial2_lf, text="Weight(lb):  ",font=("Calibri", 10))
        self.input_subj.grid(row=self.trial2_row+4, column=2, padx=5, pady=5)

        self.input_subj = ttk.Label(self.trial2_lf, text="Dominant arm:  ",font=("Calibri", 10))
        self.input_subj.grid(row=self.trial2_row+5, column=0, padx=5, pady=5)

        ### Experimental 
        # add trial2 experimental label frame
        self.trial2_exp_lf = ttk.Labelframe(self.frame2,text="Experimental", bootstyle=INFO)
        self.trial2_exp_lf.place(x=10,y=300,width=830,height=365)

        # # UP IN UP&IN
        self.title_2 = ttk.Label(self.trial2_exp_lf, text="Click to start",font=("Calibri", 12, "bold"), bootstyle=PRIMARY)
        self.title_2.grid(row=self.trial2_row+0, column=0, padx=5, pady=5)

        self.trial2_button = ttk.Button(self.trial2_exp_lf, text="Start", command=self.trial2_Start, bootstyle=DANGER)
        self.trial2_button.grid(row=self.trial2_row+0,column=1, padx=5, pady=5)

        self.trial2_button_2 = ttk.Button(self.trial2_exp_lf, text="Stop", command=self.trial2_stop, bootstyle=DANGER)
        self.trial2_button_2.grid(row=self.trial2_row+0,column=2, padx=5, pady=5)

        # Trial and Status
        self.title_2 = ttk.Label(self.trial2_exp_lf, text="Current Trial: ",font=("Calibri", 12, "bold"))
        self.title_2.grid(row=self.trial2_row+1, column=0, padx=5, pady=5)

        self.title_2 = ttk.Label(self.trial2_exp_lf, text="Current Status: ",font=("Calibri", 12, "bold"))
        self.title_2.grid(row=self.trial2_row+1, column=2, padx=5, pady=5)

        self.title_2 = ttk.Label(self.trial2_exp_lf, text="       ",font=("Calibri", 12, "bold"))
        self.title_2.grid(row=self.trial2_row+2, column=2, padx=5, pady=5) 


        # Starting 
        self.title_2 = ttk.Label(self.trial2_exp_lf, text="The Experimental Progress Bar",font=("Calibri", 12, "bold"), bootstyle=INFO)
        self.title_2.grid(row=self.trial2_row+4, column=0, columnspan=5, padx=5, pady=5)   

        self.title_2 = ttk.Label(self.trial2_exp_lf, text="       ",font=("Calibri", 12, "bold"))
        self.title_2.grid(row=self.trial2_row+5, column=0, padx=5, pady=5)   

        self.trial2_bar_max = 1000
        self.title_2_fg = ttk.Floodgauge(self.trial2_exp_lf, bootstyle=INFO, length=750, maximum=self.trial2_bar_max, font=("Calibri", 12, 'bold'),)
        self.title_2_fg.grid(row=self.trial2_row+6, column=0, columnspan=5, padx=5, pady=3)  

        # End 
        self.End_lf = ttk.Frame(self.frame2)
        self.End_lf.place(x=700,y=740,width=100,height=50)

        self.quit = ttk.Button(self.End_lf, text='Exit', command=self.close, bootstyle=DANGER)
        self.quit.grid(row=0,column=0,padx=5, pady=5)

    def set_frame3(self): 
        # --------------------------- Frame 3 ----------------------------------------------
        self.trial3_row = 1
        self.is_start_trial3 = True
        # Title
        self.title = ttk.Label(self.frame3, text="                                          Functional Scan", bootstyle=DARK, font=("Calibri", 15, "bold"), background="")
        self.title.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

         ### Description
        # add EF label frame
        self.trial3_lf = ttk.Labelframe(self.frame3,text="Preparation", bootstyle=INFO)
        self.trial3_lf.place(x=10,y=50,width=830,height=350)

        # description
        self.description_3 = ttk.Label(self.trial3_lf, text="Functional stimulation task has 6 trials. Each trial will include 5 stimulation with different force levels.",font=("Calibri", 11))
        self.description_3.grid(row=self.trial3_row+0, column=0, columnspan=5, padx=5, pady=5)

        self.description_3 = ttk.Label(self.trial3_lf, text=" The duration of each test will increase from 6.0 second to 10.0 second. The order of rest time will be ",font=("Calibri", 11))
        self.description_3.grid(row=self.trial3_row+1, column=0, columnspan=5, padx=5, pady=5)

        self.description_3 = ttk.Label(self.trial3_lf, text="random but it will include 6, 7, 8, 9, 10. The order of force level will be randomly generated by Python.",font=("Calibri", 11))
        self.description_3.grid(row=self.trial3_row+2, column=0, columnspan=5, padx=5, pady=5)

        self.description_3 = ttk.Label(self.trial3_lf, text="Order of experiment",font=("Calibri", 11, "bold"),  bootstyle=PRIMARY)
        self.description_3.grid(row=self.trial3_row+3, column=1, columnspan=2, padx=5, pady=5)
        
        self.description_3 = ttk.Label(self.trial3_lf, text="        Trial1:  [high + 9 + low + 6 + medium + 7 + low + 10 + medium + 8]",font=("Calibri", 11))
        self.description_3.grid(row=self.trial3_row+3, column=3, columnspan=4, padx=5, pady=5)

        self.description_3 = ttk.Label(self.trial3_lf, text="       Trial2:  [low + 6 + high + 8 + low + 10 + medium + 9 + medium + 7]",font=("Calibri", 11))
        self.description_3.grid(row=self.trial3_row+4, column=3, columnspan=4, padx=5, pady=5)

        self.description_3 = ttk.Label(self.trial3_lf, text="        Trial3:  [low + 7 + medium + 10 + medium + 6 + high + 8 + high + 9]",font=("Calibri", 11))
        self.description_3.grid(row=self.trial3_row+5, column=3, columnspan=4, padx=5, pady=5)

        self.description_3 = ttk.Label(self.trial3_lf, text="Trial4:  [low + 10 + medium + 6 + high + 8 + high + 9 + low + 7]",font=("Calibri", 11))
        self.description_3.grid(row=self.trial3_row+6, column=3, columnspan=4, padx=5, pady=5)

        self.description_3 = ttk.Label(self.trial3_lf, text="Trial5:  [high + 8 + high + 7 + low + 9 + medium + 6 + high + 10]",font=("Calibri", 11))
        self.description_3.grid(row=self.trial3_row+7, column=3, columnspan=4, padx=5, pady=5)

        self.description_3 = ttk.Label(self.trial3_lf, text="      Trial6:  [high + 8 + low + 10 + medium + 7 + medium + 6 + low + 9]",font=("Calibri", 11))
        self.description_3.grid(row=self.trial3_row+8, column=3, columnspan=4, padx=5, pady=5)

        ### Experimental 
        # add trial3 experimental label frame
        self.trial3_exp_lf = ttk.Labelframe(self.frame3,text="Experimental", bootstyle=INFO)
        self.trial3_exp_lf.place(x=10,y=410,width=830,height=300)

        # select trail and task
        self.title_3 = ttk.Label(self.trial3_exp_lf, text="Choose to Start the Task",font=("Calibri", 12, "bold"), bootstyle=PRIMARY)
        self.title_3.grid(row=self.trial3_row+0, column=0, padx=5, pady=5)

        self.trial3_start_StinngVar = ttk.StringVar(self.master)
        self.trial3_start_First = 'Select a task'
        self.trial3_start_StinngVar.set(self.trial3_start_First)
        self.trial3_start_Type = ["Auto", "Trial 1", "Trial 2", "Trial 3", "Trial 4", "Trial 5", "Trial 6"]
        self.trial3_start_Menu = ttk.OptionMenu(self.trial3_exp_lf, self.trial3_start_StinngVar, self.trial3_start_Type[0], *self.trial3_start_Type,)
        self.trial3_start_Menu.grid(row=self.trial3_row+0,column=1, padx=5, pady=5)

        # add start and stop button
        self.trial3_button = ttk.Button(self.trial3_exp_lf, text="Start", command=self.trial3_Start, bootstyle=DANGER)
        self.trial3_button.grid(row=self.trial3_row+0,column=2, padx=5, pady=5)

        self.trial3_button_2 = ttk.Button(self.trial3_exp_lf, text="Stop", command=self.trial3_stop, bootstyle=DANGER)
        self.trial3_button_2.grid(row=self.trial3_row+0,column=3, padx=5, pady=5)

        # time and force
        self.title_3 = ttk.Label(self.trial3_exp_lf, text="Current Trial: ",font=("Calibri", 12, "bold"))
        self.title_3.grid(row=self.trial3_row+1, column=0, padx=5, pady=5)

        self.title_3 = ttk.Label(self.trial3_exp_lf, text="Current Status: ",font=("Calibri", 12, "bold"))
        self.title_3.grid(row=self.trial3_row+1, column=2, padx=5, pady=5)

        self.title_3 = ttk.Label(self.trial3_exp_lf, text="       ",font=("Calibri", 12, "bold"))
        self.title_3.grid(row=self.trial3_row+2, column=0, padx=5, pady=5) 


        # Progress bar
        self.title_3 = ttk.Label(self.trial3_exp_lf, text="The Experimental Progress Bar",font=("Calibri", 12, "bold"), bootstyle=INFO)
        self.title_3.grid(row=self.trial3_row+4, column=0, columnspan=4, padx=5, pady=5)   

        self.title_3 = ttk.Label(self.trial3_exp_lf, text="       ",font=("Calibri", 12, "bold"))
        self.title_3.grid(row=self.trial3_row+5, column=0, padx=5, pady=5)   

        self.title_3_fg = ttk.Floodgauge(self.trial3_exp_lf, bootstyle=INFO, length=750, maximum=1000, font=("Calibri", 12, 'bold'),)
        self.title_3_fg.grid(row=self.trial3_row+6, column=0, columnspan=5, padx=5, pady=3)  


        # End 
        self.End_lf = ttk.Frame(self.frame3)
        self.End_lf.place(x=700,y=750,width=100,height=50)

        self.quit = ttk.Button(self.End_lf, text='Exit', command=self.close, bootstyle=DANGER)
        self.quit.grid(row=0,column=0,padx=5, pady=5)


    # Helper functions
    def transmit(self, header, information):
        self.data_queue.put((header, information))

    def showError(self):
        print("retrycancel: ",Messagebox.show_error(title='Oh no', message="All fields should be filled"))

    # close the window
    def close(self):
        self.transmit("Close", "close")

    def pause(self):
        self.transmit("Pause", "pause")
        self.pause_bar = True
        print("Pause")

    def calculate_bar(self, mode):

        # Trial 1
        if mode == "trial1":
            # bar time
            bar_matrix = []
            bar_matrix.append(12)
            for i in range(11):
                bar_matrix.append(int(((i*2)/19.2)*718+12))
                bar_matrix.append(int(((i*2+2)/19.2)*718+12))
        
        elif mode == "trial3_block1":
            # [low + 9 + medium + 6 + low + 7 + low + 10 + medium + 8]
            rest_list = [9, 6, 7, 10, 8]
            
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
              
            
            # insert bar time into the matrix
            
            bar_matrix = []
            start_bar = 12
            bar_max = 748
            bar_matrix.append(start_bar)
            bar_matrix.append(int((in_1/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_1/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_2/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_2/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_3/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_3/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_4/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_4/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_5/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_5/out_5)*bar_max+start_bar))

        elif mode == "trial3_block2":
            # [high + 6 + low + 8 + high + 10 + low + 9 + medium + 7]
            rest_list = [6, 8, 10, 9, 7]
            
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
              
            
            # insert bar time into the matrix
            
            bar_matrix = []
            start_bar = 12
            bar_max = 748
            bar_matrix.append(start_bar)
            bar_matrix.append(int((in_1/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_1/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_2/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_2/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_3/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_3/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_4/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_4/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_5/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_5/out_5)*bar_max+start_bar))
        
        elif mode == "trial3_block3":
            # [high + 7 + medium + 10 + medium + 6 + high + 8 + medium + 9]
            rest_list = [7, 10, 6, 8, 9]
            
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
              
            
            # insert bar time into the matrix
            
            bar_matrix = []
            start_bar = 30
            bar_max = 748
            bar_matrix.append(start_bar)
            bar_matrix.append(int((in_1/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_1/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_2/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_2/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_3/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_3/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_4/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_4/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_5/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_5/out_5)*bar_max+start_bar))
        
        elif mode == "trial3_block4":
            # [low + 10 + high + 6 + high + 8 + medium + 9 + high + 7]
            rest_list = [10, 6, 8, 9, 7]
            
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
              
            
            # insert bar time into the matrix
            
            bar_matrix = []
            start_bar = 12
            bar_max = 748
            bar_matrix.append(start_bar)
            bar_matrix.append(int((in_1/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_1/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_2/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_2/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_3/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_3/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_4/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_4/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_5/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_5/out_5)*bar_max+start_bar))
        
        elif mode == "trial3_block5":
            # [high + 8 + low + 7 + low + 9 + high + 6 + medium + 10]
            rest_list = [8, 7, 9, 6, 10]
            
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
              
            
            # insert bar time into the matrix
            
            bar_matrix = []
            start_bar = 12
            bar_max = 748
            bar_matrix.append(start_bar)
            bar_matrix.append(int((in_1/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_1/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_2/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_2/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_3/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_3/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_4/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_4/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_5/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_5/out_5)*bar_max+start_bar))
        
        elif mode == "trial3_block6":
            # [high + 8 + low + 10 + medium + 7 + medium + 6 + low + 9]
            rest_list = [8, 10, 7, 6, 9]
            
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
              
            
            # insert bar time into the matrix
            
            bar_matrix = []
            start_bar = 12
            bar_max = 748
            bar_matrix.append(start_bar)
            bar_matrix.append(int((in_1/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_1/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_2/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_2/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_3/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_3/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_4/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_4/out_5)*bar_max+start_bar))
            bar_matrix.append(int((in_5/out_5)*bar_max+start_bar))
            bar_matrix.append(int((out_5/out_5)*bar_max+start_bar))



        return bar_matrix    

    # ---------------------------------------functions in frame 0---------------------------------------

    # check if all the data has been submitted in the frame 0
    def checkFields_frame0(self):
        result = []
        for i in range(3):
            result.append(self.subject_result[i].get())
        for i in result:
            if i == '':
                self.showError()
                return False
        return True      

    def trial0_start(self):
        # save the data
        trial0_exp_saved = []
        trial0_exp_header = []
        trial0_exp_header.append('Pressure regulator value')
        trial0_exp_header.append('Solenoid value')

        # save the subject information data
        trial0_exp_saved.append(self.trial0_result[0].get())
        trial0_exp_saved.append(self.trial0_start_StinngVar.get())

        is_correct = False
        if self.checkFields_frame0():
            is_correct = True

        if is_correct:
            trial0_control_Final = dict(zip(trial0_exp_header, trial0_exp_saved))
            self.transmit("Task0_control", trial0_control_Final)
            print(trial0_control_Final)

    def trial0_save(self):
        # save the data
        trial0_saved = []
        trial0_header = []
        for i in range(5):
            trial0_header.append(self.subjectInfo[i])

        # save the subject information data
        for i in range(3):
            trial0_saved.append(self.subject_result[i].get())

        trial0_saved.insert(2, self.genders_StinngVar.get())
        trial0_saved.append(self.domArm_StinngVar.get())

        # make sure all data has been input
        is_correct = False
        if self.checkFields_frame0():
            is_correct = True
        
        # if all data has been submitted correctly
        if is_correct:
            self.label1 = ttk.Label(self.sub_lf, text='Successfully Input !', bootstyle=SUCCESS)
            self.label1.grid(row=10, column=1)

            trial0_Final = dict(zip(trial0_header, trial0_saved))
            self.transmit("Task0_save", trial0_Final)

            print(trial0_Final)

            for i in [self.trial1_lf, self.trial2_lf]:
    
                self.input_subj = ttk.Label(i, text=trial0_saved[0],font=("Calibri", 10), bootstyle=SUCCESS)
                self.input_subj.grid(row=self.trial1_row+3, column=1, padx=5, pady=5)              

                self.input_subj = ttk.Label(i, text=trial0_saved[1],font=("Calibri", 10), bootstyle=SUCCESS)
                self.input_subj.grid(row=self.trial1_row+3, column=3, padx=5, pady=5)   

                self.input_subj = ttk.Label(i, text=trial0_saved[2],font=("Calibri", 10), bootstyle=SUCCESS)
                self.input_subj.grid(row=self.trial1_row+4, column=1, padx=5, pady=5) 

                self.input_subj = ttk.Label(i, text=trial0_saved[3],font=("Calibri", 10), bootstyle=SUCCESS)
                self.input_subj.grid(row=self.trial1_row+4, column=3, padx=5, pady=5) 

                self.input_subj = ttk.Label(i, text=trial0_saved[4],font=("Calibri", 10), bootstyle=SUCCESS)
                self.input_subj.grid(row=self.trial1_row+5, column=1, padx=5, pady=5) 


    # ---------------------------------------functions in frame 1---------------------------------------

    def trial1_Start(self):
        self.transmit("Start", 'start')
        print("Start the program")
        self.trial1_iteration()

    def trial1_iteration(self):
        self.afterid_1.set(self.after(100, self.trial1_iteration))
        # add new label
        if not self.in_queue.empty():
            self.Ext_queue = self.in_queue.get_nowait()
            print(self.Program_start)

            if self.Ext_queue == 1:
                self.Program_start = True
                self.after_cancel(self.afterid_1.get())
                self.trial2_program()
                self.Program_start = False

    def trial1_program(self):
        self.pause_bar = False
        self.stop_bar = False
        # save the data
        trial1_saved = []
        trial1_header = []
        trial1_header.append('Experiment Status')

        # make sure all data has been input
        is_correct = False
        if self.checkFields_frame0():
            is_correct = True

        # if all data has been submitted correctly
        if is_correct:
            self.trial1_break = False
            for trial_count in range(1,9):
                if self.trial1_break:
                    break
                
                trial1_saved.append("Trial " + str(trial_count))
                trial1_maxFinal = dict(zip(trial1_header, trial1_saved))
                
                if self.trial_finish or self.is_start_trial1:
                    self.transmit("Task1", trial1_maxFinal)
                    print(trial1_maxFinal)
                    self.is_start_trial1 = False
                    trial1_saved.pop()
                    # trial1_saved.pop()

                # delete the old bar
                self.delete_trial1_label()
                if self.is_rest_bar:
                    self.rest_bar.place_forget()

                # add label on the bar
                self.add_trial1_status(trial_count) 
                self.add_trial1()

                self.start_trial1_bar(525)

                # rest for 30 s
                self.delete_trial1_label()
                self.rest_bar = ttk.Label(self.frame1, text="Rest for 30 seconds",font=("Calibri", 12, "bold"), bootstyle=SUCCESS)
                self.rest_bar.place(x=300,y=530)

                self.is_rest_bar = True

                self.start_trial1_bar(525)

    def add_trial1_status(self, trial_number):

        self.title_1_current_trial = ttk.Label(self.trial1_exp_lf, text="Right "+" Trial "+ str(trial_number),font=("Calibri", 12, "bold"), bootstyle=WARNING)
        self.title_1_current_trial.grid(row=self.trial1_row+1, column=1, padx=5, pady=5)

        self.title_1_status_1 = ttk.Label(self.trial1_exp_lf, text="Strong force",font=("Calibri", 12, "bold"), bootstyle=WARNING)
        self.title_1_status_1.grid(row=self.trial1_row+1, column=3, padx=5, pady=5)   

        self.is_trial1_status = True

    def delete_trial1_label(self):
        if self.is_trial1_status:
            self.title_1_current_trial.grid_forget()
            self.title_1_status_1.grid_forget()
        if self.is_trial1:
                self.delete_trial1_bar()

        self.is_trial1_status = False

    def trial1_stop(self):
        self.Program_start = False
        self.stop_bar = True
        self.trial_finish = True
        self.trial1_break = True
        self.min_value = 0
        self.title_1_fg.grid_forget()
        self.title_1_fg = ttk.Floodgauge(self.trial1_exp_lf, bootstyle=INFO, length=750, maximum=self.trial1_bar_max, font=("Calibri", 12, 'bold'),)
        self.title_1_fg.grid(row=self.trial1_row+8, column=0, columnspan=5, padx=5, pady=3)  
        self.title_1_fg['value'] = 0
        self.transmit("Stop", "stop")
        print("Stop the trial !")

    def start_trial1_bar(self, max):
        # start the progressive bar
        self.title_1_fg['maximum'] = max
        self.title_1_fg['value'] = 0

        # if bar has never been start 
        if self.has_started_bar and not self.trial_finish:
            self.min = self.min_value
        else:
            self.min = 0

        is_get_min = False

        for i in range(self.min, max):

            if self.stop_bar:
                self.title_1_fg['value'] = 0
                self.trial1_exp_lf.update()
                time.sleep(0.05)
            else:
                self.title_1_fg['value'] = i+1
                self.trial1_exp_lf.update()
                time.sleep(0.05) 
                
            if self.title_1_fg['value'] == max:
                self.trial_finish = True

    def add_trial1(self):
        self.trial1_start_pos = self.calculate_bar("trial1")

        self.trial1_1 = ttk.Label(self.frame1, text="|1:On  Off",font=("Calibri", 10, "bold"))
        self.trial1_1.place(x=self.trial1_start_pos[0],y=495)  

        self.trial1_2 = ttk.Label(self.frame1, text="|2:On  Off",font=("Calibri", 10, "bold"))
        self.trial1_2.place(x=self.trial1_start_pos[2],y=495) 

        self.trial1_3 = ttk.Label(self.frame1, text="|3:On  Off",font=("Calibri", 10, "bold"))
        self.trial1_3.place(x=self.trial1_start_pos[4],y=495) 

        self.trial1_4 = ttk.Label(self.frame1, text="|4:On  Off",font=("Calibri", 10, "bold"))
        self.trial1_4.place(x=self.trial1_start_pos[6],y=495) 

        self.trial1_5 = ttk.Label(self.frame1, text="|5:On  Off",font=("Calibri", 10, "bold"))
        self.trial1_5.place(x=self.trial1_start_pos[8],y=495) 

        self.trial1_6 = ttk.Label(self.frame1, text="|6:On  Off",font=("Calibri", 10, "bold"))
        self.trial1_6.place(x=self.trial1_start_pos[10],y=495) 

        self.trial1_7 = ttk.Label(self.frame1, text="|7:On  Off",font=("Calibri", 10, "bold"))
        self.trial1_7.place(x=self.trial1_start_pos[12],y=495) 

        self.trial1_8 = ttk.Label(self.frame1, text="|8:On  Off",font=("Calibri", 10, "bold"))
        self.trial1_8.place(x=self.trial1_start_pos[14],y=495) 

        self.trial1_9 = ttk.Label(self.frame1, text="|9:On  Off",font=("Calibri", 10, "bold"))
        self.trial1_9.place(x=self.trial1_start_pos[16],y=495) 

        self.trial1_10 = ttk.Label(self.frame1, text="|10:On  Off",font=("Calibri", 10, "bold"))
        self.trial1_10.place(x=self.trial1_start_pos[18],y=495) 

        self.trial1_11 = ttk.Label(self.frame1, text="| ",font=("Calibri", 10, "bold"))
        self.trial1_11.place(x=self.trial1_start_pos[20],y=495) 

        self.is_trial1 = True
    
    def delete_trial1_bar(self):
        # delete the trial 1 bar
        self.trial1_1.place_forget()
        self.trial1_2.place_forget()
        self.trial1_3.place_forget()
        self.trial1_4.place_forget()
        self.trial1_5.place_forget()
        self.trial1_6.place_forget()
        self.trial1_7.place_forget()
        self.trial1_8.place_forget()
        self.trial1_9.place_forget()
        self.trial1_10.place_forget()
        self.trial1_11.place_forget()

        self.is_trial1 = False

    # ---------------------------------------functions in frame 2---------------------------------------

    def trial2_Start(self):
        self.transmit("Start", 'start')
        print("Start the program")
        # clear the queue data
        while not self.in_queue.empty():
            self.in_queue.get() 
        self.BNC_2 = ttk.Label(self.frame2, text="Waiting for the signal",font=("Calibri", 12, "bold"), bootstyle=SUCCESS)
        self.BNC_2.place(x=300,y=530)
        self.trial2_iteration()


    def trial2_iteration(self):
        self.afterid_2.set(self.after(1, self.trial2_iteration))
        # add new label
        if not self.in_queue.empty():
            self.Ext_queue = self.in_queue.get_nowait()

            if self.Ext_queue == 1:
                self.Program_start = True
                self.after_cancel(self.afterid_2.get())
                self.trial2_program()
                self.Program_start = False


    
    def trial2_program(self):
        self.BNC_2.place_forget()
        self.pause_bar = False
        self.stop_bar = False
        # save the data
        trial2_saved = []
        trial2_header = []
        trial2_header.append('Experiment Status')

        # make sure all data has been input
        is_correct = False
        if self.checkFields_frame0():
            is_correct = True

        # if all data has been submitted correctly
        if is_correct:
            # rest for 30 s
            self.delete_trial2_label()
            self.rest_bar = ttk.Label(self.frame2, text="Rest for 30 seconds",font=("Calibri", 12, "bold"), bootstyle=SUCCESS)
            self.rest_bar.place(x=300,y=530)

            self.is_rest_bar = True

            self.trial2_break = False
            self.start_trial2_bar(525)
            

            for trial_count in range(1,7):
                if self.trial2_break:
                    break
                
                trial2_saved.append("Trial " + str(trial_count))
                trial2_maxFinal = dict(zip(trial2_header, trial2_saved))
                
                if self.trial_finish or self.is_start_trial2:
                    self.transmit("Task2", trial2_maxFinal)
                    print(trial2_maxFinal)
                    self.is_start_trial2 = False
                    trial2_saved.pop()

                # delete the old bar
                self.delete_trial2_label()
                if self.is_rest_bar:
                    self.rest_bar.place_forget()

                # add label on the bar
                self.add_trial2_status(trial_count) 
                self.add_trial2()

                # start the progressive bar
                self.start_trial2_bar(525)

                # rest for 30 s
                self.delete_trial2_label()
                self.rest_bar = ttk.Label(self.frame2, text="Rest for 30 seconds",font=("Calibri", 12, "bold"), bootstyle=SUCCESS)
                self.rest_bar.place(x=300,y=530)

                self.is_rest_bar = True

                self.start_trial2_bar(525)

    def add_trial2_status(self, trial_number):

        self.title_2_current_trial = ttk.Label(self.trial2_exp_lf, text="Right "+" Trial "+ str(trial_number),font=("Calibri", 12, "bold"), bootstyle=WARNING)
        self.title_2_current_trial.grid(row=self.trial2_row+1, column=1, padx=5, pady=5)

        self.title_2_status_1 = ttk.Label(self.trial2_exp_lf, text="Strong force",font=("Calibri", 12, "bold"), bootstyle=WARNING)
        self.title_2_status_1.grid(row=self.trial2_row+1, column=3, padx=5, pady=5)   

        self.is_trial2_status = True

    def delete_trial2_label(self):
        if self.is_trial2_status:
            self.title_2_current_trial.grid_forget()
            self.title_2_status_1.grid_forget()
        if self.is_trial2:
                self.delete_trial2_bar()

        self.is_trial2_status = False

    def trial2_stop(self):
        self.Program_start = False
        self.stop_bar = True
        self.trial_finish = True
        self.trial2_break = True
        self.min_value = 0
        self.title_2_fg.grid_forget()
        self.title_2_fg = ttk.Floodgauge(self.trial2_exp_lf, bootstyle=INFO, length=750, maximum=self.trial2_bar_max, font=("Calibri", 12, 'bold'),)
        self.title_2_fg.grid(row=self.trial2_row+8, column=0, columnspan=5, padx=5, pady=3)  
        self.title_2_fg['value'] = 0
        self.transmit("Stop", "stop")
        print("Stop the trial !")

    def start_trial2_bar(self, max):
        # start the progressive bar
        self.title_2_fg['maximum'] = max
        self.title_2_fg['value'] = 0

        # if bar has never been start 
        if self.has_started_bar and not self.trial_finish:
            self.min = self.min_value
        else:
            self.min = 0

        is_get_min = False

        for i in range(self.min, max):

            if self.stop_bar:
                self.title_2_fg['value'] = 0
                self.trial2_exp_lf.update()
                time.sleep(0.05)
            else:
                self.title_2_fg['value'] = i+1
                self.trial2_exp_lf.update()
                time.sleep(0.05) 
                
            if self.title_2_fg['value'] == max:
                self.trial_finish = True

    def add_trial2(self):
        self.trial2_start_pos = self.calculate_bar("trial1")

        self.trial2_1 = ttk.Label(self.frame2, text="|1:On  Off",font=("Calibri", 10, "bold"))
        self.trial2_1.place(x=self.trial2_start_pos[0],y=495)  

        self.trial2_2 = ttk.Label(self.frame2, text="|2:On  Off",font=("Calibri", 10, "bold"))
        self.trial2_2.place(x=self.trial2_start_pos[2],y=495) 

        self.trial2_3 = ttk.Label(self.frame2, text="|3:On  Off",font=("Calibri", 10, "bold"))
        self.trial2_3.place(x=self.trial2_start_pos[4],y=495) 

        self.trial2_4 = ttk.Label(self.frame2, text="|4:On  Off",font=("Calibri", 10, "bold"))
        self.trial2_4.place(x=self.trial2_start_pos[6],y=495) 

        self.trial2_5 = ttk.Label(self.frame2, text="|5:On  Off",font=("Calibri", 10, "bold"))
        self.trial2_5.place(x=self.trial2_start_pos[8],y=495) 

        self.trial2_6 = ttk.Label(self.frame2, text="|6:On  Off",font=("Calibri", 10, "bold"))
        self.trial2_6.place(x=self.trial2_start_pos[10],y=495) 

        self.trial2_7 = ttk.Label(self.frame2, text="|7:On  Off",font=("Calibri", 10, "bold"))
        self.trial2_7.place(x=self.trial2_start_pos[12],y=495) 

        self.trial2_8 = ttk.Label(self.frame2, text="|8:On  Off",font=("Calibri", 10, "bold"))
        self.trial2_8.place(x=self.trial2_start_pos[14],y=495) 

        self.trial2_9 = ttk.Label(self.frame2, text="|9:On  Off",font=("Calibri", 10, "bold"))
        self.trial2_9.place(x=self.trial2_start_pos[16],y=495)

        self.trial2_10 = ttk.Label(self.frame2, text="|10:On  Off",font=("Calibri", 10, "bold"))
        self.trial2_10.place(x=self.trial2_start_pos[18],y=495)

        self.trial2_11 = ttk.Label(self.frame2, text="| ",font=("Calibri", 10, "bold"))
        self.trial2_11.place(x=self.trial2_start_pos[20],y=495) 

        self.is_trial2 = True

    def delete_trial2_bar(self):
        # delete the trial 2 bar
        self.trial2_1.place_forget()
        self.trial2_2.place_forget()
        self.trial2_3.place_forget()
        self.trial2_4.place_forget()
        self.trial2_5.place_forget()
        self.trial2_6.place_forget()
        self.trial2_7.place_forget()
        self.trial2_8.place_forget()
        self.trial2_9.place_forget()
        self.trial2_10.place_forget()
        self.trial2_11.place_forget()

        self.is_trial2 = False


    # ---------------------------------------functions in frame 3---------------------------------------
    def trial3_Start(self):
        self.transmit("Start", 'start')
        print("Start the program")
        # clear the queue data
        while not self.in_queue.empty():
            self.in_queue.get() 
        self.BNC_3 = ttk.Label(self.frame3, text="Waiting for the signal",font=("Calibri", 12, "bold"), bootstyle=SUCCESS)
        self.BNC_3.place(x=300,y=640)
        self.trial3_iteration()
    
    def trial3_iteration(self):
        self.afterid_3.set(self.after(100, self.trial3_iteration))
        # add new label
        if not self.in_queue.empty():
            self.Ext_queue = self.in_queue.get_nowait()

            if self.Ext_queue == 1:
                self.Program_start = True
                self.after_cancel(self.afterid_3.get())
                self.trial3_program()
                self.Program_start = False

    def trial3_program(self):
        self.BNC_3.place_forget()
        self.pause_bar = False
        self.stop_bar = False
        # save the data
        trial3_saved = []

        trial3_header = []
        trial3_header.append('Experiment Mode')

        # make sure all data has been input
        is_correct = False
        if self.checkFields_frame0():
            is_correct = True

        # if all data has been submitted correctly
        if is_correct:

            if self.trial3_start_StinngVar.get() == "Auto":
                # rest for 30 s
                self.delete_trial3_label()
                self.rest_bar = ttk.Label(self.frame3, text="Rest for 30 seconds",font=("Calibri", 12, "bold"), bootstyle=SUCCESS)
                self.rest_bar.place(x=300,y=640)
                self.is_rest_bar = True

                self.start_trial3_bar(475)
                self.trial3_break = False
                for trial_count in range(1,7):
                    # if click the stop button, then stop the trial
                    if self.trial3_break:
                        break
                    
                    # send the current status to the main loop
                    trial3_saved.append("Trial " + str(trial_count))
                    trial3_maxFinal = dict(zip(trial3_header, trial3_saved))
                    if self.trial_finish or self.is_start_trial1:
                        self.transmit("Task3", trial3_maxFinal)
                        print(trial3_maxFinal)
                        trial3_saved.pop()
                        self.is_start_trial3 = False

                    # add the bar
                    if trial_count == 1:
                        self.delete_trial3_label()
                        self.add_trial3_block1()
                    elif trial_count == 2:
                        self.delete_trial3_label()
                        self.add_trial3_block2()
                    elif trial_count == 3:
                        self.delete_trial3_label()
                        self.add_trial3_block3()
                    elif trial_count == 4:
                        self.delete_trial3_label()
                        self.add_trial3_block4()
                    elif trial_count == 5:
                        self.delete_trial3_label()
                        self.add_trial3_block5()
                    elif trial_count == 6:
                        self.delete_trial3_label()
                        self.add_trial3_block6()

                    # add label on the bar
                    self.add_trial3_status(trial_count) 

                    # start the progressive bar
                    self.start_trial3_bar(760)

                    # rest for 30 s
                    self.delete_trial3_label()
                    self.rest_bar = ttk.Label(self.frame3, text="Rest for 30 seconds",font=("Calibri", 12, "bold"), bootstyle=SUCCESS)
                    self.rest_bar.place(x=300,y=640)
                    self.is_rest_bar = True

                    self.start_trial3_bar(475)

            elif self.trial3_start_StinngVar.get()[0] != "A":
                # send the current status to the main loop
                trial3_saved.append(self.trial3_start_StinngVar.get())
                trial3_maxFinal = dict(zip(trial3_header, trial3_saved))
                if self.trial_finish or self.is_start_trial3:
                    self.transmit("Task3", trial3_maxFinal)
                    self.is_start_trial3 = False
                    print(trial3_maxFinal)

                # get the block number
                trial_count = int(self.trial3_start_StinngVar.get()[6])

                # add the bar
                if trial_count == 1:
                    self.delete_trial3_label()
                    self.add_trial3_block1()
                elif trial_count == 2:
                    self.delete_trial3_label()
                    self.add_trial3_block2()
                elif trial_count == 3:
                    self.delete_trial3_label()
                    self.add_trial3_block3()
                elif trial_count == 4:
                    self.delete_trial3_label()
                    self.add_trial3_block4()
                elif trial_count == 5:
                    self.delete_trial3_label()
                    self.add_trial3_block5()
                elif trial_count == 6:
                    self.delete_trial3_label()
                    self.add_trial3_block6()

                self.add_trial3_status(int(self.trial3_start_StinngVar.get()[6]))

                # start the progressive bar
                self.start_trial3_bar(760)      
            else:
                print("retrycancel: ",Messagebox.show_error(title='Oh no', message="Please choose correct task!"))   

    def add_trial3_status(self, trial_number):
        self.title_3_current_trial = ttk.Label(self.trial3_exp_lf, text="Right "+" Trial "+ str(trial_number),font=("Calibri", 12, "bold"), bootstyle=WARNING)
        self.title_3_current_trial.grid(row=self.trial3_row+1, column=1, padx=5, pady=5)

        if trial_number == 1:
            self.title_3_status_1 = ttk.Label(self.trial3_exp_lf, text="high low medium low medium",font=("Calibri", 12, "bold"), bootstyle=WARNING)
            self.title_3_status_1.grid(row=self.trial3_row+1, column=3, padx=5, pady=5)   

            self.title_3_status_2 = ttk.Label(self.trial3_exp_lf, text="9  6  7  10  8",font=("Calibri", 12, "bold"), bootstyle=WARNING)
            self.title_3_status_2.grid(row=self.trial3_row+2, column=3, padx=5, pady=5) 
        
        elif trial_number == 2:
            self.title_3_status_1 = ttk.Label(self.trial3_exp_lf, text="low high low medium medium",font=("Calibri", 12, "bold"), bootstyle=WARNING)
            self.title_3_status_1.grid(row=self.trial3_row+1, column=3, padx=5, pady=5)   

            self.title_3_status_2 = ttk.Label(self.trial3_exp_lf, text="6  8  10  9  7",font=("Calibri", 12, "bold"), bootstyle=WARNING)
            self.title_3_status_2.grid(row=self.trial3_row+2, column=3, padx=5, pady=5) 
        
        elif trial_number == 3:
            self.title_3_status_1 = ttk.Label(self.trial3_exp_lf, text="low medium medium high high",font=("Calibri", 12, "bold"), bootstyle=WARNING)
            self.title_3_status_1.grid(row=self.trial3_row+1, column=3, padx=5, pady=5)   

            self.title_3_status_2 = ttk.Label(self.trial3_exp_lf, text="7  10  6  8  9",font=("Calibri", 12, "bold"), bootstyle=WARNING)
            self.title_3_status_2.grid(row=self.trial3_row+2, column=3, padx=5, pady=5) 

        elif trial_number == 4:
            self.title_3_status_1 = ttk.Label(self.trial3_exp_lf, text="low medium high high low",font=("Calibri", 12, "bold"), bootstyle=WARNING)
            self.title_3_status_1.grid(row=self.trial3_row+1, column=3, padx=5, pady=5)   

            self.title_3_status_2 = ttk.Label(self.trial3_exp_lf, text="10  6  8  9  7",font=("Calibri", 12, "bold"), bootstyle=WARNING)
            self.title_3_status_2.grid(row=self.trial3_row+2, column=3, padx=5, pady=5) 
        
        elif trial_number == 5:
            self.title_3_status_1 = ttk.Label(self.trial3_exp_lf, text="high high low medium high",font=("Calibri", 12, "bold"), bootstyle=WARNING)
            self.title_3_status_1.grid(row=self.trial3_row+1, column=3, padx=5, pady=5)   

            self.title_3_status_2 = ttk.Label(self.trial3_exp_lf, text="8  7  9  6  10",font=("Calibri", 12, "bold"), bootstyle=WARNING)
            self.title_3_status_2.grid(row=self.trial3_row+2, column=3, padx=5, pady=5) 
        
        elif trial_number == 6:
            self.title_3_status_1 = ttk.Label(self.trial3_exp_lf, text="high low medium medium low ",font=("Calibri", 12, "bold"), bootstyle=WARNING)
            self.title_3_status_1.grid(row=self.trial3_row+1, column=3, padx=5, pady=5)   

            self.title_3_status_2 = ttk.Label(self.trial3_exp_lf, text="8  10  7  6  9",font=("Calibri", 12, "bold"), bootstyle=WARNING)
            self.title_3_status_2.grid(row=self.trial3_row+2, column=3, padx=5, pady=5)


        self.is_trial3_status = True

    def trial3_stop(self):
        self.Program_start = False
        self.stop_bar = True
        self.trial_finish = True
        self.trial3_break = True
        self.min_value = 0
        self.title_3_fg.grid_forget()
        self.title_3_fg = ttk.Floodgauge(self.trial3_exp_lf, bootstyle=INFO, length=750, maximum=self.trial1_bar_max, font=("Calibri", 12, 'bold'),)
        self.title_3_fg.grid(row=self.trial3_row+8, column=0, columnspan=5, padx=5, pady=3)  
        self.title_3_fg['value'] = 0
        self.transmit("Stop", "stop")

    def start_trial3_bar(self, max):
        # start the progressive bar
        self.title_3_fg['maximum'] = max
        self.title_3_fg['value'] = 0

        # if bar has never been start 
        if self.has_started_bar and not self.trial_finish:
            self.min = self.min_value
        else:
            self.min = 0

        is_get_min = False

        for i in range(self.min, max):

            if self.stop_bar:
                self.title_3_fg['value'] = 0
                self.trial3_exp_lf.update()
                time.sleep(0.05)
            else:
                self.title_3_fg['value'] = i+1
                self.trial3_exp_lf.update()
                time.sleep(0.05) 
                
            if self.title_3_fg['value'] == max:
                self.trial_finish = True


    def add_trial3_block1(self):
        self.trial3_start_pos = self.calculate_bar("trial3_block1")

        self.trial3_block1_1 = ttk.Label(self.frame3, text="| H",font=("Calibri", 10, "bold"))
        self.trial3_block1_1.place(x=self.trial3_start_pos[0],y=605)  

        self.trial3_block1_2 = ttk.Label(self.frame3, text="| 9s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block1_2.place(x=self.trial3_start_pos[1],y=605) 

        self.trial3_block1_3 = ttk.Label(self.frame3, text="| L",font=("Calibri", 10, "bold"))
        self.trial3_block1_3.place(x=self.trial3_start_pos[2],y=605) 

        self.trial3_block1_4 = ttk.Label(self.frame3, text="| 6s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block1_4.place(x=self.trial3_start_pos[3],y=605) 

        self.trial3_block1_5 = ttk.Label(self.frame3, text="| M ",font=("Calibri", 10, "bold"))
        self.trial3_block1_5.place(x=self.trial3_start_pos[4],y=605) 

        self.trial3_block1_6 = ttk.Label(self.frame3, text="| 7s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block1_6.place(x=self.trial3_start_pos[5],y=605) 

        self.trial3_block1_7 = ttk.Label(self.frame3, text="| L",font=("Calibri", 10, "bold"))
        self.trial3_block1_7.place(x=self.trial3_start_pos[6],y=605) 

        self.trial3_block1_8 = ttk.Label(self.frame3, text="| 10s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block1_8.place(x=self.trial3_start_pos[7],y=605) 

        self.trial3_block1_9 = ttk.Label(self.frame3, text="| M",font=("Calibri", 10, "bold"))
        self.trial3_block1_9.place(x=self.trial3_start_pos[8],y=605) 

        self.trial3_block1_10 = ttk.Label(self.frame3, text="| 8s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block1_10.place(x=self.trial3_start_pos[9],y=605) 

        self.trial3_block1_11 = ttk.Label(self.frame3, text="| ",font=("Calibri", 10, "bold"))
        self.trial3_block1_11.place(x=self.trial3_start_pos[10],y=605) 


        self.is_trial3_block1 = True

    def delete_trial3_block1(self):
        # delete the block 1 bar
        self.trial3_block1_1.place_forget()
        self.trial3_block1_2.place_forget()
        self.trial3_block1_3.place_forget()
        self.trial3_block1_4.place_forget()
        self.trial3_block1_5.place_forget()
        self.trial3_block1_6.place_forget()
        self.trial3_block1_7.place_forget()
        self.trial3_block1_8.place_forget()
        self.trial3_block1_9.place_forget()
        self.trial3_block1_10.place_forget()
        self.trial3_block1_11.place_forget()

        self.is_trial3_block1 = False

    def add_trial3_block2(self):
        self.trial3_start_pos = self.calculate_bar("trial3_block2")

        self.trial3_block2_1 = ttk.Label(self.frame3, text="| L",font=("Calibri", 10, "bold"))
        self.trial3_block2_1.place(x=self.trial3_start_pos[0],y=605)  

        self.trial3_block2_2 = ttk.Label(self.frame3, text="| 6s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block2_2.place(x=self.trial3_start_pos[1],y=605) 

        self.trial3_block2_3 = ttk.Label(self.frame3, text="| H",font=("Calibri", 10, "bold"))
        self.trial3_block2_3.place(x=self.trial3_start_pos[2],y=605) 

        self.trial3_block2_4 = ttk.Label(self.frame3, text="| 8s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block2_4.place(x=self.trial3_start_pos[3],y=605) 

        self.trial3_block2_5 = ttk.Label(self.frame3, text="| L ",font=("Calibri", 10, "bold"))
        self.trial3_block2_5.place(x=self.trial3_start_pos[4],y=605) 

        self.trial3_block2_6 = ttk.Label(self.frame3, text="| 10s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block2_6.place(x=self.trial3_start_pos[5],y=605) 

        self.trial3_block2_7 = ttk.Label(self.frame3, text="| M",font=("Calibri", 10, "bold"))
        self.trial3_block2_7.place(x=self.trial3_start_pos[6],y=605) 

        self.trial3_block2_8 = ttk.Label(self.frame3, text="| 9s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block2_8.place(x=self.trial3_start_pos[7],y=605) 

        self.trial3_block2_9 = ttk.Label(self.frame3, text="| M",font=("Calibri", 10, "bold"))
        self.trial3_block2_9.place(x=self.trial3_start_pos[8],y=605) 

        self.trial3_block2_10 = ttk.Label(self.frame3, text="| 7s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block2_10.place(x=self.trial3_start_pos[9],y=605) 

        self.trial3_block2_11 = ttk.Label(self.frame3, text="| ",font=("Calibri", 10, "bold"))
        self.trial3_block2_11.place(x=self.trial3_start_pos[10],y=605) 


        self.is_trial3_block2 = True

    def delete_trial3_block2(self):
        # delete the block 2 bar
        self.trial3_block2_1.place_forget()
        self.trial3_block2_2.place_forget()
        self.trial3_block2_3.place_forget()
        self.trial3_block2_4.place_forget()
        self.trial3_block2_5.place_forget()
        self.trial3_block2_6.place_forget()
        self.trial3_block2_7.place_forget()
        self.trial3_block2_8.place_forget()
        self.trial3_block2_9.place_forget()
        self.trial3_block2_10.place_forget()
        self.trial3_block2_11.place_forget()

        self.is_trial3_block2 = False
    
    def add_trial3_block3(self):
        self.trial3_start_pos = self.calculate_bar("trial3_block3")

        self.trial3_block3_1 = ttk.Label(self.frame3, text="| L",font=("Calibri", 10, "bold"))
        self.trial3_block3_1.place(x=self.trial3_start_pos[0],y=605)  

        self.trial3_block3_2 = ttk.Label(self.frame3, text="| 7s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block3_2.place(x=self.trial3_start_pos[1],y=605) 

        self.trial3_block3_3 = ttk.Label(self.frame3, text="| M",font=("Calibri", 10, "bold"))
        self.trial3_block3_3.place(x=self.trial3_start_pos[2],y=605) 

        self.trial3_block3_4 = ttk.Label(self.frame3, text="| 10s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block3_4.place(x=self.trial3_start_pos[3],y=605) 

        self.trial3_block3_5 = ttk.Label(self.frame3, text="| M ",font=("Calibri", 10, "bold"))
        self.trial3_block3_5.place(x=self.trial3_start_pos[4],y=605) 

        self.trial3_block3_6 = ttk.Label(self.frame3, text="| 6s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block3_6.place(x=self.trial3_start_pos[5],y=605) 

        self.trial3_block3_7 = ttk.Label(self.frame3, text="| H",font=("Calibri", 10, "bold"))
        self.trial3_block3_7.place(x=self.trial3_start_pos[6],y=605) 

        self.trial3_block3_8 = ttk.Label(self.frame3, text="| 8s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block3_8.place(x=self.trial3_start_pos[7],y=605) 

        self.trial3_block3_9 = ttk.Label(self.frame3, text="| H",font=("Calibri", 10, "bold"))
        self.trial3_block3_9.place(x=self.trial3_start_pos[8],y=605) 

        self.trial3_block3_10 = ttk.Label(self.frame3, text="| 9s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block3_10.place(x=self.trial3_start_pos[9],y=605) 

        self.trial3_block3_11 = ttk.Label(self.frame3, text="| ",font=("Calibri", 10, "bold"))
        self.trial3_block3_11.place(x=self.trial3_start_pos[10],y=605) 


        self.is_trial3_block3 = True

    def delete_trial3_block3(self):
        # delete the block 3 bar
        self.trial3_block3_1.place_forget()
        self.trial3_block3_2.place_forget()
        self.trial3_block3_3.place_forget()
        self.trial3_block3_4.place_forget()
        self.trial3_block3_5.place_forget()
        self.trial3_block3_6.place_forget()
        self.trial3_block3_7.place_forget()
        self.trial3_block3_8.place_forget()
        self.trial3_block3_9.place_forget()
        self.trial3_block3_10.place_forget()
        self.trial3_block3_11.place_forget()

        self.is_trial3_block3 = False
    
    def add_trial3_block4(self):
        self.trial3_start_pos = self.calculate_bar("trial3_block4")

        self.trial3_block4_1 = ttk.Label(self.frame3, text="| L",font=("Calibri", 10, "bold"))
        self.trial3_block4_1.place(x=self.trial3_start_pos[0],y=605)  

        self.trial3_block4_2 = ttk.Label(self.frame3, text="| 10s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block4_2.place(x=self.trial3_start_pos[1],y=605) 

        self.trial3_block4_3 = ttk.Label(self.frame3, text="| M",font=("Calibri", 10, "bold"))
        self.trial3_block4_3.place(x=self.trial3_start_pos[2],y=605) 

        self.trial3_block4_4 = ttk.Label(self.frame3, text="| 6s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block4_4.place(x=self.trial3_start_pos[3],y=605) 

        self.trial3_block4_5 = ttk.Label(self.frame3, text="| H ",font=("Calibri", 10, "bold"))
        self.trial3_block4_5.place(x=self.trial3_start_pos[4],y=605) 

        self.trial3_block4_6 = ttk.Label(self.frame3, text="| 8s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block4_6.place(x=self.trial3_start_pos[5],y=605) 

        self.trial3_block4_7 = ttk.Label(self.frame3, text="| H",font=("Calibri", 10, "bold"))
        self.trial3_block4_7.place(x=self.trial3_start_pos[6],y=605) 

        self.trial3_block4_8 = ttk.Label(self.frame3, text="| 9s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block4_8.place(x=self.trial3_start_pos[7],y=605) 

        self.trial3_block4_9 = ttk.Label(self.frame3, text="| L",font=("Calibri", 10, "bold"))
        self.trial3_block4_9.place(x=self.trial3_start_pos[8],y=605) 

        self.trial3_block4_10 = ttk.Label(self.frame3, text="| 7s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block4_10.place(x=self.trial3_start_pos[9],y=605) 

        self.trial3_block4_11 = ttk.Label(self.frame3, text="| ",font=("Calibri", 10, "bold"))
        self.trial3_block4_11.place(x=self.trial3_start_pos[10],y=605) 


        self.is_trial3_block4 = True

    def delete_trial3_block4(self):
        # delete the block 4 bar
        self.trial3_block4_1.place_forget()
        self.trial3_block4_2.place_forget()
        self.trial3_block4_3.place_forget()
        self.trial3_block4_4.place_forget()
        self.trial3_block4_5.place_forget()
        self.trial3_block4_6.place_forget()
        self.trial3_block4_7.place_forget()
        self.trial3_block4_8.place_forget()
        self.trial3_block4_9.place_forget()
        self.trial3_block4_10.place_forget()
        self.trial3_block4_11.place_forget()

        self.is_trial3_block4 = False
    
    def add_trial3_block5(self):
        self.trial3_start_pos = self.calculate_bar("trial3_block5")

        self.trial3_block5_1 = ttk.Label(self.frame3, text="| H",font=("Calibri", 10, "bold"))
        self.trial3_block5_1.place(x=self.trial3_start_pos[0],y=605)  

        self.trial3_block5_2 = ttk.Label(self.frame3, text="| 8s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block5_2.place(x=self.trial3_start_pos[1],y=605) 

        self.trial3_block5_3 = ttk.Label(self.frame3, text="| H",font=("Calibri", 10, "bold"))
        self.trial3_block5_3.place(x=self.trial3_start_pos[2],y=605) 

        self.trial3_block5_4 = ttk.Label(self.frame3, text="| 7s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block5_4.place(x=self.trial3_start_pos[3],y=605) 

        self.trial3_block5_5 = ttk.Label(self.frame3, text="| L ",font=("Calibri", 10, "bold"))
        self.trial3_block5_5.place(x=self.trial3_start_pos[4],y=605) 

        self.trial3_block5_6 = ttk.Label(self.frame3, text="| 9s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block5_6.place(x=self.trial3_start_pos[5],y=605) 

        self.trial3_block5_7 = ttk.Label(self.frame3, text="| M",font=("Calibri", 10, "bold"))
        self.trial3_block5_7.place(x=self.trial3_start_pos[6],y=605) 

        self.trial3_block5_8 = ttk.Label(self.frame3, text="| 6s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block5_8.place(x=self.trial3_start_pos[7],y=605) 

        self.trial3_block5_9 = ttk.Label(self.frame3, text="| H",font=("Calibri", 10, "bold"))
        self.trial3_block5_9.place(x=self.trial3_start_pos[8],y=605) 

        self.trial3_block5_10 = ttk.Label(self.frame3, text="| 10s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block5_10.place(x=self.trial3_start_pos[9],y=605) 

        self.trial3_block5_11 = ttk.Label(self.frame3, text="| ",font=("Calibri", 10, "bold"))
        self.trial3_block5_11.place(x=self.trial3_start_pos[10],y=605) 


        self.is_trial3_block5 = True

    def delete_trial3_block5(self):
        # delete the block 5 bar
        self.trial3_block5_1.place_forget()
        self.trial3_block5_2.place_forget()
        self.trial3_block5_3.place_forget()
        self.trial3_block5_4.place_forget()
        self.trial3_block5_5.place_forget()
        self.trial3_block5_6.place_forget()
        self.trial3_block5_7.place_forget()
        self.trial3_block5_8.place_forget()
        self.trial3_block5_9.place_forget()
        self.trial3_block5_10.place_forget()
        self.trial3_block5_11.place_forget()

        self.is_trial3_block5 = False

    def add_trial3_block6(self):
        self.trial3_start_pos = self.calculate_bar("trial3_block6")

        self.trial3_block6_1 = ttk.Label(self.frame3, text="| H",font=("Calibri", 10, "bold"))
        self.trial3_block6_1.place(x=self.trial3_start_pos[0],y=605)  

        self.trial3_block6_2 = ttk.Label(self.frame3, text="| 8s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block6_2.place(x=self.trial3_start_pos[1],y=605) 

        self.trial3_block6_3 = ttk.Label(self.frame3, text="| L",font=("Calibri", 10, "bold"))
        self.trial3_block6_3.place(x=self.trial3_start_pos[2],y=605) 

        self.trial3_block6_4 = ttk.Label(self.frame3, text="| 10s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block6_4.place(x=self.trial3_start_pos[3],y=605) 

        self.trial3_block6_5 = ttk.Label(self.frame3, text="| M ",font=("Calibri", 10, "bold"))
        self.trial3_block6_5.place(x=self.trial3_start_pos[4],y=605) 

        self.trial3_block6_6 = ttk.Label(self.frame3, text="| 7s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block6_6.place(x=self.trial3_start_pos[5],y=605) 

        self.trial3_block6_7 = ttk.Label(self.frame3, text="| M",font=("Calibri", 10, "bold"))
        self.trial3_block6_7.place(x=self.trial3_start_pos[6],y=605) 

        self.trial3_block6_8 = ttk.Label(self.frame3, text="| 6s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block6_8.place(x=self.trial3_start_pos[7],y=605) 

        self.trial3_block6_9 = ttk.Label(self.frame3, text="| L",font=("Calibri", 10, "bold"))
        self.trial3_block6_9.place(x=self.trial3_start_pos[8],y=605) 

        self.trial3_block6_10 = ttk.Label(self.frame3, text="| 9s Off ",font=("Calibri", 10, "bold"))
        self.trial3_block6_10.place(x=self.trial3_start_pos[9],y=605) 

        self.trial3_block6_11 = ttk.Label(self.frame3, text="| ",font=("Calibri", 10, "bold"))
        self.trial3_block6_11.place(x=self.trial3_start_pos[10],y=605) 


        self.is_trial3_block6 = True

    def delete_trial3_block6(self):
        # delete the block 6 bar
        self.trial3_block6_1.place_forget()
        self.trial3_block6_2.place_forget()
        self.trial3_block6_3.place_forget()
        self.trial3_block6_4.place_forget()
        self.trial3_block6_5.place_forget()
        self.trial3_block6_6.place_forget()
        self.trial3_block6_7.place_forget()
        self.trial3_block6_8.place_forget()
        self.trial3_block6_9.place_forget()
        self.trial3_block6_10.place_forget()
        self.trial3_block6_11.place_forget()

        self.is_trial3_block6 = False


    def delete_trial3_label(self):
        if self.is_trial3_status:
            self.title_3_current_trial.grid_forget()
            self.title_3_status_1.grid_forget()
            self.title_3_status_2.grid_forget()

        if self.is_trial3_block1:
            self.delete_trial3_block1()
        elif self.is_trial3_block2:
            self.delete_trial3_block2()
        elif self.is_trial3_block3:
            self.delete_trial3_block3()
        elif self.is_trial3_block4:
            self.delete_trial3_block4()
        elif self.is_trial3_block5:
            self.delete_trial3_block5()
        elif self.is_trial3_block6:
            self.delete_trial3_block6()
        elif self.is_rest_bar:
            self.rest_bar.place_forget()
        self.is_trial3_status = False



def launchGUI(conn, in_conn):
    # run the GUI
    root = ttk.Window(
            title="Torque GUI",        
            themename="litera",     
            size=(1100,800),        
            position=(100,100),     
            minsize=(0,0),         
            maxsize=(1100,800),    
            resizable=None,         
            alpha=1.0,              
    )
    gui = GUI(root, conn, in_conn)
    root.mainloop()
    exit()


if __name__=='__main__':
    launchGUI(conn=Queue(),in_conn=Queue())
    pass
