/*MAIN main*/

// PIC32 control of pneumatic actuator

#include<xc.h>                      // processor SFR definitions
#include<sys/attribs.h>             // __ISR macro
#include<string.h>
#include<stdio.h>
#include<stdlib.h>

#include "init.h"
#include "ili9341.h"
#include "adc.h"
#include "uart.h"

#include<math.h>

double transfer_function(int voltage){
    /* Voltage divider, as built, reduces voltage from 5v to 3.27v
     int voltage has a value between 0 and 1023 (PIC32 has a 10-bit resolution ADC)
     Pressure sensor reads gage pressure
     Output is proportional to the difference between 
     applied pressure and atmospheric (ambient) pressure 
     */

    double v_supply = 3.36;
    double v_output = (voltage/1023.)*v_supply;
    
//    double v_min = v_supply * 0;
    double v_max = v_supply * 1;
    
    // Documented transfer function
//    double pressure = (v_min + ((v_max-v_min)/(0.8*v_supply))*(v_output-(0.1*v_supply)))+14.7;
    
    // Proportional transfer function
    double pressure = (((v_output/v_max))*150)-14.7;
    
    return pressure;
}

void _mon_putc (char c){
   while (U1STAbits.UTXBF); // Wait til current transmission is complete
   U1TXREG = c;
}

