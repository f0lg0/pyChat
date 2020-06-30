# pyChat
A simple, anonymous and fully encrypted chat application built using sockets in Python3

![example](./wireframes/PNG/logo.png)

# About

pyChat is a simple chat application written using sockets. Clients connect to a server which lets them send text messages to each other.

Messages are custom crafted packets built using Python3 dataclasses, we stream them using JSON due to the fact that Pickle is vulnerable to code injection. These messages are also encrypted using AES-256 to ensure privacy and anonymity to the users. We don't collect any kind of user data.

Key exchange is performed using DiffieHellman and the GUI is built using the pip library "Eel". This means that the entire user experience is coded from scratch with JS, HTML and CSS.

# Conversations

![convo](./documentation/pics/convo.png)

Every client has its own private key shared only with the server. The server will care about encrypting and decrypting with the respective key for the other clients.

Here's a more detailed example.
![detail](./documentation/pics/detail.png)

# Technical details

As mentioned in the "About" section, messages are custom dataclasses objects streamed in the universal standard JSON format. They are carefully streamed with a small buffer size thanks to the fact that every packet is preceded by a fixed length header containing information about the actual packet size.

We use AES-256 to ensure privacy to our users, we also automate the key exchange process so clients don't have to know any password.  
As stated before, key exchange is performed with a classic DiffieHellman exchange based on very large integers.

# Anonymousity

To start using pyChat you don't need any kind of account. Your precious personal data remains in your head, everything here is anonymous. You just need to care about your IP address, using a VPN is a good idea (everywhere in the Internet!).

# Requirements

Pip install the following packages.

* dataclasses_json
* pycryptodome
* pyDHE
* Eel

# Run

First boot up a server with the following command, make sure you run it on a valid IP address. If something goes wrong try to bind at 0.0.0.0 in server.py and client.py.

And then fire up the client. Connect to your newly started server and enjoy the app.

Note: you can only start one client per host. If you want to fire up multiple clients (for debugging) head over to the client.py file and de-comment the random function at line 171 and comment line 172.

```
eel.start('main.html', port=random.choice(range(8000, 8080)))
```

### 1st option:

```
python3 server.py -p <port number>
```
```
python3 client.py -s <server_ip> -p <server_port>
```

### 2nd option:

```
python3 server.py
```
```
python3 client.py
```

Everybody has the ability to start their own server, this is the key aspect of this application. You don't depend on third parties, you are your own service provider. Server can even be started on a Raspberry Pi, you don't need power. Everything is lightweight, especially server side.

## Features

* [export_chat] > export current chat to a text file

## Thank you!

Thank you for using our application! We would love to hear feedback and we are open to any kind of questions!

## Authors

[f0lg0](https://github.com/f0lg0)

[JacopoFB](https://github.com/JacopoFB)

## Contact

Open an issue here or:

[f0lg0 Twitter](https://twitter.com/f0lg0)  
[f0lg0 Reddit](https://www.reddit.com/user/_folgo_/)
