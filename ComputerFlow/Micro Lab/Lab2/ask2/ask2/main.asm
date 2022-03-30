
.org 0x0
		rjmp reset
.org 0x4
		rjmp ISR1

reset:	
	ldi r24, (1<<ISC11)|(1<<ISC10)
	out MCUCR, r24
	ldi r24, (1<<INT1)
	out GICR, r24
	sei
	clr r31	; initialize interrupt 

	ldi r24 , low(RAMEND) ; initialize stack
	out spl , r24
	ldi r24 , high(RAMEND)
	out sph , r24


	ser r26
	out DDRC, r26	; count up to 255
	out DDRB, r26	; count interrupt
	clr r26
	out DDRA, r26	; Read from PA
	out DDRD, r26	; read pind

loop:	
	out PORTC, r26	; count loop
	inc r26			; increase counter
	rjmp loop


ISR1:	
	inc r31	; push stack
	push r26		; INT1 service routine
	in r26, SREG
	push r26

	in r30, PINA	; get input
	andi r30, 0xc0	; is PA7A6  11 ?
	cpi r30, 0xc0	; 
	brne skip		; 
	mov r26, r31	;  
	rjmp getout
skip:	
	clr r26			 
getout:	
	out	PORTB, r26
	
	pop r26 ;; restore stack
	out SREG, r26
	pop r26
	reti