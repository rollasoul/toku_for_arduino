# T O K U

Script for handwriting haiku-poems to camera input powered by two neural networks (densecap and rnnlib) - and printing them on a mini-thermal printer. Should be run on remote server and local-client, optimised for raspberry-pi. Both networks come ready to go and trained as a docker-image for the server, the git-repo is mainly for the client side (with a few server-scripts as backup). 

# prerequisites
- ubuntu 16.04 server running intel xeon processors (or newer) otherwise openBLAS/torch will give you a core dumped error
- raspberry pi 3, usb camera, light sensor (or any other trigger you like), adafruit mini-thermal printer and arduino (this script is written for the uno)
- client (e.g. raspberry pi) has Processing and Arduino IDE installed

# server setup

- install docker on remote server
```
sudo apt-get install docker.io
```

- start docker machine
```
service docker start
```

- pull image for densecap and rnnlib as a package (including trained models and server scripts) from docker-cloud repository:
```
docker pull rollasoul/toku

```

- run docker image with port forwarding for port 12345
```
docker run -it -p 12345:12345 rollasoul/toku
```

# client setup

- download or clone git-repo on client (raspberry pi or mac)
- make sure you have [Processing](https://processing.org/) and [Arduino IDE](https://www.arduino.cc/)  installed - otherwise do so:
  processing for raspbian + arduino IDE for raspbian
```
curl https://processing.org/download/install-arm.sh | sudo sh
sudo apt-get update && sudo apt-get install arduino
```

- follow the installation instructions on adafruit for the [adafruit mini-thermal printer](https://learn.adafruit.com/mini-thermal-receipt-printer/)
- replace the bitmapimageconvert-files with the git-repo ones
- open the toku_pi_client.py file and replace the server address with the the address of your server (line 29 and 48)
- check all the files for correct file addresses as they are set up for /home/pi - structure

# hardware setup

- make sure your printer is connected via arduino to raspberry pi (see the adafruit mini-thermal printer for correct setup)
- check all cables and connections (usb, camera, raspberry pi, arduino, minit-thermal printer)
- raspberry pi needs proper wifi-connectivity to run this script

# run toku

now comes the fun part! 

- on server run
```
script_pi
```

- on client run 
```
script_pi
```

Both scripts are endless loops, the client script waits for a trigger from the GPIO (in our case we use a light-sensor for the signal), the server script for the image of the client. Once the webcam takes the image and sends it off to the server, densecap will generate 83 captions for the image. The script selects captions with 5 and 7 syllables. By random a 5 syllables caption, a 7 syllables caption and a 5 syllable caption will be selected and taken as 3 lines of the haiku. Rnnlib runs each line through its network and predicts a possible handwriting for them. This handwriting is plotted with an Octave-script and an image of the full handwritten haiku gets sent back to the client. Here it is resized and converted to bitmap to fit the mini-thermal printer that is controlled by the arduino. The haiku is then printed in 3 steps - as the arduino uno memory can only handle that much info per time. The whole process takes about 3 minutes, with the server part around 20 seconds, printing up to 3 mins. 

And here you go! Your own TOKU handwriting and printing poems about its surroundings.   
