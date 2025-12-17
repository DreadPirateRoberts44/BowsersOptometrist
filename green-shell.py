import pyautogui
from PIL import Image
import cv2
import numpy as np
from time import sleep
import pydirectinput

# Current Computer high score: 105

# first problems solved: 
# being stupid
# not adjusting the y value of koopa locations by the subscreen scale factor

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


shellSprite = []
marioArea = [subScreenX + 150, subScreenY + 158, 100, 120]
luigiArea = [subScreenX + 150, subScreenY + 158 + 120, 100, 120]

# Take a screenshot of the area the koopas are running through
# return image in cv2.COLOR_BGR2GRAY format
def getScreenshot(isMario = True):
    if isMario: area = marioArea
    else: area = luigiArea
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
def loadShellSprite():
    koopa = Image.open(f"assets/Green Shell/shell1.png")
    size = koopa.size
    scale = subScreenScale
    # Scales image to match original DS screen size. 
    koopa = koopa.resize((int(size[0] / scale), 
        int(size[1] / scale) ), Image.Resampling.NEAREST)
    shellSprite.append(cv2.cvtColor(np.array(koopa), cv2.COLOR_BGR2GRAY))

def testSpriteDetection(isMario = True):
    needle = shellSprite[0]
    haystack = getScreenshot(isMario)
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)

    img_rgb =cv2.cvtColor(haystack, cv2.COLOR_RGB2BGR)

    w, h = needle.shape[::-1]
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.73
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.imshow('Green Shell', img_rgb)
    cv2.waitKey(0)
    print(len(loc[0]))


# one time operation
loadShellSprite()
#testSpriteDetection(True)
#testSpriteDetection(False)
#exit()

# convert our koopa sprite(s) to a needle image to be found in the screenshot
# currently both needle and haystack are in grayscale
needle = shellSprite[0]
isMario = False

# loop while playing
while True:
    # get screenshot of the area koopas are running through
    try:
        haystack = getScreenshot(isMario)
    except:
        exit()
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where(res >= threshold)
    if len(loc[0]) > 0:
        if isMario: key = 'x'
        else:  key = 'z'
        pydirectinput.press(key, _pause=False)
        isMario = not isMario
        
        