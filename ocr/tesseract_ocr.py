import cv2
import pytesseract as tess
import numpy as np

def str_optim(src_txt):
    # multi-lines to  single line 
    lines_list = src_txt.splitlines()
    result = "".join(line.strip() for line in lines_list)
    # remove spaces 
    result = result.replace(" ", "")
    return result 


def dpi_strengthen(im):
    w = im.shape[0]
    h = im.shape[1]
    # screenshot is 96 dpi 
    magn = 300 / 96
    im = cv2.resize(im, (int(h*magn), int(w*magn)), cv2.INTER_AREA)
    return im

class ocr():
    def __init__(self, lang='jpn', preprc=False, gray_thresh=64, tess_config=r'--psm 6 --dpi 96'):
        self.lang = lang
        self.preprc = preprc
        self.gray_thresh = gray_thresh
        self.tess_config = tess_config

    # need tuning to get better perfomance
    def preprocess(self, img):
        # To Gray 
    
        enhanced_img = dpi_strengthen(img)
        kn = np.ones((3, 3), dtype=np.uint8)
        enhanced_img = cv2.erode(enhanced_img, kernel=kn)
        ret, enhanced_img = cv2.threshold(enhanced_img, self.gray_thresh, 255, cv2.THRESH_TOZERO)

        return enhanced_img
    
    def img2txt(self, img):
        if self.preprc:
            img = self.preprocess(img)
        text = tess.image_to_string(img, self.lang, config=self.tess_config)
        return str_optim(text) 
