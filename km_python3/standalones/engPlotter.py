'''
Created on Oct 17, 2018

@author: Kyle

Requires install of pip libraries: pyserial, matplotlib
'''


import sys, os, re, time, serial, math, datetime,csv
import configparser, datetime, subprocess, shutil

import subprocess, multiprocessing
from multiprocessing import Process
from subprocess import Popen
from decimal import *               #  Provides casting from '23.5' to 23.5
import tkinter as tk
from tkinter import ttk, filedialog

from collections import OrderedDict

import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib import rcParams
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from numpy.polynomial.legendre import leg2poly



"""Methods in class:
Tkinter Utility methods:
-checkSubprocesses
-tk_frameTextBox
-tk_labelEntry_singlePack
-tk_labelEntry_grid
-tk_labelEntryButton
-read_previous_GUI_file
-save_current_GUI_file

Utility methods from WNW_plot_graphs:
-time_report
-save_fig
-add_fig_to_frame
-onpick_any_pickable_object
-show_fig
-setup_legend
-seconds_to_timestring
-timestring_to_seconds
-reformat_time_ticks
-find_line_num_of_time_str_in_filtered_file

New Methods for this flightGUI:
-frame_right
-frame_center
-frame_header
"""
def getCurrentLocalTime():
    aTime = time.localtime(time.time()) #Look at this struct in debugger for other params
    strTime = "{}:{}:{}".format(aTime.tm_hour, aTime.tm_min, aTime.tm_sec)
    return strTime

def getENGReceiverData(engCom='4'):
    '''
    Input: 
    @param engCom String of an int in the range 0-9, that is the number for the comm port.
                    If the current port connecting to the ENG Rx is "COM4", then input is "4".
    Reads data from the ENG Receiver and returns
    Output:
        BER,QualityPer,FrequencyMHz,Signal Strength(dbM),Modulation,CodeRate,GuardInt, and Bandwidth
    '''
    
    #Open Serial
    # try:        
    ser = serial.Serial("COM"+engCom, baudrate=9600)  # open serial port for ENG Receiver
    a1 = chr(10)#LF
    b1 = chr(13)#CR
    quickStatusReq = 'NU010201d02b{}{}'.format(b1,a1).encode('ascii')
    #print('quickStatusReq=',quickStatusReq)

    ser.write(quickStatusReq)     # write a string

    time.sleep(0.3)
    a3 = ser.read_all()
    #print('recieve:',a3)

    berReq = 'NU0102018972{}{}'.format(b1,a1).encode('ascii')
    ser.write(berReq)     # write a string

    time.sleep(0.3)
    berRec = ser.read_all()
    #print('recieveBER:',berRec)

    ser.close()
    # except:
        # return  -1,-1,-1,-1,-1,-1,-1,-1

    serialReceived = a3
    print(serialReceived[0:12])
    print(serialReceived)
    print(berReq)
    if(str(serialReceived) == "b''" or str(berRec)=="b''" or str(serialReceived) == "b'\r\n'" or not str(serialReceived[0:12]) == "b'NU0201185000'"):
        return  -2,-1,-1,-1,-1,-1,-1,-1
    else:
        #print(serialReceived)
        sigStrHex = serialReceived[24:26]
        sigStr_dBm = int(sigStrHex, 16)
        sigStr_dBm = sigStr_dBm -256
        #print('signal strength in dBm:',str(sigStr_dBm))

        #get quickStatus signal Quality
        aHex = serialReceived[48:50]
        qualityPercent = int(aHex, 16)
        #print('signal Quality Percent:',str(qualityPercent))
        print("End: "+str(serialReceived[50:]))
        UCE = int(serialReceived[50:54],16)
        frequencyMHz = (int(a3[16:24],16)/1000)
        #print(frequencyMHz)
        modInt = int(serialReceived[26:28],16)
        modulation = ""
        if(modInt==0):
            modulation="QPSK"
        elif(modInt==1):
            modulation="16 QAM"
        elif(modInt==2):
            modulation="64 QAM"
        else:
            modulation="Unknown"
            print("ERROR: Cannot determine Modulation")
        #print(modulation)
        codeRateInt = int(serialReceived[28:30],16)
        codeRate = ""
        if(codeRateInt==0):
            codeRate="1/2"
        elif(codeRateInt==1):
            codeRate="2/3"
        elif(codeRateInt==2):
            codeRate="3/4"
        elif(codeRateInt==3):
            codeRate="5/6"
        elif(codeRateInt==4):
            codeRate="7/8"
        else:
            codeRate="Unknown"
            #print("ERROR: Cannot determine Code Rate")
        #print(codeRate)
        guardIntNum = int(serialReceived[30:32],16)
        guardInt = ""
        if(guardIntNum==0):
            guardInt="1/32"
        elif(guardIntNum==1):
            guardInt="1/16"
        elif(guardIntNum==2):
            guardInt="1/8"
        elif(guardIntNum==3):
            guardInt="1/4"
        else:
            guardInt="Unknown"
            #print("ERROR: Cannot determine Guard Interval")
        #print(guardInt)

        bwInt = int(serialReceived[32:34],16)
        bw = 0
        if(bwInt==0):
            bw=6
        elif(bwInt==1):
            bw=7
        elif(bwInt==2):
            bw=8
        else:
            bw="Unknown"
            #print("ERROR: Cannot determine BW")

        berIntegral = int(berRec[16:18],16)
        berDecimal = int(berRec[18:20],16)
        berExponent = int(berRec[20:22],16)-256
        if(berExponent==-256):
            berExponent=0
        #for i in range(10,24,2):
        #    print(i,' : ',int(serialReceived[i:i+2],16))

        #print(berIntegral,'.',berDecimal,' e',berExponent)

        BER = (berIntegral + (berDecimal/10))*(10**berExponent)

        if(BER < (1*(10**-4)) and UCE>10):
            BER = 0.99
        #print(BER)
        #print('{:.1e}'.format(BER))
        print("UCE: "+str(UCE))
        print("BER: "+str(BER))
        
        return BER,qualityPercent,frequencyMHz,sigStr_dBm,modulation,codeRate,guardInt,bw

