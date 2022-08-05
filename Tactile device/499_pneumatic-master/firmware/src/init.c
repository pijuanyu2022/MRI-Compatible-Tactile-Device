#include<xc.h>                      // processor SFR definitions
#include<sys/attribs.h>             // __ISR macro
#include<string.h>
#include<stdio.h>

#include "init.h"
#include "ili9341.h"
#include "adc.h"
#include "uart.h"

// DEVCFG0
#pragma config DEBUG = ON           // disable debugging
#pragma config JTAGEN = OFF         // disable jtag
#pragma config ICESEL = ICS_PGx1    // use PGED1 and PGEC1
#pragma config PWP = OFF            // disable flash write protect
#pragma config BWP = OFF            // disable boot write protect
#pragma config CP = OFF             // disable code protect

// DEVCFG1
#pragma config FNOSC = PRIPLL       // use primary oscillator with pll
#pragma config FSOSCEN = OFF        // disable secondary oscillator
#pragma config IESO = OFF           // disable switching clocks
#pragma config POSCMOD = HS         // high speed crystal mode
#pragma config OSCIOFNC = OFF       // disable clock output
#pragma config FPBDIV = DIV_1       // divide sysclk freq by 1 for peripheral bus clock
#pragma config FCKSM = CSDCMD       // disable clock switch and FSCM
#pragma config WDTPS = PS1048576    // use largest wdt
#pragma config WINDIS = OFF         // use non-window mode wdt
#pragma config FWDTEN = OFF         // wdt disabled
#pragma config FWDTWINSZ = WINSZ_25 // wdt window at 25%


// DEVCFG2 - get the sysclk clock to 48MHz from the 8MHz crystal
#pragma config FPLLIDIV = DIV_2     // divide input clock to be in range 4-5MHz
#pragma config FPLLMUL = MUL_24     // multiply clock after FPLLIDIV
#pragma config FPLLODIV = DIV_2     // divide clock after FPLLMUL to get 48MHz

// DEVCFG3
#pragma config USERID = 0           // some 16bit userid, doesn't matter what
#pragma config PMDL1WAY = OFF       // allow multiple reconfigurations
#pragma config IOL1WAY = OFF        // allow multiple reconfigurations

void header(){
    
    LCD_clearScreen(ILI9341_BLACK);
    
    char header[200];
    int index = 0;
    
    sprintf(header, "Northwestern University");
    while(header[index]) {
        print_header(95 + 5*index, 0, header[index]);
        index++;
    }
    
    index = 0;
    sprintf(header, "Robotics and Sensorimotor Control Lab");
    while(header[index]) {
        print_header(75 + 5*index, 8, header[index]);
        index++;
    } 
}

void init_pic(){

    __builtin_disable_interrupts(); // disable interrupts while initializing things

    // set the CP0 CONFIG register to indicate that kseg0 is cacheable (0x3)
    __builtin_mtc0(_CP0_CONFIG, _CP0_CONFIG_SELECT, 0xa4210583);
    
    BMXCONbits.BMXWSDRM = 0x0;      // 0 data RAM access wait states
    INTCONbits.MVEC = 0x1;          // enable multi vector interrupts
    DDPCONbits.JTAGEN = 0;          // disable JTAG to get pins back

    SPI1_init();
    LCD_init();
//    adcConfigureAutoScan(0x0020, 1);    // REMEMBER TO CHANGE AD1CON2SET
    adcConfigureManual();
    AD1CON1SET = 0x8000;    // start ADC    
    initUART(9600);
    
    __builtin_enable_interrupts();
    
    header();
}