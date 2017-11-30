#import numpy as np
import cv2
from PIL import Image
import sys
import pyocr
import pyocr.builders
import Searcher

class HQTrivia:
#    cam_size = (1280, 720)
    cam_size = (1920, 1080)
    question_size = (int(700),int(280))
    answer_size = (int(650),int(350))
    question_rect = ((int(cam_size[0]/2-question_size[0]/2+70),
                     int(cam_size[1]/2-question_size[1]/2)),
                    (int(cam_size[0]/2+question_size[0]/2+70),
                     int(cam_size[1]/2+question_size[1]/2)))
    answer_rect  = ((int(cam_size[0]/2-answer_size[0]/2+70),
                     int(cam_size[1]/2-answer_size[1]/2 + 350)),
                    (int(cam_size[0]/2+answer_size[0]/2+70),
                     int(cam_size[1]/2+answer_size[1]/2)+ 350))

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
        cap = cv2.VideoCapture(1)
        #cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)#doesn't seem to work?
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #print(gray.shape)
            if flip:
                gray_flip = cv2.flip(gray,1)
            else:
                gray_flip = gray
            cv2.rectangle(gray_flip, self.question_rect[0], self.question_rect[1], (0,0,0))
            cv2.rectangle(gray_flip, self.answer_rect[0], self.answer_rect[1], (0,0,0))
            # Display the resulting frame
            cv2.imshow('frame',gray_flip)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                print('capture!')
                q_p1 = self.question_rect[0]
                q_p2 = self.question_rect[1]
                q_img = gray[q_p1[1]:q_p2[1], q_p1[0]:q_p2[0]]
                ans_p1 = self.answer_rect[0]
                ans_p2 = self.answer_rect[1]
                ans_img = gray[ans_p1[1]:ans_p2[1], ans_p1[0]:ans_p2[0]]
                #q_img = cv2.medianBlur(q_img,5)
                #q_img = cv2.GaussianBlur(q_img,(3,3),0)
                ret,q_img = cv2.threshold(q_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                #ans_img = cv2.GaussianBlur(ans_img,(5,5),0)
                #ret,ans_img = cv2.threshold(ans_img,200,255,cv2.THRESH_BINARY)
                ret,ans_img = cv2.threshold(ans_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                #ans_img = cv2.adaptiveThreshold(ans_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
                #q_img = cv2.adaptiveThreshold(q_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
                cv2.imwrite('test.png',q_img)
                cv2.imwrite('test_ans.png',ans_img)
                txt = self.tool.image_to_string(
                    Image.fromarray(q_img),
                    lang=self.lang,
                    builder=pyocr.builders.TextBuilder()
                )
                anstxt = self.tool.image_to_string(
                    Image.fromarray(ans_img),
                    lang=self.lang,
                    builder=pyocr.builders.TextBuilder()
                )
                query = txt.replace('\n',' ').rstrip()
                print(query)
                anstxt = anstxt.rstrip().split('\n')
                anstxt = list(filter(lambda x: x.rstrip()!='', anstxt))
                print(anstxt)
                try:
                    self.searcher.search_answer(query,anstxt)
                except:
                    pass
            elif key == ord('q'):
                break
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    hqt = HQTrivia()
    hqt.main_loop()
