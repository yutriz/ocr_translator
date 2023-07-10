import cv2
from PIL import ImageGrab
import numpy as np

def screenshot():
    im = ImageGrab.grab()
    im_opencv = cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)
    return im_opencv

def get_roi_pos():
    screen_im = screenshot()
    min_x = 0        
    min_y = 0  
    width = 0
    height = 0      
    point1 = None
    point2 = None

    def on_mouse(event, x, y, flags, param):
        nonlocal point1, point2
        nonlocal min_x, min_y, width, height
        vis = screen_im.copy()
        if event == cv2.EVENT_LBUTTONDOWN:   
            point1 = (x, y)
            cv2.circle(vis, point1, 10, (0, 255, 0), 3)
            cv2.imshow('choosing roi', vis)
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):
            cv2.rectangle(vis, point1, (x, y), (255, 0, 0), 2)
            cv2.imshow('choosing roi', vis)
        elif event == cv2.EVENT_LBUTTONUP:         
            point2 = (x, y)
            cv2.rectangle(vis, point1, point2, (0, 0, 255), 2) 
            cv2.imshow('choosing roi', vis)
            min_x = min(point1[0], point2[0])     
            min_y = min(point1[1], point2[1])
            width = abs(point1[0] - point2[0])
            height = abs(point1[1] - point2[1])
        
    cv2.namedWindow('choosing roi', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('choosing roi', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback('choosing roi', on_mouse)
    cv2.waitKey(0)
    if min_x != 0 and min_y != 0:
        pos = (min_x, min_y, min_x+width, min_y+height)
        print(pos)
        return pos
    else:
        return None