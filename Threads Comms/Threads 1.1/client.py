import socket
import sys
from threading import Thread
import traceback

def main():
    start_client()


def start_client():
    while True:
        try:
            host = str(input("Please type in the IP: "))
            port = int(input("Please type in the port number: "))
            break
        except:
            print("Error in the values entered. Please retry.")
    print("Please enter 'exit' to exit")
    i = 1
    lista = []
    while i:
        message = input("Message #"+str(i)+">")
        lista.append(message)
        i += 1
        if message.upper() == 'EXIT':
            i = 0
    for i in range(1,len(lista)+1):
        try:
            Thread(target=hilo, args=(host, port, i, lista[i-1])).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()
    #print("Bye")
    #sock.send((client+':'+'quit').encode("utf8"))

def hilo(host, port, i, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except:
        print("Connection Error")
        sys.exit()
    sock.sendall(("Client#"+str(i)+":"+message).encode("utf8"))
    receive = sock.recv(1024).decode("utf8")
    [print(i) for i in receive.split(" ")]
if __name__ == "__main__":
     main()