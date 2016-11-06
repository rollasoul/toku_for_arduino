# toku

# prerequisites
- ubuntu 16.04 server running intel xeon processors (or newer) otherwise openBLAS/torch will give you a core dumped error
- raspberry pi 3, usb camera, light sensor, PiNoir camera, adafruit mini-thermal printer

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

client setup

- download or clone git-repo for raspberry pi with client-script
- follow the installation instructions on adafruit for the mini-thermal printer
- replace the bitmapimageconvert-files with the git-repo ones
- open the toku_pi_client.py file and replace the server address with the the address of your server (line 29 and 48)

# run toku

- on server run
```
script_pi
```

- on client run 
```
script_pi
```

