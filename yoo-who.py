import pyautogui
from PIL import Image
import cv2
import numpy as np
from time import sleep,time
import pydirectinput

# highscore 122 A-rank

# Designed to run in vertical mode (for best visual effect)
# This is very general, taken from the mario ds
# koopa corps at least won't need the top screen at all, and only a portion of the bottom screen
subScreenScale=77/32
subScreenX=652
subScreenY=552
subScreenWidth=616
subScreenHeight=462

subScreen =[subScreenX, subScreenY, subScreenWidth, subScreenHeight]

area = [subScreenX, subScreenY + 60, 260, 250]

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
    threshold = 0.6 #barrel can be .95. Mario could be done with .8, luigi needs .6, but then need filtered
                    # luigi has a lot of variance in exacly how he poses
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        #print(pt)
    #cv2.rectangle(img_rgb, (44,79), (44 + w, 79 + h), (0,0,255), 2)
    cv2.imshow('Ready Cannon', img_rgb)
    cv2.waitKey(0)
    print(len(loc[0]))


# one time operation
readyCannonNeedle = loadNeedle("readied-barrel-2")
marioNeedle = loadNeedle("mario")
luigiNeedle = loadNeedle("luigi")

#testSpriteDetection(readyCannonNeedle)
#testSpriteDetection(marioNeedle)
#testSpriteDetection(luigiNeedle)
#exit()

brosLocations = [] # format ((x,y), isMario)

# loop while playing
while True:
    # get screenshot to find mario/luigi
    try:
        haystack = getScreenshot()
    except:
        exit()
    res = cv2.matchTemplate(haystack,marioNeedle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        usePoint = True
        for usedPt in brosLocations:
            if abs(pt[0]-usedPt[0][0]) < 10 and abs(pt[1]-usedPt[0][1]) < 10:
                usePoint = False
                break
        if usePoint: 
            brosLocations.append((pt, True))
    
    res = cv2.matchTemplate(haystack,luigiNeedle,cv2.TM_CCOEFF_NORMED)
    threshold = 0.6
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        usePoint = True
        for usedPt in brosLocations:
            if abs(pt[0]-usedPt[0][0]) < 10 and abs(pt[1]-usedPt[0][1]) < 10:
                usePoint = False
                break
        if usePoint: 
            brosLocations.append((pt, False))
    
    # if we haven't found all marios/luigis, search again
    if len(brosLocations) < 8:
        continue
    elif len(brosLocations) == 9: # This seems to be the result of detecting mario as he jumps into a new barrel
        brosLocations.pop(0)
    elif len(brosLocations) > 9:  # anything else is currently unidentified
        exit()                    # Theoretcially, we could clear the brosLocations
                                  # and search again anytime we don't have exactly 8
                                  # but this should be faster, and until there's a reason against, I'm doing this
    lastCannonLocation = (0,0)
    reset = False
    t = 0
    # start checking for readied barrels until all have been fired
    while len(brosLocations) > 0:
        try:
            haystack = getScreenshot()
        except:
            exit()
        res = cv2.matchTemplate(haystack,readyCannonNeedle,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        # keep looking for a cannon until found
        if len(loc[0]) == 0:
            if reset:
                reset = False
                print("Time taken to disappear: ", round(time()-t,5))
            continue
        # get cannon x,y coordinates
        cannonLocation = (0,0)
        for pt in zip(*loc[::-1]):
            cannonLocation = (pt[0], pt[1] + 10)
            break
        
        # keep looking if we found the same cannon we just found
        if abs(cannonLocation[0] - lastCannonLocation[0]) < 10 and abs(cannonLocation[1] - lastCannonLocation[1]) < 10:
            if not reset:
                reset = True
                t = time()
            continue
        
        

        # compare to the coordinates of where each brother was found
        # whichever is closes is the brother in the loaded barrel
        closestDistance = 1000000
        closestIndex = 0
        i = 0
        while i < len(brosLocations):
            # this distance formula should suffice, and should be a little faster
            distance = abs(cannonLocation[0] - brosLocations[i][0][0]) + abs(cannonLocation[1] - brosLocations[i][0][1])
            if distance < closestDistance:
                closestIndex = i
                closestDistance = distance
            i += 1

        bro = brosLocations.pop(closestIndex)

        # checking if the bro found was mario
        if bro[1]:
            key = 'x'
        else:  key = 'z'
        pydirectinput.press(key, _pause=False)
        lastCannonLocation = cannonLocation
        





