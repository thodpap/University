; all commands: https://www.javatpoint.com/instruction-set-of-8086 
; https://www.includehelp.com/embedded-system/shift-and-rotate-instructions-in-8086-microprocessor.aspx 

; Caclulcate factorial (n) 
read:
    in CX, [0500] ; Cx = input
    mov AX, 0001   ; Accumulator = 1
    mov DX, 0000   ; DX = 0
factorial:    
    mul CX  ; DX:AX = AX * CX
    sub CX, 0001 ; Cx -= 1
    loop factorial ; loop until Cx = 0

mov [0600], AX
mov [0601], DX
hlt ; stop execution

; Calculate 1 + 2 + ... + n 
read:
    in CX, [0500]
    mov AX, 0000
sum:
    add AX, CX ; Ax += Cx
    sub CX,0001 ; Cx -= 1
    loop sum
mov [0600], AX
hlt

; find sum of 8 bit number
read:
    in CX, [0500]
    mov AX, 0000
count_sum_of_digits:
    mov DX, CX ; temp
    and DX, 0001; keep only last digit
    add AX, DX 
    shr CX, 1
    loop count_sum_of_digits ; loop until CX == 0000
mov [0600], AX
hlt

; 4 oktadiki arithmoi O3 O2 O1 O0 -> P = 8 O3 + O2 + 8*O1 + O0 
; Thema 3o (8086)

INCLUDE MACROS
DATA_SEG SEGMENT
    MSG1 DB 0AH,0DH, 'DOSE 1ο ARITHMO:$'
    MSG2 DB 0AH,0DH, 'DOSE 2ο ARITHMO:$'
    MSG3 DB 0AH,0DH, 'APOTELESMA= $'
DATA_SEG ENDS 

CODE_SEG SEGMENT
    ASSUME   CS:CODE_SEG, DS:DATA_SEG 

MAIN PROC FAR 
    MOV AX, DATA_SEG
    MOV DS, AX

ADDR1: 
    PRINT_STR MSG1 
    CALL DEC_KEYB
    cmp AL, 'Q'
    je QUIT
    MOV BL, 8
    MUL BL ; AL = AL * BL = AL * 8 -> O3 * 8
    mov BL, AL ; store high digit
    CALL OCT_KEYB
    cmp AL, 'Q'
    je quit
    add BL, AL ; O3 * 8 + O2 ; t
    
ADDR2:
    PRINT_STR MSG2
    CALL DEC_KEYB
    cmp AL, 'Q'
    je QUIT
    MOV CL, 8
    MUL CL ; AL = AL * CL = AL * 8 -> O1 * 8
    mov CL, AL ; store high digit
    CALL OCT_KEYB
    cmp AL, 'Q'
    je quit
    add CL, AL ; O1 * 8 + O0 ; 

Result:
    add CL, BL ; P 
    mov AX, CL
    mov BX, 16
    div BX ; div is on AX and remainder on DX
    ; HEX = AX * 16^1 + DX * 16^0

    PUSH AX
    CALL PRINT_HEX
    POP AX
    
QUIT: 
    EXIT
    MAIN endp
    CODE_SEG ENDS
    END MAIN
    
; thema 1 8085
START:  
    lda 2000H
    mov B,A 
    ani 01H
    jz FIRST_ZERO
    mov B,A
    ani 02H
    jz SECOND_ZERO
    jmp START
RESET:
    mvi D, 14H
FIRST_ZERO:
    dcr D
SECOND_ZERO:


Final: 
    mov A,B
    STA 3000H
    jmp START