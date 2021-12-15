;
; AssemblerApplication1.asm
;
; Created: 11/19/2021 7:38:26 PM
; Author : Admin
;
; ---- ���� �������� ���������
.DSEG
_tmp_: .byte 2
; ---- ����� �������� ���������

.CSEG
.include "m16def.inc"

.def GPreg1=r18 ;general purpose register1
.def GPreg2=r19 ;general purpose register2
.def counter=r20 ;general purpose counter
.def Cx=r17
.def level=r16
.def on_off=r21
.def lcd_flag=r28

.macro CHECK_IF_ZERO
;macro prokeimenou na mhn grafoume sunexeia 
;ean einai mhden oi r25,r24
	cpi r24,0x00

	brne END_NOT_EQUAL
	cpi r25,0x00

	brne END_NOT_EQUAL

	ldi GPreg1,0x01 ;true
	rjmp END
	
	END_NOT_EQUAL:
	ldi GPreg1,0x00 ;false

	END:
.endm

.macro CHECK_FOR_VALID_r24

	cpi r24,@0
	brne NOT_EQUAL

	ldi GPreg2,0x01 ;true
	rjmp END1

	NOT_EQUAL:
	ldi GPreg2,0x00 ;false

	END1:
.endm

.macro SET_LEDS_ON
push r18
ser r18
out PORTB,r18
pop r18
.endm

.macro SET_LEDS_OFF
push r20
clr r20
out PORTB,r20
pop r20
.endm



.macro WELCOME_USER
	
	rcall lcd_init_sim

	push r25
	push r24
	
	ldi lcd_flag, 0x02

	clr r24
	out TIMSK, r24

	cpi level, 0x04
	brlt MHN_SBHSA_OLA
	ldi r25, 0x80
	out PORTB, r25
	rjmp lets_write

	MHN_SBHSA_OLA:
	in r25, PINB
	ori r25, 0x80
	out PORTB, r25

	lets_write:

	ldi r24,'W'
	rcall lcd_data_sim ; �������� ���� byte ��������� ���� ������� ��� ������ lcd
	ldi r24,'E'
	rcall lcd_data_sim
	ldi r24,'L'
	rcall lcd_data_sim
	ldi r24,'C'
	rcall lcd_data_sim
	ldi r24,'O'
	rcall lcd_data_sim
	ldi r24,'M'
	rcall lcd_data_sim
	ldi r24,'E'
	rcall lcd_data_sim
	ldi r24,' '
	rcall lcd_data_sim
	ldi r24,'2'
	rcall lcd_data_sim
	ldi r24,'1'
	rcall lcd_data_sim
	
	ldi r24,low(4000)
	ldi r25,high(4000)
	rcall wait_msec			; DELAY 4 SECONDS (MACRO)
	
	in r25, PINB
	andi r25, 0x7F
	out PORTB, r25

	pop r24

	ldi r25, (1 << TOIE1)
	out TIMSK, r25

	pop r25
	
	ldi lcd_flag, 0x02
.endm

.macro WRONG_PASSWORD
	push r25
	push r24

	in r24, PINB
	ori r24, 0x80
	out PORTB, r24

	ldi r24,low(500)
	ldi r25,high(500)
	rcall wait_msec
	
	in r24, PINB
	andi r24, 0x7F
	out PORTB, r24

	ldi r24,low(500)
	ldi r25,high(500)
	rcall wait_msec
	
	
	in r24, PINB
	ori r24, 0x80
	out PORTB, r24

	ldi r24,low(500)
	ldi r25,high(500)
	rcall wait_msec
	
	
	in r24, PINB
	andi r24, 0x7F
	out PORTB, r24

	ldi r24,low(500)
	ldi r25,high(500)
	rcall wait_msec

	in r24, PINB
	ori r24, 0x80
	out PORTB, r24

	ldi r24,low(500)
	ldi r25,high(500)
	rcall wait_msec
	
	in r24, PINB
	andi r24, 0x7F
	out PORTB, r24

	ldi r24,low(500)
	ldi r25,high(500)
	rcall wait_msec
	
	
	in r24, PINB
	ori r24, 0x80
	out PORTB, r24

	ldi r24,low(500)
	ldi r25,high(500)
	rcall wait_msec
	
	
	in r24, PINB
	andi r24, 0x7F
	out PORTB, r24

	ldi r24,low(500)
	ldi r25,high(500)
	rcall wait_msec
	
	ldi lcd_flag, 0x02

	pop r24
	pop r25
