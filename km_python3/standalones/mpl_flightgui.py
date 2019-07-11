'''
Created on Oct 17, 2018

@author: Kyle
'''
import tkinter as tk
from tkinter import ttk, filedialog
import sys, os, re, time, serial, math
import configparser, datetime, subprocess

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
class flightGUI1():
    def __init__(self, parent=None):
        self.root=None        
        if parent is None:
            #If parent is none, make the base tk window
            self.root=tk.Tk()
            self.root.wm_title("Windfreak Step Power Control")
            self.root.minsize(400,150) # width, height
#             self.root.geometry('570x300')
        else: 
            #If a parent is given, make root a frame within parent.
            self.root = tk.Frame(parent, bg='red', relief='groove', borderwidth=5)
    
        self.gui_defaults = {'ent_logname':'wfLog',
                             'ent_outdir':'C:\WindfreakLogs',
                             'ent_ipaddress': '192.168.6.1',
                             'ent_startatten':'60',
                             'ent_stopatten':'30',
                             'ent_stepatten':'5',
                             'ent_dwelltime':'500',
                             'ent_passiveatn':'60',
                             'ent_wffreq':'1537.5',
                             'ent_wfpower':'20',
                             'ent_commport':'COM5',
                             'radbut_highlowpower':1,
                             'radbut_wfTxOnOff':0}       
        self.read_previous_GUI_file() #overides values if found   
        
        self.prev_time_report = time.time()
        
        ##############################################################
        #### Populate gui
        
        containerFrame = tk.Frame(self.root)
        fig = self.fig_sharedXaxis_3axesVert()
        dict_frames={}
        title='firstFig'
        self.add_fig_to_frame(fig, containerFrame, dict_frames, title)
        containerFrame.pack(expand=True, fill=tk.BOTH)
        
    def frame_legend(self):
        aFrm = tk.Frame(parent)
        aLab1 = tk.Label(aFrm, text='Left Power Lever Angle\n Tolerance')
        aLab2 = tk.Label(aFrm, text='Y Areas N/A\nY Areas N/A')
        aLab3 = tk.Label(aFrm, text='Legend')
        aLab4 = tk.Label(aFrm, text='* - Ang')
        aLab5 = tk.Label(aFrm, text='^ - Elev')
        aLab1.pack(side='top', anchor='w')
        aLab2.pack(side='top', anchor='w')
        aLab3.pack(side='bot', anchor='w')
        aLab4.pack(side='bot', anchor='w')
        aLab5.pack(side='bot', anchor='w')
        return aFrm
    
    def frame_header(self):
        aFrm = tk.Frame(parent)
        pass
        return aFrm
    
    def frame_center(self, parent):
        aFrm = tk.Frame(parent)
        leg1 = self.frame_legend(parent)
        leg2 = self.frame_legend(parent)
        leg3 = self.frame_legend(parent)
        leg1.grid(row=0,column=0)
        leg2.grid(row=1,column=0)
        leg3.grid(row=2,column=0)
        aFrm.columnconfigure(1,weight=1)
        aFrm.rowconfigure(3, weight=1)
        fig = self.fig_sharedXaxis_3axesVert()
        matFrame = tk.Frame(parent)
        dict_frames={}
        self.add_fig_to_frame(fig, matFrame, dict_frames, 'mat')
        matFrame.grid(row=0,column=1, rowspan=4, sticky='nsew')
        return aFrm
        
    
    def frame_right(self):
        pass
    
    

##########################################################################################
#### Tkinter methods from windfreakStepControl
##########################################################################################           
    def read_previous_GUI_file(self):
        #Declare all gui elements defaults prior to this in the init. This will override where found.
        filename = 'savedGuiValues_VarAtn.ini'
        if os.path.exists(filename):
            values = configparser.ConfigParser()
            values.read(filename)
            for (key, val) in values.items('savedGuiValues'):
                self.gui_defaults[key]=val
                
    def save_current_GUI_file(self):
        values = configparser.ConfigParser()
        
        values.add_section('savedGuiValues')
        values.set('savedGuiValues','ent_logname', self.entLogName.get())

        filename = 'savedGuiValues_Atn.ini'
        values.write(open(filename, 'w'))
        return
    
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
        
    def tk_labelEntry_singlePack(self, parent, textLab=''):
        #Assume parent is any kind of frame.
        aFrame = tk.Frame(parent)
        aLab=ttk.Label(aFrame, text=textLab)
        aLab.pack(side=tk.LEFT, expand=False)
        aEnt=ttk.Entry(aFrame)#default text?
        aEnt.pack(side=tk.LEFT,expand=True, fill=tk.X)       
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
#         ax_leg.set_facecolor('white')
#         ax_leg.set_framealpha(0.3)
        #bbox_to_anchor=(1,1) 
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
        fig.subplots_adjust(left=.17, bottom=.08, right=.97, top=.92, hspace=0.23) 
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


