import socket
import cv2
import os
import subprocess
from subprocess import Popen, PIPE, STDOUT
import time



#import RPi.GPIO as GPIO

# check the conditions in the garden with light sensor

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(4,GPIO.IN)
#lights = 0;

#while True:
        #if GPIO.input(4)== 1:
                #lights = 1
        #if GPIO.imput (4)==0:
                #lights = 0

# take image with webcam

# capture image from webcam, change directory to (densecap)pics folder, write image to folder
vidcap = cv2.VideoCapture()
vidcap.open(0)                 # 1 for external 0 for internal cam
retval, image = vidcap.retrieve()
vidcap.release()

face_file_name = "haikucam.jpg"
os.chdir('/Users/rollasoul/densecap/imgs/pics')
cv2.imwrite(face_file_name, image)

# save record of image
#time2 = time.time()
#filename = "/Users/rollasoul/densecap/imgs/saved/%sa-image.jpg"%time2
#cv2.imwrite(filename, image)

# send image and light sensor input
s = socket.socket()
host = "147.75.203.157"
port = 12345
s.connect((host, port))
f=open ("haikucam.jpg", "rb") 
l = f.read(4096)
while (l):
      s.send(l)
      l = f.read(4096)
time.sleep(3)
print "image sent"   
s.close()                # Close the connection

    # wait for densecap & rnn lib to handwrite haiku and create image
print "done"
time.sleep(3)

s = socket.socket()
host = "147.75.203.157"
port = 12345
s.connect((host, port))

print "waiting for image"

while True:
        i=1
        f = open('imageToSave'+ str(i)+".png",'wb')
        i=i+1
        while (True):
        # receive and write file
                l = s.recv(1024)
                while (l):
                        f.write(l)
                        l = s.recv(1024)
                        print "file received"
                        s.send("file received")
                s.close()
                f.close()
                break

# run processing sketch to convert png to bmp
subprocess.call('processing-java --sketch=/Users/rollasoul/Documents/Arduino/libraries/Adafruit-Thermal/processing/bitmapImageConvert --run', shell=True)

# copy processing sketch into arduino file library, compile & send to arduino sketch
shutil.copy('/Users/rollasoul/densecap/imageToSave.h', '/Users/rollasoul/densecap/A_printertest_mod/imageToSave.h')
print ("bmp copied to Arduino sketch")
os.chdir('/Users/rollasoul/densecap/A_printertest_mod')
subprocess.call('/Applications/Arduino.app/Contents/MacOS/Arduino --upload A_printertest_mod.ino', shell=True)

# open in webbrowser (if necessary)
                #webbrowser.open(nuallimages)