.endm	
	

.macro GAS_DETECTED

	push r24

	cpi lcd_flag, 0x00
	breq END_GAS_DETECTED
	rcall lcd_init_sim
	ldi lcd_flag, 0x00

	ldi r24,'G'
	rcall lcd_data_sim ; �������� ���� byte ��������� ���� ������� ��� ������ lcd
	ldi r24,'A'
	rcall lcd_data_sim
	ldi r24,'S'
	rcall lcd_data_sim
	ldi r24,' '
	rcall lcd_data_sim
	ldi r24,'D'
	rcall lcd_data_sim
	ldi r24,'E'
	rcall lcd_data_sim
	ldi r24,'T'
	rcall lcd_data_sim
	ldi r24,'E'
	rcall lcd_data_sim
	ldi r24,'C'
	rcall lcd_data_sim
	ldi r24,'T'
	rcall lcd_data_sim
	ldi r24,'E'
	rcall lcd_data_sim
	ldi r24,'D'
	rcall lcd_data_sim
	ldi r24,'!'
	rcall lcd_data_sim

	END_GAS_DETECTED:

	pop r24
.endm

.macro CLEAR
	push r24

	cpi lcd_flag, 0x01
	breq END_CLEAR
	rcall lcd_init_sim
	ldi lcd_flag, 0x01

	ldi r24,'C'
	rcall lcd_data_sim ; �������� ���� byte ��������� ���� ������� ��� ������ lcd
	ldi r24,'L'
	rcall lcd_data_sim
	ldi r24,'E'
	rcall lcd_data_sim
	ldi r24,'A'
	rcall lcd_data_sim
	ldi r24,'R'
	rcall lcd_data_sim

	END_CLEAR:

	pop r24
.endm

.macro TIMER1_INIT
	push r24

	ldi r24 ,(1<<TOIE1) ; ������������ �������� ������������ ��� ������� TCNT1
	out TIMSK ,r24 ; ��� ��� timer1
	ldi r24 ,(1<<CS12) | (0<<CS11) | (1<<CS10) ; CK/1024
	out TCCR1B ,r24 
	ldi r24,0xFC ; ������������ ��� TCNT1
	out TCNT1H ,r24 ; ��� ����������� ���� ��� 5 sec
	ldi r24 ,0xF3
	out TCNT1L ,r24
	clr r24
	
	pop r24
.endm

.macro ADC_INIT
	push r24

	ldi r24, 0x40
	out ADMUX, r24
	ldi r24, (1<<ADEN)|(1<<ADIE)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0)
	out ADCSRA, r24
	clr r24

	pop r24
.endm



.org 0x00
rjmp start
.org 0x10
rjmp TIMER1_INTERRUPT
.org 0x1C
rjmp ADC_INTERRUPT


; Replace with your application code
start:
	ldi r24, low(RAMEND)
		out SPL, r24

	ldi r24, high(RAMEND)
		out SPH, r24

    
	ser r24 ; r24 = FF
	out DDRB, r24 ; initialize  port b 
	out DDRD, r24 ; and d for output


	clr r24
	ldi r24, (1 << PC7) | (1 << PC6) | (1 << PC5) | (1 << PC4) ; ����� �� ������� �� 4 MSB
	out DDRC, r24 ; ��� ����� PORTC

	ldi lcd_flag, 0x02

	ADC_INIT
	TIMER1_INIT

	
 	 
	sei

	clr on_off

	rcall lcd_init_sim

