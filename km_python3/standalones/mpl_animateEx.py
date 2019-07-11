'''
Created on Apr 9, 2019

@author: kmyren
'''
# import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animateEx():
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

if __name__ == '__main__':
    animateEx()
    pass