def threadENGReceiver(logDir='', engCom='4', durationSec=5, intervalSec=1):
    print('params: dir:{}, com:{}, durat:{}, interval:{}'.format(logDir, engCom, durationSec, intervalSec))
    timeCount=0
    loopCount=0
    with open(logDir+os.sep+'ENG_Rx_log.csv', 'w') as f:
        firstLine = '#localTime, timeSec, frequencyMHz, sigStr_dBm, qualityPercent, modulation, codeRate, guardInt, bw, BER'
        f.write(csvLine) 
    
    while timeCount<durationSec:
        aDate = datetime.datetime.now()
        dateFormat = "{:0>2}:{:0>2}:{:0>2}:{:0>3}".format(aDate.hour, aDate.minute, aDate.second, round((aDate.microsecond)/1000))
        timeSec = aDate.hour * 3600 + aDate.minute * 60 + aDate.second + round(aDate.microsecond/1000)/(1000) 
        BER,qualityPercent,frequencyMHz,sigStr_dBm,modulation,codeRate,guardInt,bw =  getENGReceiverData(engCom=engCom)
        csvLine = '{},{},{},{},{},{},{},{},{},{}\n'.format(dateFormat,timeSec,frequencyMHz,sigStr_dBm,qualityPercent,modulation,codeRate,guardInt,bw,BER)
        with open(logDir+os.sep+'ENG_Rx_log.csv', 'a') as f:
            f.write(csvLine) 
        timeDiff = datetime.datetime.now()- aDate 
        timeDiff=0 
        print('Loop[{}] Time[{}]'.format(loopCount,timeCount))
        time.sleep(intervalSec-timeDiff)
        
        timeCount=timeCount+intervalSec
        loopCount=loopCount+1
    print("-Done Recording ENG Receiver values")
    
    

def extract_time_from_timestamp(time_stamp):
    """This function extracts time from timestamp string into both string and numerical formats"""
    
    time_format     =   "%H:%M:%S:%f"                                               #Format used by time stamps in the log string        
    time_string     =   time_stamp.strip('T[]')                                     #Removing brackets around the time stamp
    curr_time       =   datetime.datetime.strptime(time_string, time_format)
    total_time      =   curr_time.hour * 3600 + curr_time.minute * 60 + curr_time.second + curr_time.microsecond/(10**6)    #Time in seconds
            
    return time_string, total_time                                                  #Returns string and total time in that order

def extract_time_from_line(line):
    """This function returns time. As both a numerical value in seconds, and string copy of timestamp found.
    Timestamps found are normally formatted as HH:MM:SS:mmm."""
    timestamp = re.findall(r'T\[\d+:\d+:\d+:\d+\]', line)
    if (len(timestamp) > 0) :
        return extract_time_from_timestamp(timestamp[0])  #Extracting time values from time stamp

def set_entry_to_txt(entryBox):
    fileReqeusted = str(tk.filedialog.askopenfilename(filetypes=[('txt','*.txt')]))
    if os.path.exists(fileReqeusted):
        print('fileReqeusted path is good')
    else:
        print('fileReqeusted path is BAD.')
    entryBox.delete(0, tk.END)
    entryBox.insert(0,fileReqeusted) 

class engPlotter():
    def __init__(self, parent=None):
        self.root=None        
        if parent is None:
            #If parent is none, make the base tk window
            self.root=tk.Tk()
            self.root.wm_title("Eng Plotter")
            self.root.minsize(400,150) # width, height