#===============================================================================
#     def fig_connections(self, wnw_list, report_time=False,connIDs=['1']):
#         if report_time: self.time_report('Building fig2_connections')
#         fig, (ax1_isGr, ax3_state,ax4_role) = plt.subplots(3, 1, sharex=True, sharey=False)
#         self.setup_second_window(fig)                 
#         self.plot_isGroupConnected(ax1_isGr, wnw_list, connIDs=connIDs)        
#         self.plot_state_manager(ax3_state,wnw_list, connIDs=connIDs)
#         self.plot_role_slave_master(ax4_role,wnw_list, connIDs=connIDs)   
#         ax1_isGr.set_xlim(self.min_time_all,self.max_time_all)
#         self.reformat_time_ticks(ax4_role)   
#         if report_time: self.time_report('-Finished Build fig2_connections')    
#         return fig
#     
#     def setup_second_window(self,fig):            
#         fig.canvas.set_window_title("WNW Node Set")
#         fig.suptitle('Connections', weight='bold')
#         #fig.set_size_inches(9,9)
#         #if using width=6,height=8, then .01 is about the size of 1 char.
#         fig.subplots_adjust(left=.17, bottom=.08, right=.97, top=.92, hspace=0.23)  
# 
#     def plot_isGroupConnected(self, ax, wnw_list, connIDs=['1']):
#         """"M[GroupManager<1>: IsGroupConnected = 0]
#         Line: M[GroupManager<1>: IsGroupConnected = 0]
#         """
#         thisUniques={}
#         for wnw in wnw_list:
#             csv_path = os.path.join(wnw.node_output_dir,'is_group_connected-X.csv') 
#             if os.path.exists(csv_path) is False: continue
#             with open(csv_path, 'r') as csvfile:
#                 dataincsv =  csv.reader(csvfile, delimiter=',', quotechar='|')
#                 for row in dataincsv:
#                     """ CSV column format:
#                     column0: time_str  
#                     column1: time_int  
#                     column2: freq
#                     column3: conn_id  """
#                     connID=row[3] #string
#                     if connID not in connIDs:
#                         continue #Don't save any data with connID=0
#                     key= wnw.node_name + str(connID)
#                     if(key not in thisUniques):
#                         thisUniques[key]={'x':[],'y':[],'label':'','conn_id_color':'','color':''}
#                     #===========================================================
#                     ####  Attempting to remove points that keep to the same y value
#                     # if(len(thisUniques[key]['y'])>2):
#                     #     if thisUniques[key]['y'][-1:] == float(row[2]):
#                     #         print('23')
#                     #         continue
#                     #     print('1')
#                     #===========================================================
#                     y_nodeOffset = wnw.node_num%10*0.03 -0.135
#                     y_val = float(row[2]) + y_nodeOffset
#                     thisUniques[key]['x'].append(float(row[1]))
#                     thisUniques[key]['y'].append(y_val)
#                     yVals = thisUniques[key]['y']
#                     if len(yVals)>5:
#                         if (y_val==yVals[len(yVals)-1] and y_val==yVals[len(yVals)-2] and y_val==yVals[len(yVals)-3]
#                             and y_val==yVals[len(yVals)-4] and y_val==yVals[len(yVals)-5]):
#                             thisUniques[key]['y'].pop(len(thisUniques[key]['y'])-3)
#                             thisUniques[key]['x'].pop(len(thisUniques[key]['x'])-3)
#                     thisUniques[key]['label']=wnw.node_name + '-' +str(connID)
#                     thisUniques[key]['conn_id_color']=self.connId_color[int(connID)]
#                     thisUniques[key]['color']=self.node_color[wnw.node_num%10]        
#         for key in thisUniques.keys():
#             ax.plot(thisUniques[key]['x'],thisUniques[key]['y'], color=thisUniques[key]['color'],
#                     linestyle='-', marker='o', drawstyle='steps-post', 
#                     markersize=3, markeredgecolor=thisUniques[key]['color'],
#                     label=thisUniques[key]['label'], picker=3)    
#         ax.set_title('Is Group Connected')
#         ax.set_ylabel('On or Off')
#         ax.grid(alpha = 0.4, linestyle='--')
#         ax.set_ybound(lower=-0.18, upper=1.18)
#         self.setup_legend(ax)        
#         
#         
#         ylabels = ['False','True']
#         yticksFreq=[0, 1]
#         ax.set_yticks(yticksFreq)
#         ax.set_yticklabels(ylabels)
#         return
#===============================================================================
 



def main():
    aWind = flightGUI1()
    aWind.root.mainloop()

if __name__ == '__main__':
    main()