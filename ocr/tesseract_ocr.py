import cv2
import pytesseract as tess

def to_single(multilines_text):
    lines_list = multilines_text.splitlines()
    result = "".join(line.strip() for line in lines_list)
    return result 

class ocr():
    def __init__(self, lang='jpn', gray_thresh=64):
        self.lang = lang
        self.gray_thresh = gray_thresh

    # need tuning to get better perfomance
    def preprocess(self, img):
        # To Gray 
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, enhanced_img = cv2.threshold(gray_img, self.gray_thresh, 255, cv2.THRESH_TOZERO)
        return enhanced_img
    
    def img2txt(self, img):
        #while True:
        text = tess.image_to_string(self.preprocess(img), self.lang)
            #if text != "":
            #    break
        return to_single(text) 
