import subprocess
import socket
from socket import error as SocketError
import errno

import cv2
import os
import subprocess
from subprocess import Popen, PIPE, STDOUT
import time

import json
import pronouncing
from random import randint

from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from random import randint
import nltk.data

from PIL import Image
import PIL
from resizeimage import resizeimage
import sys
import time
import numpy as np

import shutil

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = '0.0.0.0' # Get local machine name
port = 12345              # Reserve a port for your service.
s.bind(('', port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
print 'listening on port 12345'
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   c.send('Thank you for connecting')
      # receive image file
   i=1
   f = open('haikucam'+ str(i)+".jpg",'wb')
   i=i+1
   # wait for densecap & rnn lib to handwrite haiku and create image
      # receive and write image
   l = c.recv(4096)
   try:
   	while (l): 
      		f.write(l)
      		l = c.recv(4096)
   except socket.error:
   	print "image received"
   	break
f.close()

# start densecap neural network to generate captions (and write them in json-file)
os.chdir('/root/densecap')
subprocess.call('/root/torch/install/bin/th run_model.lua -input_image /root/haikucam1.jpg -gpu -1', shell=True)
print "analyse image and write haiku"
# get the data from the json file
haiku_base = open('/root/densecap/vis/data/results.json')
wjson = haiku_base.read()
wjdata = json.loads(wjson)
wjdata_list = wjdata['results'][0]['captions']

# create empty storage for selected captions with fitting syllables (with either 5 or 7 syllables)
syllables5 = []
syllables7 = []
syllables23 = []

# check all captions for fitting syllables (using pronouncingpy + CMU pronouncing dictionary)
# add them to the empty storage
for i in range (1, 83):

   try:
      text = wjdata['results'][0]['captions'][i - 1]

      phones = [pronouncing.phones_for_word(p)[0] for p in text.split()]
      count = sum([pronouncing.syllable_count(p) for p in phones])
      for y in range (1, 2):
         if int(count) == 5:
            syllables5.append(wjdata['results'][0]['captions'][i - 1])
      for x in range (0, 1):
         if int(count) == 7:
            syllables7.append(wjdata['results'][0]['captions'][i - 1])
      for z in range (0, 1):
         if int(count) == 3 or int(count) == 2:
            syllables23.append(wjdata['results'][0]['captions'][i - 1])

# skip over errors caused by non-indexed word <UNK> in captions
   except IndexError:
         pass
   continue

# create arrays for pre-selections of fitting syllables
selection_line1 = ['fill']
selection_line2 = ['fill']
selection_line3 = ['fill']

# randomise selection per syllable selection
while selection_line1[0] == selection_line3[0]:
    selection_line1 = syllables5 [randint(0,(len(syllables5) -1) /2)]
    selection_line2 = syllables7 [randint(0,(len(syllables7)-1))]
    selection_line3 = syllables5 [randint(len(syllables5)/2,(len(syllables5)-1))]

# return the result
print "haiku:"
print (selection_line1)
print (selection_line2) 
print (selection_line3)
selection_line1 = ''.join(selection_line1)
selection_line2 = ''.join(selection_line2)
selection_line2 = ''.join(selection_line2)


# create lines
print "creating handwritten lines"
# let rnnlib generate the image-points for each line and save them in one file
os.chdir('/root/rnnlib/examples/online_prediction')
p = Popen(['/root/rnnlib/rnnsynth --sampleBias=2.0 synth1d@2016.08.20-04.20.35.004518.best_loss.save > lines.txt'], shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
stdout_data = p.communicate(input='%s  \n%s  \n%s  \n' %(selection_line1, selection_line2, selection_line3))[0]

# split the image-points file into different files: 
# three for the lines of the haiku and two others that store general output text
files = open('lines.txt','r').read().split('sentence:')
names=['line0.txt','line1.txt','line2.txt', 'line3.txt', 'line4.txt']
for num,file in enumerate(files):
    open(names[num],'w').write(file)

# cut off last lines in each haiku-line file to avoid printing a final dash/end-point in the plot
# line3 needs more cutting because of its longer ending
for i in names:
   if i == "line3.txt":
      readFile = open(i)
      lines = readFile.readlines()
      readFile.close()
      w = open(i, 'w')
      w.writelines([item for item in lines[:-6]])
      w.close()
   if i == "line1.txt" or i == "line2.txt":
      readFile = open(i)
      lines = readFile.readlines()
      readFile.close()
      w = open(i, 'w')
      w.writelines([item for item in lines[:-2]])
      w.close()

# plot image-points of each line with octave, save plots as png-files (plus extra resizing/cropping for line 2 with 7 syllables)
line1txt = "haikuplot('line1.txt')"
line2txt = "haikuplot7('line2.txt')"
line3txt = "haikuplot('line3.txt')"

p = Popen(['octave --no-gui'], shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
stdout_data = p.communicate(input='%s' %(line1txt))[0]
#os.chdir('/root/densecap')
for fileName in os.listdir("."):
    os.rename(fileName, fileName.replace("haikuline", "line1"))
print ("line 1 is plotted")

os.chdir('/root/rnnlib/examples/online_prediction')
p = Popen(['octave --no-gui'], shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
stdout_data = p.communicate(input='%s' %(line2txt))[0]
#os.chdir('/root/densecap')
for fileName in os.listdir("."):
    os.rename(fileName, fileName.replace("haikuline", "line2"))
#fd_img = open('line2.png', 'r')
#fd_img.seek(0)
#img = Image.open(fd_img)
#img = resizeimage.resize_crop(img, [700, 70])
#img.save('line2.png', img.format)
#fd_img.close()
print ("line 2 is plotted")

os.chdir('/root/rnnlib/examples/online_prediction')
p = Popen(['octave --no-gui'], shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
stdout_data = p.communicate(input='%s' %(line3txt))[0]
#os.chdir('/root/densecap')
for fileName in os.listdir("."):
    os.rename(fileName, fileName.replace("haikuline", "line3"))
print ("line 3 is plotted")

# get sizes of all images, resize and merge them vertically

os.chdir('/root/rnnlib/examples/online_prediction')
with Image.open('line1.png') as im:
    width, height = im.size
width1 = width
height1 = height

with Image.open('line2.png') as im:
    width, height = im.size
width2 = width
height2 = height

with Image.open('line3.png') as im:
    width, height = im.size
width3 = width
height3 = height

widths = (width1, width2, width3)
maxwidth = max(widths)

heights = (height1, height2, height3)
maxheight = max(heights)

list_im = ['line1.png', 'line2.png', 'line3.png']
for i in range (0,3): 
   with Image.open(list_im[i]) as im:
      width, height = im.size

   old_im = Image.open(list_im[i])
   old_size = old_im.size 

   new_size = (maxwidth, height + 20)
   new_im = Image.new("RGB", new_size, "white")   ## luckily, this is already black!
   new_im.paste(old_im, ((new_size[0]-old_size[0])/2, (new_size[1]-old_size[1])/2))
   new_im.save(list_im[i])

imgs    = [ PIL.Image.open(i) for i in list_im ]
min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
imgs_comb = PIL.Image.fromarray( imgs_comb)
imgs_comb.save( 'imageToSave.png' )
#imgs_comb.show()


# rotate image 90 degrees (to make it fit the thermal printer)
src_im = Image.open("imageToSave.png")
#src_im.save("/root/densecap/imgs/saved/%sb-haiku.jpg"%time2)
angle = 270
rotate = src_im.rotate( angle, expand=1 )
rotated = rotate.save("imageToSave.png")
print ("rotation finished")

# send image back to client

print "haiku handwriting (as image) generated"

s.listen(5)                 # Now wait for client connection.
print 'listening on port 12345'
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   f=open ("/root/rnnlib/examples/online_prediction/imageToSave.png", "rb") 
   l = f.read(4096)
   while (l):
      c.send(l)
      l = f.read(4096)
   print "haiku sent"
   i = c.recv(4096)
   while True: 
      if "file received" in i: 
   	 time.sleep(3)
         print "haiku received by client, closing connection"
         c.close()                # Close the connection
	 break
   break
