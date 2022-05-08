#include <atmel_start.h>
#include <util/delay.h>
#include <string.h>
int main(void)
{
	/* Initializes MCU, drivers and middleware */
	PORTB.DIRSET = PIN0_bm;
	PORTF.DIRSET = PIN4_bm | PIN5_bm;
	VPORTF.DIR = PIN4_bm | PIN5_bm;
	PORTB.DIRCLR = PIN1_bm;
	PORTC.DIR = 0xff;
	VPORTC.DIR = 0xff;
	PORTD.DIR = 0;
	atmel_start_init();
	while (1) {
	}
}
