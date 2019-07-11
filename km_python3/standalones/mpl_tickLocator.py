"""
=============
Tick locators
=============

Show the different tick locators.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time
import math
# Setup a plot such that only the bottom spine is shown
def setup(ax):
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.tick_params(which='major', width=1.00)
    ax.tick_params(which='major', length=5)
    ax.tick_params(which='minor', width=0.75)
    ax.tick_params(which='minor', length=2.5)
    ax.set_xlim(33223.23,56234.561)
    ax.set_ylim(0, 1)
    ax.patch.set_alpha(0.0)
plt.figure(figsize=(8, 6))
n = 8

####import numpy as np
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]
aList =np.arange(0,86401,60*5) #all times in day, in sec, separated by 5 minutes

xbotlim1=33223.23
xupperlim1= 56234.561
b0 = round(xbotlim1) #to seconds

a0 = round(xupperlim1)
b1 = round(b0/60/5)*60*5
""" 
[0,15,60,60*5,60*10,60*20,60*40, 60*60,60*60*2,60*60*4]
if diff time >0 and diff time< 60*5
    30 sec major ticks
    limits rounded up down to nearest minute
elif diff time>=60*5 and difftime<60*15
    1 minute ticks
    limits rounded up down to nearest 1 minute
elif diff time>=60*15 and difftime<60*30
    2 minute ticks
    limits rounded up down to 5 minute
elif diff time>=60*30 and difftime<60*60
    5 minute ticks
    limits rounded up down 5 min
elif diff time>=60*60 and difftime<60*60*2
    10 minute ticks
    limits rounded up down 10 min
