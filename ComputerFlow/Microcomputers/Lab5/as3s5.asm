

INCLUDE MACROS.ASM

DATA_SEG    SEGMENT
    NEW_LINE    DB 0AH,0DH,'$'
DATA_SEG    ENDS


CODE_SEG    SEGMENT
    ASSUME CS:CODE_SEG, DS:DATA_SEG
    
MAIN PROC FAR
    
    MOV AX,DATA_SEG
    MOV DS,AX
    
    CALL HEX_KEYB
    CMP AL,'T'
    JE QUIT
    MOV BH,AL
    CALL HEX_KEYB
    CMP AL,'T'
    JE QUIT
    MOV BL,AL
    AND BL,0FH
    SAL BL,4
    CALL HEX_KEYB
    CMP AL,'T'
    JE QUIT
    ADD BL,AL
    
    PUSH BX
    AND BH,0FH
    CMP BH,9
    JG FIX1
    ADD BH,30H
    JMP PRINTF
    
FIX1:
    ADD BH,37H
    
PRINTF:
    PRINT BH
    
    POP BX
    
    PUSH BX
    SAR BL,4
    AND BL,0FH
    CMP BL,9
    JG FIX2
    ADD BL,30H
    JMP PRINTF1
    
FIX2:
    ADD BL,37H
    
PRINTF1:
    PRINT BL
    
    POP BX
    
    PUSH BX
    AND BL,0FH
    CMP BL,9
    JG FIX3
    ADD BL,30H
    JMP PRINTF2
    
FIX3:
    ADD BL,37H
    
PRINTF2:
    PRINT BL
    
    PRINT 'H'
    
    POP BX
    PRINT ' '
    PRINT '='
    CALL PRINT_DEC
    
    PRINT ' '
    PRINT '='
    CALL PRINT_OCT
    
    PRINT ' '
    PRINT '='
    CALL PRINT_BIN
    PRNT_STR NEW_LINE
    JMP MAIN
    
QUIT:
    EXIT
         
MAIN ENDP

PRINT_DEC PROC NEAR
    PUSH AX
    PUSH CX
    PUSH BX
    PUSH DX
    
    MOV CX,1
    
    MOV AX,BX
    MOV BX,10
    
DIV1:
    MOV DX,0
    DIV BX
    PUSH DX
    CMP AX,0
    JE PRNT_10
    INC CX
    JMP DIV1
    
PRNT_10:
    POP DX
    ADD DL,30H
    PRINT DL
    LOOP PRNT_10
    
    PRINT 'D'
    
    POP DX
    POP BX
    POP CX
    POP AX
    RET
PRINT_DEC   ENDP


PRINT_OCT PROC NEAR
    
    PUSH AX
    PUSH CX
    PUSH BX
    PUSH DX
    
    MOV CX,1
    
    MOV AX,BX
    MOV BX,8
    
DIV2:
    MOV DX,0
    DIV BX
    PUSH DX
    CMP AX,0
    JE PRNT_8
    INC CX
    JMP DIV2
    
PRNT_8:
    POP DX
    ADD DL,30H
    PRINT DL
    LOOP PRNT_8
    
    PRINT 'o'
    
    POP DX
    POP BX
    POP CX
    POP AX
    RET
PRINT_OCT   ENDP


PRINT_BIN PROC NEAR
    
     PUSH AX
     PUSH CX
     PUSH BX
     PUSH DX
     
     MOV CX,1
     
     MOV AX,BX
     MOV BX,2
     
DIV3:
    MOV DX,0
    DIV BX
    PUSH DX
    CMP AX,0
    JE PRNT_2
    INC CX
    JMP DIV3
    
PRNT_2:
    POP DX
    ADD DL,30H
    PRINT DL
    LOOP PRNT_2
    
    PRINT 'B'
    
    POP DX
    POP BX
    POP CX
    POP AX
    RET
PRINT_BIN   ENDP


HEX_KEYB PROC NEAR


IGNORE:    
    READ
    CMP AL,30H        ; if input < 30H ('0') then ignore it
    JL IGNORE
    CMP AL,39H        ; if input > 39H ('9') then it may be a hex letter
    JG CHECK_LETTER
    SUB AL,30H        ; otherwise make it a hex number
    JMP INPUT_OK
 
CHECK_LETTER:
    CMP AL,'T'        ; if input = 'Q', then return to quit
    JE INPUT_OK
    CMP AL,'A'        ; if input < 'A' then ignore it
    JL IGNORE         
    CMP AL,'F'        ; if input > 'F' then ignore it
    JG IGNORE
    SUB AL,37H        ; otherwise make it a hex number
    
INPUT_OK:          
    RET  
HEX_KEYB ENDP


CODE_SEG    ENDS
    END MAIN   