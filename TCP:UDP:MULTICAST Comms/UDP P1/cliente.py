import socket

msg = "Hello Server"
bytes_tx = str.encode(msg)

server_address = ("127.0.0.1",6780)
socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket.sendto(bytes_tx, server_address)

bytes_rx = socket.recvfrom(1024)
print("RX: ", bytes_rx)
socket.close()
