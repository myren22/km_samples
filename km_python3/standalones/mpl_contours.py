'''
Created on May 7, 2019

@author: kmyren
'''

import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt


def contoursDemo():
    """From matplotlib api.
    Link: https://matplotlib.org/gallery/images_contours_and_fields/contour_demo.html 
    
    References - The use of the following functions and methods is shown in this example:
        import matplotlib
        import matplotlib.cm as cm
        matplotlib.axes.Axes.contour
        matplotlib.pyplot.contour
        matplotlib.figure.Figure.colorbar
        matplotlib.pyplot.colorbar
        matplotlib.axes.Axes.clabel
        matplotlib.pyplot.clabel
        matplotlib.axes.Axes.set_position
        matplotlib.axes.Axes.get_position
    """

    delta = 0.025
    x = np.arange(-3.0, 3.0, delta)
    y = np.arange(-2.0, 2.0, delta)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-X**2 - Y**2)
    Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
    Z = (Z1 - Z2) * 2
    #print('x:',x,'\ny',y,'\nX:',X,'\nY:',Y,'\nZ1:',Z1,'\nZ2:',Z2,'\nZ:',Z)
    
    ###############################################################################
    # Create a simple contour plot with labels using default colors.  The
    # inline argument to clabel will control whether the labels are draw
    # over the line segments of the contour, removing the lines beneath
    # the label
    fig, ax = plt.subplots()
    CS = ax.contour(X, Y, Z)    # Create contour
    ax.clabel(CS, inline=1, fontsize=10)    # 
    ax.set_title('1:Simplest default with labels')
    
    
    ###############################################################################
    # contour labels can be placed manually by providing list of positions
    # (in data coordinate). See ginput_manual_clabel.py for interactive
    # placement.
    
    fig, ax = plt.subplots()
    CS = ax.contour(X, Y, Z)
    manual_locations = [(-1, -1.4), (-0.62, -0.7), (-2, 0.5), (1.7, 1.2), (2.0, 1.4), (2.4, 1.7)]
    ax.clabel(CS, inline=1, fontsize=10, manual=manual_locations)
    ax.set_title('2:labels at selected locations')
    
    
    ###############################################################################
    # You can force all the contours to be the same color.
    
    fig, ax = plt.subplots()
    CS = ax.contour(X, Y, Z, 6,
                     colors='k',  # negative contours will be dashed by default
                     )
    ax.clabel(CS, fontsize=9, inline=1)
    ax.set_title('3:Single color - negative contours dashed')
    
    ###############################################################################
    # You can set negative contours to be solid instead of dashed:
    
    matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
    fig, ax = plt.subplots()
    CS = ax.contour(X, Y, Z, 6,
                     colors='k',  # negative contours will be dashed by default
                     )
    ax.clabel(CS, fontsize=9, inline=1)
    ax.set_title('4:Single color - negative contours solid')
    
    
    ###############################################################################
    # And you can manually specify the colors of the contour
    
    fig, ax = plt.subplots()
    CS = ax.contour(X, Y, Z, 6,
                     linewidths=np.arange(.5, 4, .5),
                     colors=('r', 'green', 'blue', (1, 1, 0), '#afeeee', '0.5')
                     )
    ax.clabel(CS, fontsize=9, inline=1)
    ax.set_title('5:Crazy lines')
    
    
    ###############################################################################
    # Or you can use a colormap to specify the colors; the default
    # colormap will be used for the contour lines
    
    fig, ax = plt.subplots()
    im = ax.imshow(Z, interpolation='bilinear', origin='lower',
                    cmap=cm.gray, extent=(-3, 3, -2, 2))
    levels = np.arange(-1.2, 1.6, 0.2)
    CS = ax.contour(Z, levels, origin='lower', cmap='flag',
                    linewidths=2, extent=(-3, 3, -2, 2))
    
    # Thicken the zero contour.
    zc = CS.collections[6]
    plt.setp(zc, linewidth=4)
    
    ax.clabel(CS, levels[1::2],  # label every second level
              inline=1, fmt='%1.1f', fontsize=14)
    
    # make a colorbar for the contour lines
    CB = fig.colorbar(CS, shrink=0.8, extend='both')
    
    ax.set_title('6:Lines with colorbar')
    
    # We can still add a colorbar for the image, too.
    CBI = fig.colorbar(im, orientation='horizontal', shrink=0.8)
    
    # This makes the original colorbar look a bit out of place,
    # so let's improve its position.
    
    l, b, w, h = ax.get_position().bounds
    ll, bb, ww, hh = CB.ax.get_position().bounds
    CB.ax.set_position([ll, b + 0.1*h, ww, h*0.8])
    
    plt.show()
    
    #############################################################################

def mpl_contoursMain():
    delta = 0.5
    x = np.arange(-3.0, 3.0, delta)
    y = np.arange(-2.0, 2.0, delta)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-X**2 - Y**2)
    Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
    Z = (Z1 - Z2) * 2
#     Z = np.ndarray()
    unfilledValue=0
    Znew = np.zeros((len(y), len(x)))
#     Znew = [[unfilledValue for i in range(len(x))] for j in range(len(y))]
#     Znew =X.copy()  
    for xindex,xvalue in enumerate(x):
        for yindex,yvalue in enumerate(y):
            print('')
            if ((xvalue>-1.5 and xvalue<-0.5) and (yvalue>-1.5 and yvalue<-0.5)):
                # Find positions within a small region, set to 2
                print('found!')
                print('--setting!')
                print('Znew at x{} y{}:{}'.format(xindex,yindex,Znew[yindex][xindex]))
                Znew[yindex][xindex]=2
            elif((xvalue>-2 and xvalue<0) and (yvalue>-2 and yvalue<0)):
                # Find positions within a medium region, but not in previous region. set to 1.
                Znew[yindex][xindex]=1
            else:
                print('not found!x{} y{}'.format(xindex,yindex))
                Znew[yindex][xindex]= 0
        
    
    #print('x:',x,'\ny',y,'\nX:',X,'\nY:',Y,'\nZ1:',Z1,'\nZ2:',Z2,'\nZ:',Z)
    
    ###############################################################################
    # Create a simple contour plot with labels using default colors.  The
    # inline argument to clabel will control whether the labels are draw
    # over the line segments of the contour, removing the lines beneath
    # the label
    fig, ax = plt.subplots()
    CS = ax.contour(X, Y, Znew)    # Create contour
    ax.clabel(CS, inline=1, fontsize=10)    # 
    ax.set_title('1:Simplest default with labels')
    
    
    ###############################################################################
    # contour labels can be placed manually by providing list of positions
    # (in data coordinate). See ginput_manual_clabel.py for interactive
    # placement.
    
#     fig, ax = plt.subplots()
#     CS = ax.contour(X, Y, Z)
#     manual_locations = [(-1, -1.4), (-0.62, -0.7), (-2, 0.5), (1.7, 1.2), (2.0, 1.4), (2.4, 1.7)]
#     ax.clabel(CS, inline=1, fontsize=10, manual=manual_locations)
#     ax.set_title('2:labels at selected locations')
    pass
    plt.show()

if __name__ == '__main__':
#     contoursDemo()
    mpl_contoursMain()
    pass