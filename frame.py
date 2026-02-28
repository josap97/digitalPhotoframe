from os import name
import cv2
import time
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
from PIL import ImageFont, ImageDraw, Image
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
for images in os.listdir(folder_dir):
    # check if the image ends with png or jpg or jpeg
    if (images.endswith(".png") or images.endswith(".jpg") or images.endswith(".jpeg")):
        imageList.append(folder_dir + images)

root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

# Define fonts
fontpath = "assets/fonts/GT-Regular.otf"
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


#posX = math.trunc(-width + functions.QuadraticEaseOut(i, 20, width))
#draw.text((posX+413, 65), 'pos', font = font75, fill=(0, 0, 0, 0), anchor="mm")

while True:
        random.shuffle(imageList)
        for img in imageList:
                image = Image.open(img)
                imw, imh = image.size
                aspectRatio = imw/imh
                if imw > imh:
                        imh = height
                        imw = round(aspectRatio * height)
                else:
                        imw = width
                        imh = round(aspectRatio * width)
                noFrames = config.imageFrames()
                for i in range(1, noFrames):
                        imageWidth = imw + functions.QuadraticEaseOutRound(i, noFrames, imw*0.05)
                        imageHeight = imh + functions.QuadraticEaseOutRound(i, noFrames, imh*0.05)
                        image = image.resize((round(imageWidth*1.05), round(imageHeight*1.05)))
                        frame = background
                        img_pil = Image.fromarray(frame)
                        draw = ImageDraw.Draw(img_pil)
                        img_pil.paste(image, (round((width - imageWidth)/2 + random.randint(0,config.positionJitter*2)-config.positionJitter), round((height-imageHeight)/2 + random.randint(0,config.positionJitter*2)-config.positionJitter)))
                        
                        t = time.localtime()
                        current_time = time.strftime("%H:%M", t)
                        draw.text((width, height), current_time, fill='grey', font=font200, anchor='rd', align="right")

                        frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
                        cv2.imshow("video", frame)
                        cv2.waitKey(round(1000/config.renderFPS))