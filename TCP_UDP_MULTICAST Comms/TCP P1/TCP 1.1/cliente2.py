import socket
import sys

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server_address = ('localhost', 6780)
sock.connect(server_address)
sock.sendall("HI TCP SERVER, I'm Client 2".encode())
data = sock.recv(1024).decode()
print("RX: ",data)


