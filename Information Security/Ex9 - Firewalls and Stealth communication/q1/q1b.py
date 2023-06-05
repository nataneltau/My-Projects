import time
import os
from scapy.all import *


WINDOW = 60
MAX_ATTEMPTS = 15


# Initialize your data structures here
# TODO: Initialize your data structures


blocked = set()  # We keep blocked IPs in this set
ip_check = dict() #dict to save the times we saw the ip's

def on_packet(packet):
    """This function will be called for each packet.

    Use this function to analyze how many packets were sent from the sender
    during the last window, and if needed, call the 'block(ip)' function to
    block the sender.

    Notes:
    1. You must call block(ip) to do the blocking.
    2. The number of SYN packets is checked in a sliding window.
    3. Your implementation should be able to efficiently handle multiple IPs.
    """
    # TODO: IMPLEMENT THIS FUNCTION
    #raise NotImplementedError()
    
    #not a stealth syn attack
    if TCP not in packet or packet[TCP].flags != 'S':
        return
    
    #it's the first time this ip send syn
    if not packet[IP].src in ip_check:
        #add the ip to dict
        ip_check[packet[IP].src] = [time.time()]
        return
    
    lst = ip_check[packet[IP].src]
    curr_time = time.time()
    #iterate through all items in list and check it there are
    #times that are earlier than WINDOW ago, delete them
    for item in lst:
        if curr_time - item > WINDOW: #more than 60 seconds
            lst.remove(item)
        else:#all the times after are later
            break
    #add currect time to the list and update dict
    lst.append(curr_time)
    ip_check[packet[IP].src] = lst
    
    if len(lst) >= 15:#check if need to block this ip
        block(packet[IP].src)
        ip_check.pop(packet[IP].src)#remove ip from dict, it block now


def generate_block_command(ip: str) -> str:
    """Generate a command that when executed in the shell, blocks this IP.

    The blocking will be based on `iptables` and must drop all incoming traffic
    from the specified IP."""
    # TODO: IMPLEMENT THIS FUNCTION
    #raise NotImplementedError()
    
    #like did in question 1a in the other VM
    cmd = "sudo iptables -A INPUT -s " + ip + " -j DROP"
    return cmd

def block(ip):
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    os.system(generate_block_command(ip))
    blocked.add(ip)


def is_blocked(ip):
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    return ip in blocked


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    sniff(prn=on_packet)


if __name__ == '__main__':
    main()
