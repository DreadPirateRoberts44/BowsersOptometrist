import pyautogui
from PIL import Image
import cv2
import numpy as np
from time import sleep,time
import pydirectinput

# highscore 24 B-Rank
#Hay Time 2.3855
#Button Time 10.41185


# Designed to run in vertical mode (for best visual effect)
# This is very general, taken from the mario ds
# koopa corps at least won't need the top screen at all, and only a portion of the bottom screen
subScreenScale=77/32
subScreenX=652
subScreenY=552
subScreenWidth=616
subScreenHeight=462

area = [subScreenX + 357,subScreenY-subScreenHeight,200,687]

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

# if we switch back to this method
# agree on color format
def testLuigiDetectionMask():
    # currently assumes BGR, which is wrong
    haystack = getScreenshot()
    img_rgb = cv2.cvtColor(haystack, cv2.COLOR_BGR2RGB)
    t = time()
    lower_yellow = np.array([130, 220, 10])
    upper_yellow = np.array([135, 224, 20])
    mask = cv2.inRange(haystack, lower_yellow, upper_yellow)
    coordinates = cv2.findNonZero(mask)
    for point in coordinates:
        cv2.rectangle(img_rgb, (point[0][0],point[0][1]), (point[0][0] + 1, point[0][1] + 1), (0,0,255), 2)
    print("Time to find with Mask: ", round(time()-t,5))
    cv2.imshow('Weegi', img_rgb)
    cv2.waitKey(0)

def testLuigiDetectionExact():
    # in RGB
    haystack = getScreenshot()
    #img_rgb = cv2.cvtColor(haystack, cv2.COLOR_BGR2RGB)
    t = time()
    # Define the blue colour we want to find - remember OpenCV uses BGR ordering
    luigi = [16,222,132]

    # Get X and Y coordinates of all blue pixels
    Y, X = np.where(np.all(haystack==luigi,axis=2))
    i = 0
    while i < len(X):
        cv2.rectangle(haystack, (X[i],Y[i]), (X[i] + 1, Y[i] + 1), (0,0,255), 2)
        i += 1
    print("Time to find with Exact: ", round(time()-t,5))
    x = round(haystack.shape[1] / 2) + 5
    print(x)
    cv2.rectangle(haystack, (x,100), (x + 1, 255), (0,0,255), 2)
    cv2.imshow('Weegi', haystack)
    cv2.waitKey(0)

# one time operation
#testLuigiDetectionMask()
#estLuigiDetectionExact()
#exit()

luigiColor = [16,222,132]
midPoint = 47 #(screenshot width / scale factor) / 2 = 42, offset 5 to the right, luigi's green isn't his center
midPointRange = 0 #15

jumpButtonPressHeight = round((subScreenY - 150) / subScreenScale)

pydirectinput.PAUSE = 0.06


# start game
""" This is for completions sake. It's a pain to rely on during dev
pyautogui.click(round(subScreenX + subScreenWidth/2), round(subScreenY + subScreenHeight/2))
pydirectinput.press('x', _pause=False)
sleep(3)
pydirectinput.press('x', _pause=False)
"""

hayTime = 0
buttonTime = 0
luigiFound = False

try:
    while True:
        t = time()
        haystack = getScreenshot()
        # Get X and Y coordinates for colors that match luigi
        Y, X = np.where(np.all(haystack==luigiColor,axis=2))
        if len(X) == 0:
            continue
            
        X.sort()
        x = X[round(len(X)/2)]

        hayTime += time() - t

        t = time()

        if Y[0] >= jumpButtonPressHeight:
            key = 'z'
            print(Y[0])
        elif x < (midPoint - midPointRange):
            key = "right"
            print("Pressed Right")
        elif x > (midPoint + midPointRange):
            key = "left"
            print("Pressed Left")
        pydirectinput.press(key, _pause=False)
        buttonTime += time() - t
        if key =='z':
            sleep(.42) #.38 if y offset is 100
            pydirectinput.press('x', _pause=False)
            luigiFound = False

except:
    print("Hay Time", round(hayTime,5))
    print("Button Time", round(buttonTime,5))
