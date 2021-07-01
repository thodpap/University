
INCLUDE MACROS.ASM

DATA_SEG    SEGMENT
    NUM1    DB ?
    NUM2    DB ?
    NEWLINE DB 0AH,0DH,'$'
DATA_SEG    ENDS


CODE_SEG    SEGMENT
     ASSUME CS:CODE_SEG, DS:DATA_SEG
     
     
MAIN PROC FAR
START: 
    MOV AX,DATA_SEG
    MOV DS,AX
    MOV BX,0
    PRINT 'Z'
    PRINT '='
    CALL DEC_KEYB        ;Read the first num in ASCII
    SUB AL,30H           ;Change to decimal number (ADD 30H)
    MOV BL,10
    MUL BL
    MOV BX,AX            ;Multiply with 10 and store in BX (BL) because its the first digit
    CALL DEC_KEYB        ;Read second digit
    MOV AH,0
    SUB AL,30H
    ADD BX,AX            ;Add it to BX => Z
    MOV NUM1,BL
    
    PRINT ' '
    PRINT 'W'
    PRINT '='
    CALL DEC_KEYB        ;Read 1st digit of 2nd num and do the same for W
    SUB AL,30H
    MOV BL,10
    MUL BL
    MOV BX,AX
    CALL DEC_KEYB
    MOV AH,0
    SUB AL,30H
    ADD BX,AX
    MOV NUM2,BL
    
    MOV AH,0
    MOV BH,0
    MOV AL,NUM1
    MOV BL,NUM2
    ADD AX,BX             ;Add the numbers
    
    PUSH AX
    PRNT_STR NEWLINE      
    POP AX
    PRINT 'Z'
    PRINT '+'
    PRINT 'W'
    PRINT '='
    
    CALL PRINT_HEX        ;Print the result in HEX
    PRINT ' '             
    PRINT 'Z'
    PRINT '-'
    PRINT 'W'
    PRINT '='
    
    MOV AH,0
    MOV BH,0
    MOV AL,NUM1
    MOV BL,NUM2
    CMP AL,BL              ;Check if W>Z in order to print minus 
    JAE POSITIVE
    PRINT '-'
    SUB BX,AX
    MOV AX,BX
    JMP PRINT_SUB

POSITIVE:
    SUB AX,BX
PRINT_SUB:

    CALL PRINT_HEX         ;Print the result
    PUSH AX
    PRNT_STR NEWLINE
    POP AX
    JMP START
    
MAIN    ENDP
    
    
   


DEC_KEYB PROC NEAR
    
IGNORE:
    READ
    CMP AL,30H              ;Read and print the decimal digits
    JL IGNORE               ;If number not 0-9 then ignore
    CMP AL,39H
    JG IGNORE
    PRINT AL
    RET
DEC_KEYB    ENDP


PRINT_HEX PROC NEAR
    
    PUSH AX                 ;Print 2-digit HEX
    SAR AL,4                ;First MSBs
    AND AL,0FH
    CMP AL,9
    JG FIX1
    ADD AL,30H
    JMP PRINTN

FIX1:
    ADD AL,37H

PRINTN:
    PRINT AL
    

    POP AX
    AND AL,0FH              ;Then LSBs
    CMP AL,9
    JG FIX2
    ADD AL,30H
    JMP PRINTN1
    
FIX2:
    ADD AL,37H

PRINTN1:
    PRINT AL
    
    RET
PRINT_HEX   ENDP   

CODE_SEG    ENDS
    END MAIN