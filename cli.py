from api.bd_api import bd_translator
from api.ali_api import ali_translator
from ocr.blocks import multi_blocks
from ocr.tesseract_ocr import ocr
import keyboard
import os
import cv2 
import argparse

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

parser = argparse.ArgumentParser(description='Ocr Translator CLI Mode')
parser.add_argument('--mode', type=str, default='blocks', help='Mode Choose: blocks/img')
parser.add_argument('--api', type=str, default='ali', help='Translator Api: ali/bd')
parser.add_argument('--img', type=str, help='img')
parser.add_argument('--tess_config', type=str, help='Tesseract Config')
parser.add_argument('--log', help="Write Log File at /d/.tran_log.txt", action='store_true')

args = parser.parse_args()

def main():

    # translator
    if args.api == 'bd':
        translator = bd_translator(bd_appid=bd_appid, bd_appkey=bd_appkey, write_log=args.log)
    elif args.api == 'ali':
        translator = ali_translator(key_id=ali_keyid, key_id_secret=ali_keyid_secret, write_log=args.log)
    
    # ocr 
    tess_ocr = ocr()
 
    # mode choose 
    if args.mode == 'blocks':
        text_zones = multi_blocks()
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
    elif args.mode == 'img':
        img = cv2.imread(args.img)
        detection = tess_ocr.img2txt(img)
        translation = translator.query(detection)
        print(translation[0])

if __name__ == "__main__":
    main()


        
    
