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
    MOV ECX, [ESP+4] #the n of the user input
    
    #basic cases n == 0 or n == 1
    CMP ECX, 0
    JLE _END_ZERO
        
    CMP ECX, 1
    JE _END_ONE
     
    #EDX will represent a_(n-2), EBX will represent a_(n-1)
    MOV EBX, 1
    MOV EDX, 0

    _LOOP:
        #each iteration we calculate a_k, if k == n (we subtract 1 from ECX each iteration) 
        #then we return a_k, else we save a_k in EBX, a_(k-1) in EDX and move to the next iteration
            
        PUSH EBX
        IMUL EBX, EBX #calculate (a_(k-1))^2
        MOV EAX, EBX
        POP EBX #need to save this value because we might use it for EDX in the next iteration
        
        PUSH EDX
        IMUL EDX, EDX #calculate (a_(k-2))^2
        ADD EAX, EDX #now EAX has a_k
        POP EDX
        
        MOV EDX, EBX # now EDX has a_(k-1)
        MOV EBX, EAX # now EBX has a_k
        
        SUB ECX, 1 #lower by one
        CMP ECX, 1 #when ECX == 1 we done
        JNE _LOOP
    
    RET
        
        
    #for base cases
    _END_ZERO:
        MOV EAX, 0
        RET
        
    _END_ONE:
        MOV EAX, 1
        RET
