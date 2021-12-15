/*
 * Avr3Ask2.c
 *
 * Created: 12/12/2021 10:02:18 PM
 * Author : thodpap
 */ 

#define F_CPU 8000000			// FREQUENCY OF ATMEGA16
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

/* Functions Declarations */
static void SUCCESS();
static void BLINK_FAIL();

static unsigned char scan_row(int i);
static unsigned char swap(unsigned char x);
static void scan_keypad();
static int scan_keypad_rising_edge();
static unsigned char keypad_to_ascii();
static unsigned char calculate_LED(void);
static int calculate_cx ();
void ADC_init(void);

/* Global Variables */
unsigned char mem[2], key_reg[2];
unsigned char first, second; // first: First key and second: Second Key; 
static int Cx = 0; // CO concentration in ppm
static unsigned char leds = 0x00, flag_MSB = 0x00, blink_flag = 0, success_flag = 0;
int count = 0;


ISR(ADC_vect) { // ADC Interrupt routine
	Cx = calculate_cx();
	leds = calculate_LED();
	
	PORTB = flag_MSB << 7; // LEDS Off
	if (Cx > 70 && blink_flag)
		PORTB |= leds;
	else if (Cx <= 70){
		PORTB |= leds;
	}
}

ISR(TIMER1_OVF_vect) {
	ADCSRA |= (1<<ADSC);          // Start the next conversion
	TCNT1 = 64755;						//Timer set to overflow in 100 msec
	TCCR1B = (1<<CS12) | (0<<CS11) | (1<<CS10); // Start again.
	
	if (count == 2) // Here we change the flag for the alarm (Blink_flag) every 2 Timer Interrupts
	{
		blink_flag = !blink_flag;
		if (success_flag == 1)
		blink_flag = 1; // HUGE_flag Turns ON only when we are in SUCCESS Mode (Correct password Typed) So we by pass Blink_flag to carry leds ON.
		count = 0;
	}
	++count;
}


int main(void)
{
    DDRB = 0xFF;        // PORTB => OUTPUT
    DDRC = 0xF0;        // KEYPAD: PORTC[7:4] => OUTPUT, PORTC[3:0] => INPUT
    
	ADC_init();
	
	TIMSK = (1 << TOIE1); //Timer1 ,interrupt enable
	TCCR1B = (1<<CS12) | (0<<CS11) | (1<<CS10);	//frequency of Timer1 8MHz/1024
	TCNT1 = 64755;		//Timer set to overflow in 100 msec

	asm("sei");				// enable interupts
	
    while (1) { 	    
	    mem[0] = 0;    // INITIALIZE RAM
	    mem[1] = 0;
	    PORTB = 0; 
	    
	    while (!scan_keypad_rising_edge()) {}
		first = keypad_to_ascii();  
		
	    // GET SECOND DIGIT
		while(!scan_keypad_rising_edge()){}
		second = keypad_to_ascii();
		
		if (first == '2' && second == '1') {
			SUCCESS();
		} else {
			BLINK_FAIL();
		}
    }
}

void SUCCESS() {
	success_flag = 1;
	flag_MSB = 1;
	PORTB = 0x80 | leds;
	_delay_ms(4000);
	PORTB = 0x00 | leds;
	flag_MSB = 0;
	success_flag = 0;
}

void BLINK_FAIL() {
	for (int i = 0; i < 4; ++i) {
		flag_MSB = 1;
		PORTB = 0x80 | leds; // 0xff;
		_delay_ms(500);
		
		flag_MSB = 0;
		PORTB = 0x00 | leds;
		_delay_ms(500);
	}
} 
 
unsigned char scan_row(int i) {   // i = 1,2,3,4
	unsigned char a = ( 1 << 3 ); // SKIP 3 LSB
	a = (a << i);			// SELECT ROW ACCORDING TO FUNCTION INPUT i
	PORTC = a;				// WE SELECT ROW BY SETTING CORRESPONDING BIT TO 1
	_delay_us(500);			// DELAY FOR REMOTE USAGE
	return PINC & 0x0F;		// WE READ THE 4 LSB, '1' INDICATES SWITCH PUSHED
}

/* FUNCTION TO SWAP LO WITH HO BITS */
unsigned char swap(unsigned char x) {
	return ((x & 0x0F) << 4 | (x & 0xF0) >> 4);
}

/* SCAN ROWS(1..4) *DIFFERENT ORDER FROM EXERSISE DOCUMENT*
* FIRST ROW: PC4->PC0: 1,  PC4->PC1: 2,  PC4->PC2: 3, PC4->PC3: A
* SECOND ROW: PC5->PC0: 4,  PC5->PC1: 5,  PC5->PC2: 6, PC5->PC3: B
* THIRD ROW: PC6->PC0: 7,  PC6->PC1: 8,  PC6->PC2: 9, PC6->PC3: C
* FOURTH ROW: PC7->PC0: *,  PC7->PC1: 0,  PC7->PC2: #, PC7->PC3: D
*/
void scan_keypad() {
	unsigned char i;
	
	// check row 1, 0b0001-ROW CORRESPONDING TO PC4
	i = scan_row(1);
	key_reg[1] = swap(i);	//key_reg[1] = first_row(4 MSB)-0000
	
	// check row 2, 0b0010-ROW CORRESPONDING TO PC5
	i = scan_row(2);
	key_reg[1] += i;		//key_reg[1] = first_row(4 MSB)-second_row(4 LSB)
	
	// check row 3, 0b0100-ROW CORRESPONDING TO PC6
	i = scan_row(3);
	key_reg[0] = swap(i);	//key_reg[0] = third_row(4 MSB) -0000
	
	// check row 4, 0b1000-ROW CORRESPONDING TO PC7
	i = scan_row(4);
	key_reg[0] += i;		//key_reg[0] = third_row(4 MSB)-fourth_row(4 LSB)
	PORTC = 0x00;			// added for remote usage
}

