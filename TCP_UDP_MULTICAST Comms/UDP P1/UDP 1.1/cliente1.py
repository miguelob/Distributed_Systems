import socket

msg = "Hello Server, I'm Client 1"
bytes_tx = str.encode(msg)

server_address = ("192.168.1.10",6780)
socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket.sendto(bytes_tx, server_address)

bytes_rx = socket.recvfrom(1024)
print("RX: ", bytes_rx)
