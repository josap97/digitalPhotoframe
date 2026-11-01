import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import config, functions, weather
import math, sys, time, random, os, asyncio
import tkinter as tk
from tkinter import ttk

rootDropdownPopup = tk.Tk()
rootDropdownPopup.geometry("200x200")

folderChoice = ''

def dropdownWindowPick():
    global folderChoice
    folderChoice = cb.get()
    rootDropdownPopup.destroy()

def dropdownWindowClose():
    rootDropdownPopup.destroy()
    exit()

folder_dir = "images/"
folderArr = []
customColours = ['#AD1D25','#1E4785','#C8CCCE','#388E3C','#E17000','#9C27B0', '#fff000']
for folder in os.listdir('images/'):
    folderArr.append(folder)

# Combobox  
cb = ttk.Combobox(rootDropdownPopup, values=folderArr)
cb.set("Select a folder to show on the frame")
cb.pack()
tk.Button(rootDropdownPopup, text="Show Selection", command=dropdownWindowPick).pack()
rootDropdownPopup.protocol("WM_DELETE_WINDOW", dropdownWindowClose)
rootDropdownPopup.mainloop()
choice = folderChoice
#folder_dir = folder_dir + folderArr[int(choice)] + '/'
folder_dir = folder_dir + folderChoice + '/'

imageList = []
for images in os.listdir(folder_dir):
    # check if the image ends with png or jpg or jpeg
    if (images.endswith(".png") or images.endswith(".jpg") or images.endswith(".jpeg")):
        imageList.append(folder_dir + images)

root = tk.Tk()
frameWidth = root.winfo_screenwidth()
frameHeight = root.winfo_screenheight()

# Define fonts
fontPath = "assets/fonts/Corbel Bold.ttf"
font200 = ImageFont.truetype(fontPath, 200)
font150 = ImageFont.truetype(fontPath, 150)
font100 = ImageFont.truetype(fontPath, 100)
font75 = ImageFont.truetype(fontPath, 75)
font50 = ImageFont.truetype(fontPath, 50)
font25 = ImageFont.truetype(fontPath, 25)
ascent, descent = font100.getmetrics()
text100Width = font100.getmask('text_string').getbbox()[2]
text100Height = font100.getmask('text_string').getbbox()[3] + descent

# Weather fonts
weatherFontPath = functions.get_emoji_font_path()
weatherFont100 = ImageFont.truetype(weatherFontPath, 100)
weatherFont50 = ImageFont.truetype(weatherFontPath, 50)
weatherFont25 = ImageFont.truetype(weatherFontPath, 25)

# Define initial frame
#background = cv2.imread("assets/F12017Set/bottomBar/backgroundBlue.png")
background = Image.new( mode = "RGB", size = (frameWidth, frameHeight), color = (0,0,0) )
background.save('assets/currentWindow.png')
background = cv2.imread("assets/currentWindow.png")
backgroundColour = (0, 0, 0)
cv2.namedWindow("Photo Frame", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Photo Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

running = True
while running:
    random.shuffle(imageList)
    for img in imageList:
        if not running:
            break
        weatherDay, weatherHour, _ = asyncio.run(weather.getWeather())
        currAccentColour = functions.HEXtoRGB(customColours[np.random.randint(0, len(customColours))])
        image = Image.open(img)
        imw, imh = image.size
        aspectRatio = imw/imh
        imh = frameHeight
        imw = round(aspectRatio * frameHeight)
        noFrames = config.imageFrames()
        for i in range(1, noFrames):
            imageWidth = imw + i*(imw*0.05)/noFrames#functions.QuadraticEaseOutRound(i, noFrames, imw*0.05)
            imageHeight = imh + i*(imh*0.05)/noFrames#functions.QuadraticEaseOutRound(i, noFrames, imh*0.05)
            imageOnFrame = image.resize((round(imageWidth*1.05), round(imageHeight*1.05)))
            frame = background
            img_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(img_pil)
            img_pil.paste(imageOnFrame, (round((frameWidth - imageWidth)/2), round((frameHeight-imageHeight)/2)))
            
            t = time.localtime()
            currentTime = time.strftime("%H:%M", t)
            draw.text((0, frameHeight-75), currentTime, fill='grey', font=font200, anchor='ld', align="right")
            currentDate = time.strftime("%a %d-%m-%Y", t)
            draw.text((0, frameHeight), currentDate, fill='grey', font=font75, anchor='ld', align="right")

            # Weather forecast
            weatherBlockWidth = 225
            weatherBlockHeight = 250
            weatherBottomIconOffset = 50
            textColour = customColours[2] if currAccentColour != functions.HEXtoRGB(customColours[2]) else customColours[1]
            for h in weatherHour:
                xCoor = frameWidth - weatherBlockWidth*1.05*(len(weatherHour)-1-h.wID)
                shape = (
                    (xCoor - weatherBlockWidth, frameHeight - weatherBlockHeight),
                    (xCoor, frameHeight),
                )
                draw.rounded_rectangle(shape, fill=tuple([int(c*(1-0.2*h.wID)) for c in currAccentColour]), radius=25)
                draw.text((xCoor - weatherBlockWidth*0.5, frameHeight-weatherBlockHeight), f'{h.timeStr}', fill=textColour, font=font50, anchor='ma')

                hAvail = weatherBlockHeight - text100Height/2 * 2
                yIconPos = frameHeight - text100Height/2 - hAvail/2
                xIconPos = xCoor - weatherBlockWidth/2
                draw.text((xIconPos, yIconPos), f'{h.emoji[0]}', fill=textColour, font=weatherFont100, anchor='mm')
                draw.text((xCoor - weatherBlockWidth*0.75, frameHeight), f'{h.temperature} °C', fill=textColour, font=font50, anchor='md')
                draw.text((xCoor - weatherBlockWidth*0.75, frameHeight-weatherBottomIconOffset), u'\N{THERMOMETER}', fill=textColour, font=weatherFont25, anchor='md')
                if h.wID == 0:
                    draw.text((xCoor - weatherBlockWidth*0.25, frameHeight-weatherBottomIconOffset), u'\N{FACE WITH THERMOMETER}', fill=textColour, font=weatherFont25, anchor='md')
                    draw.text((xCoor - weatherBlockWidth*0.25, frameHeight), f'{h.feelsLike} °C', fill=textColour, font=font50, anchor='md')
                else:
                    if h.rain > 50:
                        draw.text((xCoor - weatherBlockWidth*0.25, frameHeight-weatherBottomIconOffset), u'\N{THUNDER CLOUD AND RAIN}', fill=textColour, font=weatherFont25, anchor='md')
                    elif 25 < h.rain < 50:
                        draw.text((xCoor - weatherBlockWidth*0.25, frameHeight-weatherBottomIconOffset), u'\N{CLOUD WITH RAIN}', fill=textColour, font=weatherFont25, anchor='md')
                    elif 0 < h.rain < 25:
                        draw.text((xCoor - weatherBlockWidth*0.25, frameHeight-weatherBottomIconOffset), u'\N{CLOUD}', fill=textColour, font=weatherFont25, anchor='md')
                    draw.text((xCoor - weatherBlockWidth*0.25, frameHeight), f'{h.rain}%', fill=textColour, font=font50, anchor='md')

            frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
            cv2.imshow("Photo Frame", frame)
            if cv2.waitKey(round(1000/config.renderFPS)) & 0xFF == 27:
                running = False
                break
    cv2.destroyAllWindows()
