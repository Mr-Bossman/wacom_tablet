/**
 * \file
 *
 * \brief Driver ISR.
 *
 (c) 2020 Microchip Technology Inc. and its subsidiaries.

    Subject to your compliance with these terms,you may use this software and
    any derivatives exclusively with Microchip products.It is your responsibility
    to comply with third party license terms applicable to your use of third party
    software (including open source software) that may accompany Microchip software.

    THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
    EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
    WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
    PARTICULAR PURPOSE.

    IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE,
    INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND
    WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS
    BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
    FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
    ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
    THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
 *
 */

/*
 * Code generated by START.
 *
 * This file will be overwritten when reconfiguring your START project.
 * Please copy examples or other code you want to keep to a separate file
 * to avoid losing it when reconfiguring.
 */

#include <driver_init.h>
#include <compiler.h>
#include <util/delay.h>

volatile uint16_t blank = 0;
volatile uint8_t pix = 0;
typedef union {
	unsigned char val;
	struct {
		unsigned sel:3;
		unsigned chip:5;
	};
} conn;

#define XTOTAL 20
#define YTOTAL 13
const conn array[XTOTAL+YTOTAL] = {0b00001101, 0b00001111, 0b00001110, 0b00001100, 0b00001010, 0b00001001, 0b00001000, 0b00001011, 0b00010100, 0b00010110, 0b00010111, 0b00010101, 0b00010010, 0b00010001, 0b00010000, 0b00010011, 0b00100100, 0b00100110, 0b00100111, 0b00100101, 0b01000011, 0b01000000, 0b01000001, 0b01000010, 0b01000100, 0b01000110, 0b01000111, 0b01000101, 0b10000011, 0b10000000, 0b10000001, 0b10000010, 0b10000101};
#define BLANK 128
inline void ind(uint8_t val){
			VPORTC.OUT = (VPORTC.OUT&0xf8) | (val&7);
}
inline void sel(uint8_t val){
	VPORTC.OUT = (VPORTC.OUT&0x7) | (val<<3);
}
ISR(TCA0_CMP0_vect)
{
	/* Insert your TCA Compare 0 Interrupt handling code here */
	if(blank == BLANK){
		PORTF.OUTSET = PIN5_bm;
		PORTF.OUTSET = PIN4_bm;
		PE0_set_dir(PORT_DIR_IN);
		_delay_loop_1(5);
		OPAMP.OP0CTRLA |= OPAMP_OP0CTRLA_OUTMODE_NORMAL_gc;
	}
	if(blank == BLANK+5){
		uint16_t val = ADC_0_get_conversion(ADC_MUXPOS_AIN0_gc);
		USART_ASYNC_write((val>>8)-120);
	}
	if(blank == BLANK*2){
		OPAMP.OP0CTRLA &= ~OPAMP_OP0CTRLA_OUTMODE_NORMAL_gc; 
		PE0_set_dir(PORT_DIR_OUT);
		blank = 0;
		pix++;
		PORTF.OUTCLR = PIN4_bm;
		if(pix == 33) {
			PORTF.OUTCLR = PIN5_bm;
			pix = 0;
			USART_ASYNC_write(0xff);
		}
		conn tmp = array[pix];
		ind(tmp.sel);
		sel(~tmp.chip);
	}else
		blank++;
	/* The interrupt flag has to be cleared manually */
	TCA0.SINGLE.INTFLAGS = TCA_SINGLE_CMP0_bm;
}
