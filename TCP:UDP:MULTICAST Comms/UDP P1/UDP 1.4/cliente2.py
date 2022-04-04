import socket, pickle, time
from sys import argv

msg = input("Message> ")

error = 1
while error:
    try:
            ip = str(argv[1])
            port = int(argv[2])
            id = id(argv[3])

            message= (msg, id)
            bytes_tx = pickle.dumps(message)

            error= 0

            server_address = (ip, port)
            sck= socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

            try:
                print("Connecting to server...")

                sck.sendto(bytes_tx, server_address)
                bytes_rx = sck.recvfrom(1024)
                print("RX: ",bytes_rx)
            except:
                try:
                    print("Can't reach the server. Trying in 10 secs")
                    time.sleep(10)

                    sck.sendto(bytes_tx, server_address)
                    bytes_rx = sck.recvfrom(1024)
                    print("RX: ",bytes_rx)
                except:
                    print("Can't connect to the server <TIMEOUT>")

            socket.close()

    except ValueError:
                error = 1
                print("Check for valid arguments IP(XXX.XXX.XXX.XXX), PORT(XXXX) & ID(X) Where X is an INT.")