#             self.root.geometry('570x300')
        else: 
            #If a parent is given, make root a frame within parent.
            self.root = tk.Frame(parent, bg='red', relief='groove', borderwidth=5)
        
        #These names are lowercase and match those in savedGuiValues file.
        self.gui_defaults = {
                             'ent_engoutdir':os.getcwd(),
                             'ent_interval': '30',
                             'ent_duration':'1',
                             'ent_commport':'4',
                             'ent_dsalogpath':'C:\Modem\!DsaLogs'}       
        self.read_previous_GUI_file() #overides values if found   
        
        self.prev_time_report = time.time()
        
        self.maxTimeENG=None
        self.minTimeENG=None
        self.maxTimeDSA=None
        self.minTimeDSA=None
        
        self.entENGOutDir = None
        self.entInterval=None
        self.entDuration=None
        self.entCommPort=None
        self.entDSAlogPath=None
        self.labENGtimer=None
        self.engRxCheckAutoStopVar = tk.StringVar()
        self.populate_gui()
        self.checkSubprocesses()
        
    def populate_gui(self):
        ##############################################################
        #### Populate gui
        
        ####  ENG Receiver
        #borderwidth=3, background='gray85', pady=5, padx=5
        frmENGrxMaster = tk.LabelFrame(self.root, text='ENG Receiver' ,relief='groove')
        frmENGrxMaster.pack(fill='both', expand=True)
        
        frmOutPath,_,self.entENGOutDir,butOutPath = self.tk_labelEntryButton(frmENGrxMaster, 'Log Output Dir', 'Browse')
        if 'ent_engoutdir' in self.gui_defaults.keys():
            self.entENGOutDir.insert(0,self.gui_defaults['ent_engoutdir'])        
        frmOutPath.pack(side='top', fill='x')      
        
        frmENGRxLog = tk.Frame(frmENGrxMaster) 
        frmENGRxLog.pack(side='top', fill='both', expand=True)
        self.labENGtimer = tk.Label(frmENGRxLog,text='Time remaining(s): NaN', width= 30)
        self.labENGtimer.pack(side='right', fill='both', expand=True)
        #ENG Rx - Start Stop - Checkbuttons
        frmCheckStartStop = tk.Frame(frmENGRxLog)
        frmCheckStartStop.pack(side='right',fill='y')
        self.engRxCheckAutoStopVar = tk.StringVar()
        butENGRXStart = tk.Radiobutton(frmCheckStartStop, text='Start',indicatoron=False, variable=self.engRxCheckAutoStopVar, value='Start',background='green',width=10)
        butENGRXStart.pack(side='top',anchor='n',fill='both', expand=True)
        butENGRXStop = tk.Radiobutton(frmCheckStartStop, text='Stop', indicatoron=False, variable=self.engRxCheckAutoStopVar, value='Stop',background='red',width=10)
        butENGRXStop.pack(side='bottom',anchor='s',fill='both', expand=True)
        
        frmIntDur = tk.Frame(frmENGRxLog)
        frmIntDur.pack(side='left',fill='both')
        aFrame, aLab, self.entInterval = self.tk_labelEntry_singlePack(frmIntDur, textLab='Interval(sec)' )
        if 'ent_interval' in self.gui_defaults.keys():
            self.entInterval.insert(0,self.gui_defaults['ent_interval']) 
        aFrame.pack(side='top', fill='x')
        aFrame, aLab, self.entDuration = self.tk_labelEntry_singlePack(frmIntDur, textLab='Duration(sec)')
        aFrame.pack(side='top', fill='x')
        if 'ent_duration' in self.gui_defaults.keys():
            self.entDuration.insert(0,self.gui_defaults['ent_duration']) 
        aFrame, aLab, self.entCommPort = self.tk_labelEntry_singlePack(frmIntDur, textLab='COM Port[1-9]')
        aFrame.pack(side='top', fill='x')
        if 'ent_commport' in self.gui_defaults.keys():
            self.entCommPort.insert(0,self.gui_defaults['ent_commport']) 
        #############################################################
        
        butPlotENG = ttk.Button(frmENGrxMaster,text='butPlotENG')
        butPlotENG.pack(side='top', fill='x',padx=10,pady=2)
        #############################################################
        #### DSA Log
        frmDSAMaster = tk.LabelFrame(self.root, text='Log Path')
        frmDSAMaster.pack(side='top',fill='x', expand=True, pady=5)
        frmDSAlog, labDSAlog, self.entDSAlogPath, butDSAlog =self.tk_labelEntryButton(frmDSAMaster, textLab='DSA Log',textBut='Browse')
        if 'ent_dsalogpath' in self.gui_defaults.keys():
            self.entDSAlogPath.insert(0,self.gui_defaults['ent_dsalogpath']) 
        frmDSAlog.pack(side='top', fill='x')
        butDSAlog['command']= lambda: set_entry_to_txt(entDSAlogPath)
        butDSAlog.pack(side='top', fill='x')
        
        butPlotDSA = ttk.Button(frmDSAMaster,text='butPlotDSA')
        butPlotDSA.pack(side='top', fill='x', padx=10,pady=2)
        #############################################################
        #Make a new dir, with a copy of DSA log, ENG Rx csv, and matplot pngs
        frmPostTest = tk.LabelFrame(self.root, text='Post-Test')
        frmPostTest.pack(side='top', fill='x', expand=True)
        butSaveTest = tk.Label(frmPostTest, justify='center',
                                 text='Make a new dir storing copies of DSA Log & ENG Receiver,\nCreate plots of data.')#undle ENG Receiver .csv & DSA Log together\nin a new dir   
        butSaveTest.pack(side='top', fill='x', expand=True)
        butSaveTest = ttk.Button(frmPostTest, text='Save Logs & Plots')  
        butSaveTest.pack(side='top', fill='x',padx=10,pady=2)
        #############################################################
        
        #Bind commands to all buttons that need it.
        
        #Browse Buttons
        butOutPath['command'] = lambda: self.set_entry_to_dir(self.entENGOutDir)
        butDSAlog['command']= lambda: set_entry_to_txt(self.entDSAlogPath)
        #Start Stop Buttons
        butENGRXStart['command']=self.eventStartENGlog #will stop eng thread, grab duration/interval/com values
        butENGRXStop['command']=self.eventStopENGlog 
        
        #Plot Buttons
        butPlotENG['command']= self.plotWindowENG
        butPlotDSA['command']= self.plotWindowDSA
        butSaveTest['command']=self.eventSaveTests
        

    def eventStartENGlog(self):
        # Input: com port, duration, interval, eng log path
