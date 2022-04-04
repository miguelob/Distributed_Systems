import socket
# Client 1
error = 1
while error:
    try:
        port = int(input("Provide port number (e.g 6780): "))
        msg = "Hello Server, I'm Client 1"
        bytes_tx = str.encode(msg)

        server_address = ("127.0.0.1",port)
        socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        socket.sendto(bytes_tx, server_address)

        bytes_rx = socket.recvfrom(1024)
        print("RX: ", bytes_rx)
        error = 0
    
    except ValueError:
        print("It has to be a number (e.g 6780)")
        error = 1
