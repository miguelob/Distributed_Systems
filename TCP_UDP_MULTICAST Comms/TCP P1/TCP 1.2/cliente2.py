import socket
import sys

MTU = 20
MSG = "Hello Server I'm Client 2, this is a long message that you will recieved in chunks of 20 bytes."

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server_address = ('localhost', 6780)
sock.connect(server_address)
sock.sendall(MSG.encode())
while 1:
    data = sock.recv(MTU).decode()
    if len(data) == MTU:
        print("RX: ",data)
    else:
        print("RX: ",data)
        break
