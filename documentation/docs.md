# AppName - Documentation

## Index

* About
* Conversations
* Technical details
* Anonymousity
* Server
* Client
* GUI
* Requirements
* Get Started
* Features
* Themes
* Authors

## About

<app_name> is a simple chat application written using sockets.  Clients connect to a server which lets them send text messages to each  other.

Messages are custom crafted packets built using Python3 dataclasses and we stream them usign JSON. These messages are also encrypted using AES-256 to  ensure privacy and anonymity to the users.

Key exchange is performed using DiffieHellman and the GUI is built  using the pip library "Eel". This means that the entire user experience is coded from scratch with JS, HTML and CSS.

## Conversations

![convo](/media/leonardo/Leonardo/code/Python/socket/chatroom/documentation/pics/convo.png)

Every client has its own private key generated only with the server. The server will care about encrypting and decrypting with the respective key of the other clients.

Here's a more detailed example.

![detail](/media/leonardo/Leonardo/code/Python/socket/chatroom/documentation/pics/detail.png)

## Technical details

As mentioned in the "About" section, messages are custom dataclasses objects streamed in the universal standard JSON format. They are carefully streamed with a small buffer size thanks to the fact that every packet is preceded by a fixed length header containing information about the actual packet size.  

![msg](/media/leonardo/Leonardo/code/Python/socket/chatroom/documentation/pics/msg.png)

But why JSON?

We have chosen to use JSON to serialize our data because Pickle is vulnerable to code injection. We don't have this problem with JSON because, as you may know, JSON data is in a string format. No bytes, no pain.

![sample](/media/leonardo/Leonardo/code/Python/socket/chatroom/documentation/pics/sample.png)

We use AES-256 to ensure privacy to our users and we also automate the key exchange process so clients don't have to know any password.
As stated before, key exchange is performed with a classic DiffieHellman exchange based on very large integers.

This is an example of a valid key:

![key](/media/leonardo/Leonardo/code/Python/socket/chatroom/documentation/pics/ex.png)

The key exchange is performed immediately after the established connection between server and client

## Anonymousity

To start using <app_name> you don't need any kind of account. Your precious personal data remains in your head, everything here is  anonymous. You just need to care about your IP address, using a VPN is a good idea (everywhere in the Internet!). The server logs only the messages to be able to serve them in case of an export chat request, this ca be easily removed if you want. Otherwise, once the server gets stopped, logs are cleared.

## Server

Once the server is up and running it constantly listens for incoming messages, these are the steps involved in the handler function (the core of the sever):

![](/media/leonardo/Leonardo/code/Python/socket/chatroom/documentation/pics/steps.png)

The Handler function then processes the finally decrypted messages and decides what to do with it based on the 'typ' field:

![](/media/leonardo/Leonardo/code/Python/socket/chatroom/documentation/pics/handler.png)



## Client

Once the client scripts gets fired up it tries to connect to the server set before:

![](/media/leonardo/Leonardo/code/Python/socket/chatroom/documentation/pics/connect.png)

Once a connection is established it listens for the AES vector and for the public information about the key sent by the server. Once those are received it generates the shared secret and it shares his public information so the server can do the same. Once AES is initialized it proceeds with the user name setting.

The client also has the same method for streaming, decrypting and converting to object as the server.

## GUI

The graphical user interface is built entirely from scratch using JavaScript, HTML and CSS thanks to the Eel library. This library lets you use fronted languages to build GUIs for Python projects. 

We strongly recommend you to check Eel [GitHub](https://github.com/samuelhwilliams/Eel) page, there you can find a proper documentation.

Basically we "expose" Python functions in order to make them accessible from JavaScript.

![](/media/leonardo/Leonardo/code/Python/socket/chatroom/documentation/pics/exposed.png)

This is an example of an exposed function inside client.py. In order to use "sendMsg", a class method, we need to expose it from another function: "exposeSendMsg", located outside the Client class. This way we can use the function in a JavaScript file. Note that we can't expose functions inside a class.

Here's the JS code:

![](/media/leonardo/Leonardo/code/Python/socket/chatroom/documentation/pics/exposed_js.png)

## Requirements

- Python 3.x
- socket
- json
- threading
- sys
- datetime
- time
- argparse
- dataclasses_json
- pycryptodome
- pyDHE
- Eel

This application is built using Python3 and it depends on those libraries. You may need to "pip install" them.

## Get Started

### 1st option:

```
python3 server.py -p <port number>
python3 client.py -s <server_ip> -p <server_port>
```

### 2nd option:

```
python3 server.py
python3 client.py
```

Everybody has the ability to start their own server, this is the key aspect of this application. You don't depend on third parties, you are your own service provider. Server can even be started on a Raspberry Pi, you don't need power. Everything is lightweight, especially server side.

The first option involves parsing the values at the beginning, if you don't do that then the app will ask you to do that later on during execution.

Note: you may have python3 aliased to just "python"; so consider that.

## Features

These are the current built in feature to out Application, if you have an idea about a new feature don't be afraid and contact us!

- [export_chat] > export current chat to a text file
- [help] > display all possible commands

## Themes

AppName as different built in themes with the default one being the *Nordic* theme. Here' s a list:

* Pure Black
* Dark
* Light
* Nord

## Authors

[f0lg0](https://github.com/f0lg0)

[JacopoFB](https://github.com/JacopoFB)

