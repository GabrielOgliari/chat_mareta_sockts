import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('152.67.55.209', 80))
client.send("I am CLIENT\n".encode())
from_server = client.recv(4096)
client.close()