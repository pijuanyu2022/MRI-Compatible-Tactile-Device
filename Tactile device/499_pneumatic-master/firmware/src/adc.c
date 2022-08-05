/*
 * ADC code was borrowed from the M5 makerspace
 * Department of Electrical and Computer Engineering
 * University of Massachusetts
 * http://umassamherstm5.org/tech-tutorials/pic32-tutorials/pic32mx220-tutorials/adc
 */

#include <xc.h>
#include "init.h"
#include "adc.h"

int analogRead(char analogPIN){
    AD1CHS = analogPIN << 16;       // AD1CHS<16:19> controls which analog pin goes to the ADC
 
    AD1CON1bits.SAMP = 1;           // Begin sampling
    while( AD1CON1bits.SAMP );      // wait until acquisition is done
    while( ! AD1CON1bits.DONE );    // wait until conversion done
 
    return ADC1BUF0;                // result stored in ADC1BUF0
}

int analogRead_auto (){
    int voltage;
    
    while(! IFS0bits.AD1IF);       // wait until buffers contain new samples
    AD1CON1bits.ASAM = 0;           // stop automatic sampling (essentially shut down ADC in this mode)

    if(AD1CON2bits.BUFS == 1){     // check which buffers are being written to and read from the other set
        voltage = ADC1BUF2;
    }
    else{
        voltage = ADC1BUFA;

    }
    AD1CON1bits.ASAM = 1;           // restart automatic sampling
    IFS0CLR = 0x10000000;           // clear ADC interrupt flag
    
    return voltage;
}

void delay_us(unsigned t){          // See Timers tutorial for more info on this function

    T1CON = 0x8000;                 // enable Timer1, source PBCLK, 1:1 prescaler
 
    // delay 100us per loop until less than 100us remain
    while( t >= 100){
        t-=100;
        TMR1 = 0;
        while( TMR1 < SYSCLK/10000);
    }
 
    // delay 10us per loop until less than 10us remain
    while( t >= 10){
        t-=10;
        TMR1 = 0;
        while( TMR1 < SYSCLK/100000);
    }
 
    // delay 1us per loop until finished
    while( t > 0)
    {
        t--;
        TMR1 = 0;
        while( TMR1 < SYSCLK/1000000);
    }
 
    // turn off Timer1 so function is self-contained
    T1CONCLR = 0x8000;
} // END delay_us()
 
void adcConfigureManual(){
    AD1CON1CLR = 0x8000;    // disable ADC before configuration
 
    AD1CON1 = 0x00E0;       // internal counter ends sampling and starts conversion (auto-convert), manual sample
    AD1CON2 = 0;            // AD1CON2<15:13> set voltage reference to pins AVSS/AVDD
    AD1CON3 = 0x0f01;       // TAD = 4*TPB, acquisition time = 15*TAD
} // END adcConfigureManual()

void adcConfigureAutoScan(unsigned adcPINS, unsigned numPins){
    AD1CON1 = 0x0000; // disable ADC
 
    // AD1CON1<2>, ASAM    : Sampling begins immediately after last conversion completes
    // AD1CON1<7:5>, SSRC  : Internal counter ends sampling and starts conversion (auto convert)
    AD1CON1SET = 0x00e4;
 
    // AD1CON2<1>, BUFM    : Buffer configured as two 8-word buffers, ADC1BUF7-ADC1BUF0, ADC1BUFF-ADCBUF8
    // AD1CON2<10>, CSCNA  : Scan inputs
    AD1CON2 = 0x0402;
 
    // AD2CON2<5:2>, SMPI  : Interrupt flag set at after numPins completed conversions
//    AD1CON2SET = (numPins-1) << 2;
    AD1CON2SET = 0x0011;    // Set the buffer (Table 22-1) 0x0011 reads ADC1BUF2
 
    // AD1CON3<7:0>, ADCS  : TAD = TPB * 2 * (ADCS<7:0> + 1) = 4 * TPB in this example
    // AD1CON3<12:8>, SAMC : Acquisition time = AD1CON3<12:8> * TAD = 15 * TAD in this example
    AD1CON3 = 0x0f01;
 
    // AD1CHS is ignored in scan mode
    AD1CHS = 0;
 
    // select which pins to use for scan mode
    AD1CSSL = adcPINS;
}

void ctmu_setup() {
    // base level current is about 0.55uA
    CTMUCONbits.IRNG = 0b11; // 100 times the base level current
    CTMUCONbits.ON = 1; // Turn on CTMU

    // 1ms delay to let it warm up
    _CP0_SET_COUNT(0);
    while (_CP0_GET_COUNT() < 48000000 / 2 / 1000) {
    }
}

int ctmu_read(int pin, int delay) {
    int start_time = 0;
    
    AD1CHSbits.CH0SA = pin;
    
    // Manual sampling start
    AD1CON1bits.SAMP = 1;
    // Ground the pin
    CTMUCONbits.IDISSEN = 1; 
    
    // Wait 1 ms for grounding
    start_time = _CP0_GET_COUNT();
    while (_CP0_GET_COUNT() < start_time + 48000000 / 2 / 1000) {}
    CTMUCONbits.IDISSEN = 0; // End drain of circuit

    // Begin charging the circuit
    CTMUCONbits.EDG1STAT = 1; 

    // wait delay core ticks (on order of 2 microseconds)
    start_time = _CP0_GET_COUNT();
    while (_CP0_GET_COUNT() < start_time + delay) {}
    
    // Stop charging circuit
    CTMUCONbits.EDG1STAT = 0; 
    
    // Begin analog-to-digital conversion
    AD1CON1bits.SAMP = 0;
    while (!AD1CON1bits.DONE){} // Wait for ADC conversion
    
    AD1CON1bits.DONE = 0; // ADC conversion done, clear flag
    
    return ADC1BUF0; // Get the value from the ADC
}

unsigned int do_cap(int pin, int delay) {
  int i = 0;
  int sum = 0;
  int win = 10; // window to average over
  while (i<=win) {
    sum += ctmu_read(pin, delay);
    i++;
  }
  return (sum/win);
}