INCLUDE MACROS.ASM



DATA_SEG    SEGMENT
    STRING DB 20 DUP(?)
    NEWLINE DB 0AH,0DH,'$'
DATA_SEG ENDS

CODE_SEG SEGMENT
    ASSUME CS:CODE_SEG, DS:DATA_SEG
    
MAIN PROC FAR

   
    MOV AX,DATA_SEG
    MOV DS,AX
        
START:
      
    MOV CX,20
    MOV DI,0
    
INITIALIZATION:
    MOV [STRING+DI],0
    INC DI                      ;Initialization with 0s in case we press ENTER mid-way and to delete everything from last run
    LOOP INITIALIZATION
    
    MOV CX,20                   ;Loop for 20 chars          
    MOV DI,0
    MOV DX,0
                 
INPUT:
    CALL GET_CHAR               ;Read char
    CMP AL,0DH 
    JE AUXILIARY                ;If enter go to auxiliary
    MOV [STRING+DI],AL          ;Else store in table String
    INC DI                      
    LOOP INPUT                  ;Loop 
        
    
AUXILIARY:    
    MOV CX,DX                   ;DX has the number of chars
    MOV DI,0
DISPLAY:
    PRINT [STRING+DI]           ;Print the chars
    INC DI
    LOOP DISPLAY                ;Loop for the num of chars
    
    PRNT_STR NEWLINE
        
    MOV CX,DX
    INC CX
    MOV DI,0
    
CHARACTERS:
    MOV AL,[STRING+DI]          ;Load the chars
    INC DI
    DEC CX
    CMP CX, 00H                 ;If we reached 0 then stop
    JZ  CONTINUE
    CMP AL,'a'                  ;If the char is a letter
    JL CHARACTERS
    CMP AL,'z'
    JG CHARACTERS
    SUB AL,20H                  ;Subtract 20H to make it upper 
    PRINT AL                    ;Print it
    JMP CHARACTERS
    
CONTINUE:                       ;Now for the numbers
    PRINT '-'
    MOV DI,0
    MOV CX,DX
    INC CX

NUMBERS:
    MOV AL,[STRING+DI]
    INC DI
    DEC CX
    CMP CX,00H
    JZ CONTINUE2                ;If char is num then print it
    CMP AL,30H
    JL NUMBERS
    CMP AL,39H
    JG NUMBERS
    PRINT AL
    JMP NUMBERS

CONTINUE2:
            
    PRNT_STR NEWLINE
    JMP START

QUIT:
    EXIT
MAIN ENDP        
    
             

GET_CHAR PROC NEAR
IGNORE:
    READ
    CMP AL,3DH                  ;If char is = then quit
    JE QUIT
    CMP AL,0DH                  ;Char must be either ENTER or Number or small letter
    JE OK 
    CMP AL,30H
    JL IGNORE
    CMP AL,39H
    JG CHECK_LETTER
    JMP OK
    
CHECK_LETTER:
    CMP AL,'a'
    JL IGNORE
    CMP AL,'z'
    JG IGNORE

OK: 
    INC DX                      ;Num of chars read
    RET
GET_CHAR ENDP

CODE_SEG    ENDS
    END MAIN