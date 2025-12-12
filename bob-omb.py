import pyautogui
from PIL import Image
import cv2
import numpy as np
import time

# Current Computer high score: 399

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
subScreenScale=77/32
subScreenX=652
subScreenY=552
subScreenWidth=616
subScreenHeight=462

bobombSprites = []
screenshotYOffset = 135
bobombRunningArea = [subScreenX, subScreenY + screenshotYOffset, 130, 260]

# for bob-omb blitz, we also care where madame is
madameArea = [subScreenX + 200, subScreenY + screenshotYOffset, 400, 240]

# Take a screenshot of the area the bob-ombs are running through
# return image in cv2.COLOR_BGR2GRAY format
def getScreenshot(isBobomb):
    if isBobomb: area = bobombRunningArea
    else: area = madameArea
    # Takes a screenshot based on which screen is required. 
    screenshot = pyautogui.screenshot(
        region= area)
    size = screenshot.size
    scale = subScreenScale
    # Scales image to match original DS screen size. 
    screenshot = screenshot.resize((int(size[0] / scale), 
        int(size[1] / scale) ), Image.Resampling.NEAREST)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)

# Loads the bob-omb sprite "needle" images to find in the screenshots we take
# currently, the one image of a bob-omb face is sufficient
def loadBobombSprites():
    bobomb = Image.open(f"assets/Bob-omb Blitz/bob-omb-full.png")
    size = bobomb.size
    scale = subScreenScale
    # Scales image to match original DS screen size. 
    bobomb = bobomb.resize((int(size[0] / scale), 
        int(size[1] / scale) ), Image.Resampling.NEAREST)
    bobomb = cv2.cvtColor(np.array(bobomb), cv2.COLOR_BGR2GRAY)
    bobombSprites.append(bobomb)

def testSpriteDetection():
    needle = bobombSprites[0]
    haystack = getScreenshot(True)
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)

    img_rgb =cv2.cvtColor(haystack, cv2.COLOR_RGB2BGR)

    w, h = needle.shape[::-1]
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.imshow('Bob-omb', img_rgb)
    cv2.waitKey(0)
    print(loc)

def testMadameDetection(needle):
    haystack = getScreenshot(False)
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)
    img_rgb =cv2.cvtColor(haystack, cv2.COLOR_RGB2BGR)

    w, h = needle.shape[::-1]
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.imshow('Bob-omb', img_rgb)
    cv2.waitKey(0)
    print(loc)

# Loads the sprite for madame
def loadMadameSprite():
    madame = Image.open(f"assets/Bob-omb Blitz/broque-madame.png")
    size = madame.size
    scale = subScreenScale
    # Scales image to match original DS screen size. 
    madame = madame.resize((int(size[0] / scale), 
        int(size[1] / scale) ), Image.Resampling.NEAREST)
    return cv2.cvtColor(np.array(madame), cv2.COLOR_BGR2GRAY)

def moveBomb(x,y, madameBroqueY):
    x = x * subScreenScale + subScreenX
    y = y * subScreenScale + subScreenY + screenshotYOffset   
    madameBroqueY = madameBroqueY * subScreenScale + subScreenY + screenshotYOffset   
    pyautogui.mouseDown(x, y, _pause=False)
    pyautogui.moveTo(subScreenX + 130,madameBroqueY)
    pyautogui.mouseUp(subScreenX + 130,madameBroqueY)
    

loadBobombSprites()
madameNeedle = loadMadameSprite()
bobombNeedle = bobombSprites[0]
#testMadameDetection(madameNeedle)
#testSpriteDetection()
#exit()

w, h = madameNeedle.shape[::-1]
w2, h2 = bobombNeedle.shape[::-1]
# loop while playing
while True:
    # get screenshot of the area goombas are running through
    try:
        bombhaystack = getScreenshot(True)
        madameHaystack = getScreenshot(False)
    except:
        exit()
    # Determine Madame Y position
    y = 0
    res = cv2.matchTemplate(madameHaystack,madameNeedle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        y = pt[1] + h
        break
    # Find all bob-ombs
    res = cv2.matchTemplate(bombhaystack,bobombNeedle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        moveBomb(pt[0],pt[1] + h2/2, y)
        break