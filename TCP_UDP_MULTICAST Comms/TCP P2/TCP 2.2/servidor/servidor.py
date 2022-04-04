import socket, pickle, datetime, traceback
from sys import argv

print("TCP Server up and listening")
error = 1
tmp = 1
while error:
    try:    
        ip = str(argv[1])
        port = int(argv[2])

        if tmp:
            sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            server_address = (ip, port)
            sock.bind(server_address)
            sock.listen(1)
            tmp =0
        connection, client_addess = sock.accept()

        finish = 1
        while finish:
            try:
                data = connection.recv(1024)
                unwrapped = pickle.loads(data)
                if "EXIT" in unwrapped[1].upper():
                    finish = 0
                    error = 0
                    print("Exit command recieved by Client: " + str(unwrapped[0]))
                    connection.sendall(pickle.dumps("Bye"))
                    connection.close()
                elif "UNLOCK" in unwrapped[1].upper():
                    connection.sendall("File was sucessfully unlocked".encode())
                elif "LOCK" in unwrapped[1].upper():
                    connection.sendall("lOCK DONE.".encode())
                elif "GET" in unwrapped[1].upper():
                    spt = unwrapped[1].split()
                    file_name = spt[1]
                    f = open(file_name,'rb')
                    l = f.read(1024)
                    while l:
                        print("Sending...")
                        connection.sendall(l)
                        l = f.read(1024)
                    connection.sendall("END".encode())
                    f.close()
                elif "PUT" in unwrapped[1].upper():
                    spt = unwrapped[1].split()
                    file_name = spt[1]
                    l = connection.recv(1024)
                    if "ERROR" in l.decode():
                        print("Cant READ/OPEN that file. Please try again.")
                    else:
                        f = open(file_name,'wb')
                        while l:
                            f.write(l)
                            l = connection.recv(1024)
                            if "END" in l.decode():
                                break
                        f.close()
                        print("File recieved successfully")           
                else:
                    msg = "Hi client, I only accept 5 commands: exit, lock, get, put, & unlock."
                    connection.sendall(pickle.dumps(msg))
            except IOError:
                #traceback.print_exc()
                msg = "ERROR"
                connection.sendall(msg.encode())
            except:
                #traceback.print_exc()
                finish = 0
    except ValueError:
        #traceback.print_exc()
        print("Invalid input, please type a valid port (e.g 6780)")
        error = 1
    except:
        #traceback.print_exc()
        print("Server was successfully closed.")
        error = 0

