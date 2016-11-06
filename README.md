# toku

prerequisites
- ubuntu 16.04 server running intel xeon processors (or newer) otherwise openBLAS/torch will give you a core dumped error
- raspberry pi 3, usb camera, light sensor, PiNoir camera

server setup

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

- run docker image with open port 12345
```
docker run -it -p 12345:12345 rollasoul/toku
```

client setup
- download or clone git-repo for raspberry pi with client-script