int main() {

    // Initializations//    AD1CON1SET = 0x8000;    // start ADC

    
    // Touch Sensor
    ANSELBbits.ANSB2 = 1;           // sets RB3 (AN4) as analog
    TRISBbits.TRISB2 = 1;           // sets RB2 as input
//    
//    // Pressure Sensor
    ANSELBbits.ANSB3 = 1;           // sets RB3 (AN5) as analog
    TRISBbits.TRISB3 = 1;           // sets RB3 as input
//    
////    // Toggle Switch
//    TRISBbits.TRISB10 = 1;          // RB10 as input
//    TRISBbits.TRISB11 = 1;          // RB11 as input
//    ANSELBbits.ANSB12 = 0;          // B12 as digital
    TRISBbits.TRISB12 = 0;          // RB12 as output (pwm @ motor driver)
//    TRISBbits.TRISB13 = 0;          // RB13 as output
    
    TRISBbits.TRISB10 = 0;          // RB10 as output
//    LATBbits.LATB10 = 1;            // set RB10 as high
    LATBbits.LATB10 = 0;            // set RB10 as high

    init_pic();
    
    // variables
    int voltage = 0;
    int cap = 0;
    double pressure=0;
    char temp_msg[30]; 
//    char message[200]; 
//    char rx_msg[10];
    
//    added for pwm
    //        LATBbits.LATB12 = 1;
//        LATAbits.LATB12 = 1;   // B12 is high
//        LATAbits.LATB13 = 1;   // B13 is high
        
//        USE THESE TWO BELOW TO QUICK CHANGE BETWEEN THE TWO SOLENOIDS (EE EXTEND/IN)
//        LATBbits.LATB12 = 1;   // B12 is high (PHase; GPIO)
        LATBbits.LATB12 = 0;   // B12 is low (PHase; GPIO)
        
        RPB13Rbits.RPB13R = 0b0110;       // B13 is set  (ENable; PWM)
//        TRISBbits.TRISB11 = 0;
//        RPB11R = 0b0110;       // B13 is set  (ENable; PWM)
//        LATBbits.LATB12 = 0;   // B12 is low
//        LATBbits.LATB13 = 0;   // B13 is low
        T2CONbits.TCKPS = 2;     // set the timer prescaler so that you can use the largest PR2 value as possible without going over 65535 and the frequency is 50Hz
//        T2CONbits.TCKPS = 5;     // 11 = 1:256 prescale value
        PR2 = 62499; // period = (PR2+1) * N * 12.5 ns = 0.02 s, 50 Hz=> (PR2+1) * N = 16,000,000 => N=256, PR2 = 62499
//        PR2 = 3125;
        TMR2 = 0;                // initial TMR2 count is 0
        OC5CONbits.OCM = 0b110;  // PWM mode without fault pin; other OCxCON bits are defaults
        OC5RS = 0;             // duty cycle = OCxRS/(PR2+1) default to 0
//        OC5R = 0;              // initialize before turning OCx on; afterward it is read-only
        OC5R = 1;
        T2CONbits.ON = 1;        // turn on Timer2
        OC5CONbits.ON = 1;       // turn on OCx
        //------------------------
        /* added second output compare for pres reg control*/
        RPB11Rbits.RPB11R = 0b0101; // Set pin B11 to OC4
        T3CONbits.TCKPS = 2;     // set the timer prescaler so that you can use the largest PR2 value as possible without going over 65535 and the frequency is 50Hz
//        T2CONbits.TCKPS = 5;     // 11 = 1:256 prescale value
//        PR3 = 62499; // period = (PR2+1) * N * 12.5 ns = 0.02 s, 50 Hz=> (PR2+1) * N = 16,000,000 => N=256, PR2 = 62499
        PR3 = 3125;
        TMR3 = 0;                // initial TMR2 count is 0
        OC4CONbits.OCM = 0b110;  // PWM mode without fault pin; other OCxCON bits are defaults
        OC4RS = 0;             // duty cycle = OCxRS/(PR2+1) default to 0
//        OC5R = 0;              // initialize before turning OCx on; afterward it is read-only
        OC4R = 1;
        T3CONbits.ON = 1;        // turn on Timer2
        OC4CONbits.ON = 1;       // turn on OCx
        OC4CONbits.OCM = 0b110;  // PWM mode without fault pin; other OCxCON bits are defaults
        OC4RS = 0;             // duty cycle = OCxRS/(PR2+1) default to 0
//        OC5R = 0;              // initialize before turning OCx on; afterward it is read-only
        OC4R = 1;
        OC4CONbits.ON = 1;       // turn on OCx
        /*end*/
        __builtin_enable_interrupts();
        
        void delay(unsigned long int time){
                _CP0_SET_COUNT(0);
                 while(_CP0_GET_COUNT() < time){}
                _CP0_SET_COUNT(0);
           }
        
//        int zeroDeg = 4000;
//        int oneEightyDeg = 29000;
//        unsigned long dt = 48000;//each cycle is 0.5sec / 50 = 0.01 sec
//        //OC5RS = oneEightyDeg;
//        // set OCxRS to get between a 0.5ms and 2.5ms pulse out of the possible 20ms (50Hz)
//        float f = 0.5;
//        double t = 0;
//    end
        
    while (1) {

        _CP0_SET_COUNT(0);                  // start timer 
//        int i = 0;
        
//        voltage = analogRead_auto();        // returns value between 0 and 1023
        voltage = analogRead(5);
        pressure = transfer_function(voltage);       
        
//        moved up here for testing
        char presout[50];
//        float num = 23.34;
//        float capfloat = cap;
        sprintf(presout, "%f", pressure);
//        getchar();
//        printf("\n The current pressure sensed is %s", presout);
//        printf("\n The current pressure sensed is %s PSI", presout);
        printf("\n");
        getchar();
        writeUART(presout);

//        while(1){
//            OC5RS = (oneEightyDeg-zeroDeg)* (sin(2*PI*f*t) + 0.5);
//            t += 0.01*4;
//            delay(dt);
//        }
        
//        OC5RS = (oneEightyDeg-zeroDeg)* (sin(2*PI*f*t) + 0.5);
//        t += 0.01*4;
//        delay(dt);
        
//        OC5RS = 50;      // too small
        OC5RS = 40000;      // works
//        OC5RS = 1600;   //for solenoid i think
//        OC5RS = 2000;
//        OC5RS = 3000;
//        OC4RS = 40000;
        OC4RS = 3000;   // for pres reg i think but who really knows
        
        
//      end

        sprintf(temp_msg, "Pressure:           %5.3f PSI ", pressure);
        write_screen(28, 24, temp_msg);
        
        sprintf(temp_msg, "Update Frequency:    %3.1f Hz", (24000000.0/_CP0_GET_COUNT()));
        write_screen(28, 40, temp_msg);
        
        sprintf(temp_msg, "RB10, Pin 21:   %d", PORTBbits.RB10);
        write_screen(28, 56, temp_msg);
        
        sprintf(temp_msg, "RB11, Pin 22:   %d", PORTBbits.RB11);
        write_screen(28, 72, temp_msg);
        
        sprintf(temp_msg, "RB12, Pin 23:   %d", LATBbits.LATB12);
        write_screen(28, 88, temp_msg);
        
        sprintf(temp_msg, "RB13, Pin 24:   %d", LATBbits.LATB13);
        write_screen(28, 104, temp_msg);
        
//  
        sprintf(temp_msg, "real RB13, Pin 24:   %d", OC5RS);
        write_screen(28, 120, temp_msg);
        
        // ---capacitance sensor---
        cap = ctmu_read(4, (4800000/4)); // tuned
        sprintf(temp_msg, "cap %d   ", cap);
        write_screen(200, 88, temp_msg);
        
        if (cap<200){
            sprintf(temp_msg, "Touched: yes");
            while(_CP0_GET_COUNT() < 48000000 / 2 / 1000){}
        }
        else{
            sprintf(temp_msg, "Touched: no ");
        }
        write_screen(200, 104, temp_msg);
        
        // ---added for testing---
//        writeUART("IIIIT'S JONNY!!!");
        
//        char capout[50];
////        float num = 23.34;
////        float capfloat = cap;
//        sprintf(capout, "%i", cap);
//        printf("\n The string for the num is %s", capout);
//        getchar();
//        writeUART(capout);
        
    }
}
