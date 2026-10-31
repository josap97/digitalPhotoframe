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
import bubbleExport

intermediatePlotting = False
numBubbles = 20
totalFrames = 10**3
writeVideo = True
root = tkinter.Tk()
config.winwidth = root.winfo_screenwidth()
config.winheight = root.winfo_screenheight()
config.rmin = 0.05*min(config.winwidth, config.winheight)
config.rmax = 0.25*min(config.winwidth, config.winheight)
config.Vmax = min(config.winwidth, config.winheight)/60
config.VrandMax = config.Vmax*0.05
root.destroy()

class bubblePosition:
    def __init__(self):
        self.bubbleID = None
        self.px = 0
        self.py = 0
        self.vx = 0
        self.vy = 0
        self.r = 0
        self.posXHistory = []
        self.posYHistory = []
        self.active = False
        self.initFrame = 0
        self.lastFrame = totalFrames

def detectCollisions():
    dirChanged = np.zeros(len(bubbles))
    for t in range(len(bubbles)):
        target = bubbles[t]
        p1x = target.px
        p1y = target.py
        r1 = target.r
        for i in range(len(bubbles)):
            if i != t:
                bc = bubbles[i]
                p2x = bc.px
                p2y = bc.py
                r2 = bc.r
                r12Sq = (r2+r1)**2
                dSq = (p2x - p1x)**2 + (p2y-p1y)**2
                if dSq <= r12Sq:
                    if dirChanged[i] == 0:
                        bc.vx = -1 * bc.vx
                        bc.vy = -1 * bc.vy
                        dirChanged[i] = 1
                    if dirChanged[t] == 0:
                        dirChanged[t] = 1
                        target.vx = -1 * target.vx
                        target.vy = -1 * target.vy
    if np.max(dirChanged) > 0:
        return True
    else:
        return False

def createBubble():
    bubble = bubblePosition()
    xPos, yPos, Vx, Vy, r = pd.getEntryPoint()
    bubble.px = xPos
    bubble.py = yPos
    bubble.vx = Vx
    bubble.vy = Vy
    bubble.r = r
    bubble.bubbleID = b
    bubble.posXHistory.append(xPos)
    bubble.posYHistory.append(yPos)
    bubble.active = True
    return bubble

bubbles = []
for b in range(0, numBubbles):
    createCount = 0
    bubble = createBubble()
    bubble.initFrame = 0
    bubbles.append(bubble)
    if detectCollisions():
        createNew = True
        while createNew:
            bubble = createBubble()
            bubble.initFrame = 0
            createCount += 1
            bubbles[-1] = bubble
            if not detectCollisions():
                createNew = False
            elif createCount >= 10:
                createNew = False
                numBubbles -= 1
                bubbles.pop(-1)
                print('fail, destroyed')

Navg = 50
# In bubble loop
for i in range(0, totalFrames):
    print(f'run {i} with {len(bubbles)} bubbles')
    for b in bubbles:
        if not b.active:
            b.posXHistory.append(b.posXHistory[-1])
            b.posYHistory.append(b.posYHistory[-1])
            continue
        xPos, yPos, Vx, Vy, onScreen = pd.getNewPos(b.px, b.py, b.vx, b.vy, b.r)
        if (i-b.initFrame) > Navg and np.std(max(b.posXHistory[-Navg:], b.posYHistory[-Navg:])) < np.sqrt(Vx**2+Vy**2)*config.dt:
            #onScreen = False
            print('bublle stationary, discarded!!!')
        if onScreen:
            b.px = xPos
            b.py = yPos
            b.posXHistory.append(xPos)
            b.posYHistory.append(yPos)
        else:
            b.active = False
            b.lastFrame = i
            newBubble = createBubble()
            newBubble.posXHistory = (np.ones(len(bubbles[0].posXHistory))*b.px).tolist()
            newBubble.posYHistory = (np.ones(len(bubbles[0].posYHistory))*b.py).tolist()
            bubbles.append(newBubble)
    detectCollisions()

print(bubbles[0].posXHistory)

if writeVideo:
    bubbleExport.export_bubble_video(bubbles, out_path="bubblePositionVideo.mp4")