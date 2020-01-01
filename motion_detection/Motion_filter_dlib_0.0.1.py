import cv2
import os
import time
import glob
import os.path as path
import numpy as np
import dlib

def mofilter():
    PHOTOS_DIR = 'PreCheck'
    CHECKED_PHOTOS_DIR = 'PostCheck'
    
    def draw_border(filepath, pt1, pt2, color, thickness, r, d):
        x1, y1 = pt1
        x2, y2 = pt2

        # Top left drawing
        cv2.line(filepath, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
        cv2.line(filepath, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
        cv2.ellipse(filepath, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

        # Top right drawing
        cv2.line(filepath, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
        cv2.line(filepath, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
        cv2.ellipse(filepath, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)

        # Bottom left drawing
        cv2.line(filepath, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
        cv2.line(filepath, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
        cv2.ellipse(filepath, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

        # Bottom right drawing
        cv2.line(filepath, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
        cv2.line(filepath, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
        cv2.ellipse(filepath, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)

    # iterate all the photos and mark rectangles on detected faces
    filepaths = glob.glob(path.join(PHOTOS_DIR, '*.jpg'))
    for filepath in filepaths:
        image = cv2.imread(filepath, cv2.IMREAD_COLOR)
        crop_img = image[25:720, 150:1280]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        overlay = image.copy()
        output = image.copy()
        alpha  = 0.5
        detector = dlib.get_frontal_face_detector()
        face_rects = detector(gray, 0)
        for i, d in enumerate(face_rects):
            x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
            draw_border(overlay, (x1, y1), (x2, y2), (50, 255, 0), 2, 10, 10)

        var = 'rectangles[]'
        
        if str(face_rects) != str(var):
            cv2.imwrite(path.join(CHECKED_PHOTOS_DIR, path.basename(filepath)), overlay)
            print('[*] Face Detected')
            try:
                os.remove(path.join(PHOTOS_DIR, path.basename(filepath)))
                print('PreCheck Copy Deleted!')
            except:
                pass
        elif str(face_rects) == str(var):
            try:
                os.remove(path.join(PHOTOS_DIR, path.basename(filepath)))
                print(('---> '+filepath+' Deleted!'))
            except:
                pass
            try:
                os.remove(path.join(CHECKED_PHOTOS_DIR, path.basename(filepath)))
                print(('---> '+filepath+' Deleted!'))
            except:
                pass
        else:
            print("Hmmmm...?")

mofilter()
