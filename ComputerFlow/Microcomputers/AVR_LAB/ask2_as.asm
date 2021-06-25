;
; AssemblerApplication1.asm
;
; Created: 5/16/2021 3:13:49 PM
; Author : Admin
;


.include "m16def.inc"

ser r24 
out DDRB, r24 ;B is output port
clr r24
out DDRA, r24 ; A is input port


reset:

	in r25, PINA ;xxxxDCBA, original
	mov r26, r25 
	andi r26, 0x01 ;for A
	lsr r25
	mov r24, r25
	andi r24, 0x01 ;for B
	lsr r25
	mov r23, r25
	andi r23, 0x01 ;for C
	lsr r25
	mov r22, r25 
	andi r22, 0x01 ;for D

F0:
	mov r0, r26 ;temp for A
	mov r1, r24 ;temp for B
	mov r2, r23 ;temp for C
	mov r3, r22 ;temp for D

	com r2
	and r0, r2 ; AC'

	and r0, r1 ;ABC'

	com r2
	and r2, r3 ;CD

	or r0, r2 ;ABC'+CD
	com r0 ;result of F0
	mov r16, r0
	andi r16, 0x01

nop

F1:
	or r26, r24 ;A+B
	or r23, r22 ;C+D
	and r26, r23 ;result of F1

	lsl r26
	or r16, r26 ; results ofr F1,F0 to the to LSB's of port B
	

out PORTB, r16 ;result to port B
jmp reset

