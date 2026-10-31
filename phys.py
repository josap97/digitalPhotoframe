import sys
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter
else:
    import tkinter
import random
import config
import physDefinitions as pd

intermediatePlotting = False
root = tkinter.Tk()
config.winwidth = root.winfo_screenwidth()
config.winheight = root.winfo_screenheight()
root.destroy()

xPos, yPos, Vx, Vy, r = pd.getEntryPoint()
xArr = []
yArr = []
VxArr = []
VyArr = []

# In bubble loop
for i in range(0,10**4):
    positionMap = np.zeros([config.winheight, config.winwidth])
    xPos, yPos, Vx, Vy = pd.getNewPos(xPos, yPos, Vx, Vy)
    positionMap, collide, colx, coly = pd.editPosMap(positionMap, xPos, yPos, r)
    if collide:
        print("collide")
        xPos, yPos, Vx, Vy = pd.getNewPos(xPos, yPos, Vx*-1, Vy*-1)
    VxArr.append(Vx)
    VyArr.append(Vy)
    xArr.append(xPos)
    yArr.append(yPos)
    if round(i/100) == i/100 and intermediatePlotting:
        plt.imshow(positionMap)
        plt.show()


plt.plot(xArr, yArr)
plt.show()