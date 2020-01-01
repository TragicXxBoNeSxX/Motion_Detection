import time as t
import cv2
import dlib
import datetime
import numpy as np
import os
import glob
import os.path as path

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while(cap.isOpened()):
  current_frame = cap.read()[1]
  previous_frame = cap.read(current_frame-1)[1]
  
  current_frame_gray = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
  previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
  frame_diff = cv2.absdiff(current_frame_gray, previous_frame_gray)

  # Change value depending on: Resolution, Quality, etc..
  # 795000 works well for 720p
  if cv2.countNonZero(frame_diff) < 795000:
    text = "Standby"
    cv2.putText(current_frame, "Camera Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(current_frame, datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p"), (10, current_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)


  if cv2.countNonZero(frame_diff) > 795000:
    text = "Motion Detected"
    cv2.putText(current_frame, "Camera Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(current_frame, datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p"), (10, current_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.imwrite(datetime.datetime.now().strftime('PreCheck/'+'%m-%d-%Y_%Hh%Mm%Ss') + '.jpg', current_frame)
    print("Image Captured!")

  cv2.namedWindow('Motion Detection', cv2.WND_PROP_FULLSCREEN)
  cv2.setWindowProperty('Motion Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
  cv2.imshow('Motion Detection', current_frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()

def find_uglies():
    for file_type in ['PreCheck']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('Uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('Uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)

                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly, question).any()):
                        print('Ugly Image')
                        print(current_image_path)
                        os.remove(current_image_path)

                except Exception as e:
                    print((str(e)))

def filter_img():
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

find_uglies()
filter_img()

