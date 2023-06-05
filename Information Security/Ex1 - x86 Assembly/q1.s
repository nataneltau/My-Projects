# Declare the assembly flavor to use the intel syntax.
.intel_syntax noprefix

# Define a symbol to be exported from this file.
.global my_function

# Declare symbol type to be a function.
.type my_function, @function

# Code follows below.

my_function:
    # This code reads the first argument from the stack into EBX.
    # (If you need, feel free to edit/remove this line).
    MOV EBX, DWORD PTR [ESP + 4]

    # <<<< PUT YOUR CODE HERE >>>>
    # TODO:
    # 1. Read the input to the function from EBX.
    # 2. Save the result in the register EAX.
    
    
    MOV ECX, 0 #counter to our loop
    
    #in the loop we check for every ECX if ECX*ECX=EBX if so it's sqrt(EBX) else if 
    #there is no such sqrt (or the EBX == 0) we will get overflow at some point, and EDX will be negative and we will retrun 0
    _LOOP:
    INC ECX
    MOV EDX, ECX
    IMUL EDX, EDX
    CMP EDX, EBX
    JE _END
    CMP EDX, 0
    JGE _LOOP #jump if EDX >= 0
    
    MOV EAX, 0
    RET
    
    _END:
    MOV EAX, ECX
    RET
    # This returns from the function (call this after saving the result in EAX).
    # (If you need, feel free to edit/remove this line).
    
