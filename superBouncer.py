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

area = [subScreenX,subScreenY-subScreenHeight,subScreenWidth,subScreenHeight * 2]

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
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


def testLuigiDetection():
    # in BGR
    haystack = getScreenshot()
    img_rgb = cv2.cvtColor(haystack, cv2.COLOR_BGR2RGB)
    lower_yellow = np.array([130, 220, 10])
    upper_yellow = np.array([135, 224, 20])
    mask = cv2.inRange(haystack, lower_yellow, upper_yellow)
    coordinates = cv2.findNonZero(mask)
    for point in coordinates:
        cv2.rectangle(img_rgb, (point[0][0],point[0][1]), (point[0][0] + 1, point[0][1] + 1), (0,0,255), 2)
    cv2.imshow('Weegi', img_rgb)
    cv2.waitKey(0)


# one time operation
testLuigiDetection()
