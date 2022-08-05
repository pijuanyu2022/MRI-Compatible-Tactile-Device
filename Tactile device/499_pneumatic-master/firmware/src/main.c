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
#define MAX_MESSAGE_LENGTH 200

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
    char message[MAX_MESSAGE_LENGTH];
    int  pressure_value = 100;
    int  solenoid_value = 0;
    double pressure = 0;
    
    // Touch Sensor
    ANSELBbits.ANSB2 = 1;           // sets RB3 (AN4) as analog
    TRISBbits.TRISB2 = 1;           // sets RB2 as input
//    
//    // Pressure Sensor
    ANSELBbits.ANSB3 = 1;           // sets RB3 (AN5) as analog
    TRISBbits.TRISB3 = 1;           // sets RB3 as input
//    
    TRISBbits.TRISB12 = 0;          // RB12 as output (pwm @ motor driver)
    TRISBbits.TRISB10 = 0;          // RB10 as output

    LATBbits.LATB10 = 0;            // set RB10 as high

    init_pic();
    
    // variables
    int voltage = 0;
    int cap = 0;
    char temp_msg[30]; 

    // added for PWM
    // pressure control
    RPB11Rbits.RPB11R = 0b0101; // Set pin B11 to OC2
    T2CONbits.TCKPS = 2;     // set the timer prescaler so that you can use the largest PR2 value as possible without going over 65535 and the frequency is 50Hz N = 8 
    PR2 = 3150;
    TMR2 = 0;                // initial TMR2 count is 0
    OC2CONbits.OCM = 0b110;  // PWM mode without fault pin; other OCxCON bits are defaults
    OC2RS = 0;             // duty cycle = OCxRS/(PR2+1) default to 0
    OC2R = 1;
    T2CONbits.ON = 1;        // turn on Timer2
    OC2CONbits.ON = 1;       // turn on OCx
        
    // solenoid
    LATBbits.LATB12 = 1;
    
    // solenoid control
    RPB13Rbits.RPB13R = 0b0110;
    OC5CONbits.OCM = 0b110;
    OC5RS = 0;
    OC5R = 1;
    OC5CONbits.ON = 1;       // turn on OCx
    // end
    __builtin_enable_interrupts();

    void delay(unsigned long int time){
            _CP0_SET_COUNT(0);
             while(_CP0_GET_COUNT() < time){}
            _CP0_SET_COUNT(0);
       }
        
    while (1) {

        _CP0_SET_COUNT(0);                  // start timer 
        readUART(message, MAX_MESSAGE_LENGTH);
        int len = strlen(message);
        char c = message[len-1];
        int x = c - '0';
            
        if (atoi(message) == 0) {
            solenoid_value = 0;
            pressure_value = 100;
        }
        else{
            message[len - 1] = '\0';
            solenoid_value = x;
            pressure_value = atoi(message);
        }
        sprintf(temp_msg, "Solenoid_value:  %d", solenoid_value);
        write_screen(28, 24, temp_msg);
        sprintf(temp_msg, "Pressure_value:  %d", pressure_value);
        write_screen(160, 24, temp_msg);
        LATBbits.LATB12 = solenoid_value;
        
        int BNC_cabel = PORTBbits.RB5;
        voltage = analogRead(4)*10+BNC_cabel;
        
        pressure = transfer_function(voltage);       
        
//      Send message to computer
        
        char presout[50];
        sprintf(presout, "%d", voltage);
        char solenoid_str[50];
        sprintf(solenoid_str, "%d", solenoid_value);
        printf("\n");
        getchar();
        strcat(presout, solenoid_str);
        
//        char BNC_str[50];
//        int BNC_cabel = PORTBbits.RB5;
//        sprintf(BNC_str, "%d", BNC_cabel);
//        printf("\n");
//        getchar();
//        strcat(presout, BNC_str);
        
        writeUART(presout);

        OC5RS = 3100;      // high level    
        OC2RS = pressure_value;   // 0 - 3100   
//        OC2RS = 2500;   // 0 - 3100  
       
        
//      end

//        sprintf(temp_msg, "Pressure value:  %d", pressure_value);
//        write_screen(28, 24, temp_msg);
        
        sprintf(temp_msg, "Update Frequency:    %3.1f Hz", (24000000.0/_CP0_GET_COUNT()));
        write_screen(28, 40, temp_msg);
        
        sprintf(temp_msg, "Voltage:   %d", voltage);
        write_screen(28, 56, temp_msg);
        
        sprintf(temp_msg, "Pressure:   %f", pressure);
        write_screen(160, 56, temp_msg);
        
        sprintf(temp_msg, "RB11, Pin 22:   %d", PORTBbits.RB11);
        write_screen(28, 72, temp_msg);
        
        sprintf(temp_msg, "RB5, Pin 14:   %d", PORTBbits.RB5);
        write_screen(28, 140, temp_msg);
        
        sprintf(temp_msg, "RB12, Pin 23:   %d", LATBbits.LATB12);
        write_screen(28, 88, temp_msg);
        
        sprintf(temp_msg, "RB13, Pin 24:   %d", LATBbits.LATB13);
        write_screen(28, 104, temp_msg);
        
        
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
        
    }
}