#         argsIn=[self.entENGOutDir.get(),self.entCommPort.get(),int(self.entDuration.get()),int(self.entInterval.get())]
        self.processENG = Process(target=threadENGReceiver, args=(self.entENGOutDir.get(),self.entCommPort.get(),int(self.entDuration.get()),Decimal(self.entInterval.get())))
        self.processENG.start()
        self.labENGtimer['text']= 'Time remaining(s): '+self.entDuration.get()
        self.updateClock()
        # Modifies: Time label, state of eng fields
        
    def eventStopENGlog(self):  
        self.labENGtimer['text'] = 'Time remaining(s): Stopped'
        self.processENG.terminate()
        self.engRxCheckAutoStopVar.set('Stop')

    def updateClock(self):
        if self.engRxCheckAutoStopVar=='Stop':
            print('-update clock stop-')
            return
        aMatch = re.search('(-?\d+)',self.labENGtimer['text'] )
        if aMatch:
            timeRemaining = int(aMatch.group(1))-1
            if timeRemaining <1:
                self.eventStopENGlog()
                print('time ran out')
                return
            self.labENGtimer['text'] = 'Time remaining(s): '+ str(timeRemaining)
            self.root.after(1000,self.updateClock)

    def plotWindowENG(self):
        newWindow = tk.Toplevel()
        #### ENG Receiver
        containerFrame = tk.Frame(newWindow)
        fig = self.engRxPlots(os.path.join(self.entENGOutDir.get(),'ENG_Rx_log.csv'))
        dict_frames={}
        title='firstFig'
        self.add_fig_to_frame(fig, containerFrame, dict_frames, title)
        containerFrame.pack(side='left', expand=True, fill=tk.BOTH)   
 
    def plotWindowDSA(self):
        newWindow = tk.Toplevel()
        #### DSA Plots
        containerFrame = tk.Frame(newWindow)
        fig = self.dsaLogExtractor(self.entDSAlogPath.get())
        dict_frames={}
        title='firstFig'
        self.add_fig_to_frame(fig, containerFrame, dict_frames, title)
        containerFrame.pack(side='left', expand=True, fill=tk.BOTH) 
    
    def eventSaveTests(self):
        #Make a new dir, timestamped, for files
        aDate = datetime.datetime.now()
        dirname = self.entENGOutDir.get()+ os.sep + aDate.strftime('LogsENG_%Y_%m_%d-%H_%M_%S' +  os.sep) 
        os.mkdir(dirname)
        #copy dsa and eng files into it
        engFile= os.path.join(dirname,'ENG_Rx_log.csv')
        dsaFile=os.path.join(dirname,os.path.basename(self.entDSAlogPath.get()))
        shutil.copy(self.entDSAlogPath.get(), dirname) #copy file to dir
        shutil.copyfile(os.path.join(self.entENGOutDir.get(),'ENG_Rx_log.csv'), engFile) #copy file to new full pathname
        #determine the min and max times of dsa
        maxTimeENG=None
        minTimeENG=None
        maxTimeDSA=None
        minTimeDSA=None
        
        with open(dsaFile,'r') as f:
            for lineNum, line in enumerate(f,1):
                aMatch = re.search(r'T\[\d+:\d+:\d+:\d+\]', line)
                if aMatch:
                    time_string, total_time= extract_time_from_line(line)
                    if minTimeDSA is None:
                        minTimeDSA=total_time
                    elif minTimeDSA>total_time:
                        minTimeDSA=total_time
                    if maxTimeDSA is None:
                        maxTimeDSA=total_time
                    elif maxTimeDSA<total_time:
                        maxTimeDSA=total_time
        with open(engFile,'r') as f:
            dataincsv =  csv.reader(f, delimiter=',', quotechar='|')
            for row in dataincsv:
                total_time=float(row[1])
                if minTimeENG is None:
                    minTimeENG=total_time
                elif minTimeENG>total_time:
                    minTimeENG=total_time
                if maxTimeENG is None:
                    maxTimeENG=total_time
                elif maxTimeENG<total_time:
                    maxTimeENG=total_time
        maxTimeAll =maxTimeENG
        if maxTimeENG<maxTimeDSA: maxTimeAll=maxTimeDSA
        minTimeAll =minTimeENG
        if minTimeENG>minTimeDSA: minTimeAll=minTimeDSA
        figDsa = self.dsaLogExtractor(dsaFile, minTimeAll, maxTimeAll)
        figDsa.savefig(dirname+os.sep+'figDsa.png', dpi=150)
        figEng = self.engRxPlots(engFile, minTimeAll, maxTimeAll)
        figEng.savefig(dirname+os.sep+'figEng.png', dpi=150)
        
        # Embed in a tk window
        newWindow = tk.Toplevel()
        # newWindow.row_configure(weight=1)
        # newWindow.column_configure(weight=1)
        
        dict_frames={}
        title='dsaFig'
        containerFrame = tk.Frame(newWindow)
        self.add_fig_to_frame(figDsa, containerFrame, dict_frames, title)
        containerFrame.pack(side='left', expand=True, fill=tk.BOTH)   
        # containerFrame.grid(row=0, column=0, stick='nsew')
        
        title='engFig'
        containerFrame = tk.Frame(newWindow)
        self.add_fig_to_frame(figEng, containerFrame, dict_frames, title)
        containerFrame.pack(side='right', expand=True, fill=tk.BOTH) 
        # containerFrame.grid(row=0, column=0, stick='nsew')
    
        
        

