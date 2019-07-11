'''
Created on Mar 12, 2019

@author: kmyren
'''
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection

import time,csv
import math
from datetime import datetime


# import numpy as np
# import matplotlib.pyplot as plt




class uavPlotMap():
    def __init__(self):
        self.dateFormat = "%Y-%m-%dT%H:%M:%SZ"
    def mainMatlabFig(self):
        fig = plt.figure(figsize=(8, 6))

        ax = plt.subplot(1, 1, 1)
        
        # Populate ax with data
    def setAxUavPositions(self):
        pass

def setScenarioValues():
    """ These values are: 
        
        location data.corners, borders, center
        uav start positions
        scenario/ emitter positions. read file, 
        """
    pass

def animationExample():
    """Example of how to make an animated plot from intervals of a line.
    Key takeaway, is add each artist for that time, to a single list for that time."""
    fig = plt.figure()
    
    # ims is a list of lists, each row is a list of artists to draw in the
    # current frame; here we are just animating one artist, the image, in
    # each frame
    ims = []
    xList=[]
    yList=[]
    line2Tuple=[]
    for i in range(60):
        xList.append(i)
        yList.append(i*i)            
        line1, = plt.plot(xList,yList, animated=True)
        if i>20:
            #experiment with a second line, that is a list of tuples
            line2Tuple.append((i,30-i*i))
            line2, =plt.plot(*zip(*line2Tuple), animated=True)            
            ims.append([line1,line2]) #every artist to be rendered in animation should be placed in this
        else:
            ims.append([line1])
    plt.rcParams['animation.ffmpeg_path'] = r'C:\FFmpeg\bin\ffmpeg.exe'
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                    repeat_delay=1000)
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    ani.save('dynamic_images.mp4', writer=writer)
    
    plt.show()
def animationOfUavPath():
    """ Create an animation of the flight paths of each UAV + other details
    This method is aimed at replicating Zach's matlab code that plots 
        -each UAVs flight path
        -emitter detections
        request_task:
        -search_target_area: 
            rectangle box, striped black edges. [a diamond for each UAV assigned]
            linestyle='--', color='k'            
        -localize_source:[red box. 3 diamonds on top representing 3 assigned UAVs]
            linestyle='-', color='r'
        -identify_source_type:
            NO MESSAGES FROM SEER YET.
            planned: linestyle='--', color='m'
    Questions/ToDo:
        -first implement a frame by frame animation replicating Zach's sim style.      
    """
    pass

def latLong2distMeters(lat1, long1, lat2, long2):
    """  """
    #print("sin:",sin(45))
    u = math.sin(math.radians((lat2-lat1)/2))   #Just a subset of formula needed 
    v = math.sin(math.radians((long2-long1)/2))
    earthRadius = 6371.0
    
    #  Final Formula
    a1 =  1000*2*earthRadius
    a2 = math.asin(math.sqrt(u*u + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * v * v))
    distMeters = a1*a2 
    return distMeters

# Setup a plot such that only the bottom spine is shown
def setupAxTicksSpines(ax):
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.tick_params(which='major', width=1.00)
    ax.tick_params(which='major', length=5)
    ax.tick_params(which='minor', width=0.75)
    ax.tick_params(which='minor', length=2.5)
    ax.patch.set_alpha(0.0)
    
def plotUAVtimeChunkedLines(axesIn,UavDfIn, colorIn=''):
    """Separated by UAV Id prior to this"""
    UavDfIn.index = pd.to_datetime(UavDfIn['Message_Time'], format=dateFormat)
    uav_grouped = UavDfIn.groupby(pd.Grouper(freq='1Min'))
    numPoints = len(uav_grouped)
    point=1
    for group_name, df_group in uav_grouped:
        #print(group_name) # the time grouping
        xlist=[]
        ylist=[]
        xlist = [df_group['Longitude']]
        alphaCalc = (float(point)/(numPoints-1))*(3/5) + 0.4
        axesIn.plot(df_group['Longitude'],df_group['Latitude'],alpha=alphaCalc,color=colorIn)
#         if point ==1:
#             ax.plot(df_group['Longitude'],df_group['Latitude'],alpha=alphaCalc,color=colorIn)
#         else:
#             ax.plot(df_group['Longitude'],df_group['Latitude'],alpha=alphaCalc,color=colorIn)
        point=point+1
        #Works! Not needed, but works for inspecting each row in group.
