import random
import config

def getEntryPoint():
        xPos = round(random.random() * config.winwidth)
        yPos = round(random.random() * config.winheight)
        Vx = (random.random() - 0.5) * config.Vmax
        Vy = (random.random() - 0.5) * config.Vmax
        r = round(random.random() * config.rmax)
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

def getNewPos(xPos, yPos, Vx, Vy):
        yPos = yPos + Vy*config.dt - 0.5*config.g*config.dt**2
        xPos = xPos + Vx*config.dt
        if yPos < 0:
                yPos = yPos * -1
                Vy = Vy * -1
                Vy = Vy - config.g*config.dt
        elif yPos > config.winheight:
                yPos = config.winheight - (yPos - config.winheight)
                Vy = Vy * -1
                Vy = Vy - config.g*config.dt
        if xPos < 0:
                xPos = xPos * -1
                Vx = Vx * -1
        elif xPos > config.winwidth:
               xPos = config.winwidth - (xPos - config.winwidth)
               Vx = Vx * -1
        return xPos, yPos, Vx, Vy

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