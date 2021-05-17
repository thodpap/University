/*
 * main.c
 *
 * Created: 5/16/2021 7:09:28 PM
 *  Author: Admin
 */ 

#include <xc.h>
#include <avr/io.h>

int main(void){
	
	DDRA = 0xFF; //port A output
	DDRC = 0x00; // port C input (SWx's)
	char led;
	
	led = 0x01;
	PORTA = led;
	
	
	while(1){
		
		if((PINC & 0x01) == 1){
			while((PINC & 0x01) == 1){}
			if(led == 128){
				led = 0x01; // led = 1 if before led == 128
			}
			else led = led << 1;
		}
		
		if((PINC & 0x02) == 2){
			while((PINC & 0x02) == 2){}
			if(led == 1){
				led = 1 << 7; // led = 128 if before led == 0
			}
			else led = led >> 1;
		}
		
		if((PINC & 0x04) == 4){
			while((PINC & 0x04) == 4){}
			led = 1 << 7;
		}
		
		if((PINC & 0x08) == 8){
			while((PINC & 0x08) == 8){}
			led = 0x01;
		}
		
		PORTA = led;
	}
	
}