import socket
PORT = 1234
IP = "192.168.1.34"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket object with socket families types --> streaming socket
s.bind((IP, PORT))
s.listen(5)

print(f"Starting server ({IP}) on port {PORT}")
while True:
    print("Running...")
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    clientsocket.send(bytes("Welcome to the server!", "utf-8"))