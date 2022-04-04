import socket

msg = "Hello Client"
bytes_tx = str.encode(msg)

socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket.bind(("192.168.53.5",6780))

while 1:
    bytes_rx = socket.recvfrom(1024)
    message = bytes_rx[0].decode()
    address = bytes_rx[1]
    if "EXIT" in message.upper():
        socket.close()
    print("IP ", address)
    print(message)
    socket.sendto(bytes_tx,address)
