import pyautogui, logging, time
import numpy as np
import cv2 as cv
from PIL import ImageGrab
from objectidentification import *

logging.basicConfig(level=logging.WARNING, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#logging.disable(logging.DEBUG) # uncomment to block debug log messages

#SOLUTION: https://stackoverflow.com/questions/35325042/python-logging-disable-logging-from-imported-modules/35325280

import os

# Global variables
GAME_REGION = ()
PLAYER_CENTER = ()
GREEN_HEALTH = [(0, 254, 16), (1, 255, 17)]
ORANGE_HEALTH = [(15, 127, 254), (16, 128, 255)]
RED_HEALTH = [(15, 15, 223), (16, 16, 224)]
HEALTH = [GREEN_HEALTH, ORANGE_HEALTH, RED_HEALTH]
GHOST_GOD = [[(242, 242, 242), (243, 243, 243)], [(160, 160, 160), (161, 161, 161)]]

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
    gameRegionTopLeftX = topLeftX - 1104
    gameRegionTopLeftY = topLeftY - 295
    GAME_REGION = (gameRegionTopLeftX, gameRegionTopLeftY, gameRegionTopLeftX + 1200, gameRegionTopLeftY + 900)
    PLAYER_CENTER = (topLeftX + 455, topLeftY + 460)
    logger.debug('Game region found: %s' % (GAME_REGION,))

def play():
    global HEALTH

    logger.debug('Looking for enemies...')

    while True:
        screenshot = ImageGrab.grab(bbox=GAME_REGION)
        print(screenshot)
        screenshot = np.array(screenshot)
        #print(screenshot)
        screenshot = screenshot[:, :, ::-1].copy()

        healthCnts = getCnts(screenshot, HEALTH)
        aimbot(healthCnts, GAME_REGION, 10, -30)
        #explore()

if __name__ == '__main__':
    main()

#tutorial picture is shifted one pixel left?
