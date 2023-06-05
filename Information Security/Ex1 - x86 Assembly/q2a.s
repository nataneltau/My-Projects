# Declare the assembly flavor to use the intel syntax.
.intel_syntax noprefix

# Define a symbol to be exported from this file.
.global my_function

# Declare symbol type to be a function.
.type my_function, @function

# Code follows below.

my_function:
    # <<<< PUT YOUR CODE HERE >>>>
    # TODO:
    # 1. Read the input to the function from the stack.
    # 2. Save the result in the register EAX (and then return!).
    # 3. Make sure to include a recursive function call (the recursive function
    #    can be this function, or a helper function defined later in this file).
        
    MOV EDX, [ESP+4] #the n of the user input
        
    #basic cases n == 0 or n == 1
    CMP EDX, 0
    JLE _END_ZERO
        
    CMP EDX, 1
    JE _END_ONE
    
    #save EBP like in recitation
    PUSH EBP
    MOV EBP, ESP
    
    #calculate a_(n-1) using recurssion, so we sub 1 from EDX and save it because recurssion call might change register value and 
    #also we send that way the argument for the recurssion
    SUB EDX, 1
    PUSH EDX
    CALL my_function
    
    #recover old EDX value
    POP EDX
    
    #the result from recurssion are in EAX, save in EBX (a_(n-1))^2, again push because recurssion call might change register value and
    #also we send that way the argument for the recurssion
    MOV EBX, EAX
    IMUL EBX, EBX
    PUSH EBX
    
    #calculate a_(n-2) using recurssion
    SUB EDX, 1
    PUSH EDX
    CALL my_function
    
    POP EDX
    POP EBX
    
    #the result from recurssion are in EAX, save in EDX (a_(n-2))^2
    MOV EDX, EAX
    IMUL EDX, EDX
    
    #calculate a_n and save in EAX, then recover EBP like in recitation and return 
    MOV EAX, EDX
    ADD EAX, EBX
     
    MOV ESP, EBP
    POP EBP
    RET
    
    #for base cases
    _END_ZERO:
        MOV EAX, 0
        RET
        
    _END_ONE:
        MOV EAX, 1
        RET
    
