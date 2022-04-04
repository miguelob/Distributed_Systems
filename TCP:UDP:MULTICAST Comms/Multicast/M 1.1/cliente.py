import socket, struct

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
error = 1
while error:
    msg = input("Message> ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind(('',MCAST_PORT))
    sock.sendto(str.encode(msg), (MCAST_GRP,MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    ttl = struct.pack('b',1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    if "ADIOS" == msg:
        print("Exiting multicast group & closing client.")
        sock.close()
        error = 0
    else:
        data = sock.recv(1024).decode()
        if "ADIOS" in data.upper():
            print("Exiting multicast group & closing client.")
            sock.close()
            error = 0
        else:
            print("RX: ",data)
