import pyautogui
from PIL import Image, ImageDraw
import cv2
import numpy as np
from time import time

# Designed to run in vertical mode (for best visual effect)
# This is very general, taken from the mario ds
# Goomba storm at least won't need the top screen at all, and only a portion of the bottom screen

# Refers to the top screen of the DS
mainScreenScale=2.35
mainScreenX=652
mainScreenY=89
mainScreenWidth=615
mainScreenHeight=460

# Refers to the bottom screen of the DS
#subScreenScale=28/11
#subScreenX=652 # this is definitely right
#subScreenY=754
#subScreenWidth=424 # we only need to cover the distance between bowser and madam bloque
#subScreenHeight=318 # we likely can reduce this significantly
# maintain aspect raio. DS is 256/192

subScreenScale=3.75
subScreenX=960
subScreenY=182
subScreenWidth=960
subScreenHeight=720


runningGoombaSprites = []
goombaRunningArea = [ subScreenX, subScreenY, subScreenWidth, subScreenHeight]


def getScreenshot() -> Image:
    # Takes a screenshot based on which screen is required. 
    screenshot = pyautogui.screenshot(
        region= goombaRunningArea)
    #screenshot.show()
    size = screenshot.size
    scale = subScreenScale
    # Scales image to match original DS screen size. 
    screenshot = screenshot.resize((int(size[0] / scale), 
        int(size[1] / scale) ), Image.Resampling.NEAREST)
    return screenshot

def loadRunningGoombaSprites():
    goomba = Image.open(f"assets/Goomba Storm/goomba-face.png")
    runningGoombaSprites.append(goomba)

def localToGlobalPosition(position) -> tuple:
    # Converts a position on the subscreen to a position on the total screen. 
    scale = subScreenScale
    return (
        ( position[0] * scale ) + subScreenX,
        ( position[1] * scale ) + subScreenY
    )

screenshot = getScreenshot()
loadRunningGoombaSprites()

try: 
    stopWatch = time()
    location = pyautogui.locate(runningGoombaSprites[0], screenshot, confidence=.5)
    print("PyautoGui Locate Time:", round(time()-stopWatch,5))
except:
    location = None
print(location)
if location is not None:
    # 3. Convert to OpenCV format (NumPy array)
    screenshot_np = np.array(screenshot)
    
    # Convert RGB to BGR for OpenCV
    screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    
    # 4. Draw the rectangle
    # The Box object contains (left, top, width, height)
    x, y, width, height = location
    cv2.rectangle(screenshot_cv, (x, y), (x + width, y + height), (0, 0, 255), 2) # Red box, 2 pixels thick
    # 5. Display the image
    cv2.imshow("Located Image with Box", screenshot_cv)
    cv2.waitKey(0) # Wait for a key press to close the window
    print(localToGlobalPosition(location))
else: print("Needle not found")

template = cv2.cvtColor(np.array(runningGoombaSprites[0]), cv2.COLOR_BGR2GRAY)#cv2.imread("assets/Goomba Storm/goomba-running1.png")
img_rgb =cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
img_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)

w, h = template.shape[::-1]
stopWatch = time()
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.7
loc = np.where( res >= threshold)
print("OpenCV Locate Time:", round(time()-stopWatch,5))
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
 
cv2.imwrite('res.png',img_rgb)