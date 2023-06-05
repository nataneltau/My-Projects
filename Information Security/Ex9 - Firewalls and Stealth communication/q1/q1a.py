from scapy.all import *
from typing import List, Iterable


OPEN = 'open'
CLOSED = 'closed'
FILTERED = 'filtered'


def generate_syn_packets(ip: str, ports: List[int]) -> list:
    """
    Returns a list of TCP SYN packets, to perform a SYN scan on the given
    TCP ports.

    Notes:
    1. Do NOT add any calls of your own to send/receive packets.
    """
    # TODO: IMPLEMENT THIS FUNCTION
    #raise NotImplementedError()
    #will store packets here
    result_packets = []
    
    for port in ports:
        ip_syn_pack = IP(dst = ip) #desired ip
        #desired port, syn packet
        tcp_syn_pack = TCP(dport = port, flags = 'S')
        pack = ip_syn_pack / tcp_syn_pack
        #add packet to list
        result_packets.append(pack)
    
    #list contain packets with ports from ports list and ip equal
    #to ip argument
    return result_packets 
    


def analyze_scan(ip: str, ports: List[int], answered: Iterable, unanswered: Iterable) -> dict:
    """Analyze the results from `sr` of SYN packets.

    This function returns a dictionary from port number (int), to
    'open' / 'closed' / 'filtered' (strings), based on the answered and unanswered
    packets returned from `sr`.

    Notes:
    1. Use the globals OPEN / CLOSED / FILTERED as declared above.
    """
    # TODO: IMPLEMENT THIS FUNCTION
    results = dict()
    
    #syn ack flag is SA
    open_flag = 'SA'
    
    #in answered we have the packet we sent and the answer we got for them
    for sent_packet, received_packet in answered:
        #the flag we got back
        flags = received_packet[TCP].flags
        
        if flags == open_flag:#this port is open
            results[received_packet[TCP].sport] = OPEN
        else:#this port is close
            results[received_packet[TCP].sport] = CLOSED
    
    for orgin_packet in unanswered:#there is only the packet we sent
        results[orgin_packet[TCP].dport] = FILTERED
    
    return results
    #raise NotImplementedError()


def stealth_syn_scan(ip: str, ports: List[int], timeout: int):
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    packets = generate_syn_packets(ip, ports)
    answered, unanswered = sr(packets, timeout=timeout)
    return analyze_scan(ip, ports, answered, unanswered)


def main(argv):
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    if not 3 <= len(argv) <= 4:
        print('USAGE: %s <ip> <ports> [timeout]' % argv[0])
        return 1
    ip = argv[1]
    ports = [int(port) for port in argv[2].split(',')]
    if len(argv) == 4:
        timeout = int(argv[3])
    else:
        timeout = 5
    results = stealth_syn_scan(ip, ports, timeout)
    for port, result in results.items():
        print('port %d is %s' % (port, result))


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
