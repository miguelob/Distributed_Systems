import socket, traceback
import sys

MTU = 20
MSG = "Hello Client, this is a long message that you will recieved in chunks of 20 bytes."
error = 1

while error:
    try:
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        server_address = ('localhost', 6780)
        sock.bind(server_address)
        sock.listen(1)
        print("TCP Server ready")

        while 1:
            print("Waiting for connections...")
            sock.listen(1)
            connection, client_addess = sock.accept()
            print("New connection from ", client_addess)
            while 1:
                data = connection.recv(MTU).decode()
                if len(data) >= MTU:
                    print("RX: ",data)
                else:
                    print("RX: ",data)
                    if "EXIT" in data.upper():
                        connection.sendall("Bye".encode())
                        connection.close()
                        sock.close()
                    break
            connection.sendall(MSG.encode())
        
    except:
#        traceback.print_exc()
        print("Server was successfully closed.")
        error = 0

