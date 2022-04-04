import socket, pickle
# Cliente 2
error = 1
while error:
    try:
        port = int(input("Provide port number (e.g 6780): "))
        msg = input("Message> ")
        id = 2
        bytes_tx = (id, msg)

        server_address = ("127.0.0.1",port)
        socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        socket.sendto(pickle.dumps(bytes_tx), server_address)

        if msg.upper() != "EXIT":
            bytes_rx = socket.recvfrom(1024)
            message = pickle.loads(bytes_rx[0])
            print("RX: ", message)
        error = 0
        
    except ValueError:
        print("It has to be a number (e.g 6780)")
        error = 1

