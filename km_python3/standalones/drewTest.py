'''
Created on May 3, 2019

@author: kmyren
'''

import numpy as np
import matplotlib.pyplot as plt

def plotBar(dictIn):
    N = 5
    menMeans = (20, 35, 30, 35, 27)
    womenMeans = (25, 32, 34, 20, 25)
    menStd = (2, 3, 4, 1, 2)
    womenStd = (3, 5, 2, 3, 3)
    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence
    
    p1 = plt.bar(ind, menMeans, width, yerr=menStd)
    p2 = plt.bar(ind, womenMeans, width,
                 bottom=menMeans, yerr=womenStd)
    
    plt.ylabel('Scores')
    plt.title('Scores by group and gender')
    plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
    plt.yticks(np.arange(0, 81, 10))
    plt.legend((p1[0], p2[0]), ('Men', 'Women'))
    
    plt.show()

def dictFormat():
    latit = 20.232
    longit = 30.434
    numChan = 4
    myDict = {(latit, longit):numChan, (21.002, 31.222):5}
    for key in myDict:
        
        print('key:',key)
        print('value:',myDict[key])
    return myDict

if __name__ == '__main__':
    aDict = dictFormat()
    plotBar(aDict)
    pass