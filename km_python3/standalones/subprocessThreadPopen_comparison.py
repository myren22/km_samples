'''
Created on Nov 14, 2018

@author: Kyle


    This file is too show and compare the different ways available to run subprocesses/threads in python.
There is a great deal of overlap between the libraries and both could meet the needs for the program you
are making. However the different grammar and contexts can make switching between difficult.

The following are examples from my use cases of:
    - Running a python method that will terminate and not rejoin program
        - giving that python method input parameters
    - Running a python file as if from terminal on windows, such that a cmd window shows output while running
    - Opening an excel file, and being able to check when the file is closed.
    - 
    
Key Takeaways from reading this post https://stackoverflow.com/questions/2629680/deciding-among-subprocess-multiprocessing-and-thread-in-python 
    - subprocessing is best for executables
    - multiprocessing is best for pythons call and CPU managing. Gives each process own memory and other attributes
    - threading meant for single cpu i/o switching. Generally superseded by multiprocessing
    - ?Parallel Python(pp) - Alternative to multiprocessing that has more message/data passing features
When running this program, toggle comments in the main at the end for the desired example
'''
#### Imports
import time, datetime
import subprocess
from subprocess import Popen


#### 1. 
def printXtimesAndTerminate(printAmount=20, interval=0.5):
    if interval<=0: 
        print('Error: interval must be greater than 0')
        return
    timeCount=0
    loopCount=0
    
    while timeCount<durationSec:
        print('Loop[{}] Time[{}]'.format(loopCount,timeCount))
        time.sleep(intervalSec)
        
        timeCount=timeCount+intervalSec
        loopCount=loopCount+1
    print('Completed "printXtimesAndTerminate"')
    return

###
from multiprocessing import Process, Value, Array

def example1_process(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

def test_example1_multiprocessing():
    #Value and Array are special shared memory types
    numShared = Value('d', 0.0)
    arrShared = Array('i', range(10))
    
    #Using Process from multiprocessing. 
    p = Process(target=example1_process, args=(numShared, arrShared))
    p.start()
    time.sleep(1)
    print("pre:",num.value)
    print("pre:",arr[:])
    
    p.join() #This just makes program

    print("post:",num.value)
    print("post:",arr[:])
    
def test_example2_executable():
    """args is string of args ex: "python3 C:/filePath/file.py", 
    or if file has default a default opener like word or excel files, just give the fill path.
    
    creationflags=subprocess.CREATE_NEW_CONSOLE  --> makes print output appear in a container separate from main
    
    shell if true means args are treated like windows cmd string. Unsure of all ways this changes things.
        Some effects: stops new cmd window being made. can open files that have default opener by just giving path. 
    
    Process starts immediately, and cmd window closes when opened program dies"""
    
    filepath = "helloWorld.py"
    
    aThread = subprocess.Popen(args="python "+filepath, creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    threadOpenTxtFile = subprocess.Popen(args=r"C:\Users\Kyle\Downloads\venkat000000000.txt", shell=True) 
    #subprocess.Popen(relative_filepath, shell=True)
    
    time.sleep(3)
    ###### ... after the program has started, wherever you need to check status of process
    
    if aThread.poll() is not None:
        print("Sub process has terminated")
    else:
        print("Sub process still alive")


def main():
    test_example2_executable()        
    return
    #### Example 1. subprocess a python method
    
    #### Example 2. Running a python file from terminal  

if __name__ == '__main__':
    main()