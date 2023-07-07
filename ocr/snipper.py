import win32api, win32con, win32gui, win32ui
import numpy as np
import cv2
from .roi import get_roi_pos

def get_window_pos(handle):
    if win32gui.IsWindow(handle) \
    and win32gui.IsWindowEnabled(handle) \
    and win32gui.IsWindowVisible(handle):   
        return win32gui.GetWindowRect(handle)
    else:
        print("Error, invalid handle.")
        return None
 
def get_window_handle(keyword):
    """
    results be like ['handle_0', 'title_0', 'handle_1', 'title_1', ...]
    """
    windows_list = []
    results = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), windows_list)
    for window in windows_list:
        classname = win32gui.GetClassName(window)
        title = win32gui.GetWindowText(window)
        if title.find(keyword) != -1:
            results.append(window)
            results.append(title)
            print(f'handle:{window} title:{title} classname:{classname}')
    return results
 

class snipper():
    # don't use any methods except get_snip
    # no images until get_snip()
    # Mode: block / window
    def __init__(self, mode='block', window_title_kw=''):
        self.mode = mode
        self.window_title_keyword = window_title_kw
        monitor_specs = win32api.EnumDisplayMonitors(None,None) 
        self.monitor_w = monitor_specs[0][2][2]
        self.monitor_h = monitor_specs[0][2][3]
        if self.mode == 'window':
            self.get_window()
        elif self.mode == 'block':
            self.get_block()
  

    def get_snip(self):
        """
        pos = [x1, y1, x2, y2]
        output:
            image in opencv
        """
        # why -16 ? https://www.cnblogs.com/octoberkey/p/14917087.html
        if self.mode == 'window':
            w = self.snip_pos[2] - self.snip_pos[0] - 16 
            h = self.snip_pos[3] - self.snip_pos[1] - 16 
            sp = (self.snip_pos[0]+8, self.snip_pos[1]+8)
        elif self.mode == 'block':
            w = self.snip_pos[2] - self.snip_pos[0]  
            h = self.snip_pos[3] - self.snip_pos[1] 
            sp = (self.snip_pos[0], self.snip_pos[1])

        hwnDC = win32gui.GetWindowDC(0)
        # mfc = Miscrosoft Foundation Classes
        mfcDC = win32ui.CreateDCFromHandle(hwnDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((0,0), (w, h), mfcDC, sp, win32con.SRCCOPY)
        signedIntsArray = saveBitMap.GetBitmapBits(True)
        im_opencv = np.frombuffer(signedIntsArray, dtype = 'uint8')
        im_opencv.shape = (h, w, 4)
        im = cv2.cvtColor(im_opencv, cv2.COLOR_RGBA2RGB)

        cv2.imwrite("snip.png", im)

        return im

    def get_window(self):
        keyword = self.window_title_keyword
        window_options = get_window_handle(keyword)
        if len(window_options)/2 == 1.0:
            handle = window_options[0]
        else:
            handle = input('enter the handle number:')
        window_pos = get_window_pos(handle)
        self.snip_pos = window_pos



    def get_block(self):
        block_pos = get_roi_pos()
        if block_pos != None:
            self.snip_pos = block_pos


        
