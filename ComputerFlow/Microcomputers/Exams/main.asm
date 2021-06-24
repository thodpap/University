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