##########################################################################################
#### Tkinter methods from windfreakStepControl
##########################################################################################           
    def read_previous_GUI_file(self):
        #Declare all gui elements defaults prior to this in the init. This will override where found.
        filename = 'savedGuiValues_engTest.ini'
        if os.path.exists(filename):
            values = configparser.ConfigParser()
            values.read(filename)
            #Note: case is ignored when saving, so key needs to match lower case
            for (key, val) in values.items('savedGuiValues'):
                self.gui_defaults[key]=val
                
    def save_current_GUI_file(self):
        values = configparser.ConfigParser()
        
        values.add_section('savedGuiValues')
        #Note: case is ignored when saving, all field names below will be forced lower.
        values.set('savedGuiValues','ent_engoutdir', self.entENGOutDir.get())
        values.set('savedGuiValues','ent_interval', self.entInterval.get())
        values.set('savedGuiValues','ent_duration', self.entDuration.get())
        values.set('savedGuiValues','ent_commport', self.entCommPort.get())
        values.set('savedGuiValues','ent_dsalogpath', self.entDSAlogPath.get())

        filename = 'savedGuiValues_engTest.ini'
        values.write(open(filename, 'w'))
        return
    
    def set_entry_to_dir(self, entry):
        dirRequested = filedialog.askdirectory()
        #fileReqeusted = str(tk.filedialog.askopenfilename(initialdir='../data_collection', filetypes=[('Excel files','*.xlsx')]))
        if os.path.exists(dirRequested):
            print('dirReqeusted path is good')
        else:
            print('dirReqeusted path is BAD.')
        if len(dirRequested)>1:
            entry.delete(0, tk.END)
            entry.insert(0,dirRequested)  
    
    def checkSubprocesses(self):
        # This is where any state checks and updates can be placed.
        # The tk method .after(time_ms, method) is non blocking and can be recurive.
        # If the tk widget .after is used on is destroyed, then the method will cleanly not fire.
        
        # polling subprocesses, recording current gui values, etc done here.
        
        self.save_current_GUI_file()
        # after time is in milliseconds       
        self.root.after(500, self.checkSubprocesses)
        
    def tk_frameTextBox(self, parent, titleText='Title', buttonText='Button'):
        frmTextBox = tk.Frame(parent,bg = '#ffffff',
                  borderwidth=1, relief="sunken")
        scrollbar = tk.Scrollbar(frmTextBox) 
        editArea = tk.Text(frmTextBox,  wrap="word",
                           yscrollcommand=scrollbar.set, 
                           borderwidth=0, highlightthickness=0)
        scrollbar.config(command=editArea.yview)
        titleLabel = tk.Label(frmTextBox, text=titleText)
        titleLabel.pack(side='top', fill='x', anchor='nw', expand=True)
        editArea['width']=25
        editArea['height']=15
        #DEBUG Note:: textbox & scrollbar dimensions are unpredictable.
        #   They do not expand or contract past certain amounts and are
        #   prone to size issues. Not setting the width/height makes 
        #   the widgets very large.
        scrollbar.pack(side="right", fill="y", expand=True, anchor='e')
        editArea.pack(side="left", fill="both", expand=True, anchor='center')
        return frmTextBox, editArea, titleLabel, scrollbar
        
    def tk_labelEntry_singlePack(self, parent, textLab='',width=-1):
        #Assume parent is any kind of frame.
        aFrame = tk.Frame(parent)
        aLab=ttk.Label(aFrame, text=textLab)
        aLab.pack(side=tk.LEFT, expand=False)
        if width==-1:            
            aEnt=ttk.Entry(aFrame)#default text?
            aEnt.pack(side=tk.LEFT,expand=True, fill=tk.X)    
        else:
            aEnt=ttk.Entry(aFrame, width=width)#default text?
            aEnt.pack(side=tk.LEFT,expand=False)     
        # aFrame needs to be positioned with grid or pack inside of parent after returning.
        return aFrame, aLab, aEnt
    
    def tk_labelEntry_grid(self, parent, listTuples=[]):
        #Assume parent is any kind of frame.
        #ListTuples example:
        #     listTuples = [
        #         ("dwellTime", "Dwell Time(s)"),
        #         ("startAtten","Start Atn(dB)"),
        #         ("stopAtten", "Stop Atn(dB)"),
        #         ("stepAtten", "Step Atn(dB)"),
        #     ]
        #Entry values are assigned a default from self.gui_defaults, or left blank.
        aFrame = tk.Frame(parent)
        aFrame.grid_columnconfigure(1, weight=0)
        aFrame.grid_columnconfigure(2, weight=1)
        aDict = {}
        for index in range(0, len(listTuples)):
            key=listTuples[index][0]
            text=listTuples[index][1]
            #keyLabel
            aLab=ttk.Label(aFrame, text=text)
            aLab.grid(row=index, column=0,sticky='W')#.pack(side=tk.LEFT, expand=False)
            aEnt=ttk.Entry(aFrame)
            aEnt.grid(row=index, column=1,sticky=tk.EW) 
            aDict['lab_'+key]=aLab 
            aDict['ent_'+key]=aEnt    
            entKey ='ent_'+key
            if entKey in self.gui_defaults.keys():
                aDict['ent_'+key].insert(0, self.gui_defaults['ent_'+key])
        # aFrame needs to be positioned with grid or pack inside of parent after returning.
        return aFrame, aDict
        
    def tk_labelEntryButton(self, parent, textLab='',textBut=''):
        #Assume parent is any kind of frame.
        aFrame = tk.Frame(parent)
        aLab=ttk.Label(aFrame, text=textLab)
        aLab.pack(side=tk.LEFT, expand=False)
        aEnt=ttk.Entry(aFrame)#default text?
        aEnt.pack(side=tk.LEFT,expand=True, fill=tk.X)        
        aBut=ttk.Button(aFrame, text=textBut)
        aBut.pack(side=tk.RIGHT,expand=False)
        # aFrame needs to be positioned with grid or pack inside of parent after returning.
        return aFrame, aLab, aEnt, aBut

