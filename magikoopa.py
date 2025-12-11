import pyautogui
from PIL import Image
import cv2
import numpy as np
import time

# Current Computer high score:

# Next problems:
# score sucks
# alignment of bowser and koopa shells (I'm grabbing middle of bowser aiming at middle of koopa, should that change?)
# prediction of where shells will be
# poor detection might cause shells to steal focus from each other

# Designed to run in vertical mode (for best visual effect)
# This is very general, taken from the mario ds
# koopa corps at least won't need the top screen at all, and only a portion of the bottom screen
subScreenScale=77/32
subScreenX=652
subScreenY=552
subScreenWidth=616
subScreenHeight=462


magikoopaSprites = []

koopaRunningArea = [ subScreenX, subScreenY + 158, 455, 240]

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

# Loads the magikoopa sprite "needle" images to find in the screenshots we take
# currently, the one image of a magikoopa face is sufficient
def loadMagikoopaSprites():
    magikoopa = Image.open(f"assets/Magikoopa Mob/magikoopa-arm.png")
    magikoopaSprites.append(magikoopa)

def testSpriteDetection():
    needle = cv2.cvtColor(np.array(magikoopaSprites[0]), cv2.COLOR_BGR2GRAY)
    haystack = getScreenshot()
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)

    img_rgb =cv2.cvtColor(haystack, cv2.COLOR_RGB2BGR)

    w, h = needle.shape[::-1]
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.imshow('Magikoopa', img_rgb)
    cv2.waitKey(0)
    print(loc)


# one time operation
loadMagikoopaSprites()
testSpriteDetection()

        