'''
Created on Nov 14, 2018

@author: Kyle

Utils file to speed up generating and creating certain basic window arrangements
using TkInter.
'''
import tkinter
from tkinter import ttk, filedialog

    
def set_entry_to_dir(entry):
    dirRequested = filedialog.askdirectory()
    #fileReqeusted = str(tk.filedialog.askopenfilename(initialdir='../data_collection', filetypes=[('Excel files','*.xlsx')]))
    if os.path.exists(dirRequested):
        print('dirReqeusted path is good')
    else:
        print('dirReqeusted path is BAD.')
    if len(dirRequested)>1:
        entry.delete(0, tk.END)
        entry.insert(0,dirRequested)  
            
            
#####################################################################
####         Not Utils, but commonly used.
######################################################################

#===============================================================================
# def read_previous_GUI_file(self):
#     #Declare all gui elements defaults prior to this in the init. This will override where found.
#     filename = 'savedGuiValues_engTest.ini'
#     if os.path.exists(filename):
#         values = configparser.ConfigParser()
#         values.read(filename)
#         for (key, val) in values.items('savedGuiValues'):
#             self.gui_defaults[key]=val
#             
# def save_current_GUI_file(self):
#     values = configparser.ConfigParser()
#     
#     values.add_section('savedGuiValues')
#     values.set('savedGuiValues','ent_logname', self.entLogName.get())
# 
#     filename = 'savedGuiValues_engTest.ini'
#     values.write(open(filename, 'w'))
#     return
#===============================================================================