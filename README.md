# ChatRoom
A simple chat room built using sockets with Python3

![example](./banner/example.png)

# About

ChatRoom is a simple chat application written using sockets. Clients connect to a server which lets them send text messages to each other.

This was initially developed under a Linux system so it may have issues under Windows. Currently we are working 
on porting it to Windows. 

# Requirements 

* Python3

All the libraries inside this code should be already installed, in case just pip install the followings:

* socket
* pickle
* threading
* sys
* datetime
* time

# Run 

```
python3 server.py -p <port number>
python3 client.py -s <server_ip> -p <server_port>
```
## Features

* [export_chat] > export current chat to a text file 
* [help] > display all possible commands

## Authors

[f0lg0](https://github.com/f0lg0)

[JacopoFB](https://github.com/JacopoFB)


