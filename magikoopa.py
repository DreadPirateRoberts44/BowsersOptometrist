import pyautogui
from PIL import Image
import cv2
import numpy as np
from time import time, sleep

# Current Computer high score: 345

# Designed to run in vertical mode (for best visual effect)
# This is very general, taken from the mario ds
# koopa corps at least won't need the top screen at all, and only a portion of the bottom screen
subScreenScale=77/32
subScreenX=652
subScreenY=552
subScreenWidth=616
subScreenHeight=462

refreshRate = .1

magikoopaSprites = []

screenshotYOffset = 75
screenshotXOffset = 75
# low bound is subY + 50 + 275
koopaRunningArea = [ subScreenX + screenshotXOffset, subScreenY + screenshotYOffset, 335, 260]

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
    threshold = 0.74
    loc = np.where(res >= threshold)
    #print(len(loc[0]))
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

def calculateSlope(x1,y1,x2,y2):
    if x1 == x2:
        x1 += 1
    m = int((y2 - y1) / (x2 - x1))
    return m

def dragTo(x,y, dragTime):
    x = x * subScreenScale + subScreenX + screenshotXOffset
    y = y * subScreenScale + subScreenY + screenshotYOffset      
    pyautogui.moveTo(x,y, duration=dragTime)



#best so far includes the pause on drag, but with very minor pause. 


# one time operation
loadMagikoopaSprites()
pyautogui.PAUSE = .03
#testSpriteDetection()
#exit()
#we never need to let up (it also doesn't matter where the mouse starts, at least if it's on screen)
pyautogui.moveTo(subScreenX + 30, subScreenY + 30)
pyautogui.mouseDown(_pause = False)

# convert our magikoopa sprite(s) to a needle image to be found in the screenshot
# currently both needle and haystack are in grayscale
needle = cv2.cvtColor(np.array(magikoopaSprites[0]), cv2.COLOR_BGR2RGB)
w, h = needle.shape[1], needle.shape[0]

# every 9 rounds adds a magikoopa (at least to a total of 6)
roundNumber = 1
numberOfMagikoopas = 3

#refreshTime = time()
pts = []
# loop while playing
while True:
    # get screenshot of the area goombas are running through
    #stopWatch = time()
    try:
        #diff = time() - refreshTime
        #sleep(max(diff, 0))
        haystack = getScreenshot()
        #refreshTime = time()
    except:
        exit()
    res = cv2.matchTemplate(haystack,needle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    #if len(loc[0])>0: print("Image Detection Time: ", round(time()-stopWatch,5))
    
    minX = 1000
    minY = 1000
    maxX = 0
    maxY = 0
    #stopWatch = time()
    for pt in zip(*loc[::-1]):
        if len(pts) == 0:
            pts.append(pt)
            minX = pt[0]
            maxX = pt[0]
            minY = pt[1]
            maxY = pt[1]
            continue
        usePoint = True
        for usedPt in pts:
            if abs(pt[0]-usedPt[0]) < 10 and abs(pt[1]-usedPt[1]) < 10:
                usePoint = False
                break
        if usePoint: 
            pts.append(pt)
            if pt[0] < minX: minX = pt[0]
            if pt[0] > maxX: maxX = pt[0]
            if pt[1] < minY: minY = pt[1]
            if pt[1] > maxY: maxY = pt[1]
    
    #if len(pts) < numberOfMagikoopas: continue
    #print("Duplicate Removal Time: ", round(time()-stopWatch,5))
    # if difference is bigger vertically, sort top to bottom, else sort left to right
    #stopWatch = time()
    if maxY - minY > maxX - minX:
        pts.sort(key=lambda x: x[1])
    else:
        pts.sort()
    #print("Sort Time: ", round(time()-stopWatch,5))
    
    
    # Identify lines and remove points
    times = [0]
    i = 0
    #print(pts)
    """
    while i + 2 < len(pts):
        m = calculateSlope(pts[i + 2][0],pts[i + 2][1], pts[i][0],pts[i][1])
        y1 = m * (pts[i + 1][0] - pts[i][0]) + pts[i][1]
        if abs(y1-pts[i][1]) < 10:
            pts.pop(i + 1)
            times.append(.1001)
        else: 
            times.append(0)
            i += 1
    times.append(0)
    #print(pts)
    #print(times)
    
    #stopWatch = time()
    i = 0
    """
    #print(pts)
    for pt in pts:
        dragTo(pt[0] + 3, pt[1] + 5, 0)
        #i += 1
    #print("Drag Time: ", round(time()-stopWatch,5))


    #if roundNumber % 9 == 0 and roundNumber < 30: numberOfMagikoopas += 1
    #roundNumber += 1 
    pts = []
    
    