PROGRAM:

	clr r24
	clr r25


	
	
	LOOP:
	rcall scan_keypad_rising_edge_sim

	CHECK_IF_ZERO ;check if r25 == 0 & r24 == 0
	cpi GPreg1,0x01
	breq LOOP

	
	rcall keypad_to_ascii_sim
	

	CHECK_FOR_VALID_r24 '2'
	sbrs GPreg2, 0
	rjmp ABORT
	


	LOOP1:
	rcall scan_keypad_rising_edge_sim

	CHECK_IF_ZERO ;check if r25 == 0 & r24 == 0
	cpi GPreg1,0x01
	breq LOOP1

	movw r26,r24 ;temporary regs for result
	rcall keypad_to_ascii_sim

	CHECK_FOR_VALID_r24 '1'
	cpi GPreg2,0x00
	breq ABORT

	WELCOME_USER

	rjmp PROGRAM

	ABORT:

	WRONG_PASSWORD
	
	rjmp PROGRAM


	ADC_INTERRUPT:
	push r26
	push r25
	push r24
	push r23
	push r22
	in r25, ADCL
	in r26, ADCH
	andi r26, 0x03
	cpi r26, 0x03
	breq seven_leds_on_off
	cpi r26, 0x02
	breq six_leds_on_off
	cpi r26, 0x01
	breq five_leds_on_off
	cpi r25, 0xCE
	brsh four_leds_on_off
	cpi r25, 0x7E
	brsh three_leds_on
	cpi r25, 0x49
	brsh two_leds_on

	one_led_on:
	CLEAR
	ldi level, 0x01
	in r22, PINB
	andi r22, 0x80
	ori r22, 0x01
	out PORTB, r22
	rjmp END_ADC

	six_leds_on_off:
	rjmp six_leds_on_off1

	five_leds_on_off:
	rjmp five_leds_on_off1

	four_leds_on_off:
	rjmp four_leds_on_off1

	three_leds_on:
	rjmp three_leds_on1

	two_leds_on:
	rjmp two_leds_on1

	seven_leds_on_off:
	GAS_DETECTED
	ldi level, 0x07
	in r22, PINB
	andi r22, 0x80
	cpi on_off, 0x00
	breq write_on_seven
	out PORTB, r22
	ldi on_off, 0x00
	rjmp END_ADC

	write_on_seven:
	ori r22, 0x7F
	out PORTB, r22
	ldi on_off, 0x01
	rjmp END_ADC


	six_leds_on_off1:
	GAS_DETECTED
	ldi level, 0x06
	in r22, PINB
	andi r22, 0x80
	cpi on_off, 0x00
	breq write_on_six
	out PORTB, r22
	ldi on_off, 0x00
	rjmp END_ADC

	write_on_six:
	ori r22, 0x3F
	out PORTB, r22
	ldi on_off, 0x01
	rjmp END_ADC


	five_leds_on_off1:
	GAS_DETECTED
	ldi level, 0x05
	in r22, PINB
	andi r22, 0x80
	cpi on_off, 0x00
	breq write_on_five
	out PORTB, r22
	ldi on_off, 0x00
	rjmp END_ADC

	write_on_five:
	ori r22, 0x1F
	out PORTB, r22
	ldi on_off, 0x01
	rjmp END_ADC

	four_leds_on_off1:
	GAS_DETECTED
	ldi level, 0x04
	in r22, PINB
	andi r22, 0x80
	cpi on_off, 0x00
	breq write_on_four
	out PORTB, r22
	ldi on_off, 0x00
	rjmp END_ADC

	write_on_four:
	ori r22, 0x0F
	out PORTB, r22
	ldi on_off, 0x01
	rjmp END_ADC


	three_leds_on1:
	CLEAR
	ldi level, 0x03
	in r22, PINB
	andi r22, 0x80
	ori r22, 0x07
	out PORTB, r22
	rjmp END_ADC


	two_leds_on1:
	CLEAR
	ldi level, 0x02
	in r22, PINB
	andi r22, 0x80
	ori r22, 0x03
	out PORTB, r22

	END_ADC:
	pop r22
	pop r23
	pop r24
	pop r25
	pop r26

	reti


	TIMER1_INTERRUPT:
	push r26
	push r25
	push r24

	in r26, ADCSRA
	ldi r25, (1 << ADSC)
	or r26, r25
	out ADCSRA, r26
	ldi r24,0xFC ; ������������ ��� TCNT1
	out TCNT1H ,r24 ; ��� ����������� ���� ��� 5 sec
	ldi r24 ,0xF3
	out TCNT1L ,r24
	
	pop r24
	pop r25
	pop r26

	reti


	scan_row_sim:
	out PORTC, r25 ; � ���������� ������ ������� ��� ������ �1�
	push r24 ; ����� ������ ��� ����������� ��� �� �����
	push r25 ; ���������� ��� ������������ ��������������
	ldi r24,low(500) ; ���������
	ldi r25,high(500)
	rcall wait_usec
	pop r25
	pop r24 ; ����� ����� ������
	nop
	nop ; ����������� ��� �� �������� �� ����� � ������ ����������
	in r24, PINC ; ����������� �� ������ (������) ��� ��������� ��� ����� ���������
	andi r24 ,0x0f ; ������������� �� 4 LSB ���� �� �1� �������� ��� ����� ���������
	ret ; �� ���������

	scan_keypad_sim:
	push r26 ; ���������� ���� ����������� r27:r26 ����� ����
	push r27 ; ��������� ���� ���� �������
	ldi r25 , 0x10 ; ������ ��� ����� ������ ��� ������������� (PC4: 1 2 3 A)
	rcall scan_row_sim
	swap r24 ; ���������� �� ����������
	mov r27, r24 ; ��� 4 msb ��� r27
	ldi r25 ,0x20 ; ������ �� ������� ������ ��� ������������� (PC5: 4 5 6 B)
	rcall scan_row_sim
	add r27, r24 ; ���������� �� ���������� ��� 4 lsb ��� r27
	ldi r25 , 0x40 ; ������ ��� ����� ������ ��� ������������� (PC6: 7 8 9 C)
	rcall scan_row_sim
	swap r24 ; ���������� �� ����������
	mov r26, r24 ; ��� 4 msb ��� r26
	ldi r25 ,0x80 ; ������ ��� ������� ������ ��� ������������� (PC7: * 0 # D)
	rcall scan_row_sim
	add r26, r24 ; ���������� �� ���������� ��� 4 lsb ��� r26
	movw r24, r26 ; �������� �� ���������� ����� ����������� r25:r24
	clr r26 ; ���������� ��� ��� ������������� ��������
	out PORTC,r26 ; ���������� ��� ��� ������������� ��������
	pop r27 ; ��������� ���� ����������� r27:r26
	pop r26
	ret

	scan_keypad_rising_edge_sim:
	push r22 ; ���������� ���� ����������� r23:r22 ��� ����
	push r23 ; r26:r27 ����� ���� ��������� ���� ���� �������
	push r26
	push r27
	rcall scan_keypad_sim ; ������ �� ������������ ��� ���������� ���������
	push r24 ; ��� ���������� �� ����������
	push r25
	ldi r24 ,15 ; ����������� 15 ms (������� ����� 10-20 msec ��� ����������� ��� ���
	ldi r25 ,0 ; ������������ ��� ������������� � ������������� ������������)
	rcall wait_msec
	rcall scan_keypad_sim ; ������ �� ������������ ���� ��� ��������
	pop r23 ; ��� ������� ���������� �����������
	pop r22
	and r24 ,r22
	and r25 ,r23
	ldi r26 ,low(_tmp_) ; ������� ��� ��������� ��� ��������� ����
	ldi r27 ,high(_tmp_) ; ����������� ����� ��� �������� ����� r27:r26
	ld r23 ,X+
	ld r22 ,X
	st X ,r24 ; ���������� ��� RAM �� ��� ���������
	st -X ,r25 ; ��� ���������
	com r23
	com r22 ; ���� ���� ��������� ��� ����� ������ �������
	and r24 ,r22
	and r25 ,r23
	pop r27 ; ��������� ���� ����������� r27:r26
	pop r26 ; ��� r23:r22
	pop r23
	pop r22
	ret 

	keypad_to_ascii_sim:
	push r26 ; ���������� ���� ����������� r27:r26 ����� ����
	push r27 ; ��������� ���� ��� �������
	movw r26 ,r24 ; ������ �1� ���� ������ ��� ���������� r26 ��������
	; �� �������� ������� ��� ��������
	ldi r24 ,'*'
	; r26
	;C 9 8 7 D # 0 *
	sbrc r26 ,0
	rjmp return_ascii
	ldi r24 ,'0'
	sbrc r26 ,1
	rjmp return_ascii
	ldi r24 ,'#'
	sbrc r26 ,2
	rjmp return_ascii
	ldi r24 ,'D'
	sbrc r26 ,3 ; �� ��� ����� �1������������ ��� ret, ������ (�� ����� �1�)
	rjmp return_ascii ; ���������� �� ��� ���������� r24 ��� ASCII ���� ��� D.
	ldi r24 ,'7'
	sbrc r26 ,4
	rjmp return_ascii
	ldi r24 ,'8'
	sbrc r26 ,5
	rjmp return_ascii
	ldi r24 ,'9'
	sbrc r26 ,6
	rjmp return_ascii ;
	ldi r24 ,'C'
	sbrc r26 ,7
	rjmp return_ascii
	ldi r24 ,'4' ; ������ �1� ���� ������ ��� ���������� r27 ��������
	sbrc r27 ,0 ; �� �������� ������� ��� ��������
	rjmp return_ascii
	ldi r24 ,'5'
	;r27
	;� 3 2 1 B 6 5 4
	sbrc r27 ,1
	rjmp return_ascii
	ldi r24 ,'6'
	sbrc r27 ,2
	rjmp return_ascii
	ldi r24 ,'B'
	sbrc r27 ,3
	rjmp return_ascii
	ldi r24 ,'1'
	sbrc r27 ,4
	rjmp return_ascii ;
	ldi r24 ,'2'
	sbrc r27 ,5
	rjmp return_ascii
	ldi r24 ,'3' 
	sbrc r27 ,6
	rjmp return_ascii
	ldi r24 ,'A'
	sbrc r27 ,7
	rjmp return_ascii
	clr r24
	rjmp return_ascii
	return_ascii:
	pop r27 ; ��������� ���� ����������� r27:r26
	pop r26
	ret 

	write_2_nibbles_sim:
	push r24 ; ����� ������ ��� ����������� ��� �� �����
	push r25 ; ���������� ��� ������������ ��������������
	ldi r24 ,low(6000) ; ���������
	ldi r25 ,high(6000)
	rcall wait_usec
	pop r25
	pop r24 ; ����� ����� ������
	push r24 ; ������� �� 4 MSB
	in r25, PIND ; ����������� �� 4 LSB ��� �� �������������
	andi r25, 0x0f ; ��� �� ��� ��������� ��� ����� ����������� ���������
	andi r24, 0xf0 ; ������������� �� 4 MSB ���
	add r24, r25 ; ������������ �� �� ������������ 4 LSB
	out PORTD, r24 ; ��� �������� ���� �����
	sbi PORTD, PD3 ; ������������� ������ Enable ���� ��������� PD3
	cbi PORTD, PD3 ; PD3=1 ��� ���� PD3=0
	push r24 ; ����� ������ ��� ����������� ��� �� �����
	push r25 ; ���������� ��� ������������ ��������������
	ldi r24 ,low(6000) ; ���������
	ldi r25 ,high(6000)
	rcall wait_usec
	pop r25
	pop r24 ; ����� ����� ������
	pop r24 ; ������� �� 4 LSB. ��������� �� byte.
	swap r24 ; ������������� �� 4 MSB �� �� 4 LSB
	andi r24 ,0xf0 ; ��� �� ��� ����� ���� �������������
	add r24, r25
	out PORTD, r24
	sbi PORTD, PD3 ; ���� ������ Enable
	cbi PORTD, PD3
	ret

	lcd_data_sim:
	push r24
	push r25
	sbi PORTD,PD2
	rcall write_2_nibbles_sim
	ldi r24,43
	ldi r25,0
	rcall wait_usec
	pop r25
	pop r24
	ret

	lcd_command_sim:
	push r24 ; ���������� ���� ����������� r25:r24 ����� ����
	push r25 ; ��������� ���� ��� �������
	cbi PORTD, PD2 ; ������� ��� ���������� ������� (PD2=0)
	rcall write_2_nibbles_sim ; �������� ��� ������� ��� ������� 39�sec
	ldi r24, 39 ; ��� ��� ���������� ��� ��������� ��� ��� ��� ������� ��� lcd.
	ldi r25, 0 ; ���.: �������� ��� �������, �� clear display ��� return home,
	rcall wait_usec ; ��� �������� ��������� ���������� ������� ��������.
	pop r25 ; ��������� ���� ����������� r25:r24
	pop r24
	ret 

	lcd_init_sim:
	push r24 ; ���������� ���� ����������� r25:r24 ����� ����
	push r25 ; ��������� ���� ��� �������

	ldi r24, 40 ; ���� � �������� ��� lcd ������������� ��
	ldi r25, 0 ; ����� ������� ��� ���� ��� ������������.
	rcall wait_msec ; ������� 40 msec ����� ���� �� �����������.
	ldi r24, 0x30 ; ������ ��������� �� 8 bit mode
	out PORTD, r24 ; ������ ��� �������� �� ������� �������
	sbi PORTD, PD3 ; ��� �� ���������� ������� ��� �������
	cbi PORTD, PD3 ; ��� ������, � ������ ������������ ��� �����
	ldi r24, 39
	ldi r25, 0 ; ��� � �������� ��� ������ ��������� �� 8-bit mode
	rcall wait_usec ; ��� �� ������ ������, ���� �� � �������� ���� ����������
	; ������� 4 bit �� ������� �� ���������� 8 bit
	push r24 ; ����� ������ ��� ����������� ��� �� �����
	push r25 ; ���������� ��� ������������ ��������������
	ldi r24,low(1000) ; ���������
	ldi r25,high(1000)
	rcall wait_usec
	pop r25
	pop r24 ; ����� ����� ������
	ldi r24, 0x30
	out PORTD, r24
	sbi PORTD, PD3
	cbi PORTD, PD3
	ldi r24,39
	ldi r25,0
	rcall wait_usec 
	push r24 ; ����� ������ ��� ����������� ��� �� �����
	push r25 ; ���������� ��� ������������ ��������������
	ldi r24 ,low(1000) ; ���������
	ldi r25 ,high(1000)
	rcall wait_usec
	pop r25
	pop r24 ; ����� ����� ������
	ldi r24,0x20 ; ������ �� 4-bit mode
	out PORTD, r24
	sbi PORTD, PD3
	cbi PORTD, PD3
	ldi r24,39
	ldi r25,0
	rcall wait_usec
	push r24 ; ����� ������ ��� ����������� ��� �� �����
	push r25 ; ���������� ��� ������������ ��������������
	ldi r24 ,low(1000) ; ���������
	ldi r25 ,high(1000)
	rcall wait_usec
	pop r25
	pop r24 ; ����� ����� ������
	ldi r24,0x28 ; ������� ���������� �������� 5x8 ��������
	rcall lcd_command_sim ; ��� �������� ��� ������� ���� �����
	ldi r24,0x0c ; ������������ ��� ������, �������� ��� �������
	rcall lcd_command_sim
	ldi r24,0x01 ; ���������� ��� ������
	rcall lcd_command_sim
	ldi r24, low(1530)
	ldi r25, high(1530)
	rcall wait_usec
	ldi r24 ,0x06 ; ������������ ��������� ������� ���� 1 ��� ����������
	rcall lcd_command_sim ; ��� ����� ������������ ���� ������� ����������� ���
	; �������������� ��� ��������� ��������� ��� ������
	pop r25 ; ��������� ���� ����������� r25:r24
	pop r24
	ret
	wait_msec:
	push r24				; 2 ������ (0.250 �sec)
	push r25				; 2 ������
	ldi r24 , low(998)		; ������� ��� �����. r25:r24 �� 998 (1 ������ - 0.125 �sec)
	ldi r25 , high(998)		; 1 ������ (0.125 �sec)
	rcall wait_usec			; 3 ������ (0.375 �sec), �������� �������� ����������� 998.375 �sec
	pop r25					; 2 ������ (0.250 �sec)
	pop r24					; 2 ������
	sbiw r24 , 1			; 2 ������
	brne wait_msec			; 1 � 2 ������ (0.125 � 0.250 �sec)
	ret						; 4 ������ (0.500 �sec)

	wait_usec:
	sbiw r24 ,1			; 2 ������ (0.250 �sec)
	nop					; 1 ������ (0.125 �sec)
	nop					; 1 ������ (0.125 �sec)
	nop					; 1 ������ (0.125 �sec)
	nop					; 1 ������ (0.125 �sec)
	brne wait_usec		; 1 � 2 ������ (0.125 � 0.250 �sec)
	ret					; 4 ������ (0.500 �sec)


	