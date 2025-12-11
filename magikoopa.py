import pyautogui
from PIL import Image
import cv2
import numpy as np

# Current Computer high score: 177

# Designed to run in vertical mode (for best visual effect)
# This is very general, taken from the mario ds
# koopa corps at least won't need the top screen at all, and only a portion of the bottom screen
subScreenScale=77/32
subScreenX=652
subScreenY=552
subScreenWidth=616
subScreenHeight=462


magikoopaSprites = []

screenshotYOffset = 50

koopaRunningArea = [ subScreenX, subScreenY + screenshotYOffset, 455, 375]

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
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB)

# Loads the magikoopa sprite "needle" images to find in the screenshots we take
# currently, the one image of a magikoopa face is sufficient
def loadMagikoopaSprites():
    magikoopa = Image.open(f"assets/Magikoopa Mob/magikoopa-magic2.png")
    size = magikoopa.size
    scale = subScreenScale
    # Scales image to match original DS screen size. 
    magikoopa = magikoopa.resize((int(size[0] / scale), 
        int(size[1] / scale) ), Image.Resampling.NEAREST)
    magikoopaSprites.append(magikoopa)

def testSpriteDetection():
    needle = cv2.cvtColor(np.array(magikoopaSprites[0]), cv2.COLOR_BGR2RGB)
    haystack = getScreenshot()
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)

    img_rgb =cv2.cvtColor(haystack, cv2.COLOR_RGB2BGR)

    w, h = needle.shape[1], needle.shape[0]
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    pts = []
    for pt in zip(*loc[::-1]):
        if len(pts) == 0:
            pts.append(pt)
            continue
        usePoint = True
        for usedPt in pts:
            if abs(pt[0]-usedPt[0]) < 5 and abs(pt[1]-usedPt[1]) < 5:
                usePoint = False
                break
        if usePoint: pts.append(pt)

    for pt in pts:
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.imshow('Magikoopa', img_rgb)
    cv2.waitKey(0)
    print(loc)
    print(pts)


def dragTo(x,y):
    x = x * subScreenScale + subScreenX
    y = y * subScreenScale + subScreenY + screenshotYOffset      
    pyautogui.moveTo(x,y)


# one time operation
loadMagikoopaSprites()

#testSpriteDetection()
#exit()
#we never need to let up (it also doesn't matter where the mouse starts, at least if it's on screen)
pyautogui.mouseDown(subScreenX + 30, subScreenY + 30, _pause=False)


# convert our magikoopa sprite(s) to a needle image to be found in the screenshot
# currently both needle and haystack are in grayscale
needle = cv2.cvtColor(np.array(magikoopaSprites[0]), cv2.COLOR_BGR2RGB)
w, h = needle.shape[1], needle.shape[0]

# every 9 rounds adds a magikoopa (at least to a total of 6)
roundNumber = 1
numberOfMagikoopas = 3

# loop while playing
while True:
    # get screenshot of the area goombas are running through
    try:
        haystack = getScreenshot()
    except:
        exit()
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    pts = []
    for pt in zip(*loc[::-1]):
        if len(pts) == 0:
            pts.append(pt)
            continue
        usePoint = True
        for usedPt in pts:
            if abs(pt[0]-usedPt[0]) < 10 and abs(pt[1]-usedPt[1]) < 10:
                usePoint = False
                break
        if usePoint: 
            i = 0
            while i < len(pts):
                if pt[0] < pts[i][0]: 
                    pts.insert(i,pt)
                    break
                i += 1
            if (i == len(pts)): pts.append(pt)
    #if len(pts) < numberOfMagikoopas: continue
    for pt in pts:
        dragTo(pt[0] + 3, pt[1] + 5)
    #dragTo(10,10)

    #if roundNumber % 9 == 0 and roundNumber < 30: numberOfMagikoopas += 1
    #roundNumber += 1 
    
    