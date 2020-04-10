import pyautogui, logging, cv2, time

logging.basicConfig(level=logging.WARNING, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#logging.disable(logging.DEBUG) # uncomment to block debug log messages

#SOLUTION: https://stackoverflow.com/questions/35325042/python-logging-disable-logging-from-imported-modules/35325280

import os

# Global variables
GAME_REGION = ()

class Enemy():
    def __init__(self, name, var, coords):
        self.name = name
        self.var = var
        self.coords = None

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
    region = pyautogui.locateOnScreen(imPath('player_icon.png'), confidence=.95)
    if region is None:
        raise Exception('Could not find game on screen. Is the game visible?')

    # calculate game region
    topLeftX = region[0]
    topLeftY = region[1]
    GAME_REGION = (topLeftX - 1104, topLeftY - 295, 1200, 900)
    logger.debug('Game region found: %s' % (GAME_REGION,))

def play():
    logger.debug('Looking for enemies...')
    hobbit_archer = Enemy('Hobbit Archer', 'hobbit_archer', None)
    snake = Enemy('Snake', 'snake', None)
    pirate = Enemy('Pirate', 'pirate', None)
    bandit = Enemy('Bandit', 'bandit', None)

    enemies = [hobbit_archer, snake, pirate, bandit]
    while True:
        for i in range(len(enemies)):
            enemies[i].coords = pyautogui.locateCenterOnScreen(imPath('%s.png' % enemies[i].var), region=GAME_REGION, confidence=.65)
            if enemies[i].coords is not None:
                logger.debug('Enemy found: ' + enemies[i].name + ' at %s' % (enemies[i].coords,))
                pyautogui.mouseDown(enemies[i].coords)
                time.sleep(1)
                pyautogui.mouseUp()

if __name__ == '__main__':
    main()

#tutorial picture is shifted one pixel left?
