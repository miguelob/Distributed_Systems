import socket, pickle, traceback
from sys import argv

error = 1
while error:
    try:
        ip = str(argv[1])
        port = int(argv[2])
        print("UDP Server up and listening")
    

        socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        socket.bind((ip,port))

        while 1:
            bytes_rx = socket.recvfrom(1024)
            unwrapped = pickle.loads(bytes_rx[0])
            address = bytes_rx[1]
            if "EXIT" in unwrapped[1].upper():
                print("Exit command recieved by Client: " + str(unwrapped[0]))
                socket.sendto(pickle.dumps("Bye"),address)
                socket.close()
            else:
                print("Message from client {}: {}".format(unwrapped[0],unwrapped[1]))
                print("Client IP address: " + address[0] + " and port: " + str(address[1]))
                print("{} characteres revieved.".format(len(unwrapped[1])))
                
                msg = "Recieved {} characteres from Client {}.".format(len(unwrapped[1]),unwrapped[0])
                socket.sendto(pickle.dumps(msg),address)

        
    except ValueError:
        #traceback.print_exc()
        print("Invalid input, please type a valid port (e.g 6780)")
        error = 1

    except:
        #traceback.print_exc()
        print("Server was successfully closed.")
        error = 0
