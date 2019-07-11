'''
Created on Jun 22, 2018

@author: Kyle

Overivew: Various class declarations of tk object

Resources:  Stackoverflow discussion on TK object styling
    -link: https://stackoverflow.com/questions/16115378/tkinter-example-code-for-multiple-windows-why-wont-buttons-load-correctly

'''

import tkinter as tk
import numpy
import math
import matplotlib

# root = tk.Tk()
# root.geometry('500x500+80+50')
# aFrame = tk.Frame(root)
# aFrame.grid(row=1,column=1)




class Demo1:
    """A generic object of TK where the class is making the contents of MASTER. """
    def __init__(self, master):    
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text='New Window', width=25, command=self.new_window)
        self.button1.pack()
        self.frame.pack()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)


class Demo2:
    """A generic object of TK where the class is making the contents of MASTER. """
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text='Quit', width=25, command=self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()


class aFrameClass(tk.Frame):
    """An object of TK where the class is forced to be of type frame"""
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #self.master = master    #Should not need to be called.
        self.main_create()
        self.pack()

    def main_create(self):
        """Where majority of creation for contents within self should be done."""
        print('hello')
        aLabel = tk.Label(self, text='aLabel')
        aLabel.grid(row=0,column=0)

    def some_event(self):
        self.master.destroy()

    def create_objects(self):
        print('create')


class aToplevelClass(tk.Toplevel):     
    """An object of TK where the class is forced to be of type toplevel"""
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Demo 3")
        self.button = tk.Button(self, text="Button 2", # specified self as master
                                width=25, command=self.close_window)
        self.button.pack()

    def close_window(self):
        self.destroy()
        
def main(): 
    """First method. creates the only instance of tk, that all others descend from."""
    root = tk.Tk()
    #root.geometry('500x500+80+50')##width, height, x_pos, y_pos
    
    #### Filling out the contents of root with app
    #app = Demo1(root)   # This fills root with
    ###creating a frame within root with
    aNewFrame = aFrameClass(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()    