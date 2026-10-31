import random
import config
import numpy as np

def getEntryPoint():
        xPos = round(random.random() * config.winwidth)
        yPos = round(random.random() * config.winheight)
        Vx = (random.random()) * config.Vmax
        Vy = (random.random()) * config.Vmax
        r = round(random.random() * (config.rmax - config.rmin)) + config.rmin
        if random.random() > 0.5: # Start on sides
                if xPos > config.winwidth * 0.5:
                        xPos = config.winwidth
                        Vx = -1 * Vx
                else:
                        xPos = 0
                        Vx = Vx
        else:   # Start on top/bottom
                if yPos > config.winheight * 0.5:
                        yPos = config.winheight
                        Vy = Vy * -1
                else:
                        yPos = 0
                        Vy = Vy
        return xPos, yPos, Vx, Vy, r

def getNewPos(xPos, yPos, Vx, Vy, r):
        yPos = yPos + Vy*config.dt - 0.5*config.g*config.dt**2
        xPos = xPos + Vx*config.dt
        onScreen = True
        if yPos - r < 0:
                yPos = r + np.abs(yPos)
                Vy = Vy * -1
                Vy = Vy - config.g*config.dt
        elif yPos + r > config.winheight:
                yPos = config.winheight - r #- (yPos - config.winheight)
                Vy = Vy * -1
                Vy = Vy - config.g*config.dt
        if xPos + r < 0:
                xPos = xPos#r + np.abs(xPos)
                Vx = Vx #* -1
                onScreen = False
        elif xPos - r > config.winwidth:
               xPos = xPos#config.winwidth - r #- (xPos - config.winwidth)
               Vx = Vx #* -1
               onScreen = False
        return xPos, yPos, Vx + (np.random.rand()-0.5)*config.VrandMax, Vy + (np.random.rand()-0.5)*config.VrandMax, onScreen

def editPosMap(posMap, xPos, yPos, r):
        curPosMap = posMap
        xPos = round(xPos)
        yPos = round(yPos)
        for i in range(-1* r, r):
                y = yPos + r  - i
                if (y>0) and (y<config.winheight):
                        for j in range(xPos - i, xPos + i):
                                if (j>0) and (j<config.winwidth):
                                        if curPosMap[i][j] == 1:
                                                return posMap, True, i, j
                                        curPosMap[i][j] = 1
        return curPosMap, False, 0, 0