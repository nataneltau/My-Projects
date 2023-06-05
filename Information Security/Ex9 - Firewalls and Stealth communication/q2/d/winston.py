import socket
from scapy.all import *
import sys

SRC_PORT = 65000


def send_message(ip: str, port: int):
    """Send a *hidden* message to the given ip + port.

    Julia expects the message to be hidden in the TCP metadata, so re-implement
    this function accordingly.

    Notes:
    1. Use `SRC_PORT` as part of your implementation.
    """
    # TODO: RE-IMPLEMENT THIS FUNCTION
    #add pading to the message so it will divide in 3, 
    #in addition make it int so we can manipulate it's bits
    #and count the number of packet we will sent
    msg = b'I love you'
    pad_msg = msg.ljust((len(msg)) + 2, b'\0')
    int_msg = int.from_bytes(pad_msg, sys.byteorder)
    amount_trip = (len(pad_msg) * 8) // 3

    #we start from the end, that way it worked, don't ask
    #every iteration we send the same packet, with different seq number
    #represnting the location of the bits and different reserved
    for i in range(amount_trip - 1, -1, -1):
        ip_pack = IP(dst=ip)#desired ip
        #sport should be SRC_PORT
        tcp_pack = TCP(sport=SRC_PORT, dport=port, flags="SA", seq=i, ack=amount_trip)
        #take 3 bits and shift 
        three_bits = int_msg & 7
        int_msg >>= 3
        pack = ip_pack / tcp_pack
        #add the 3 bits to the packet
        pack.reserved = three_bits
        send(pack)
        
    #raise NotImplementedError()
    


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    send_message('127.0.0.1', 1984)


if __name__ == '__main__':
    main()
