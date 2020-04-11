import pyautogui, logging, time
import numpy as np
import cv2 as cv
from PIL import ImageGrab

logging.basicConfig(level=logging.WARNING, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#logging.disable(logging.DEBUG) # uncomment to block debug log messages

#SOLUTION: https://stackoverflow.com/questions/35325042/python-logging-disable-logging-from-imported-modules/35325280

import os

# Global variables
GAME_REGION = ()

def main():
    logger.debug('Program Started. Press Ctrl-C to abort at any time.')
    logger.debug('To interrupt mouse movement, move mouse to upper left corner.')
    getGameRegion()
    play()

def imPath(filename):
    return os.path.join('images', filename)

def getGameRegion():
    global GAME_REGION

    # identify the identifier
    logger.debug('Finding game region...')
    region = pyautogui.locateOnScreen(imPath('player_icon.png'), confidence=.9)
    if region is None:
        raise Exception('Could not find game on screen. Is the game visible?')

    # calculate game region
    topLeftX = region[0]
    topLeftY = region[1]
    GAME_REGION = (topLeftX - 1104, topLeftY - 295, 1200, 900)
    logger.debug('Game region found: %s' % (GAME_REGION,))

def play():
    logger.debug('Looking for enemies...')

    lower_green = (0, 254, 16)
    upper_green = (1, 255, 17)
    lower_orange = (15, 127, 254)
    upper_orange = (16, 128, 255)
    lower_red = (15, 15, 223)
    upper_red = (16, 16, 224)

    while True:
        screenshot = ImageGrab.grab(bbox=GAME_REGION)
        screenshot = np.array(screenshot)
        screenshot = screenshot[:, :, ::-1].copy()

        mask_green = cv.inRange(screenshot, lower_green, upper_green)
        mask_orange = cv.inRange(screenshot, lower_orange, upper_orange)
        mask_red = cv.inRange(screenshot, lower_red, upper_red)
        mask = cv.add(mask_green, mask_orange)
        mask = cv.add(mask, mask_red)

        cnt, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

        for rect in cnt:
            M = cv.moments(rect)
            if M['m00'] != 0:
                centroid_x = int(M['m10']/M['m00'])
                centroid_y = int(M['m01']/M['m00'])

                if centroid_x < 1190 and centroid_y > 30:
                    pyautogui.click(GAME_REGION[0] + centroid_x + 10, GAME_REGION[1] + centroid_y - 30)

if __name__ == '__main__':
    main()

#tutorial picture is shifted one pixel left?
