import socket, pickle, traceback

error = 1
while error:
    try:
        port = int(input("Please input the desire port (e.g 6780): "))
        print("UDP Server up and listening")
    

        socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        socket.bind(("127.0.0.1",port))

        while 1:
            bytes_rx = socket.recvfrom(1024)
            unwarapped = pickle.loads(bytes_rx[0])
            address = bytes_rx[1]
            if "EXIT" in unwarapped[1].upper():
                socket.close()
            else:
                print("Message from client {}: {}".format(unwarapped[0],unwarapped[1]))
                print("Client IP address: " + address[0] + " and port: " + str(address[1]))
                print("{} characters revieved.".format(len(unwarapped[1])))
                
                msg = "Hello Client {}. I have recieve {} characters.".format(unwarapped[0],len(unwarapped[1]))
                socket.sendto(pickle.dumps(msg),address)

        
    except ValueError:
        print("Invalid input, please type a valid port (e.g 6780)")
        error = 1

    except:
#        traceback.print_exc()
        print("Server was successfully closed.")
        error = 0
