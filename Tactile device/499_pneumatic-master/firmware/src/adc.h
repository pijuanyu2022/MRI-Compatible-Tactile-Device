/*
 * ADC code was borrowed from the M5 makerspace
 * Department of Electrical and Computer Engineering
 * University of Massachusetts
 * http://umassamherstm5.org/tech-tutorials/pic32-tutorials/pic32mx220-tutorials/adc
 */

#include<xc.h>
#include<sys/attribs.h>

#ifndef ADC__H__
#define ADC__H__

int analogRead(char analogPIN);
int analogRead_auto();
void adcConfigureManual();
void adcConfigureAutoScan(unsigned adcPINS, unsigned numPins);

void ctmu_setup();
int ctmu_read(int pin, int delay);
unsigned int do_cap(int pin, int delay);

#endif // ADC__H__