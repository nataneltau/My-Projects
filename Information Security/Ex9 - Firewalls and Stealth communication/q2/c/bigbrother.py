import math
from scapy.all import *


LOVE = 'love'
unpersons = set()


def spy(packet):
    """Check for love packets and encrypted packets.

    For each packet containing the word 'love', or a packed which is encrypted,
    add the sender's IP to the `unpersons` set.

    Notes:
    1. Use the global LOVE as declared above.
    """
    # TODO: IMPLEMENT THIS FUNCTION
    #raise NotImplementedError()
    #print(unpersons)
    #this is the entropy limit 
    high_entropy = 3.0
    #check if pakcet is TCP
    if packet.haslayer(TCP):
        #read it's data, cause why not
        data_packet = str(packet[TCP].payload)
        if LOVE in data_packet:#check if LOVE inside his data
            #print("hi")
            unpersons.add(packet[IP].src)
        
        #check if shannon_entropy higher than high_entropy
        elif shannon_entropy(data_packet) > high_entropy:
            #print("x")
            unpersons.add(packet[IP].src)
    
    #print(unpersons)


def shannon_entropy(string: str) -> float:
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    distribution = [float(string.count(c)) / len(string)
                    for c in set(string)]
    return -sum(p * math.log(p) / math.log(2.0) for p in distribution)


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    sniff(iface=get_if_list(), prn=spy)


if __name__ == '__main__':
    main()
