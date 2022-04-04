import threading, socket, struct, sys

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

def send(name):
    global stop
    global sock
    i = 0
    while stop==False:
        msg = input("Message> ")
        sock.sendto(str.encode(msg), (MCAST_GRP,MCAST_PORT))

        if "ADIOS" == msg:
            print("Exiting multicast group & closing client.")
            sock.close()
            stop = False
 

name="thread1"
stop=False
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
ttl = struct.pack('b',1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
sock.bind(('',MCAST_PORT))
reader = threading.Thread(target=send, args=(name,))
reader.start()
while stop==False:
    data = sock.recv(1024).decode()
    if "ADIOS" in data.upper():
        print("Exiting multicast group & closing client.")
        sock.close()
        stop = True
    else:
        print("RX: ",data)
print("Stop thread")
