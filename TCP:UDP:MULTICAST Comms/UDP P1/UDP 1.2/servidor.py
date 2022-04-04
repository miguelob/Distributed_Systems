import socket
import traceback
# Server
error = 1
while error:
    try:
        port = int(input("Please input the desire port (e.g 6780): "))
        print("UDP Server up and listening")
        msg = "Hello Client"
        bytes_tx = str.encode(msg)

        socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        socket.bind(("127.0.0.1",port))

        while 1:
            bytes_rx = socket.recvfrom(1024)
            message = bytes_rx[0].decode()
            address = bytes_rx[1]
            if "EXIT" in message.upper():
                socket.close()
            else:
                print("Message from client: " + message)
                print("Client IP address: " + address[0] + " and port: " + str(address[1]))
                socket.sendto(bytes_tx,address)

        
    except ValueError:
        print("Invalid input, please type a valid port (e.g 6780)")
        error = 1

    except:
        print("Server was successfully closed.")
        error = 0
