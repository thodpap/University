;
; ask1_s.asm
;
; Created: 11/1/2021 8:31:08 PM
; Author : thodpap
;

;.include "m16def.inc"
; Replace with your application code 
ser r24
out DDRB, r24 ; B is output
clr r24
out DDRC, r24 ; C is input
	
start: 
	in r25, PINC ; xxxxDCBA, input
	mov r26, r25
	andi r26, 0x01 ; input & 0x01 -> A
	
	lsr r25 ; input is xxxxxDCB

	mov r24, r25 ; B
	andi r24, 0x01 ; 
	
	lsr r25 ; input is xxxx xxDC

	mov r23, r25 ; C
	andi r23, 0x01; 
	
	lsr r25 ; xxxx xxxD
	
	mov r22, r25 ; D
	andi r22, 0x01
	
F0:
	mov r16, r26 ; A
	mov r17, r24 ; B
	mov r18, r23 ; C
	mov r19, r22 ; D

	com r16; A'
	andi r16, 0x01

	and r16, r17 ; A' B

	com r17 ; B'
	andi r17, 0x01
	and r17, r18 ; B'C
	and r17, r19 ; B'CD

	or r16, r17 ; F0 = A'B | B'CD
	com r16  ; F0 = F0'
	andi r16, 0x01
	  

F1:
	and r26, r23 ; AC
	or r24, r22 ; B | D
	or r26, r24 ; Result of F1

	lsl r26

	or r16, r26 ; results of F1F0 

out PORTB, r16 ; result port B
rjmp start
	;;lsr 
