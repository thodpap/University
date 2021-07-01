INCLUDE MACROS.ASM

PRINT_DEC MACRO
    PUSH AX
    ADD DL,30H
    MOV AH,2
    INT 21H
    POP AX
ENDM

DATA_SEG    SEGMENT
    MSG1     DB "START (Y, N):",0AH,0DH,'$'
    ERROR    DB "ERROR",0AH,0DH,'$'
    NUMBER1 DB ?
    NUMBER2 DB ?
    NUMBER3 DB ?
    TEMP    DB "TEMP IS: ",'$'
    NEWLINE DB 0AH,0DH,'$'
DATA_SEG    ENDS



CODE_SEG    SEGMENT
    ASSUME CS:CODE_SEG, DS:DATA_SEG
    

MAIN PROC FAR
    
    MOV AX,DATA_SEG
    MOV DS,AX
    PRNT_STR MSG1
    CALL YES_NO         ;Wait for 'Y'
    
    CMP AL,'N'
    JE QUIT             ;If 'N' QUIT
    
    
START:
    MOV AX,0
    MOV BX,0
    
    CALL READ_HEX       ;Read the first digit
    CMP AL,'N'
    JE QUIT
    MOV BH,AL           ;Store in BH
    
    CALL READ_HEX
    CMP AL,'N'
    JE QUIT
    AND AL,0FH          ;Second digit shifted left 4 times in BL
    SAL AL,4
    MOV BL,AL
    
    CALL READ_HEX
    CMP AL,'N'
    JE QUIT
    AND AL,0FH          ;Third digit added in BL, now BX has the bits
    ADD BL,AL
    
    MOV AX,BX
    
    CMP AX,3071         ;If bits > 3071 then it is ERROR
    JG IS_ERROR
    
    CMP AX,800H         ;If bits <= 800H = 2048 then it is in region 1
    JLE REGION1
    
REGION2:                ;Else in region 2
    MOV BX,8000
    MUL BX              ;Multiply with 8000 (800*10*bits) 
    MOV BX,1024
    DIV BX              ;Divide the res with 1024 
    MOV BX,12000        ;Subtract 12000
    SUB AX,BX
    PUSH AX             ;Store T = 8000*bits/1024 - 12000
    PRNT_STR TEMP       
    POP AX
    CALL PRINT_TEMP     ;Print the Temperature
    JMP START 


REGION1:
    MOV BX,1000         ;T = 1000*bits/511
    MUL BX
    MOV BX,511
    DIV BX
    PUSH AX
    PRNT_STR TEMP
    POP AX
    CALL PRINT_TEMP     ;Print the temperature
    JMP START
     
    
IS_ERROR:
    PRNT_STR ERROR
    JMP START
    
QUIT:
    EXIT
        
    
MAIN    ENDP


YES_NO PROC NEAR
IGNORE:
    READ
    CMP AL,'Y'             ;Ignore everything except Y or N
    JE OK
    CMP AL,'N'
    JE OK
    JMP IGNORE
OK:
    RET
YES_NO  ENDP


READ_HEX PROC NEAR
IGNORE1:
    READ
    CMP AL,30H              ;Read hex numbers in correct form or N for QUIT
    JL IGNORE1
    CMP AL,39H
    JG CHECK1
    SUB AL,30H
    JMP OK1
   
CHECK1:
    CMP AL,'N'
    JE OK1
    CMP AL,'A'
    JL IGNORE1
    CMP AL,'F'
    JG IGNORE1
    SUB AL,37H
    
OK1:
    RET
READ_HEX    ENDP


PRINT_TEMP PROC NEAR
    PUSH AX
    MOV CX,0                
DECI:
    MOV DX,0
    MOV BX,10             ;Divide with 10
    DIV BX
    PUSH DX               ;Store ones,tens,hunds
    INC CX
    CMP AX,0
    JNE DECI              ;If it is not the last digit repeat
    
    DEC CX                  
    CMP CX,0              ;If there was only one digit then print 0 and print the digit after ','
    JNE PRNT2
    PRINT '0'
    JMP LAST
    
PRNT2:                    
    POP DX                ;Print the all the digits except from the last one
    PRINT_DEC
    LOOP PRNT2
    
LAST:
    PRINT ','             ;Print ',' and print the last digit
    POP DX
    PRINT_DEC
    
    PRINT ' '
    PRINT 0F8H
    PRINT 'C'
    PRNT_STR NEWLINE
    
    POP AX
    
    RET
PRINT_TEMP  ENDP

CODE_SEG    ENDS
    END MAIN
    