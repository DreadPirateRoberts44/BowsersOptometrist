import pyautogui
from PIL import Image
import cv2
import numpy as np

# Current Computer high score: 999

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
bobombRunningArea = [subScreenX + 75, subScreenY + screenshotYOffset + 200, 50, 75]

# for bob-omb blitz, we also care where madame is
madameArea = [subScreenX + 200, subScreenY + screenshotYOffset, 400, 320]

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
    pyautogui.mouseDown(x, y)
    #time.sleep(.01) # this is still a little too fast, so it will occassionally miss. But for being faster, the trade off is worth it. Room to optimize
    pyautogui.moveTo(subScreenX + 130,madameBroqueY)
    pyautogui.mouseUp(subScreenX + 130,madameBroqueY)
    

loadBobombSprites()
madameNeedle = loadMadameSprite()
bobombNeedle = bobombSprites[0]
pyautogui.PAUSE = .05

w, h = madameNeedle.shape[::-1]
w2, h2 = bobombNeedle.shape[::-1]
madameY = 0
bombLocations = [ (35, 89), (30, 73), (25, 58), (20, 44), (15, 31), (10, 15)]
# loop while playing
while True:
    # get screenshot of the area goombas are running through
    try:
        bombhaystack = getScreenshot(True)
    except:
        exit()

    # Determine Bob-ombs are ready
    res = cv2.matchTemplate(bombhaystack,bobombNeedle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where(res >= threshold)
    if len(loc[0]) == 0: continue

    foundMadame = False
    # Search for madame until we have her new location after we know bob-ombs are ready
    while not foundMadame:
        madameHaystack = getScreenshot(False)
        # Determine Madame Y position
        res = cv2.matchTemplate(madameHaystack,madameNeedle,cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            madameY = pt[1] + h
            foundMadame = True
            break

    for pt in bombLocations:
        moveBomb(pt[0],pt[1] + h2/2, madameY)