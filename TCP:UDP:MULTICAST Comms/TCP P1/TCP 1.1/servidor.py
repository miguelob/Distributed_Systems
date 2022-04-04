import socket, traceback
import sys
# Server
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
            data = connection.recv(1024).decode()
            
            if "EXIT" in data.upper():
                connection.sendall("Bye".encode())
                connection.close()
                sock.close()
            else:
                print("RX: ",data)
                connection.sendall("HI TCP CLIENT".encode())
        
    except:
#        traceback.print_exc()
        print("Server was successfully closed.")
        error = 0

