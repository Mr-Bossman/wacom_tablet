#include <atmel_start.h>
#include <util/delay.h>
#include <string.h>
int main(void)
{
	/* Initializes MCU, drivers and middleware */

	atmel_start_init();
	PORTB.DIRSET = PIN0_bm;
	PORTF.DIRSET = PIN4_bm | PIN5_bm;
	VPORTF.DIR = PIN4_bm | PIN5_bm;
	PORTB.DIRCLR = PIN1_bm;
	PORTC.DIR = 0xff;
	VPORTC.DIR = 0xff;
	PORTD.DIR = 0;
	PORTE.PIN0CTRL = 0;
	PORTD.PIN3CTRL = 0;
	while (1) {
	}
}
