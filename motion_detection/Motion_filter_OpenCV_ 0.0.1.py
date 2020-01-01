import cv2
import os
import time
import glob
import os.path as path
import numpy as np

def mofilter():
    PHOTOS_DIR = 'PreCheck'
    CHECKED_PHOTOS_DIR = 'PostCheck'

    # mark faces on given image
    def mark_face(cascade, filepath):
        image = cv2.imread(filepath, cv2.IMREAD_COLOR)
        crop_img = image[25:720, 150:1280]
        faces = cascade.detectMultiScale(crop_img, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        return image

    def detect_face(cascade, filepath):
        image = cv2.imread(filepath, 0)
        crop_img = image[25:720, 150:1280]
        faces = cascade.detectMultiScale(crop_img)
        face = None
        
        for (x, y, w, h) in faces:
            if face is None or w * h > face[2] * face[3]:
                face = (x, y, w, h)

        if face is None:
            return filepath, 0, None
        else:
            return filepath, 1, face

    default_cascade = cv2.CascadeClassifier('C:\\Users\\sion_\\Desktop\\Python Projects\\Zero\\Visual\\Face_Recog\\haarcascade_frontalface_default.xml')

    # iterate all the photos and mark rectangles on detected faces
    filepaths = glob.glob(path.join(PHOTOS_DIR, '*.jpg'))
    for filepath in filepaths:
        marked_image = mark_face(default_cascade, filepath)
        fpath, count, region = detect_face(default_cascade, filepath)
        if region != None:
            cv2.imwrite(path.join(CHECKED_PHOTOS_DIR, path.basename(filepath)), marked_image)
            print('[*] Face Detected')
            try:
                os.remove(path.join(PHOTOS_DIR, path.basename(filepath)))
                print('PreCheck Copy Deleted!')
            except:
                pass
        elif region == None:
            try:
                os.remove(path.join(PHOTOS_DIR, path.basename(filepath)))
                print((filepath+' Deleted!'))
            except:
                pass
            try:
                os.remove(path.join(CHECKED_PHOTOS_DIR, path.basename(filepath)))
                print((filepath+' Deleted!'))
            except:
                pass
        else:
            print("Hmmmm...?")
            
mofilter()
