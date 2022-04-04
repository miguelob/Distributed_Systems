import socket, pickle, time, datetime
from sys import argv

msg = input("Message> ")

error = 1
while error:
        try:
            ip = str(argv[1])
            port = int(argv[2])
            id = int(argv[3])

            message = (id,msg)
            bytes_tx = pickle.dumps(message)

            error = 0

            server_address = (ip,port)
            sck = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

            try:
                print("Connecting to server...")
                sck.sendto(bytes_tx, server_address)

                bytes_rx = sck.recvfrom(1024)
                time = pickle.loads(bytes_rx[0])
                address = bytes_rx[1]
                
                print("Date recieved by the Server: {}".format(time))
                print("Server IP address: " + address[0] + " and port: " + str(address[1]))

                print("Elapsed time in seconds: {}".format((datetime.datetime.now() - time).total_seconds()))

            except:
                try:
                    #print("Can't reach the server. Trying in 10 secs")
                    time.sleep(5)

                    sck.sendto(bytes_tx, server_address)

                    bytes_rx = sck.recvfrom(1024)
                    time = pickle.loads(bytes_rx[0])
                    address = bytes_rx[1]

                    print("Date recieved by the Server: {}".format(time))
                    print("Server IP address: " + address[0] + " and port: " + str(address[1]))

                    print("Elapsed time in seconds: {}".format((datetime.datetime.now() - time).total_seconds()))

                except:
                    print("Can't connect to the server. Rason: TIMEOUT")

            socket.close()

        except ValueError:
            error = 1
            print("Check for valid arguments IP(XXX.XXX.XXX.XXX), PORT(XXXX) & ID(X) Where X is an INT.")
        except:
            print("Closing the Client.")

