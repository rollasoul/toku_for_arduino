# T O K U

Script for handwriting haiku-poems to camera input powered by two neural networks (densecap and rnnlib). Should be run on remote server and local-client, optimised for raspberry-pi. Both networks come ready to go and trained as a docker-image for the server, the git-repo is mainly for the client side (with a few server-scripts as backup). 

# prerequisites
- ubuntu 16.04 server running intel xeon processors (or newer) otherwise openBLAS/torch will give you a core dumped error
- raspberry pi 3, usb camera, light sensor (or any other trigger you like), adafruit mini-thermal printer and arduino (this script is written for the uno)

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
- follow the installation instructions on adafruit for the mini-thermal printer
- replace the bitmapimageconvert-files with the git-repo ones
- open the toku_pi_client.py file and replace the server address with the the address of your server (line 29 and 48)
- check all the files for correct file addresses as they are set up for /home/pi - structure

# hardware setup

- make sure your printer is connected via arduino to raspberry pi (see the adafruit mini-thermal printer for correct setup)
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
And here you go! Your own TOKU handwriting poems about its surroundings (with a little help by 2 neural networks ...) 
