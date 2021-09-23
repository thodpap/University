;; Let's suppose we want to make a LED run from left to right
;; DDRA is output and DDRB is input

.include "m16def.inc"

reset:
    ser r24       ; r24 = 0xFF ; ser: set all bits in register
    out DDRA, r24 ; A is ouptut
    clr r24; r24 = 0x00 ; clr: clear all bits in register
    out DDRB, r24 ; B is input 

    ldi r25, 0x01 ; load 1 on r25
    ;r24 is our counter for led position ;; initially here it is 0

;
left: 
    in r26, PINB ; read port B ; input as xxxx xxxx
    andi r26, 0x01 ; Isolate PB0  ; r26:  0000 000x
    cpi r26, 0x01  ; compare r26 with 0x01
    breq left ; if r26 = 0x01 then jump to right

    out PORTA, r25 
    inc r24 ; increment our counter
    lsl r25 ; logical shift left -> from 0000 0010 -> 0000 0100 -> 0000 1000 etc
    cpi r24, 0x07 
    breq right ; if counter has counted 7 times then jump to right
    rjmp left ; else jump left

right:
    in r26, PINB
    andi r26, 0x01; 
    cpi r26, 0x01
    breq right
    
    out PORTA, r25
    dec r24 
    lsr r25 
    cpi r24, 0x00
    breq left
    rjmp right