#         for row_index, row in df_group.iterrows():
#             print ("row_index/specificTime=",row_index,":",row['Longitude'], row['Latitude'])
def plotMsgCsv(axesIn, msgPath):
    """ 
    make an X for every Search_target_area.
    make a    for every Localize source
    make a  * for every emitter identified
    
    Topic,ID,Task,Priority,Lat0,Lon0,North0,East0,Lat1,Lon1,
    North1,East1,Lat2,Lon2,North2,East2,Lat3,Lon3,North3,East3,
    Assignee(s),High Queue Count,Medium Queue Count,Low Queue Count,Time Stamp    
    """
    listLat=[]
    listLong=[]
    # Emitter Identified
    with open(msgPath) as f:
        dataincsv = csv.reader(f, delimiter=',', quotechar='|')
        for lineNum, line in enumerate(dataincsv,0):
            if lineNum==0: 
                continue
            if line[0]=='emitter_identified':
                #print('found emiter')
                listLat.append(float(line[4]))
                listLong.append(float(line[5]))
    axesIn.plot(listLong, listLat, linestyle='', color='k', marker='*')
    
    # Search Target Area
#     listLat=[]
#     listLong=[]
#     with open(msgPath) as f:
#         dataincsv = csv.reader(f, delimiter=',', quotechar='|')
#         for lineNum, line in enumerate(dataincsv,0):
#             if lineNum==0: 
#                 #print('first line', line)                
#                 continue
#             if line[2]=='SEARCH_TARGET_AREA':
#                 print('found search target area')
#                 listLat.append(float(line[4]))
#                 listLong.append(float(line[5]))
#     axesIn.plot(listLong, listLat, linestyle='', color='k', marker='*')
                
#     msg_df = pd.read_csv(msgPath)
#     msg_df.head()

def plotSearchTargetArea(msgPath):
    
    msg_df = pd.read_csv(msgPath)
    msg_df.head()
    UavDfIn.index = pd.to_datetime(UavDfIn['Message_Time'], format=dateFormat)
    uav_grouped = UavDfIn.groupby(pd.Grouper(freq='1Min'))
    numPoints = len(uav_grouped)
    point=1
    for group_name, df_group in uav_grouped:
        #print(group_name) # the time grouping
        xlist=[]
        ylist=[]
        xlist = [df_group['Longitude']]
        alphaCalc = (float(point)/(numPoints-1))*(3/5) + 0.4
        axesIn.plot(df_group['Longitude'],df_group['Latitude'],alpha=alphaCalc,color=colorIn)
#         if point ==1:        
#             ax.plot(df_group['Longitude'],df_group['Latitude'],alpha=alphaCalc,color=colorIn)
#         else:
#             ax.plot(df_group['Longitude'],df_group['Latitude'],alpha=alphaCalc,color=colorIn)
        point=point+1


def plotlineFromUavinAoaDirection():
    """ make a line from the UAV towards the direction of the emitter 
    get uavDf, 
    select rows with SignalId>0
    line segements, of uav[long,lat],
    """
    pass
def addEmitterCircles(ax, scenarioNum):
    emitters=[]
    rangeDist=[]
    if scenarioNum==0:
        return
    elif(scenarioNum==1):
        emitters=[(-84.9967,35.0687)]
        rangeDist=[0.005]
    elif(scenarioNum==2):
        emitters=[(-84.9967,35.0687),(-84.9741,35.0748)]
        rangeDist=[0.005]
    elif(scenarioNum==3):
        emitters=[(-84.9967,35.0687),(-84.9741,35.0748),(-84.9904,35.0686)]
        rangeDist=[0.005,0.005,0.0025]
    elif(scenarioNum==4):
        print('hello!')
        emitters= [(-84.9903,35.0616),(-85.0074,35.0747),(-84.9659,35.0798),(-84.9903,35.0616)]
        rangeDist=[0.005,0.005,0.0025]
    elif(scenarioNum==5):
        emitters=[(-84.9903,35.0616),(-85.0074,35.0747),(-84.9659,35.0798),(-84.9903,35.0616)]###Todo change
        rangeDist=[]
    else:
        return
    print(emitters[0])
    patches =[]
    num=int(len(emitters))
    print('len emitt', num)
    for i in range(num):
        circle = Circle(emitters[i], 0.005)
        patches.append(circle)
        print('addeed')
    p = PatchCollection(patches, alpha=0.4)
#     p.set_array(np.array(colors))
    ax.add_collection(p)

