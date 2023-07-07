from trans_api.bd_api import bd_translator
from trans_api.ali_api import ali_translator
from ocr.blocks import multi_blocks
from ocr.tesseract_ocr import ocr
import keyboard
import os

bd_appid  = os.getenv('BD_APPID')
bd_appkey = os.getenv('BD_APPID_KEY')
ali_keyid = os.getenv('ALI_KEYID') 
ali_keyid_secret = os.getenv('ALI_KEYID_SECRET') 

def updated_snippers_images(m_blocks):
    images = list()
    for index in range(0, m_blocks.snippers_num):
        im = m_blocks.snippers_images()[index]
        images.append(im)
    return images

def main():
    #translator = bd_translator(from_lang='jp', to_lang='zh',\
    #                           bd_appid=bd_appid,\
    #                           bd_appkey=bd_appkey) 
    
    translator = ali_translator(key_id=ali_keyid, key_id_secret=ali_keyid_secret)
    text_zones = multi_blocks()
    tess_ocr = ocr(gray_thresh=64)
    #tess_ocr = ocr(preprc=True, tess_config=r'--dpi 300 --psm 6')

    while True:
        text_images = updated_snippers_images(text_zones) 
        ocr_detection = list()
        for index in range(0, text_zones.snippers_num):
            block_detection = tess_ocr.img2txt(text_images[index]) 
            if block_detection == "" or block_detection == None:
                block_detection = "no text detected"
            ocr_detection.append(block_detection)
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


        
    
