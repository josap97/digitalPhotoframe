from os import name
import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
from PIL import ImageFont, ImageDraw, Image, ImageOps
import config
import functions
import math, sys, time, random, os
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter
else:
    import tkinter

folder_dir = "images/"
folderArr = []
i = 0
print('Type the number relating to the folder you want to display and hit enter:')
for folder in os.listdir('images/'):
     folderArr.append(folder)
     print(str(i) + '. ' + folder)
     i = i + 1
choice = input()
folder_dir = folder_dir + folderArr[int(choice)] + '/'

imageList = []
imgVisible = []
imgPosition = []
imgSize = []
for images in os.listdir(folder_dir):
    # check if the image ends with png or jpg or jpeg
    if (images.endswith(".png") or images.endswith(".jpg") or images.endswith(".jpeg")):
        imageList.append(folder_dir + images)

random.shuffle(imageList)

root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

# Define fonts
fontpath = "assets/fonts/Formula1-Regular.ttf"
font200 = ImageFont.truetype(fontpath, 200)
font150 = ImageFont.truetype(fontpath, 150)
font100 = ImageFont.truetype(fontpath, 100)
font75 = ImageFont.truetype(fontpath, 75)
font50 = ImageFont.truetype(fontpath, 50)
font25 = ImageFont.truetype(fontpath, 25)

# Define initial frame
#background = cv2.imread("assets/F12017Set/bottomBar/backgroundBlue.png")
background = Image.new( mode = "RGB", size = (width, height), color = (0,0,0) )
background.save('assets/currentWindow.png')
background = cv2.imread("assets/currentWindow.png")
backgroundColour = (0, 0, 0)
cv2.namedWindow("video", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Define images
topBar = Image.open("assets/F12017Set/bottomBar/topBar.png")
teamColour = (255,0,0)


#posX = math.trunc(-width + functions.QuadraticEaseOut(i, 20, width))
#draw.text((posX+413, 65), 'pos', font = font75, fill=(0, 0, 0, 0), anchor="mm")

imgCircleList = []
noFrames = round(config.renderFPS * config.windowTimer / 1000)
for img in imageList:
        image = Image.open(img)
        imw, imh = image.size
        aspectRatio = imw/imh
        if imw > imh:
                imh = height
                imw = imh
                size = (imh, imh)
        else:
                imw = width
                imh = imw
                size = (imw, imw)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + size, fill=255)

        image = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
        image.putalpha(mask)
        imgCircleList.append(image)
        index = len(imgVisible)
        if(index > 3):
                imgVisible.append([imgVisible[-3][0] + noFrames, imgVisible[-3][1] + 4 * noFrames])
        elif(index<1):
              imgVisible.append([0, 4*noFrames])
        else:
              imgVisible.append([imgVisible[-1][0] + noFrames, imgVisible[-1][1] + 4 * noFrames])

log = imgCircleList[0]
for i in range(1, imgVisible[-1][1]):
        frame = background
        img_pil = Image.fromarray(frame)
        for j in range(0, len(imgVisible)):
                image = imgCircleList[j]
                frameMin = imgVisible[j][0]
                frameMax = imgVisible[j][1]
                imgFrame = i - frameMin + 1
                if i > frameMin and i < frameMax:
                        if imgFrame < noFrames:
                                imageWidth = functions.QuadraticEaseOutRound(imgFrame, noFrames, height * config.imageSize)
                        elif imgFrame > 3 * noFrames and imgFrame < 4*noFrames - 1:
                              imageWidth = functions.QuadraticEaseOutInvRound(imgFrame - 3*noFrames, noFrames + 1, height * config.imageSize)
                        elif imgFrame > 4*noFrames-1:
                              break
                        else:
                              imageWidth = round(height * config.imageSize)
                        maxEndPosition = (height-imageWidth)/2
                        radius = min(maxEndPosition, functions.QuadraticEaseOut(imgFrame, noFrames, maxEndPosition))
                        phi = -functions.QuadraticEaseOutInv(imgFrame, noFrames * 4, 2 * np.pi)
                        x = round(radius * np.cos(phi)) + round(width * 0.5)
                        y = round(radius * np.sin(phi)) + round(height * 0.5)
                        image = image.resize((imageWidth, imageWidth))
                        
                        draw = ImageDraw.Draw(img_pil)
                        img_pil.paste(image, (x, y), image)
        frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

        cv2.imshow("video", frame)
        cv2.waitKey(round(1000/config.renderFPS))