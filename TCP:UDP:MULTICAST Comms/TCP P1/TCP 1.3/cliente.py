import socket, pickle, datetime, traceback
from sys import argv
import time as TIME

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
            sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

            tmp = []
            iniTime = datetime.datetime.now()
            print("Start 100000 calls")
            
            check = 1
            for i in range(99999):
                #print("i: "+str(i))
                try:
                    if check:
                        check = 0
                        sock.connect(server_address)
                    sock.sendall(bytes_tx)
                    bytes_rx = sock.recv(1024)
                    time = pickle.loads(bytes_rx)

                    tmp.append((datetime.datetime.now() - time).total_seconds())
                except:
                    #traceback.print_exc()
                    try:
                        print("Can't connect. Trying in 5 seconds")
                        TIME.sleep(5)
                        sock.connect(server_address)
                        sock.sendall(bytes_tx)
                        bytes_rx = sock.recv(1024)
                        time = pickle.loads(bytes_rx)

                        tmp.append((datetime.datetime.now() - time).total_seconds())
                    except:
                        #traceback.print_exc()
                        print("Can't connect to the server. Reason: TIMEOUT")
                        sock.close()
                        break
            print("Total time elapsed: {}".format((datetime.datetime.now() - iniTime).total_seconds()))
            print("Averaged difference time in seconds: {}".format((sum(tmp)/len(tmp))))    
            #socket.close()
            
        except ValueError:
            #traceback.print_exc()
            error = 1
            print("Check for valid arguments IP(XXX.XXX.XXX.XXX), PORT(XXXX) & ID(X) Where X is an INT.")
        except:
            #traceback.print_exc()
            print("Closing the Client.")

