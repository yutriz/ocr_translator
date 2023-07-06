from trans_api.bd_api import bd_translator
from ocr.blocks import multi_blocks
from ocr.tesseract_ocr import ocr
import keyboard

def updated_snippers_images(m_blocks):
    images = list()
    for index in range(0, m_blocks.snippers_num):
        im = m_blocks.snippers_images()[index]
        images.append(im)
    return images

def main():
    
    bd_appid = ''
    bd_appkey = ''
    translator = bd_translator(from_lang='jp', to_lang='zh',\
                               bd_appid=bd_appid,\
                               bd_appkey=bd_appkey) 
    text_zones = multi_blocks()
    tess_ocr = ocr(gray_thresh=64)

    while True:
        text_images = updated_snippers_images(text_zones) 
        ocr_detection = list()
        for index in range(0, text_zones.snippers_num):
            ocr_detection.append(tess_ocr.img2txt(text_images[index]))
            query_text = "\n".join(ocr_detection)
        #print(f'query text is \n{query_text}')
        print("*************************************")
        translation = translator.query(query_text)
        for index in range(0, text_zones.snippers_num):
            print(f'Block_{index+1}:\n{translation[index]}\n')
        # c for continue 
        keyboard.wait('c')


if __name__ == "__main__":
    main()


        
    
