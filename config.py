import random

global windowTimer, renderFPS, imageSize, positionJitter
windowTimer = 2000      # Length of time (in ms) an image should be displayed
renderFPS = 60
imageSize = 0.25        # as a fraction of the screensize
positionJitter = 0      # number of pixels around the centre of the screen where the image can be shown. Default at 0 as it can be jarring
dayTime = True          # True or False to add time and date to the bottom right of the screen

def windowTime():
    modifier = random.randint(0, int(windowTimer*0.2)) - windowTimer*0.1
    currTime = round(windowTimer + modifier)
    return currTime

def imageFrames():
    frames = round(windowTime()/1000 * renderFPS)
    return frames

# phys.py settings
global Vmax, rmax, g, FPS, dt, winwidth, winheight
Vmax = 200
VrandMax = 10
rmax = 500
rmin = 100
g = 0#9.81
FPS = 10
dt = 1/FPS
winwidth = 0
winheight = 0