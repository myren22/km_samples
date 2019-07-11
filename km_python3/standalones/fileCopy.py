'''
Created on May 9, 2018

@author: Kyle
'''
import os
import re
import shutil
import tkinter as tk



def filesort(inputPath, outputPath):
    """
    -get the correct node dirs    
    -get lsdir
    for file in lsdir
        if file is not aDir: continue
            aMatch = re.search('$N(\d+)', filename)
        if aMatch:
            correctName = 'node'+aMatch[1]
            #  in outputdir
            os.mkdir(correctName)
            #  in made dir
            os.mkdir('black')
            # >place bwf1 files in dir
            os.mkdir('red')
            # >place rwf1 files in dir
            #place other files at top level
    """
    print('')
    for file in os.listdir(inputPath):
        if not os.path.isdir(file):
            continue
        aMatch = re.search('$N(\d+)', file)
        if aMatch:
            correctName = 'node'+str(aMatch[1])

            os.mkdir(os.path.join(outputPath,correctName))
            os.mkdir(os.path.join(outputPath,correctName,'black'))
            os.mkdir(os.path.join(outputPath,correctName,'red'))
            for subDir in os.walk(file):
                print('--')

    src=None
    dst=None
    shutil.copyfile(src, dst)

def main():
    """
    Create some basic GUI
    Input Dir    -label/enter
    Output Dir -label/enter
    Start Button
    copy ./path/dirInputName
    output  ./pathOut/reformat_dirInputName.zip
    
    inputLabel
    inputEnter
    outputLabel
    outputEnter
    startButton    
    """
    
    aRoot = tk.Tk()
    root = tk.Frame(aRoot)
    root.grid(row=2,column=2)
    
    inputLabel=tk.Label(root,text='Input Path:')
    inputEnter=tk.Entry(root,width=80)
    outputLabel=tk.Label(root,text='Output Path:')
    outputEnter=tk.Entry(root,width=80)
    startButton = tk.Button(root,width=10,height=1, text='Start')
    #  Width and height dont increase at the same rate. Height is multiplier on text height.
    #  Width, unsure what the unit for increasing this is.
    inputLabel.grid(row=2,column=2,sticky='e')
    inputEnter.grid(row=2,column=3,sticky='ew')
    outputLabel.grid(row=3,column=2,sticky='e')
    outputEnter.grid(row=3,column=3,sticky='ew')
    startButton.grid(row=4,column=2,columnspan=2, sticky='ew',padx=3, pady=3)
    
    def buttonPress():
        inputStr= inputEnter.get()
        outputStr=outputEnter.get()
        filesort(inputStr, outputStr)
    startButton['command']=buttonPress  
    root.mainloop()
    


if __name__ == '__main__':
    main()



'''
python call getList(nodeId)
    returnList=[]
    index=0
    while True:
        valAt =  c++.getIndex(nodeId,index)
        if valAt == -1    #the number/symbol to indicate end
            return returnList
        else:
            returnList.append[]
        if index>500: 
            print("check if terminator isnt being accepted")
            break
        index=index+1
    #  should only return here if break in while triggered.
    return returnList   
'''
    
'''
python call getList(nodeId)
    returnList=[]
    index=0
    intSize = c++.getSizeArray(None)
    for i in range(0,intSize):
        item = c++.getIndexAt(i)
        returnList.append(item)
    return returnList
    
    #this format requires 2 external lib methods per list    
    
    while True:
        valAt =  c++.getIndex(nodeId,index)
        if valAt == -1    #the number/symbol to indicate end
            return returnList
        else:
            returnList.append[]
        if index>500: 
            print("check if terminator isnt being accepted")
            break
        index=index+1
    #  should only return here if break in while triggered.
    return returnList   
'''