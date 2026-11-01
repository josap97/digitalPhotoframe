import math
from typing import ChainMap
from numpy import floor, trunc
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 2, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def stProgressBar(iteration, total):
    return math.trunc(iteration/total)

def QuadraticEaseOut(t, tMax, change):
    return float(change)*((float(t)/float(tMax)-1)**3+1)

def QuadraticEaseOutInv(t, tMax, change):
    return float(change) - float(change)*((float(t)/float(tMax)-1)**3+1)

def QuadraticEaseOutRound(t, tMax, change):
    return round(float(change)*((float(t)/float(tMax)-1)**3+1))

def QuadraticEaseOutInvRound(t, tMax, change):
    return round(float(change) - float(change)*((float(t)/float(tMax)-1)**3+1))

def drawWithBlur(image):
        bg = Image.new('RGBA', image.size)
        blur = image.filter(ImageFilter.BoxBlur(50))
        #blur = image.filter(ImageFilter.GaussianBlur(radius=50))

        bg.paste(blur,blur)
        bg.paste(image,image)

        return bg

def calcAngle2008(RPM):
    return ((RPM-6000)/14000*360*0.75-90)/180

def getBrandImg(brandString):
    files = os.listdir("assets/brands")
    for f in files:
        if(brandString.lower() in f):
            return f

def getCarClass(classString):
    classList = ['LMP1','LMH','DPi','LMP2','LMP3','GTEPro','GTEAM','GTLM','GTD','GTP']
    classColours = [(266,33,28),(266,33,28),(35,31,32),(49,96,150),(253,103,26),(0,149,59),(252,79,0),(208,51,58),(1,174,66),(208,51,58)]

    result = dict()

    for i in range(0, len(classList)):
        if(classList[i].lower() in classString.lower()):
            result["name"] = classList[i]
            result["colour"] = classColours[i]
    return result

def getEnduranceAngle(currPosition):
    #print("pos: " +str(currPosition) + " angle: " + str(-1*(currPosition-50)/50*33))
    return -1*(currPosition-50)/50*33

def get_emoji_font_path():
    """Locate a system font that supports emojis."""
    # Common emoji font paths across OS
    candidates = [
        "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",  # Linux
        "/System/Library/Fonts/Apple Color Emoji.ttc",        # macOS
        "C:\\Windows\\Fonts\\seguiemj.ttf",                  # Windows (Segoe UI Emoji)
        "C:\\Windows\\Fonts\\seguisym.ttf",                  # Windows (Symbola fallback)
        "assets\\fonts\\weather-icons-master\\font\\weathericons-regular-webfont.ttf",       # General comes with this package
    ]
    
    for path in candidates:
        if os.path.exists(path):
            return path
    
    # Fallback: try to find any .ttf/.ttc with 'emoji' in name
    import glob
    for ext in ['*.ttf', '*.ttc']:
        matches = glob.glob(f"/usr/share/fonts/**/{ext}", recursive=True) + \
                  glob.glob(f"C:/Windows/Fonts/*{ext}")
        for m in matches:
            if 'emoji' in m.lower():
                return m
                
    raise FileNotFoundError("No emoji-supporting font found. Install 'Noto Color Emoji' or similar.")

def HEXtoRGB(hex):
    h = hex.lstrip('#')
    rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return rgb