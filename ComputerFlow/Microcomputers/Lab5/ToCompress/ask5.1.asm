
INCLUDE MACROS.ASM

DATA_SEG    SEGMENT
    TABLE   DB 128 DUP(?)
    AVERAGE DB ?             
    MIN     DB ?
    MAX     DB ?
    NEWLINE DB 0AH,0DH,'$'
DATA_SEG    ENDS


CODE_SEG    SEGMENT
    ASSUME CS:CODE_SEG, DS:DATA_SEG



MAIN PROC FAR
    MOV AX,DATA_SEG
    MOV DS,AX
    
    MOV AL,128      ;ак = 128
    MOV DI,0

STORE:
    MOV [TABLE+DI],AL    ;Fill table with numbers: 128-1
    DEC AL
    INC DI
    CMP DI,128           ;Check if 128, entire table is filled
    JNE STORE
    
    
    MOV DX,0
    MOV DI,1            ;calculating the avg of the odd numbers
    MOV AX,0
    
SUM:
    MOV AL,[TABLE+DI]
    ADD DX,AX           ;DX contains the sum
    
    ADD DI,2
    CMP DI,129
    JNE SUM
    
    MOV AX,DX
    MOV DX,0
    MOV CX,64
    DIV CX              ;Divide sum with 64
    MOV DX,AX
    MOV AVERAGE,DL
    
    
    MOV MAX,0
    MOV MIN,128
    MOV DI,0
    
MIN_MAX:
    MOV AL,[TABLE+DI]   ;Calculate min and max 
    CMP MIN,AL          ;If number >MIN check if it can be max
    JNA DO_MAX
    MOV MIN,AL          ;else do the number the new min
    
DO_MAX:
    CMP MAX,AL          ;If number <MAX skip
    JAE SKIP
    MOV MAX,AL          ;else number is the new max
    
SKIP:
    INC DI              ;Check next number
    CMP DI,128          
    JNE MIN_MAX 
    
    
    MOV AL,AVERAGE
    MOV AH,0
    MOV CX,0

BCD: 
    MOV DX,0
    MOV BX,10
    DIV BX
    PUSH DX             ;Continuous divisions with 10 while pushing the result in the stack
    INC CX
    CMP AX,0
    JNE BCD 
    
    
ADDR3:
    POP DX              ;Pop the results of the div from last to first and print 
    ADD DX,30H
    PRINT DL
    LOOP ADDR3
    
    PRNT_STR NEWLINE 
    
    MOV AL,MIN
    SAR AL,4
    AND AL,0FH          ;Keep the 4 MSBs, print in HEX
    CALL PRINT_HEX
    MOV AL,MIN
    AND AL,0FH          ;Print LSBs in HEX
    CALL PRINT_HEX 
    PRINT 'H'
    PRINT ' '
    
    MOV AL,MAX          ;Same for max
    SAR AL,4
    AND AL,0FH
    CALL PRINT_HEX
    MOV AL,MAX
    AND AL,0FH
    CALL PRINT_HEX 
    PRINT 'H' 
    
    EXIT 

MAIN    ENDP

PRINT_HEX PROC NEAR
    CMP AL,9
    JG FIX
    ADD AL,30H      ;If num is >9 then add 30H
    JMP ADDR2
    
FIX:
    ADD AL,37H      ;else add 37H for the correct ASCII
ADDR2:
    PRINT AL
    RET
PRINT_HEX ENDP

CODE_SEG    ENDS
    END MAIN
    
    
    
    