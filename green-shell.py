import pyautogui
from PIL import Image
import cv2
import numpy as np
from time import sleep,time
import pydirectinput
import copy
import matplotlib.pyplot as plt

# Current Computer high score: 131

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

subScreen =[subScreenX, subScreenY, subScreenWidth, subScreenHeight]

shellSprite = []
marioArea = [subScreenX + 135, subScreenY + 158 + 20, 100, 90]
luigiArea = [subScreenX + 135, subScreenY + 158 + 140, 100, 90]
xOffset = 0
yOffset = 0

# Take a screenshot of the area the koopas are running through
# return image in cv2.COLOR_BGR2GRAY format
def getScreenshot(isMario = True):
    if isMario: 
        area = copy.deepcopy(marioArea)
        area[1] += yOffset
    else: 
        area = copy.deepcopy(luigiArea)
        area[1] -= yOffset
    area[0] += xOffset
    

    # Takes a screenshot based on which screen is required. 
    screenshot = pyautogui.screenshot(
        region= area)
    size = screenshot.size
    scale = subScreenScale
    # Scales image to match original DS screen size. 
    screenshot = screenshot.resize((int(size[0] / scale), 
        int(size[1] / scale) ), Image.Resampling.NEAREST)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)

# Take a screenshot of the area the koopas are running through
# return image in cv2.COLOR_BGR2GRAY format
def getFullScreenshot(isMario = True):
    # Takes a screenshot based on which screen is required. 
    screenshot = pyautogui.screenshot(
        region= subScreen)
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

def testOffsetPaths(isMario = True):
    haystack = getFullScreenshot(isMario)
    img_rgb =cv2.cvtColor(haystack, cv2.COLOR_RGB2BGR)
    xOffset = 0
    yOffset = 0
    if isMario:
        area = marioArea
    else:
        area = luigiArea
    i = 0
    print(area)
    while i < 40:
        cv2.rectangle(img_rgb, 
                      (
                          int((area[0] + xOffset - subScreenX) / subScreenScale),
                            int((area[1] + yOffset - subScreenY) / subScreenScale)
                        ), 
                     (int((area[0] + area[2] + xOffset - subScreenX) / subScreenScale),
                      int((area[1] + area[3] + yOffset - subScreenY)/subScreenScale))
                      , (0,0,255), 2)
        xOffset += 4
        if isMario:
            yOffset += 1
        else: yOffset -= 1
        i += 1
    cv2.imshow('Green Shell', img_rgb)
    cv2.waitKey(0)

# one time operation
loadShellSprite()
#testSpriteDetection(True)
#testSpriteDetection(False)
#testOffsetPaths()
#testOffsetPaths(False)
#exit()
#pydirectinput.PAUSE = .03
# convert our koopa sprite(s) to a needle image to be found in the screenshot
# currently both needle and haystack are in grayscale
needle = shellSprite[0]
isMario = False
roundBuffer = 10
inputs = []
# how long it waited between each button push
times = []
stopWatch = 0
threshold = .7
i = 1
# loop while playing
while True:
    # get screenshot of the area koopas are running through
    try:
        haystack = getScreenshot(isMario)
    except:
        print(inputs[len(inputs) - 1])
        break
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)
    
    loc = np.where(res >= threshold)
    if len(loc[0]) > 0:
        if isMario:
            key = 'x'
        else:  key = 'z'
        pydirectinput.press(key, _pause=False)
        difference = round(time() - stopWatch, 3)
        times.append(difference)
        stopWatch = time()
        isMario = not isMario
        inputs.append(key)
        if i % roundBuffer == 0:
            xOffset += 4
            yOffset += 1
        if i == 100:
            threshold = .66
        #    roundBuffer = 2
        i += 1
        
times.pop(0)
xValues = []
i = 0
while i < len(times):
    xValues.append(i + 1)
    i += 1
print(times)
print(xValues)

plt.plot(xValues, times)

plt.xlabel('Index')
plt.ylabel('Time Between')
plt.title('A Basic Python Graph')

# Displaying the plot
plt.show()
