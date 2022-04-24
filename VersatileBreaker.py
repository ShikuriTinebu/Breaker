# You can run the code using this link: https://tinyurl.com/Shikuri-Breaker




#Imports (This code was written on google collab, however import files in other code editors as necessary)
import numpy as np
import time
import cv2
import io
import PIL
from IPython.display import display, Javascript, Image, Audio
from base64 import b64decode, b64encode
from google.colab.output import eval_js
import html
from gtts import gTTS
import sys
import os

#Variables Assignment
num_of_faces = 0
num_of_pictures_taken = 0
minutes_running = 2
end_time = time.time() + 60 * minutes_running
face_cascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))

# function to convert the JavaScript object into an OpenCV image
def js2img(jsr):
  iwizbyts = b64decode(jsr.split(',')[1])
  jpgnp = np.frombuffer(iwizbyts, dtype=np.uint8)
  img = cv2.imdecode(jpgnp, flags=1)
  return img
def qb2byts(qbra):
  qbtablet = PIL.Image.fromarray(qbra, 'RGBA')
  strongEyes = io.BytesIO()
  qbtablet.save(strongEyes, format='png')
  qbbyts = 'data:image/png;base64,{}'.format((str(b64encode(strongEyes.getvalue()), 'utf-8')))
  return qbbyts


# Functions for starting Stream with Webcam
def video_frame(label, bbox):
  data = eval_js('stream_frame("{}", "{}")'.format(label, bbox))
  return data

def video_stream():
  js = Javascript('''
    var stream;
    var video;
    var rstrt;
    var iwizperiodic;
    var div = null;
    var unfinished = null;
    var stopp = false;
    var titleperiodic;

    function rmD() {
       stream.getVideoTracks()[0].stop();
       video.remove();
       div.remove();
       video = null;
       div = null;
       stream = null;
       iwizperiodic = null;
       rstrt = null;
       titleperiodic = null;
    }
    
    function animeFr() {
      if (!stopp) {
        window.requestAnimationFrame(animeFr);
      }
      if (unfinished) {
        var mark = "";
        if (!stopp) {
          rstrt.getContext('2d').drawImage(video, 0, 0, 640, 480);
          mark = rstrt.toDataURL('image/jpeg', 0.8)
        }
        var pl = unfinished;
        unfinished = null;
        pl(mark);
      }
    }
    
    async function crD() {
      if (div !== null) {
        return stream;
      }

      div = document.createElement('div');
      div.style.border = '2px solid black';
      div.style.padding = '3px';
      div.style.width = '100%';
      div.style.maxWidth = '600px';
      document.body.appendChild(div);
      
      const mohit = document.createElement('div');
      mohit.innerHTML = "<span>Status:</span>";
      titleperiodic = document.createElement('span');
      titleperiodic.innerText = 'No data';
      titleperiodic.style.fontWeight = 'bold';
      mohit.appendChild(titleperiodic);
      div.appendChild(mohit);
           
      video = document.createElement('video');
      video.style.display = 'block';
      video.width = div.clientWidth - 6;
      video.setAttribute('playsinline', '');
      video.onclick = () => { stopp = true; };
      stream = await navigator.mediaDevices.getUserMedia(
          {video: { facingMode: "environment"}});
      div.appendChild(video);

      iwizperiodic = document.createElement('img');
      iwizperiodic.style.position = 'absolute';
      iwizperiodic.style.zIndex = 1;
      iwizperiodic.onclick = () => { stopp = true; };
      div.appendChild(iwizperiodic);
      
      const instruction = document.createElement('div');
      instruction.innerHTML = 
          '<span style="color: red; font-weight: bold;">' +
          'Click on the video or this text to end</span>';
      div.appendChild(instruction);
      instruction.onclick = () => { stopp = true; };
      
      video.srcObject = stream;
      await video.play();

      rstrt = document.createElement('canvas');
      rstrt.width = 640; //video.videoWidth;
      rstrt.height = 480; //video.videoHeight;
      window.requestAnimationFrame(animeFr);
      
      return stream;
    }
    async function stream_frame(label, imgData) {
      if (stopp) {
        rmD();
        stopp = false;
        return '';
      }

      var preCreate = Date.now();
      stream = await crD();
      
      var preShow = Date.now();
      if (label != "") {
        titleperiodic.innerHTML = label;
      }
            
      if (imgData != "") {
        var videoRect = video.getClientRects()[0];
        iwizperiodic.style.top = videoRect.top + "px";
        iwizperiodic.style.left = videoRect.left + "px";
        iwizperiodic.style.width = videoRect.width + "px";
        iwizperiodic.style.height = videoRect.height + "px";
        iwizperiodic.src = imgData;
      }
      
      var preCapture = Date.now();
      var mark = await new Promise(function(resolve, reject) {
        unfinished = resolve;
      });
      stopp = false;
      
      return {'create': preShow - preCreate, 
              'show': preCapture - preShow, 
              'capture': Date.now() - preCapture,
              'img': mark};
    }
    ''')

  display(js)
  
#Python Speech Function
def speak(text: str):
    tts = gTTS(text=text, lang="en")
    filename = "sound.mp3"
    tts.save(filename)
    Audio(filename, autoplay = True)


#Start Code
video_stream()
label_html = 'Breaker is running...'
bbox = ''
count = 0 
while (time.time() < end_time):
    jsr = video_frame(label_html, bbox)
    if not jsr:
        break
    img = js2img(jsr["img"])
    qbra = np.zeros([480,640,4], dtype=np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    for (x,y,w,h) in faces:
      qbra = cv2.rectangle(qbra,(x,y),(x+w,y+h),(255,0,0),2)
      num_of_faces +=1
    qbra[:,:,3] = (qbra.max(axis = 2) > 0 ).astype(int) * 255
    qbbyts = qb2byts(qbra)
    bbox = qbbyts
    num_of_pictures_taken += 1

text = ""
if(num_of_faces > (num_of_pictures_taken*0.75)):
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
