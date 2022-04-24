import cv2
import time
import numpy as np
from pandas import notnull
from adafruit_servokit import Servokit
from IPython.display import display, Javascript, Image, Audio
from gtts import gTTS
import sys
import os

#Camera size constants
dW=224
dH=224
flip=2
#Servokit pan and tilt measurements
kit = Servokit(channels=16)
p = 90
t = 90
kit.servo[0].angle=p
kit.servo[1].angle=t
#Time measurements
minutes_running = 20
end_time = time.time() + 60 * minutes_running

#Uncomment These next Two Line for Pi Camera
#camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=224, height=224, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#cam= cv2.VideoCapture(camSet)
 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
#cam=cv2.VideoCapture(0)

#Cascade Face Download: https://github.com/opencv/opencv/blob/27c15bed601b9dd8e808d0fc1958001a6d123299/data/haarcascades/haarcascade_frontalface_default.xml
#Cascade Eye Download: https://github.com/opencv/opencv/blob/27c15bed601b9dd8e808d0fc1958001a6d123299/data/haarcascades/haarcascade_eye.xml

face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_eye.xml')

facesSpotted = 0
totalFaces = 0

#Main code for running camera face recognition
while (time.time() < end_time) < 1200:
    ret, frame = cam.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    totalFaces += 1
    #Draws rectangles around the face so user knows they are being detected.
    for (x, y, w, h) in faces:
        facesSpotted+=1
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
        xc = x+(w/2)
        yc = y+ (h/2)
        ep = xc - (dW/2)
        et = yc - (dH/2)
        if abs(ep) >15 :
            p = p - (ep/50)
        if abs(et) > 15 :
            t = t - (et/50)
        if(p > 180):
            pan = 180 
        if(p < 0):
            p = 0
        if(t >180):
            t = 180
        if(t< 0):
            t = 0
        kit.servo[0].angle=p
        kit.servo[1].angle=t
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for(ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ew+ex, eh + ey), (255, 0, 0), 2)
        break
    cv2.imshow('Breaker',frame)
    if cv2.waitKey(1)==ord('q'):
        break
#Results Analysis  
text = ""
if(facesSpotted > (totalFaces*0.75)):
  t2 = "You need to take a break for " + str(minutes_running*0.25) + " minutes"
  text = "It's time to get up and take a break!"
  print(text)
  print(t2)
else:
  text = "You can continue on with your buisness"
  print(text)
tts = gTTS(text=text, lang="en")
filename = "sound.mp3"
tts.save(filename)
Audio(filename, autoplay = True)

cam.release()
cv2.destroyAllWindows() 
