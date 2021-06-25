; all commands: http://ww1.microchip.com/downloads/en/devicedoc/atmel-0856-avr-instruction-set-manual.pdf
; fast commands: https://microchipdeveloper.com/8avr:alu
; http://www.rjhcoding.com/avr-asm-registers.php 

; DDRx - Data Direction Register
; PORTx - Pin Output Register
; PINx - Pin Input Register
; Where x = Port Name (A, B, C, D)

DDRA = 0x00;      //make PORTA all inputs 
PORTA = 0xFF;    //enable all pull-ups 
data = PINA;        //read PORTA pins into variable data

DDRB  = 0x00;        //make PORTB all inputs 
PORTB = 0x00;        //disable pull-ups and make all pins tri-state

DDRA  = 0x0F;        //lower pins output, higher pins input 
PORTA = 0xF0;        //output pins set to 0, input pins enable pull-ups

.include "m16def.inc"

ser r24 ; set register r24 = 0xFF
out DDRB, r24 ;B is output port
clr r24 ; clear register to r24 = 0x00
out DDRA, r24 ; A is input port
 
reset: 
    in r24 PINA ; Read input from PINA  ****DCBA 

    mov r25 r24  
    andi r25 0x01 ; Get A  
    lsr r24

    mov r26 r24 
    andi r26 0x01 ; Get B  
    lsr r24;

    mov r27 r24  
    andi r27 0x01 ; Get C to first bit
    lsr r24 

    mov r28 r24  
    andi r28 0x01 ; Get D to first bit 

F0: ; F0 = (ABC' + CD)' 
    mov r0 r25 ; A
    mov r1 r26 ; B
    mov r2 r27 ; C
    mov r3 r28 ; D

    ; A B C'
    and r0 r1 ; A * B
    mov r1 r2 ; Move C to r1 too
    neg r1 ; Compliment of C
    and r1 0x01 ; remove 1s 
    and r0 r1; (A*B) * C' 

    ; CD
    add r2 r3 

    or r0 r2 ; + 
    neg r0 ; compliement of the result
    and r0 0x01 ; keep result

F1: ; F1= (A+B)*(C+D)
    ; r25 r26 r27 r28
    or r25 r26 
    or r27 r28
    and r25 r27

FixAns:
    lsl r25 
    or r25 r0 ; F1 | F0  -> result on r25
    out PORTB r25 

    jmp reset 






sbis PIND,2 
rjmp init

K1:sbis PIND, 1
	rjmp W1
	ldi r16, 0x02
	out PORTB, r16
	rjmp A1

W1: sbis PIND, 4
	rjmp K1
	ldi r16, 0x02
	out PORTB, r16
	rjmp A1

init: sbis PIND,2
	rjmp init
	rjmp K1

A1: sbis PIND, 0
	rjmp A1

K0:sbis PIND, 3
	rjmp W2
	ldi r16, 0x01
	out PORTB, r16
	rjmp init
W2: sbis PIND, 4
	rjmp K0
	ldi r16, 0x01
	out PORTB, r16
	rjmp init

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
ser r24 ; set register r24 = 0xFF
out DDRB, r24 ;B is output port
clr r24 ; clear register to r24 = 0x00
out DDRB, r24 ; A is input port

ldi r17, 0x01; isogio check buttons
sbis PIND, 2 ; isogio check buttons
rjmp init ; else isiogio 
 
K1:sbis PIND, 1 ; isogio check buttons
	rjmp W1
	ldi r16, 0x02
	out PORTB, r16
	rjmp A1 

W1: sbis PIND, 4 ; first floor and W
	rjmp K1
	ldi r16, 0x02
	out PORTB, r16
	rjmp A1

init: sbis PIND,2 ; if floor zero 
   	out PORTB, r17

A0: : sbis PIND, 2  ; if first floor send 0 else check buttons
	rjmp A1	
	ldi r16, 0x00
	out PORTB, r16
	rjmp K1

A1: sbis PIND, 0 ; if first floor and read A1
	rjmp A0
	ldi r16, 0x00
	out PORTB, r16

K0:sbis PIND, 3 ; if first floor and read K0
	rjmp W2
   	out PORTB, r17
	rjmp init

W2: sbis PIND, 4 ; if first floor and read W
	rjmp K0
   	out PORTB, r17
	rjmp init


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

INCLUDE	MACROS

DATA_SEG	SEGMENT
	MSG1	DB 0AH,0DH, ‘DOSE 1o ARITHMO =  $'
	MSG2	DB 0AH,0DH, ‘DOSE 2o ARITHMO = $'
    MSG3	DB 0AH,0DH, ‘DOSE 3o ARITHMO = $'
    MSG4 	DB 0AH,0DH, ‘APOTELESMA = $'
    MSG5	DB 0AH,0DH, APOTELESMA = yperx$'
DATA_SEG	ENDS

CODE_SEG	SEGMENT
	ASSUME   CS:CODE_SEG, DS:DATA_SEG

MAIN	PROC	FAR
MOV	AX, DATA_SEG
MOV	DS, AX

MOV AX, DATA_SEG
MOV DS,AX

START:
    PRINT_STR MSG1
    CALL DEC_KEYB
    CMP AL,'Q'
    JE QUIT
    MOV BL,10
    MUL BL ; multiply first digit by 10 
    MOV BL,AL
    CALL DEC_KEYB
    CMP AL,'Q'
    JE QUIT
    ADD BL,AL ; add the number this way we create the first number in B

    PRINT_STR MSG2
    CALL DEC_KEYB 
    CMP AL,'Q'
    JE QUIT
    MOV DL,10
    MUL DL
    MOV DL,AL ; save the 3rd number

    PRINT_STR MSG3
    CALL DEC_KEYB
    CMP AL,'Q'
    JE QUIT
    ADD AL,DL ; add the 4th number
    MUL BL ; multiply with B
    MOV CX,4 ;counter =  4 for proper prints

Read_char:
    CALL DEC_KEYB ; read the h character
    CMP AL, 'h'
    JE CHECK 
    JMP QUIT

CHECK:  
    CMP 0400H ; check if we have overflow
    JL PRINT
    JMP OVERFLOW 


PRINT:
    PRINT_STR MSG4
    ROL AX,1 ; rotate AX once to get the LSB in the MSB position
    ROL AX,1
    ROL AX,1
    ROL AX,1
    MOV DL,AL
    AND DL,0FH ; we keep only the 4 lsb of DL, that are the 4 MSB's result that get printed each time
    PUSH AX
    CALL PRINT_HEX
    POP AX
    LOOP PRINT
    JMP START

OVERFLOW:
    PRINT_STR MSG5
    JMP ADDR1

QUIT: EXIT
    MAIN E