##########################################################################################
#### Matplotlib methods from WNW_plot_graphs
##########################################################################################
    def add_fig_to_frame(self, fig, containerFrame,dict_frames, title):
        #Given a matplotlib figure, and a tk frame, setup the figure within the container frame.
        #Additionally, add this frame to a dict with the title as a key.
        
        #  This method controls matplotlib events internally. 
        def onpick_any_pickable_object(event):
            """This is called upon any matplotlib element that has the pickable element being clicked
            Method first determines which type  object created event[ex: legend, line]
            Depending on object, execute click behavior.
            Current Behaviors:
                -if legend: toggle visibility of all lines corresponding to legend entry.
                -if line: output X,Y coordinates, line label, timestring based on X val
                    -if toggleGoto==True: open a the filtered txt doc of node in notepad++, at timestring of point clicked
            """                          
            event_fig=event.artist.figure
            artistLabel=event.artist.get_label()
            
            print('Click Event', artistLabel)
            ##if legend click
            if('Legend_' in artistLabel):
                print('Toggling Visibility')
                strAfterLeg=artistLabel[7:] 
                legline=event.artist    
                for fig_axes in event_fig.get_axes():
                    for actualLine in fig_axes.get_lines():
                        actualLineLabel= actualLine.get_label()
                        if(actualLineLabel==strAfterLeg):
                            notCurVis = not actualLine.get_visible()
                            actualLine.set_visible(notCurVis)
                            if notCurVis:
                                legline.set_alpha(1.0)
                            else:
                                legline.set_alpha(0.2)
            else:
                line=event.artist
                xdata, ydata = line.get_data()
                ind = event.ind
                print('Line X,Y:', xdata[ind], ydata[ind])
                time_str = self.seconds_to_timestring(xdata[ind[0]]) #prints 'HH:MM:SS:mmm' 
                
                #using time string, search total_time-time_str-line_num list, for line_num.
                if (self.boolTog): #open notepad++ @ line_num using cmd line.
                    #this code works, however needs to be made to take correct node dpl file, and find the line_num
                    
                    #find wnw instance this line belongs to 
                    ourWNW=None                    
                    for wnw in self.wnw_list:
                        if wnw.node_name in artistLabel:
                            ourWNW=wnw
                    offset = self.offsetList[ourWNW.node_num]
                    time_str = self.seconds_to_timestring(xdata[ind[0]]+offset)
                    textfile_path = ourWNW.node_output_dir+os.sep+ 'filtered_DSABLACK.txt'
                    line_num = self.find_line_num_of_time_str_in_filtered_file(time_str, textfile_path)                        
                    notepad_path= ''
                    if os.path.isdir(r'C:\Program Files\Notepad++'):
                        notepad_path=r'C:\Program Files\Notepad++'
                    elif(os.path.isdir(r'C:\Program Files (x86)\Notepad++')):
                        notepad_path=r'C:\Program Files (x86)\Notepad++'
                    else:
                        print('notepad++ is not installed')
                        return
                        
                    #textfile_path= r'C:\Users\Kyle\Documents\DSAStyleLog\ColinDSALogs\127Black.txt' #<-- TO BE MADE VARIABLE 
                    #line_num= 12000 #<-- TO BE MADE VARIABLE                         
                    cmd_start= r'start cmd /k "cd ' #then notepad_path
                    cmd_middle = r' & notepad++.exe -n' #then line number, then textfilepath,                        
                    full_open_txt_cmd= ('{}{}{}{} {} & exit \"'.format(cmd_start, notepad_path, cmd_middle, str(line_num), textfile_path))                        
                    
                    print(full_open_txt_cmd)
                    if(line_num>0): #if str_time was not found, line_num would be -1.
                        os.system(full_open_txt_cmd)
                    else:
                        print('time str not found in file')
            event_fig.canvas.draw() 
            return #==========end onpick method
        
        thisFigFrame=tk.Frame(containerFrame)
        thisCanvas = FigureCanvasTkAgg(fig, thisFigFrame)
        thisCanvas.mpl_connect('pick_event', onpick_any_pickable_object)
        thisCanvas.draw()
        thisCanvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(thisCanvas, thisFigFrame)
        toolbar.update()
        thisCanvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True) 
        thisFigFrame.grid(row=0, column=0, sticky="nsew")
        dict_frames[title]=thisFigFrame
        
    def show_fig(self, fig_name, dict_frames):
        print('call raise [{}]'.format(fig_name))
        try:
            frame= dict_frames[fig_name]
            frame.tkraise()       
            print('-Raised Frame:', fig_name)
        except:
            print('Unable to raise frame [{}]'.format(fig_name))
        
    def time_report(self, msg_out=''):
        """ Report elapsed time, current time. Give message
        print output format:
            Time[00:11:22] Elapsed[0000] - X has finished plotting
            Time[00:11:22] Elapsed[0000] - Y has started plotting
            Time[00:11:22] Elapsed[0000] - Y has finished plotting
            Time[00:11:22] Elapsed[0000] - Y has finished saving
        """
        current_time = time.time()
        elapsed_time = current_time - self.prev_time_report
        self.prev_time_report = current_time
        
        tLoc = time.localtime()
        local_time_formatted = time.strftime('{}:{}:{}'.format(tLoc.tm_hour, tLoc.tm_min, tLoc.tm_sec))
        
        #TODO:message buffer implementation
        print('Time[{}] Elapsed[{:04.2f}] - {}'.format(local_time_formatted, elapsed_time, msg_out))

    def save_fig(self, fig, filename='unlabelled_fig.png', dpi_in=150, report_time=False):
        """ A secure method for saving figs to drive. 
        Uses the top level dir. Checks for redundant writes. Reports time taken"""
        #=======================================================================
        # if self.save_plots==False:
        #     return
        #=======================================================================
        full_path_saved = os.path.join(self.base_output_dir, filename)
        if os.path.exists(full_path_saved):
            print('An image has already been saved of this figure')
            print('Path of Image[Ocuppied]', full_path_saved)
        else:            
            if report_time: self.time_report('Saving image:{}'.format(filename))
            fig.savefig(full_path_saved, dpi=dpi_in)
            if report_time: self.time_report('Finished save:{}'.format(filename))
        return

    def setup_legend(self,ax, nCol=1):
        handles, labels = ax.get_legend_handles_labels()    
        by_label = OrderedDict(zip(labels, handles))
        for key in by_label.keys():
            #  Make line we will use to replace handle 
            colorline=by_label.__getitem__(key).get_color()        
            newlegline = mlines.Line2D([], [],linewidth=4, color=colorline, label='Legend_'+key)
            by_label.__setitem__(key, newlegline)          
        ax_leg = ax.legend(by_label.values(), by_label.keys(), loc='upper left', ncol=nCol,
                           fancybox=True, shadow=False)#,facecolor='white', framealpha=0.3)
        if(ax_leg is not None):
            for legline in ax_leg.get_lines():   #activate the legend labels to have pick events
                legline.set_picker(5)
                
        return
        
    def seconds_to_timestring(self, seconds_given):
        #  Handle ms
        seconds_given=seconds_given*1000
        milliseconds=seconds_given%1000
        seconds_given=seconds_given/1000
        hours= math.floor(seconds_given/ 3600)
        secondsWithoutHours = seconds_given%3600
        minutes = math.floor(secondsWithoutHours/ 60)
        seconds = int(secondsWithoutHours%60)
        time_str = "T[%02i:%02i:%02i:%03i]" % (hours, minutes, seconds,milliseconds)
        print(time_str)
        return time_str
    
    def timestring_to_seconds(self, time_stamp):     
        """Take a string timestamp 'HH:MM:SS:fff' and convert it to a float"""
        time_format     =   "%H:%M:%S:%f"                                               #Format used by time stamps in the log string        
        time_string     =   time_stamp.strip('T[]')                                     #Removing brackets around the time stamp
        curr_time       =   datetime.datetime.strptime(time_string, time_format)
        total_time      =   curr_time.hour * 3600 + curr_time.minute * 60 + curr_time.second + curr_time.microsecond/(10**6)  #Time in seconds                
        return total_time  #time_string, 
    
    def reformat_time_ticks(self, ax):
        """Given an ax with the x axis used for time, determine smart ticks placements based on hours or minutes.
        
            TODO: Make time ticks only use meaningful minutes for ticks. Matplotlib tick locators don't handle 
        steps in multiples of 60 easily. Scott a binomial method to determine a suitable bound and tick. 
        Uncertain how to apply this. This method does not work with Spectrogram, as its time range has already been modified to hours. 
        """
        lim1, lim2 = ax.get_xlim()
        lim1 = math.floor(lim1/60/1)*60*1 #round to nearest 5 minutes
        lim2 = math.ceil(lim2/60/1)*60*1 #round to nearest 5 minutes
        ax.set_xlim(lim1,lim2)
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(15, min_n_ticks=5))
        formatter = matplotlib.ticker.FuncFormatter(lambda ms, x: time.strftime('%H:%M:%S', time.gmtime(ms)))
        ax.xaxis.set_major_formatter(formatter)
        ax.tick_params('x', labelrotation=290)
        return
    
    def find_line_num_of_time_str_in_filtered_file(self, time_str, filtered_file_path):
        
        with open(filtered_file_path, 'r', encoding="ansi") as f :
            for line_num, line in enumerate(f, 1):
                if (len(line) > 0) :
                    if time_str in line:
                        return line_num     
        return -1 #if not found
