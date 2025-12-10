import pyautogui
from PIL import Image
import cv2
import numpy as np
import time

# Current Computer high score: 12

# Designed to run in vertical mode (for best visual effect)
# This is very general, taken from the mario ds
# koopa corps at least won't need the top screen at all, and only a portion of the bottom screen
subScreenScale=77/32
subScreenX=652
subScreenY=552
subScreenWidth=616
subScreenHeight=462


koopaSprites = []

koopaRunningArea = [ subScreenX + 86, subScreenY + 158, 455, 240]

# Take a screenshot of the area the koopas are running through
# return image in cv2.COLOR_BGR2GRAY format
def getScreenshot():
    # Takes a screenshot based on which screen is required. 
    screenshot = pyautogui.screenshot(
        region= koopaRunningArea)
    size = screenshot.size
    scale = subScreenScale
    # Scales image to match original DS screen size. 
    screenshot = screenshot.resize((int(size[0] / scale), 
        int(size[1] / scale) ), Image.Resampling.NEAREST)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)

# Loads the koopa sprite "needle" images to find in the screenshots we take
# currently, the one image of a koopa face is sufficient
def loadKoopaSprites():
    koopa = Image.open(f"assets/Koopa Corps/koopa2.png")
    koopaSprites.append(koopa)

def testSpriteDetection():
    needle = cv2.cvtColor(np.array(koopaSprites[0]), cv2.COLOR_BGR2GRAY)
    haystack = getScreenshot()
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)

    img_rgb =cv2.cvtColor(haystack, cv2.COLOR_RGB2BGR)

    w, h = needle.shape[::-1]
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.5
    loc = np.where(res >= threshold)
    x = 10000
    y = 0
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        if pt[0] < x:
            x = pt[0]
            y = pt[1]
    cv2.imshow('Koopa', img_rgb)
    cv2.waitKey(0)
    #print(loc)
    #print(x, y)
    #moveBowser(koopaRunningArea[0], (y + 11) * subScreenScale + subScreenY + 158)

def moveBowser(x,y):
    time.sleep(.04)
    pyautogui.moveTo(x,y)

# one time operation
loadKoopaSprites()
#testSpriteDetection()
#exit()
# Initial mouse down coordinates of bowser
bowserX= subScreenX + 30
boswerStartY = 822


# convert our koopa sprite(s) to a needle image to be found in the screenshot
# currently both needle and haystack are in grayscale
needle = cv2.cvtColor(np.array(koopaSprites[0]), cv2.COLOR_BGR2GRAY)
w, h = needle.shape[::-1]

#we never need to let up
pyautogui.mouseDown(bowserX, boswerStartY, _pause=False)

# loop while playing
while True:
    # get screenshot of the area koopas are running through
    haystack = getScreenshot()
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    x = 10000
    y = 0
    for pt in zip(*loc[::-1]):
        if pt[0] < x:
            x = pt[0]
            y = pt[1]
    if x == 10000: continue
    moveBowser(bowserX, (y + 11) * subScreenScale + subScreenY + 158)
        
        