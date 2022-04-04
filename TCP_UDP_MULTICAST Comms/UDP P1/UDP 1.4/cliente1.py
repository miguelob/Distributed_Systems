import socket, pickle, traceback, time
from sys import argv

error = 1
time_acum = 1

ip = "127.0.0.1" #str(argv[1])
port = 6780#int(argv[2])
id = 1#int(argv[3])
text = "Hola que tal"#str(input("Please input the message: "))

while error:
    try:   

        server_address = (ip,port)
        sck = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        sck.bind(server_address)
        
        tmp = 1
        print(time_acum)
        bytes_tx = (id, text)

        
        while tmp:
            sck.sendto(pickle.dumps(bytes_tx),server_address)
            
        if time_acum == 4 and tmp == 0:
        
            bytes_rx = sck.recvfrom(1024)
            message = pickle.loads(bytes_rx[0])
            print("RX: ", message)
            
        else:
            print("Max time reached. Pleasy try again later.")
    
    except ValueError:
        traceback.print_exc()
        print("It has to be a number (e.g 6780)")
        error = 1
    except:
        print("entra exception")
        traceback.print_exc()
        print("Waiting to connect: " + str(time_acum*10) + " seconds of 30 max")
        time_acum += 1
        if time_acum == 4:
            tmp = 0
            break
        time.sleep(10)
        
    