def plotUavAt100mby100mGrid():
    #######################################
    #plots the 100m by 100m grid
    for xpos in range(0,41):
        print(xpos)
        for ypos in range(1,40):
            xCalc = xlongeast - xpos*xlong100mIncrement
            yCalc = ylatsouth + ypos*ylat100mIncrement
            ax.plot(xCalc, yCalc, color='green', marker='o', linestyle='dashed',
                    linewidth=2, markersize=3)
####

def scenarioVals():
    # Boundaries = Scenario 1
#     ylatsouth=35.0600
#     ylatnorth=35.0960
#     ylatcenter = (ylatsouth+ylatnorth)/2
#     ylatdifference = ylatnorth - ylatsouth    #35.0600-35.0960 = 0.0360
#     ylat100mIncrement = ylatdifference/40
#     xlongwest=-85.0085
#     xlongeast=-84.9645
#     
#     xlongcenter = (xlongwest+ xlongeast)/2
#     xlongdifference = abs(xlongeast-xlongwest) #85.0085-84.9645 = 0.0440
#     xlong100mIncrement = xlongdifference/40
    emitList=[]
    anEmitDict={'latitude':0,'longitude':0,'rangeMeters':0} #other potential fields: color, lat-long on edges of range.
    searchBoundariesDict={'latitudeSouthBorder':0,'latitudeSouthBorder':0,
                          'latitudeSouthBorder':0,'latitudeSouthBorder':0,}
    searchBoundariesDict={'cornerNW':0,'cornerNE':0,
                          'cornerSE':0,'cornerSW':0,}
    westborder = latLong2distMeters(ylatsouth, xlongwest, ylatnorth, xlongwest)
    eastborder = latLong2distMeters(ylatsouth, xlongeast, ylatnorth, xlongeast)
    northborder = latLong2distMeters(ylatnorth, xlongwest, ylatnorth, xlongeast)
    southborder = latLong2distMeters(ylatsouth, xlongwest, ylatsouth, xlongeast)
    print("latDiff:",ylatdifference)
    print("west border:", westborder, ". east border:", eastborder)#length from north to south, on these borders.
    print("longDiff", xlongdifference)
    print("north border:", northborder)
    print("south border:", southborder)
    
def setupAxAs(ax):
    #### ===============
    # Actually draw plot
    ax.set_xlim(xlongwest, xlongeast)
    ax.set_ylim(ylatsouth, ylatnorth)
    
    # Major ticks represent Lat-Long, 400m increments.
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.005))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.005))
    # ax.xaxis.set_major_locator(ticker.MaxNLocator(10))
    plt.grid(b=True, which='minor',axis='y')
    
    ## Minor ticks represent meters 100 meter increments
    ax.xaxis.set_minor_locator(ticker.LinearLocator(numticks=41))#40+1 for edge.
    ax.yaxis.set_minor_locator(ticker.LinearLocator(numticks=41))#xy minor is same.
    plt.grid(b=True, which='minor',axis='x') #sets grid visibility for axis-major/minor to true.
    
    ax.tick_params('x', labelrotation=290)

def main_distUAVmap():
    """
    assume region borders.
    
    set scenario"""
    # Boundaries = Demo 1
    ylatsouth=35.0600
    ylatnorth=35.0960
    ylatcenter = (ylatsouth+ylatnorth)/2
    ylatdifference = ylatnorth - ylatsouth     # 35.0600 - 35.0960 = 0.0360
    ylat100mIncrement = ylatdifference/40
    xlongwest=-85.0085
    xlongeast=-84.9645
    
    xlongcenter = (xlongwest+xlongeast)/2
    xlongdifference = abs(xlongeast-xlongwest) # 85.0085 - 84.9645 = 0.0440
    xlong100mIncrement = xlongdifference/40
    
    # Scenario  # Setup
    figTitle = 'Scenario 1'
    fig.suptitle(figTitle)
    addEmitterCircles(ax, 4)
    
    uavLog = r"C:\Users\Kyle\Desktop\ForDsclient\test-04-05_5b_sce4\uavLog\UAV.csv"
    msgLog=  r'C:\Users\Kyle\Desktop\ForDsclient\test-04-05_5b_sce4\uavLog\msgLog.csv'
    
    uav_df = pd.read_csv(uavLog)
    uav_df.head()
    
    colorList=['#0000FF','#000080','#4169E1','#7B68EE','#8A2BE2']
    for uav_i in range(0,5):
        #Get uav specific rows.
        uav_i_df = uav_df[uav_df['UAV_ID'] == i]
        plotUAVtimeChunkedLines(ax,uav_i_df, colorList[i])
    
    plotMsgCsv(ax, msgLog)
    

    return

if __name__ == '__main__':
    main_distUAVmap()