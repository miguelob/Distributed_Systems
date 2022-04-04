import socket
import sys
# cliente 1
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.56.6', 502)
sock.connect(server_address)
sock.sendall('\x00\x04\x00\x00\x00\x06\x01\x05\x00\x01\xff\x00'.encode())
data = sock.recv(49096)#.decode('hex')
print("RX: ",data)


