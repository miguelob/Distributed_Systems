import socket, pickle, datetime, traceback
from sys import argv

print("TCP Server up and listening")
error = 1
while error:
    try:    
        ip = str(argv[1])
        port = int(argv[2])

        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        server_address = (ip, port)
        sock.bind(server_address)
        sock.listen(1)
        connection, client_addess = sock.accept()

        finish = 1
        while finish:
            try:
                data = connection.recv(1024)
                unwrapped = pickle.loads(data)
                #print(unwrapped)
                if "EXIT" in unwrapped[1].upper():
                    finish = 0
                    error = 0
                    print("Exit command recieved by Client: " + str(unwrapped[0]))
                    connection.sendall(pickle.dumps("Bye"))
                    connection.close()
                else:
                    time = datetime.datetime.now()
                    connection.sendall(pickle.dumps(time))
            except:
                finish = 0
    except ValueError:
        #traceback.print_exc()
        print("Invalid input, please type a valid port (e.g 6780)")
        error = 1
    except:
        #traceback.print_exc()
        print("Server was successfully closed.")
        error = 0

