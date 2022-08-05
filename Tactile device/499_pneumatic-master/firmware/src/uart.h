#include<xc.h>
#include<sys/attribs.h>

#ifndef UART__H__
#define UART__H__

void initUART(int desired_baud);
void writeUART(char * string);
void readUART(char * message, int maxLength);

#endif // UART__H__