
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
    
    MOV AL,128
    MOV DI,0

STORE:
    MOV [TABLE+DI],AL
    DEC AL
    INC DI
    CMP DI,128
    JNE STORE
    
    
    MOV DX,0
    MOV DI,1
    MOV AX,0
    
SUM:
    MOV AL,[TABLE+DI]
    ADD DX,AX
    
    ADD DI,2
    CMP DI,129
    JNE SUM
    
    MOV AX,DX
    MOV DX,0
    MOV CX,64
    DIV CX
    MOV DX,AX
    MOV AVERAGE,DL
    
    
    MOV MAX,0
    MOV MIN,128
    MOV DI,0
    
MIN_MAX:
    MOV AL,[TABLE+DI]
    CMP MIN,AL
    JNA DO_MAX
    MOV MIN,AL
    
DO_MAX:
    CMP MAX,AL
    JAE SKIP
    MOV MAX,AL
    
SKIP:
    INC DI
    CMP DI,128
    JNE MIN_MAX 
    
    
    MOV AL,AVERAGE
    MOV AH,0
    MOV CX,0

BCD: 
    MOV DX,0
    MOV BX,10
    DIV BX
    PUSH DX
    INC CX
    CMP AX,0
    JNE BCD 
    
    
ADDR3:
    POP DX
    ADD DX,30H
    PRINT DL
    LOOP ADDR3
    
    PRNT_STR NEWLINE 
    
    MOV AL,MIN
    SAR AL,4
    AND AL,0FH
    CALL PRINT_HEX
    MOV AL,MIN
    AND AL,0FH
    CALL PRINT_HEX 
    PRINT 'H'
    PRINT ' '
    
    MOV AL,MAX
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
    ADD AL,30H
    JMP ADDR2
    
FIX:
    ADD AL,37H
ADDR2:
    PRINT AL
    RET
PRINT_HEX ENDP

CODE_SEG    ENDS
    END MAIN
    
    
    
    