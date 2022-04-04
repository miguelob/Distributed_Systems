import socket, pickle, datetime, traceback
from sys import argv
import time as TIME

error = 1
state = ""
while error:
        try:
            ip = str(argv[1])
            port = int(argv[2])
            id = int(argv[3])

            server_address = (ip,port)
            sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            sock.connect(server_address)
            msg = input("Message> ")

            if "GET" in msg.upper():
                if state == "lock":
                    spt = msg.split()
                    file_name = spt[1]

                    message = (id,msg)
                    bytes_tx = pickle.dumps(message)
                    sock.sendall(bytes_tx)
                    l = sock.recv(1024)
                    if "ERROR" in l.decode():
                        print("Cant READ/OPEN that file. Please try again.")
                    else:
                        f = open(file_name,'wb')
                        while l:
                            f.write(l)
                            l = sock.recv(1024)
                            if "END" in l.decode():
                                break
                        f.close()
                        print("File recieved successfully")
                        state = "get"
                else:
                    state = ""
                    print("Secuence was incorrect. Restart it")
            elif "PUT" in msg.upper():
                if state == "get":
                    message = (id,msg)
                    bytes_tx = pickle.dumps(message)
                    sock.sendall(bytes_tx)
                    spt = msg.split()
                    file_name = spt[1]
                    f = open(file_name,'rb')
                    l = f.read(1024)
                    while l:
                        print("Sending...")
                        sock.sendall(l)
                        l = f.read(1024)
                    sock.sendall("END".encode())
                    f.close()
                    print("File sent successfully")
                    state = "put"
                else:
                    state = ""
                    print("Secuence was incorrect. Restart it")
                
            elif "UNLOCK" in msg.upper():
                if state == "put":
                    message = (id,msg)
                    bytes_tx = pickle.dumps(message)
                    sock.sendall(bytes_tx)
                    print("RX: ",sock.recv(1024).decode())
                    state = ""
                else:
                    state = ""
                    print("Secuence was incorrect. Restart it")
            elif "LOCK" in msg.upper():
                if state == "":
                    message = (id,msg)
                    bytes_tx = pickle.dumps(message)
                    sock.sendall(bytes_tx)
                    print("RX: ",sock.recv(1024).decode())
                    state = "lock"
                else:
                    state = ""
                    print("Secuence was incorrect. Restart it")
            elif msg.upper() == "EXIT":
                message = (id,msg)
                bytes_tx = pickle.dumps(message)
                sock.sendall(bytes_tx)
                print("RX: ",pickle.loads(sock.recv(1024)))
                error = 0
                sock.close()
                break
            else:
                message = (id,msg)
                bytes_tx = pickle.dumps(message)
                sock.sendall(bytes_tx)
                print("RX: ",pickle.loads(sock.recv(1024)))
            
        except ValueError:
            #traceback.print_exc()
            error = 1
            print("Check for valid arguments IP(XXX.XXX.XXX.XXX), PORT(XXXX) & ID(X) Where X is an INT.")
        except:
            traceback.print_exc()
            print("Closing the Client.")
            error = 0

