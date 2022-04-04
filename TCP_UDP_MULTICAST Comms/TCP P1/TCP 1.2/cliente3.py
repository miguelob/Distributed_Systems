import socket
import sys

MTU = 20

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server_address = ('localhost', 6780)
sock.connect(server_address)
sock.sendall("EXIT".encode())
while 1:
    data = sock.recv(20).decode()
    if len(data) == MTU:
        print("RX: ",data)
    else:
        print("RX: ",data)
        break