else:
    30 minuteticks
    limits rounded to nearest 30 min
    """

print("alist:", aList)
print('find nearest bot=',str(find_nearest(aList, xbotlim1)))
print('s')


#+#+#+#+
# import matplotlib
# import matplotlib.pyplot as plt


#===============================================================================
# segtime = [1000, 2000, 3000, 3500, 7000]
# segStrength = [10000, 30000, 15000, 20000, 22000]    
# 
# fig, ax = plt.subplots()
# plt.plot(segtime, segStrength)
# 
# formatter = matplotlib.ticker.FuncFormatter(lambda ms, x: time.strftime('%M:%S', time.gmtime(ms // 1000)))
# ax.xaxis.set_major_formatter(formatter)
# 
# plt.show()
#===============================================================================
#+##+#+#+#+#+#+

#===============================================================================
# # Null Locator
# ax = plt.subplot(n, 1, 1)
# setup(ax)
# ax.xaxis.set_major_locator(ticker.NullLocator())
# ax.xaxis.set_minor_locator(ticker.NullLocator())
# ax.text(0.0, 0.1, "NullLocator()", fontsize=14, transform=ax.transAxes)
# 
# # Multiple Locator
# ax = plt.subplot(n, 1, 2)
# setup(ax)
# ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
# ax.text(0.0, 0.1, "MultipleLocator(0.5)", fontsize=14,
#         transform=ax.transAxes)
#===============================================================================

#===============================================================================
# # Fixed Locator
# ax = plt.subplot(n, 1, 3)
# setup(ax)
# majors = [0, 1, 5]
# ax.xaxis.set_major_locator(ticker.FixedLocator(majors))
# minors = np.linspace(0, 1, 11)[1:-1]
# ax.xaxis.set_minor_locator(ticker.FixedLocator(minors))
# ax.text(0.0, 0.1, "FixedLocator([0, 1, 5])", fontsize=14,
#         transform=ax.transAxes)
#===============================================================================

#===============================================================================
# # Linear Locator
# ax = plt.subplot(n, 1, 4)
# setup(ax)
# ax.xaxis.set_major_locator(ticker.LinearLocator(3))
# ax.xaxis.set_minor_locator(ticker.LinearLocator(31))
# ax.text(0.0, 0.1, "LinearLocator(numticks=3)",
#         fontsize=14, transform=ax.transAxes)
#===============================================================================

#===============================================================================
# # Index Locator
# ax = plt.subplot(n, 1, 5)
# setup(ax)
# ax.plot(range(0, 5), [0]*5, color='White')
# ax.xaxis.set_major_locator(ticker.IndexLocator(base=.5, offset=.25))
# ax.text(0.0, 0.1, "IndexLocator(base=0.5, offset=0.25)",
#         fontsize=14, transform=ax.transAxes)
#===============================================================================

#===============================================================================
# # Auto Locator
# ax = plt.subplot(n, 1, 6)
# setup(ax)
# ax.xaxis.set_major_locator(ticker.AutoLocator())
# ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
# ax.text(0.0, 0.1, "AutoLocator()", fontsize=14, transform=ax.transAxes)
#===============================================================================

# time locator
ax = plt.subplot(n, 1, 1)
setup(ax)
lim1, lim2 = 33223.23,56234.561
lim1 = round(lim1/60/10)*60*10
lim2 = round(lim2/60/10)*60*10
diff_steps = lim2-lim1
print(str(diff_steps))
ax.set_xlim(lim1,lim2)
# ax.set_xlim(33223.23,56234.561)

ax.xaxis.set_major_locator(ticker.AutoLocator())
# ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
# ax.xaxis.set_major_locator(ticker.MaxNLocator(25,min_n_ticks=1))
formatter = matplotlib.ticker.FuncFormatter(lambda ms, x: time.strftime('%H:%M:%S', time.gmtime(ms)))
ax.xaxis.set_major_formatter(formatter)
# ax.set_xmajorticklabels(ax.get_xmajorticklabels(), rotation=90)
ax.tick_params('x', labelrotation=290)
print(ax.get_xticks())
# ax.text(0.0, 0.1, "AutoLocator()", fontsize=14, transform=ax.transAxes)
#=======

# time locator
ax = plt.subplot(n, 1, 3)
setup(ax)
lim1 = round(lim1/60/5)*60*10
lim2 = round(lim2/60/5)*60*10
ax.set_xlim(lim1,lim2)
# ax.set_xlim(55884.961,56234.561)

# ax.xaxis.set_major_locator(ticker.AutoLocator())
# ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.xaxis.set_major_locator(ticker.MaxNLocator(15, min_n_ticks=5))
formatter = matplotlib.ticker.FuncFormatter(lambda ms, x: time.strftime('%H:%M:%S', time.gmtime(ms)))
ax.xaxis.set_major_formatter(formatter)
# ax.set_xmajorticklabels(ax.get_xmajorticklabels(), rotation=90)
ax.tick_params('x', labelrotation=290)
# ax.text(0.0, 0.1, "AutoLocator()", fontsize=14, transform=ax.transAxes)
#=======

lim1, lim2 = ax.get_xlim()
lim1 = math.floor(lim1/60/5)*60*5 #round to nearest 5 minutes
lim2 = math.ceil(lim2/60/5)*60*5 #round to nearest 5 minutes
ax.set_xlim(lim1,lim2)
ax.xaxis.set_major_locator(ticker.MaxNLocator(15, min_n_ticks=5))
formatter = matplotlib.ticker.FuncFormatter(lambda ms, x: time.strftime('%H:%M:%S', time.gmtime(ms)))
ax.xaxis.set_major_formatter(formatter)
ax.tick_params('x', labelrotation=290)


# MaxN Locator
ax = plt.subplot(n, 1, 7)
setup(ax)
ax.xaxis.set_major_locator(ticker.MaxNLocator(4))
ax.xaxis.set_minor_locator(ticker.MaxNLocator(40))#, steps=[60,60*5,60*15, 60*30, 60*60]))
ax.text(0.0, 0.1, "MaxNLocator(n=4)", fontsize=14, transform=ax.transAxes)

# Log Locator
ax = plt.subplot(n, 1, 8)
setup(ax)
ax.set_xlim(10**3, 10**10)
ax.set_xscale('log')
ax.xaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=15))
ax.text(0.0, 0.1, "LogLocator(base=10, numticks=15)",
        fontsize=15, transform=ax.transAxes)

# Push the top of the top axes outside the figure because we only show the
# bottom spine.
plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=1.05)

plt.show()