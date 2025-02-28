#include <msp430.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER_SIZE 32  // Adjust buffer size if necessary

// Define output pins for controlling the pumps
#define PUMP1_PIN BIT0  // Example: P1.0
#define PUMP2_PIN BIT1  // Example: P1.1
#define PUMP3_PIN BIT2  // Example: P1.2
#define PUMP4_PIN BIT3  // Example: P1.3
#define PUMP5_PIN BIT4  // Example: P1.4

void init_serial();
void init_gpio();
void read_serial_values(int *val1, int *val2, int *val3, int *val4, int *val5);
void control_pumps(int val1, int val2, int val3, int val4, int val5);

int main() {
    WDTCTL = WDTPW | WDTHOLD;  // Stop watchdog timer
    init_serial();
    init_gpio();

    int value1, value2, value3, value4, value5;

    while (1) {
        read_serial_values(&value1, &value2, &value3, &value4, &value5);
        control_pumps(value1, value2, value3, value4, value5);
    }
}

// Initialize UART (adjust for your MSP430 model)
void init_serial() {
    P1SEL |= BIT1 + BIT2;  // Set P1.1 (RX) and P1.2 (TX) for UART mode
    P1SEL2 |= BIT1 + BIT2;

    UCA0CTL1 |= UCSSEL_2;  // Use SMCLK
    UCA0BR0 = 104;         // Baud rate 9600 for 1MHz clock
    UCA0BR1 = 0;
    UCA0MCTL = UCBRS0;     // Modulation
    UCA0CTL1 &= ~UCSWRST;  // Initialize USCI state machine
}

// Initialize GPIO for pump control
void init_gpio() {
    P1DIR |= PUMP1_PIN | PUMP2_PIN | PUMP3_PIN | PUMP4_PIN | PUMP5_PIN;  // Set pins as output
    P1OUT &= ~(PUMP1_PIN | PUMP2_PIN | PUMP3_PIN | PUMP4_PIN | PUMP5_PIN); // Ensure all pumps are off
}

// Read serial data and parse integer values
void read_serial_values(int *val1, int *val2, int *val3, int *val4, int *val5) {
    char buffer[BUFFER_SIZE];
    int index = 0;
    char c;

    // Read from UART until newline is received
    while (index < BUFFER_SIZE - 1) {
        while (!(IFG2 & UCA0RXIFG)); // Wait for RX buffer to be ready
        c = UCA0RXBUF;  // Read received character

        if (c == '\n' || c == '\r') break;  // Stop on newline
        buffer[index++] = c;
    }
    buffer[index] = '\0';  // Null-terminate string

    // Parse integers from received buffer
    sscanf(buffer, "%d,%d,%d,%d,%d", val1, val2, val3, val4, val5);
}

// Control relays based on received values
void control_pumps(int val1, int val2, int val3, int val4, int val5) {
    if (val1 > 0) P1OUT |= PUMP1_PIN; else P1OUT &= ~PUMP1_PIN;
    if (val2 > 0) P1OUT |= PUMP2_PIN; else P1OUT &= ~PUMP2_PIN;
    if (val3 > 0) P1OUT |= PUMP3_PIN; else P1OUT &= ~PUMP3_PIN;
    if (val4 > 0) P1OUT |= PUMP4_PIN; else P1OUT &= ~PUMP4_PIN;
    if (val5 > 0) P1OUT |= PUMP5_PIN; else P1OUT &= ~PUMP5_PIN;
}
