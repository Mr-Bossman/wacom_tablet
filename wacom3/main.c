#include <atmel_start.h>

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	PORTC.DIR = 0xff;
	VPORTC.DIR = 0xff;
	atmel_start_init();

	/* Replace with your application code */
	while (1) {
	}
}
