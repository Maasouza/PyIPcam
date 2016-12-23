import cv2
import numpy as np
import urllib
import time
"""
http://192.168.1.10:81/videostream.cgi
"""

face_cascade = cv2.CascadeClassifier('cascade\haarcascade_frontalface_default.xml')


stream=urllib.urlopen('http://192.168.1.10:81/videostream.cgi?user=admin&pwd=admin')

bytes=''

last = 0

while True:
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
        if(len(faces)!=0 and last+10<time.time()):
            last = time.time()
            h = time.strftime("%X")
            d = time.strftime("%x")
            cv2.imwrite(h+"_"+d+'.png',frame)
        cv2.imshow('camera',frame)
        if cv2.waitKey(1) ==27:
            exit(0)