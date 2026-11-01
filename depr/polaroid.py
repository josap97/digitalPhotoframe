from os import name
import cv2
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
imageSize = 0.8 # Max image size as ratio of full frame
barModifier = 0.9

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

overlayStyle = ['polaroid', 'christmas']
overlayPick = overlayStyle[0]


while True:
        random.shuffle(imageList)
        for img in imageList:
                currRotation = random.randrange(-10,10)
                # Polaroid Frame
                polaroidOverlay = Image.open("assets/polaroid/" + overlayPick + "Overlay.png")
                polaroidOverlay = polaroidOverlay.rotate(currRotation, Image.NEAREST, expand = 1)
                polaroidOverlayAlpha = Image.open("assets/polaroid/" + overlayPick + "OverlayAlpha.png")
                polaroidOverlayAlpha = polaroidOverlayAlpha.rotate(currRotation, Image.NEAREST, expand = 1)

                # IMG load
                image = Image.open(img)
                image = image.rotate(currRotation, Image.NEAREST, expand = 1)
                imw, imh = image.size
                aspectRatio = imw/imh
                if imw > imh:
                        imh = height * imageSize
                        imw = round(aspectRatio * height * imageSize)
                else:
                        imw = width * imageSize
                        imh = round(aspectRatio * width * imageSize)
                noFrames = config.imageFrames()
                for i in range(1, noFrames):
                        imageWidth = imw + functions.QuadraticEaseOutRound(i, noFrames, imw*0.05)
                        imageHeight = imh + functions.QuadraticEaseOutRound(i, noFrames, imh*0.05)
                        image = image.resize((round(imageWidth*1.05), round(imageHeight*1.05)))
                        polaroidOverlay = polaroidOverlay.resize((round(imageWidth*1.05), round(imageHeight*1.05)))
                        polaroidOverlayAlpha = polaroidOverlayAlpha.resize((round(imageWidth*1.05), round(imageHeight*1.05)))
                        frame = background
                        img_pil = Image.fromarray(frame)
                        draw = ImageDraw.Draw(img_pil)
                        img_pil.paste(image, (round((width - imageWidth)/2 + random.randint(0,config.positionJitter*2)-config.positionJitter), round((height-imageHeight)/2 + random.randint(0,config.positionJitter*2)-config.positionJitter)), polaroidOverlayAlpha)
                        img_pil.paste(polaroidOverlay, (round((width - imageWidth)/2 + random.randint(0,config.positionJitter*2)-config.positionJitter), round((height-imageHeight)/2 + random.randint(0,config.positionJitter*2)-config.positionJitter)), polaroidOverlay)

                        # Draw Overlay
                        #draw.rectangle([(round((width - imageWidth)/2*barModifier), round((height-imageHeight)/2*barModifier)), (width - round((width - imageWidth)/2*barModifier), round((height-imageHeight)/2*barModifier) + round(imageHeight * 0.2))], fill="#ffffff")
                        #draw.rectangle([(round((width - imageWidth)/2*barModifier), round((height-imageHeight)/2*barModifier)), (round((width - imageWidth)/2*barModifier+imageWidth * 0.2), round((height-imageHeight)/2) + round(imageHeight))], fill="#ffffff")
                        #draw.rectangle([(round(imageWidth + (width - imageWidth)/2*barModifier), round((height-imageHeight)/2*barModifier)), (round(imageWidth + (width - imageWidth)/2*barModifier+imageWidth * 0.2), round((height-imageHeight)/2) + round(imageHeight))], fill="#ffffff")
                        frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

                        cv2.imshow("video", frame)
                        cv2.waitKey(round(1000/config.renderFPS))