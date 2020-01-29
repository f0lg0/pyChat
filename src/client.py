import socket

PORT = 1234
IP = socket.gethostname()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

client.connect(("192.168.1.34", PORT))
print(f"Host: {IP} | Port: {PORT}")
msg = client.recv(1024)
print(msg.decode("utf-8"))

def send_msg():
    to_send_msg = input(">")
    client.send(bytes(to_send_msg, "utf-8"))

while True:
    send_msg()