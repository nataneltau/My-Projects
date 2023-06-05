from scapy.all import *


LOVE = 'love'
unpersons = set()


def spy(packet):
    """Check for love packets.

    For each packet containing the word 'love', add the sender's IP to the
    `unpersons` set.

    Notes:
    1. Use the global LOVE as declared above.
    """
    # TODO: IMPLEMENT THIS FUNCTION
    #raise NotImplementedError()
    #print(unpersons)
    #check if pakcet is TCP
    if packet.haslayer(TCP):
        #read it's data, cause why not
        data_packet = str(packet[TCP].payload)
        if LOVE in data_packet:#check if LOVE inside his data
            #print("hi")
            unpersons.add(packet[IP].src)
    
    #print(unpersons)


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    sniff(iface=get_if_list(), prn=spy)


if __name__ == '__main__':
    main()
