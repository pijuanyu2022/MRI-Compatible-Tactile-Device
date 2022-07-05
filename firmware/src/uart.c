#include <xc.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "init.h"
#include "adc.h"
#include "ili9341.h"

void initUART(int desired_baud){
    
    U1MODE = 0;
    // Set U1TX pin to B4
    RPB4Rbits.RPB4R = 0b0001;
    
    // Set U1RX pin to A4
    U1RXRbits.U1RXR = 0b0010;
    
    // Turn on UART1 without interrupt
    U1MODEbits.BRGH = 0;                            // set baud to 9600 bits/sec
    U1BRG = (SYSCLK / (16 * desired_baud)) - 1;     // This is the formula straight from the datasheet
    
    // 8-bit, no parity bit, 1 stop bit (8N1 setup)
    U1MODEbits.PDSEL = 0;
    U1MODEbits.STSEL = 0;
    
    // Configure TX and RX pins as output and input pins
    U1STAbits.UTXEN = 1;
    U1STAbits.URXEN = 1;
    
    // Configure hardware flow control using RTS and CTS
    U1MODEbits.UEN = 2;
    
    // Enable the UART
    U1MODEbits.ON = 1;
}

void writeUART(char * string){
    while (*string != '\0'){
        while (U1STAbits.UTXBF){;}      // Wait until TX buffer isn't full
        U1TXREG = *string;
        string++;
    }
}

void readUART(char * message, int maxLength){
  
    char data = 0;
    int complete = 0, num_bytes = 0;

    // loop until you get a '\r' or '\n'
    while (!complete) {
        if (U1STAbits.URXDA) { // if data is available
            data = U1RXREG;      // read the data
            if ((data == '\n') || (data == '\r')) {
                complete = 1;
            } 
            else {
                message[num_bytes] = data;
                ++num_bytes;
                // roll over if the array is too small
                if (num_bytes >= maxLength) {
                    num_bytes = 0;
                }
            }
        }
        else{
            complete = 1;
        }
    }
  // end the string
  message[num_bytes] = '\0';
}