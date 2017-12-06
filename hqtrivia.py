import numpy as np
import cv2
import subprocess
from PIL import Image
import sys, os
import pyocr
import pyocr.builders
import Searcher
import time
#w 1324 h 2222
q_box_scale = np.array([150/1324,400/2222,1187/1324,850/2222])
a_box_scale = np.array([150/1324,900/2222,1187/1324,1450/2222])

class HQTrivia:
    def __init__(self):
        # initialize OCR
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print("No OCR tool found")
            sys.exit(1)
        self.tool = tools[0]
        print("Will use tool '%s'" % (self.tool.get_name()))
        langs = self.tool.get_available_languages()
        print("Available languages: %s" % ", ".join(langs))
        self.lang = langs[0]
        print("Will use lang '%s'" % (self.lang))
        # initialize searcher class
        self.searcher = Searcher.Searcher()

    def main_loop(self,flip=False):
        while(True):
            input('Press Enter to capture...')
            print('capture!')
            # try:
            #     os.remove('./screenshot.png')
            # except:
            #     pass
            # subprocess.call(['./iphone_screenshot.sh'])
            # time.sleep(0.5)
            try:
                screenshot = Image.open("./screenshot.png").convert('L') #convert to greyscale
            except:
                print('Screenshot not captured!')
                continue

            screen_w,screen_h = screenshot.size
            screen_box = np.array([screen_w,screen_h,screen_w,screen_h])
            print(screen_w)
            print(screen_h)
            q_img = screenshot.crop(tuple(screen_box*q_box_scale))
            q_img_arr = np.asarray(q_img)
            q_img_arr = cv2.medianBlur(q_img_arr,3)
            ret,q_img_arr = cv2.threshold(q_img_arr,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            cv2.imwrite('q_img.png',q_img_arr)
            q_img = Image.fromarray(q_img_arr)

            a_img = screenshot.crop(tuple(screen_box*a_box_scale))
            a_img_arr = np.asarray(a_img)
            a_img_arr = cv2.medianBlur(a_img_arr,3)
            ret,a_img_arr = cv2.threshold(a_img_arr,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            cv2.imwrite('a_img.png',a_img_arr)
            a_img = Image.fromarray(a_img_arr)

            txt = self.tool.image_to_string(
                q_img,
                lang=self.lang,
                builder=pyocr.builders.TextBuilder()
            )
            anstxt = self.tool.image_to_string(
                a_img,
                lang=self.lang,
                builder=pyocr.builders.TextBuilder()
            )
            query = txt.replace('\n',' ').rstrip()
            print(query)
            anstxt = anstxt.rstrip().split('\n')
            anstxt = list(filter(lambda x: x.rstrip()!='', anstxt))
            print(anstxt)
            try:
                pass
                #self.searcher.search_answer(query,anstxt)
            except:
                pass

if __name__ == '__main__':
    hqt = HQTrivia()
    hqt.main_loop()
