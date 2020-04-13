import numpy as np
import cv2 as cv
import pyautogui
import time

def getCnts(img, arr):
    mask = cv.inRange(img, arr[0][0], arr[0][1])
    for bound in arr:
        if bound is not arr[0]:
            low = bound[0]
            high = bound[1]
            bound_mask = cv.inRange(img, low, high)
            mask = cv.add(mask, bound_mask)
    cnts, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    return cnts

def aimbot(cnts, region, shift_right, shift_down):
    for cnt in cnts:
        M = cv.moments(cnt)
        if M['m00'] != 0:
            centroid_x = int(M['m10']/M['m00'])
            centroid_y = int(M['m01']/M['m00'])

            if centroid_x < 1200 - shift_down and centroid_y > shift_down * -1:
                pyautogui.click(region[0] + centroid_x + shift_right, region[1] + centroid_y + shift_down)

def explore():
    pyautogui.keyDown('w')
    time.sleep(.5)
    pyautogui.keyDown('d')
    pyautogui.keyUp('w')
    time.sleep(.5)
    pyautogui.keyDown('s')
    pyautogui.keyUp('d')
    time.sleep(.5)
    pyautogui.keyDown('a')
    pyautogui.keyUp('s')
