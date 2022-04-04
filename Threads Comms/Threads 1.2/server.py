import socket
import sys
import traceback
from threading import Thread

def main():
     start_server()
        
def start_server():
    while True:
        try:
            host = str(input("Please type in the IP: "))
            port = int(input("Please type in the port number: "))
            break
        except:
            print("Error in the values entered. Please retry.")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")
    try:
        sock.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    sock.listen(6) # queue up to 6 requests
    print("Socket now listening")
    # infinite loop- do not reset for every requests
    while True:
        connection, address = sock.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connection from client " + ip + ":" + port)
        try:
            Thread(target=clientThread, args=(connection, ip, port)).start()
        except:
            print("Thread did not start.")
            #traceback.print_exc()
    sock.close()
    
def clientThread(connection, ip, port, max_buffer_size = 1024):
    is_active = True
    while is_active:
        client_input = connection.recv(max_buffer_size).decode("utf8")
        #print(client_input)
        clientid,msg=client_input.split(":")
        if "EXIT" in msg.upper():
            connection.send("ok".encode("utf8"))
            print("Client {} is requesting to quit".format(clientid))
            print("Connection " + ip + ":" + port + " closed")
        else:
            print("Client {} sent data: {}".format(clientid,msg))
            connection.send(msg.encode("utf8"))
        connection.close()
        is_active = False

if __name__ == "__main__":
    main()