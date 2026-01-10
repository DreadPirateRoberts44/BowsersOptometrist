import pyautogui
from PIL import Image
import cv2
import numpy as np
from time import sleep
import pydirectinput
import copy


# Designed to run in vertical mode (for best visual effect)
# This is very general, taken from the mario ds
# koopa corps at least won't need the top screen at all, and only a portion of the bottom screen
subScreenScale=77/32
subScreenX=652
subScreenY=552
subScreenWidth=616
subScreenHeight=462

subScreen =[subScreenX, subScreenY, subScreenWidth, subScreenHeight]

area = [subScreenX, subScreenY, 300, 400]

# Take a screenshot of the area the koopas are running through
# return image in cv2.COLOR_BGR2GRAY format
def getScreenshot():
    # Takes a screenshot based on which screen is required. 
    screenshot = pyautogui.screenshot(
        region= area)
    size = screenshot.size
    scale = subScreenScale
    # Scales image to match original DS screen size. 
    screenshot = screenshot.resize((int(size[0] / scale), 
        int(size[1] / scale) ), Image.Resampling.NEAREST)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)

# Loads the koopa sprite "needle" images to find in the screenshots we take
# currently, the one image of a koopa face is sufficient
def loadNeedle(filename):
    needle = Image.open(f"assets/Yoo Who Cannon/" + filename + ".png")
    size = needle.size
    scale = subScreenScale
    # Scales image to match original DS screen size. 
    needle = needle.resize((int(size[0] / scale), 
        int(size[1] / scale) ), Image.Resampling.NEAREST)
    return cv2.cvtColor(np.array(needle), cv2.COLOR_BGR2GRAY)

def testSpriteDetection(needle):
    cv2.imshow('Ready Cannon', needle)
    haystack = getScreenshot()
    cv2.imshow('Ready Cannon', haystack)
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)

    img_rgb =cv2.cvtColor(haystack, cv2.COLOR_RGB2BGR)

    w, h = needle.shape[::-1]
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8 #barrel can be .95. Mario could be done with .8, luigi needs .6, but then need filtered
                    # luigi has a lot of variance in exacly how he poses
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.imshow('Ready Cannon', img_rgb)
    cv2.waitKey(0)
    print(len(loc[0]))


# one time operation
readyCannonNeedle = loadNeedle("readied-barrel")
marioNeedle = loadNeedle("mario")
luigiNeedle = loadNeedle("luigi-hat")

#testSpriteDetection(readyCannonNeedle)
testSpriteDetection(marioNeedle)
testSpriteDetection(luigiNeedle)