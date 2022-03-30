/*
 * ask3.c
 *
 * Created: 11/2/2021 10:18:14 PM
 * Author : thodpap
 */ 

#define F_CPU 8000000UL

#include <avr/io.h>
#include <avr/interrupt.h> 

ISR(INT0_vect)
{ 
	// 1000 0001
	// PA2 ON ->  PORTC : 0000 0010
	// PA2 OFF -> PORTC : 0000 0011
	char A = PINA;
	char input = PINB;
	
	/*  i = 1, 2, 4, 8, 16, 32, 64, 128
		j = 0, 1, 2, 3, 4,  5,  6,  7
		
		input & i save the j-th digit 0..010...0 >> j -> 1 
										0..000...0 >> j -> 0
			
		if 0 then count += 0
		if 1 then count += 1
	*/
	int count = 0;
	for(int i = 1, j = 0; i < (1 << 8); i *= 2, ++j) { 
		count += (input & i) >> j;
	} 
	if (A & 0x04) { // if PA2 is ON transform to binary
		int t = 0;
		for(int i = 0; i < count; ++i) {
			t *= 2; // 000000 -> 000001 -> 0000010 + 1-> 0000011 -> 0000110 + 1 0000111 
			t += 1;
		}
		count = t;
	} // else if PA2 is OFF just keep the counter as it is
	PORTC = count;
}

int main(void)
{
	DDRA = 0x00; // A input
	DDRB = 0x00; // B input
	DDRC = 0xff; //	C output 
	
	GICR = 1<<INT0;		/* Enable INT0*/
	MCUCR = (1<<ISC01) | (1<<ISC00);  /* Trigger INT0 on rising edge */
	asm("sei");			/* Enable Global Interrupt */
	
    while (1) {
		asm("nop");
	}
}

