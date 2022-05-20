#include <atmel_start.h>
#include <util/delay.h>
#include <string.h>
int main(void)
{
	/* Initializes MCU, drivers and middleware */

	OPERATIONAL_AMPLIFIER_0_init();
	CLKCTRL_init();
	EVENT_SYSTEM_0_init();
	SLPCTRL_init();
	CPUINT_init();
	DAC_0_init();
	ADC_0_init();
	PORTMUX.TCAROUTEA |= 5;
	TIMER_0_init();
	BOD_init();
	USART_ASYNC_init();
	PORTB.DIRSET = PIN0_bm;
	PORTF.DIRSET = PIN4_bm | PIN5_bm;
	PORTB.DIRCLR = PIN1_bm;
	PORTC.DIR = 0xff;
	PORTD.DIR = 0;
	PORTD.PIN3CTRL = 0;
	while (1) {
	}
}