##########################################################################################
#### Matplotlib figure methods from WNW_plot_graphs
##########################################################################################
    def fig_sharedXaxis_3axesVert(self,listDataSets=None, report_time=False):
        #Test value ranges
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, sharey=False)
        fig.subplots_adjust(left=.17, bottom=.10, right=.97, top=.92, hspace=0.23) 
        self.ax_powerLevelAngle(ax1)
        self.ax_powerLevelAngle(ax2)
        self.ax_powerLevelAngle(ax3)
        ax3.set_xlabel('Flight Time (sec)')
        return fig

    def ax_powerLevelAngle(self, ax):
        newFont = {'fontsize': rcParams['axes.titlesize'],
                     'fontweight' : rcParams['axes.titleweight'],
                     'verticalalignment': 'baseline'
                     } #'horizontalalignment': loc
        ax.set_title('Power Level', loc='left', fontdict=newFont)
        ax.set_ylabel('Power Level Angle (sec)')
        #ax.set_xlabel('Flight Time (sec)' ) #only figxlabel
        ax.grid(alpha = 0.4, linestyle='--')
        #Plot
        randData = np.random.rand(100)*2000
        ax.plot(randData,marker='o')
        #self.setup_legend(ax)#Unsure what we even want from legend        
        return

    def fig_engReceiver(self, report_time=False):
        fig, (ax1ber, ax2pwr, ax3quality, ax4freq) = plt.subplots(3, 1, sharex=True, sharey=False)
        fig.subplots_adjust(left=.17, bottom=.10, right=.97, top=.92, hspace=0.23) 
        
        timeList,berList,qualList,sigPwrList,freqList = [],[],[],[],[]
        dirPathLog = r'.'
        csv_path = os.path.join(dirPathLog, 'ENG_test_log.csv') 
        
        if os.path.exists(csv_path) is False: 
            print('---Path of ENG logs in invalid!!!')
            return fig
        
        with open(csv_path, 'r') as csvfile:
            #print('DEBUG: in plot_ax_freq_111-2') 
            dataincsv =  csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in dataincsv:
                if ":" not in row[0]: continue
                """ CSV column format:
                [0:time_str, 1:ber, 2:quality, 3:signalPower, 4:freqMHz] """
                timeList.append(double(row[0]))
                berList.append(double(row[1]))
                qualList.append(double(row[2]))
                sigPwrList.append(double(row[3]))
                freqList.append(double(row[4]))
        
        
        self.ax_BER(ax1ber, timeList, berList)
        self.ax_powerLevelDb(ax2pwr, timeList, sigPwrList)
        self.ax_engQuality(ax3quality, timeList, qualList)
        self.ax_engFreq(ax4freq, timeList, freqList)
        
        return fig
    
    def ax_BER(self, ax, xList, yList):
        ax.set_title('BER over Time')
        ax.set_ylim(0,1)
        ax.plot(xList, yList)        
        return
    
    def ax_powerLevelDb(self, ax, xList, yList):
        ax.set_ylabel("Power dBm @ENG Rx")
        ax.set_ylim(0,-120)
        ax.plot(xList, yList)
        return
    
    def ax_engQuality(self, ax, xList, yList):
        ax.set_ylabel("Signal Quality %")
        ax.set_ylim(0,100)
        ax.plot(xList, yList)
        return
    
    def ax_engFreq(self, ax, xList, yList):
        ax.set_ylabel("ENG Frequency")
        ax.set_ylim(2020,2120)
        ax.plot(xList, yList)
        return
        



 
    def dsaLogExtractor(self, logPath, minTime=None, maxTime=None):
        dataDict={'drl':{'x':[],'y':[]},                  
                  'ttntAvailableChannels':{'x':[],'y':[]},
                  'ttntSelected':{'x':[],'yChanMHz':[],'loFreq':[]}
                  }
        logMintime=None
        logMaxTime=None
        with open(logPath, 'r', encoding='utf-8', errors='ignore') as f:
            for lineNum, line in enumerate(f,1):
                #Get DRL channels
                aMatch = re.search('M\[ActiveDsaChannel<C=(-?\d+)>: center Freq ([\d\s]+) Hz',line)
                if aMatch:
                    timeStr, timeSec = extract_time_from_line(line)
                    if logMintime is None: logMintime=timeSec
                    logMaxTime = timeSec
                    dataDict['drl']['x'].append(timeSec)
                    dataDict['drl']['y'].append(aMatch.group(2))                    
                    pass
                #Get TTNT available channnels
                aMatch = re.search('M\[TTNT available Channel List: center Freq([\d\s]+) Hz',line)
                if aMatch:
                    timeStr, timeSec = extract_time_from_line(line)
                    if logMintime is None: logMintime=timeSec
                    logMaxTime = timeSec
                    dataDict['ttntAvailableChannels']['x'].append(timeSec)
                    dataDict['ttntAvailableChannels']['y'].append(aMatch.group(1))
                    pass
                
                #Get TTNT Selected Channels
                aMatch = re.search('M\[Selected TTNT channel:\s?(\d+) Hz, LO Center Frequency:\s?(\d+) Hz',line)
                if aMatch:
                    timeStr, timeSec = extract_time_from_line(line)
                    if logMintime is None: logMintime=timeSec
                    logMaxTime = timeSec
                    dataDict['ttntSelected']['x'].append(timeSec)
                    dataDict['ttntSelected']['yChanMHz'].append(int(aMatch.group(1))/1e6 ) #
                    dataDict['ttntSelected']['loFreq'].append(aMatch.group(1))
                    
                    pass
        ############
        # Now to make Fig using logpath
        plt.rcParams.update({'figure.figsize': [9, 6]})
        plt.rcParams.update({'font.size': 7})
        fig, (ax1drl, ax2ttnt, ax3ttnt) = plt.subplots(3, 1, sharex=True, sharey=False)
        fig.subplots_adjust(left=.17, bottom=.10, right=.97, top=.92, hspace=0.23)
        fig.suptitle('DSA Logs')
        
        if minTime is None:
            ax1drl.set_xlim(logMintime, logMaxTime)
        else:
            ax1drl.set_xlim(minTime, maxTime)
        
        # ax1 DRL
        xList=[]
        yList=[]
        for i in range(0, len(dataDict['drl']['x'])):
            freqSplit = dataDict['drl']['y'][i].split(' ')            
            for freq in freqSplit:
                if freq=='':continue
                xList.append(dataDict['drl']['x'][i])
                yList.append(int(freq)/1e6)
        ax1drl.plot(xList,yList, linestyle='', marker='o', markersize=2)
        ax1drl.set_ylabel('DRL Freq\nList(MHz)')
        
        #ax2 TTNT Freq List
        xList=[]
        yList=[]
        for i in range(0, len(dataDict['ttntAvailableChannels']['x'])):
            freqSplit = dataDict['ttntAvailableChannels']['y'][i].split(' ')            
            for freq in freqSplit:
                if freq=='':continue
                xList.append(dataDict['ttntAvailableChannels']['x'][i])
                yList.append(int(freq)/1e6)
        ax2ttnt.plot(xList,yList, linestyle='', marker='o', markersize=2)
        ax2ttnt.set_ylabel('TTNT Freq\nList(MHz)')
        
        #ax3 TTNT Current
        ax3ttnt.plot(dataDict['ttntSelected']['x'], dataDict['ttntSelected']['yChanMHz'], 
                     linestyle='-', marker='o',markersize=2)
        ax3ttnt.set_ylabel('TTNT Selected\n Freq(MHz)')
        self.reformat_time_ticks(ax3ttnt)
        
        return fig
        
    def engRxPlots(self, logPath, minTime=None, maxTime=None):
        columns={'timeStr':[],'timeTotalSec':[],'ber':[],'qualityPercent':[],'frequencyMHz':[],
            'sigStr_dBm':[],'modulation':[],'codeRate':[],'guardInt':[],'bw':[]}

        with open(logPath, 'r', encoding='utf-8', errors='ignore') as f:            
            dataincsv = csv.reader(f, delimiter=',', quotechar='|')
            for row in dataincsv:
                if '#' in row[0]: continue
                if '-2' in row[9]: continue
                columns['timeTotalSec'].append(float(row[1]))
                columns['ber'].append(row[9])
                columns['qualityPercent'].append(float(row[4]))
                columns['sigStr_dBm'].append(float(row[3]))
                
                columns['frequencyMHz'].append(float(row[2]))
                columns['modulation'].append(row[5])
                columns['codeRate'].append(row[6])
                columns['guardInt'].append(row[7])
                columns['bw'].append(row[8])
        ############
        # Now to make Fig using logpath
        plt.rcParams.update({'figure.figsize': [9, 6]})
        plt.rcParams.update({'font.size': 7})
        fig, (ax1sigPower, ax2perc, ax3ber, axFreq) = plt.subplots(4, 1, sharex=True, sharey=False)
        fig.subplots_adjust(left=.17, bottom=.10, right=.97, top=.92, hspace=0.23)
        fig.suptitle('ENG Receiver')
        
        if minTime is not None:
            ax1sigPower.set_xlim(minTime, maxTime)
        
        #ax Signl Strength/Power in dBm
        ax1sigPower.plot(columns['timeTotalSec'],columns['sigStr_dBm'], 
            linestyle='-', marker='o', markersize=2)
        ax1sigPower.set_ylabel('Signal Power(dBm)') 
        
        #ax Quality Percent
        ax2perc.plot(columns['timeTotalSec'],columns['qualityPercent'],
            linestyle='', marker='o', markersize=2)
        ax2perc.set_ylabel('Quality Percent')
        
        #ax BER 
        ax3ber.plot(columns['timeTotalSec'],columns['ber'], 
                     linestyle='-', marker='o',markersize=2)
        ax3ber.set_ylabel('Frequency(MHz)')
        
        self.reformat_time_ticks(axFreq)
        #ax BER
        axFreq.plot(columns['timeTotalSec'],columns['frequencyMHz'], 
                     linestyle='-', marker='o',markersize=2)
        axFreq.set_ylabel('Frequency(MHz)')
        return fig   
        

def main():
    aWind = engPlotter()
    aWind.root.mainloop()
    time.sleep(2)

if __name__ == '__main__':
    main()