int scan_keypad_rising_edge() {
	// CHECK KEYPAD
	scan_keypad();						// RETURNS RESULTS IN key_reg
	// ADD TEMPORARY VARIABLES
	unsigned char tmp_keypad[2];
	tmp_keypad[0] = key_reg[0];			//tmp_keypad HOLD ACQUIRED DATA FROM SCAN_KEYPAD()
	tmp_keypad[1] = key_reg[1];
	
	_delay_ms(0x15);					// APOFYGH SPINTHIRISMOU
	
	
	scan_keypad();
	key_reg[0] &= tmp_keypad[0];		// APPORIPSE TIS TIMES POU EMFANISAN SPINTHIRISMO
	key_reg[1] &= tmp_keypad[1];
	
	tmp_keypad[0] = mem[0];				// BRING LAST STATE OF SWITCHES FROM RAM TO tmp_keypad
	tmp_keypad[1] = mem[1];
	
	mem[0] = key_reg[0];				// STORE NEW KEYPAD STATE IN RAM FOR FUTURE CALL
	mem[1] = key_reg[1];
	
	
	key_reg[0] &= ~tmp_keypad[0];		// FIND KEYPAD SWITCHES THAT HAVE JUST BEEN PRESSED
	key_reg[1] &= ~tmp_keypad[1];
	
	return (key_reg[0] || key_reg[1]); // 16 BIT VALUE INDICATING FRESHLY PRESSED SWITCHES - RETURNS 0 IF NO SWITCH PRESSED
}

/* CONVERT VALUE TO ASCII CODE *CHECK COMMENT ABOVE SCAN_KEYPAD FOR CORRESPONDENCE
* key_reg[0] = third_row(4 MSB)-fourth_row(4 LSB)
* key_reg[1] = first_row(4 MSB)-second_row(4 LSB)
* LSB -> MSB == LEFT -> RIGHT IN KEYPAD */
unsigned char keypad_to_ascii() {
	if (key_reg[0] & 0x01)
		return '*';
	
	if (key_reg[0] & 0x02)
		return '0';
	
	if (key_reg[0] & 0x04)
		return '#';
	
	if (key_reg[0] & 0x08)
		return 'D';
	
	if (key_reg[0] & 0x10)
		return '7';
	
	if (key_reg[0] & 0x20)
		return '8';
	
	if (key_reg[0] & 0x40)
		return '9';
	
	if (key_reg[0] & 0x80)
		return 'C';
	
	if (key_reg[1] & 0x01)
		return '4';
	
	if (key_reg[1] & 0x02)
		return '5';
	
	if (key_reg[1] & 0x04)
		return '6';
	
	if (key_reg[1] & 0x08)
		return 'B';
	
	if (key_reg[1] & 0x10)
		return '1';
	
	if (key_reg[1] & 0x20)
		return '2';
		
	if (key_reg[1] & 0x40)
		return '3';
	
	if (key_reg[1] & 0x80)
		return 'A';
	
	// Nothing Found
	return 0;
}


unsigned char calculate_LED(void){
	if (Cx < 30) 
		return 0x01; // if   0 <= CO < 30 ppm LEDS_PORTB -> 	X0000001
	else if (Cx < 50) 
		return 0x03; // if  30 <=  CO < 50 ppm LEDS_PORTB -> 	X0000011
	else if (Cx < 70) 
		return 0x07; // if  50 <=  CO < 70 ppm LEDS_PORTB -> 	X0000111
	else if (Cx < 80) 
		return 0x0F; // if  70 <=  CO < 80 ppm LEDS_PORTB -> 	X0001111
	else if (Cx < 105) 
		return 0x1F;// if  80 <=  CO < 105 ppm LEDS_PORTB -> 	X0011111
	else if (Cx < 140) 
		return 0x3F;// if 105 <=  CO < 140 ppm LEDS_PORTB -> 	X0111111
	else 
		return 0x7F; 				  // if CO >= 140 ppm LEDS_PORTB -> 	X1111111
}

void ADC_init(void) // Initialize ADC
{
	ADMUX = 0x40;
	ADCSRA = ( 1 << ADEN | 1 << ADIE | 1 << ADPS2 | 1 << ADPS1 | 1 << ADPS0 );
}

int calculate_cx () {
	volatile float sensitivity = 129.0, Vgas0 = 0.1;
	volatile float Vin = ADC * 5.0/1024.0; // Vin  = (ADC/5)/1024
	volatile float M = sensitivity * 0.0001; // Cx = (1/M) * (Vin - Vgas0)
	return (1/M) * (Vin - Vgas0);
}

