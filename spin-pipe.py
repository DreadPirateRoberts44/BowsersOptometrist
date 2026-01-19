import pyautogui
from PIL import Image
import cv2
import numpy as np
import pydirectinput

# high score 55 A-Rank

subScreenScale=77/32
subScreenX=652
subScreenY=552
subScreenWidth=616
subScreenHeight=462

area = [subScreenX + 360,subScreenY-subScreenHeight + 40,75,200]

# Take a screenshot of the area the koopas are running through
# return image in format
def getScreenshot():
    # Takes a screenshot based on which screen is required. 
    # taken in RGB
    screenshot = pyautogui.screenshot(
        region= area)
    size = screenshot.size
    scale = subScreenScale
    # Scales image to match original DS screen size. 
    screenshot = screenshot.resize((int(size[0] / scale), 
        int(size[1] / scale) ), Image.Resampling.NEAREST)
    return np.array(screenshot) # updated to not convert to BGR, should save time

def testPipeDetectionExact():
    # in RGB
    haystack = getScreenshot()
    #img_rgb = cv2.cvtColor(haystack, cv2.COLOR_BGR2RGB)
    # Define the blue colour we want to find - remember OpenCV uses BGR ordering
    pipe = [8,181,255]

    # Get X and Y coordinates of all blue pixels
    Y, X = np.where(np.all(haystack==pipe,axis=2))
    i = 0
    while i < len(X):
        cv2.rectangle(haystack, (X[i],Y[i]), (X[i] + 1, Y[i] + 1), (0,0,255), 2)
        i += 1
    cv2.imshow('Pipe', haystack)
    cv2.waitKey(0)
    print(len(Y))


# one time operation
#testPipeDetectionExact()
#exit()

marioOnBottom = True
pipeColor = [8,181,255]
lastY = -1
spinning = False
emptyFrames = 0
midPoint = 100 / subScreenScale
verticalTolerance = 30 # changing this from 20 to 30 took our score from 18 to 55

while True:
    haystack = getScreenshot()
    Y, X = np.where(np.all(haystack==pipeColor,axis=2))
    Y.sort()
    # if we're not currently spinning and don't find the pipe, search again
    if not spinning and len(Y) == 0: continue
    # if we are spinning and don't find the pipe
    if len(Y) == 0: 
        # we've not found the pipe for too long
        # meaning the pipe has dropped and we need to jump
        if emptyFrames > 10:
            # press button of bro on bottom
            if marioOnBottom:
                key = 'x'
            else:  key = 'z'
            pydirectinput.press(key, _pause=False)
            emptyFrames = 0
            spinning = False # we also aren't spinning until we see the pipe again
        else: 
            emptyFrames += 1 # otherwise, incrment times we haven't seen the pipe
        continue
    # if we can see the pipe
    # assume it's spinning and reset empty frames, since they should be consecutive
    # (had issue with empty frames found between rounds)
    spinning = True
    emptyFrames = 0
    y = Y[0]
    # if the the pipe crossed halfway mark vertically, we flip which bro is on top
    # unless the gap between last and current is large, that means the pipe rotated 
    # to the other side
    if abs(y-lastY) < verticalTolerance and ((y > midPoint and lastY < midPoint) or (y < midPoint and lastY > midPoint)):
        marioOnBottom = not marioOnBottom
    # update last known y position
    lastY = y
