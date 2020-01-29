import socket

PORT = 1234
IP = socket.gethostname()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
print(f"Host: {IP} | Port: {PORT}")
msg = s.recv(1024)
print(msg.decode("utf-8"))