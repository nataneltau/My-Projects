import socket
from scapy.all import * 
import sys

SRC_PORT = 65000

def desired_packet(packet, port):
    """THIS FUNCTION RETURN TRUE IF THE PACKET IS 
        THE DESIRED PACKET"""
    return packet.haslayer(TCP) and packet[TCP].sport == SRC_PORT and packet[TCP].dport == port and packet[TCP].flags == "SA"


def receive_message(port: int) -> str:
    """Receive *hidden* messages on the given TCP port.

    As Winston sends messages encoded over the TCP metadata, re-implement this
    function so to be able to receive the messages correctly.

    Notes:
    1. Use `SRC_PORT` as part of your implementation.
    """
    # TODO: RE-IMPLEMENT THIS FUNCTION
    #raise NotImplementedError()
    #init
    amount_trip = -1
    num_pack_reci = -2
    all_packet = dict()
    
    #while we don't get all the packet or while we at the beginning 
    while num_pack_reci < amount_trip:
    
        #sniff packet, need timeout else it's stuck 
        packets_sniff = sniff(iface=get_if_list(), timeout = 5)
        
        
        for packet in packets_sniff:
            #check if the desired packet
            if desired_packet(packet, port):
                #check if we at the beginning, if so initialize correct 
                if amount_trip == -1:
                    num_pack_reci = 0
                    amount_trip = packet[TCP].ack
                seq_num = packet[TCP].seq
                #check if the seq_num in all_packet
                if seq_num not in all_packet:
                    #add seq_num to dict with his bits
                    all_packet[seq_num] = packet[TCP].reserved
                    num_pack_reci += 1
    
    #let's start to build the message
    secret_msg = 0
    #iterate through all keys in the dict in the sorted
    #order and build the message like we dismentle it
    for index in sorted(all_packet.keys()):
        trip_bits = all_packet[index] & 7
        secret_msg = (secret_msg << 3) + trip_bits
        
    #print(msg)    
    #make the message to byte then decode and return it
    msg_byt = secret_msg.to_bytes((secret_msg.bit_length())//8+1, sys.byteorder)
    msg = msg_byt.decode('latin-1')
    return msg
    

def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    message = receive_message(1984)
    print('received: %s' % message)


if __name__ == '__main__':
    main()
