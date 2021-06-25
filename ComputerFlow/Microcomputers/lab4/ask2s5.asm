
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
    CALL DEC_KEYB
    SUB AL,30H
    MOV BL,10
    MUL BL
    MOV BX,AX
    CALL DEC_KEYB
    MOV AH,0
    SUB AL,30H
    ADD BX,AX
    MOV NUM1,BL
    
    PRINT ' '
    PRINT 'W'
    PRINT '='
    CALL DEC_KEYB
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
    ADD AX,BX
    
    PUSH AX
    PRNT_STR NEWLINE
    POP AX
    PRINT 'Z'
    PRINT '+'
    PRINT 'W'
    PRINT '='
    
    CALL PRINT_HEX
    PRINT ' '
    PRINT 'Z'
    PRINT '-'
    PRINT 'W'
    PRINT '='
    
    MOV AH,0
    MOV BH,0
    MOV AL,NUM1
    MOV BL,NUM2
    CMP AL,BL
    JAE POSITIVE
    PRINT '-'
    SUB BX,AX
    MOV AX,BX
    JMP PRINT_SUB

POSITIVE:
    SUB AX,BX
PRINT_SUB:

    CALL PRINT_HEX
    PUSH AX
    PRNT_STR NEWLINE
    POP AX
    JMP START
    
MAIN    ENDP
    
    
   


DEC_KEYB PROC NEAR
    
IGNORE:
    READ
    CMP AL,30H
    JL IGNORE
    CMP AL,39H
    JG IGNORE
    PRINT AL
    RET
DEC_KEYB    ENDP


PRINT_HEX PROC NEAR
    
    PUSH AX
    SAR AL,4
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
    AND AL,0FH
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