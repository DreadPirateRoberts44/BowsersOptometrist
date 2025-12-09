import pyautogui
from PIL import Image
import cv2
import numpy as np

# Current Computer high score: 80


# Designed to run in vertical mode (for best visual effect)
# This is very general, taken from the mario ds
# Goomba storm at least won't need the top screen at all, and only a portion of the bottom screen
"""
# Refers to the top screen of the DS unneeded for goomba storm
mainScreenScale=2.35
mainScreenX=652
mainScreenY=89
mainScreenWidth=615
mainScreenHeight=460
"""

# Refers to the bottom screen of the DS
#subScreenScale=28/11
#subScreenX=652 # this is definitely right
#subScreenY=754
#subScreenWidth=424 # we only need to cover the distance between bowser and madam bloque
#subScreenHeight=318 # we likely can reduce this significantly
# maintain aspect raio. DS is 256/192

# Using this for now, this is horizontal layout full bottom screen. Looking to reduce in scope, and/or replace with vertical
subScreenScale=3.75
subScreenX=960
subScreenY=182
subScreenWidth=960
subScreenHeight=720


runningGoombaSprites = []

goombaRunningArea = [ subScreenX, subScreenY, subScreenWidth, subScreenHeight]

# Take a screenshot of the area the goombas are running through
# return image in cv2.COLOR_BGR2GRAY format
def getScreenshot():
    # Takes a screenshot based on which screen is required. 
    screenshot = pyautogui.screenshot(
        region= goombaRunningArea)
    size = screenshot.size
    scale = subScreenScale
    # Scales image to match original DS screen size. 
    screenshot = screenshot.resize((int(size[0] / scale), 
        int(size[1] / scale) ), Image.Resampling.NEAREST)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)

# Loads the goomba sprite "needle" images to find in the screenshots we take
# currently, the one image of a goomba face is sufficient
def loadGoombaSprites():
    goomba = Image.open(f"assets/Goomba Storm/goomba-face.png")
    runningGoombaSprites.append(goomba)

# Moves the mouse to and clicks the location
# bounds is in the format [x, y, w, h]
# where x and y are only relative to the screenshot taken, not the postion of your very real ds monitor display
def pressIcon(bounds):
    # Finds center of the icon. 
    #print(bounds)
    iconCenter = pyautogui.center(bounds)

    position = ( 
        ( iconCenter[0] * subScreenScale ) 
            + subScreenX,                 
        ( iconCenter[1] * subScreenScale ) 
            + subScreenY
    )

    # Clicks on the icon. 
    pyautogui.moveTo(position[0] + 125, position[1])
    pyautogui.drag(0, 1, 0.15) # I believe we must use a drag here, as just clicking is not fast enough for the ds to register as input

# one time operation
loadGoombaSprites()
# convert our goomba sprite(s) to a needle image to be found in the screenshot
# currently both needle and haystack are in grayscale
needle = cv2.cvtColor(np.array(runningGoombaSprites[0]), cv2.COLOR_BGR2GRAY)
w, h = needle.shape[::-1]

# loop while playing
while True:
    # get screenshot of the area goombas are running through
    haystack = getScreenshot()
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        pressIcon([pt[0], pt[1], w, h])
        break
        