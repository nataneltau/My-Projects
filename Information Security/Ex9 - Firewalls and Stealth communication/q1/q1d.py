from scapy.all import *


def on_packet(packet):
    """Implement this to send a SYN ACK packet for every SYN.

    Notes:
    1. Use *ONLY* the `send` function from scapy to send the packet!
    """
    # TODO: IMPLEMENT THIS FUNCTION
    #raise NotImplementedError()
    #not a tcp syn packet
    if TCP not in packet or packet[TCP].flags != 'S':
        return
    
    #let's create a packet that will look like
    #a normal behavior and send it to the sender
    ip_syn_pack = IP(dst = packet[IP].src)#send back to the sender
    #the flag need to be SA like in normal situation
    tcp_syn_pack = TCP(sport = packet[TCP].dport , dport = packet[TCP].sport, flags = 'SA', seq = packet[TCP].ack, ack = packet[TCP].seq + 1)
    pack = ip_syn_pack / tcp_syn_pack
    send(pack)
    
    
def main(argv):
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    sniff(prn=on_packet)


if __name__ == '__main__':
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    import sys
    sys.exit(main(sys.argv))
