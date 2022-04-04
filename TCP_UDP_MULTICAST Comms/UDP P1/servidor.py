import socket

msg = "Hello Client"
bytes_tx = str.encode(msg)

socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket.bind(("127.0.0.1",6780))

bytes_rx = socket.recvfrom(1024)
message = bytes_rx[0]
address = bytes_rx[1]
print(message)
socket.sendto(bytes_tx,address)