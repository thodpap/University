;
; AssemblerApplication1.asm
;
; Created: 5/16/2021 3:13:49 PM
; Author : Admin
;


.include "m16def.inc"

reset:
	ser r24 
	out DDRA, r24 ;A is output port
	clr r24
	out DDRB, r24 ;B is input port
	ldi r25, 0x01
	;r24 is our counter for led position

; Replace with your application code
left:
	in r26, PINB ;read B port (input port)
	andi r26, 0x01 ;isolate first bit (PB0)
	cpi r26, 0x01 
	breq left ;if 1 do nothing
	out PORTA, r25 ;else continue process
	inc r24 ;increase counter
	lsl r25 ;logical shift left
	cpi r24, 0x07 ;if counter == 7 then we jump to right which will open PA7 (we already did lsl) and then will do logical shift right
	breq right
	rjmp left
	;nop



right:
	in r26, PINB ;read B port (input port)
	andi r26, 0x01 ;isolate first bit (PB0)
	cpi r26, 0x01 
	breq right ;if 1 do nothing
	out PORTA, r25 ;else continue process
	dec r24 ;decrease counter
	lsr r25 ;logical shift right
	cpi r24, 0x00 ;if counter == 1 then we jump to left which will open PA0 (we already did lsr) and then will do logical shift left
	breq left
	rjmp right
	;nop



