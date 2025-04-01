//#include <avr/io.h>

//port definitions
#define PORTB_reg  (*((volatile uint8_t *) 0x25))
#define PORTC_reg  (*((volatile uint8_t *) 0x28))
#define PORTD_reg  (*((volatile uint8_t *) 0x2B))

//function declarations
uint8_t dbouncer(uint8_t regIn, uint8_t pinIn, uint8_t *inputState);
uint8_t relayControl(uint8_t pinInCon, uint8_t *regOut, uint8_t pinOut, char* pinName);

//pin mapping
const uint8_t analogPin = A0;  //analog  input

//initialize pin variables
//Register D
uint8_t D2  = 2; uint8_t D3  = 3; uint8_t D4  = 4; 
uint8_t D5  = 5; uint8_t D6  = 6; uint8_t D7  = 7; 
//Register B     
uint8_t D8  = 0; uint8_t D9  = 1; uint8_t D10 = 2; 
uint8_t D11 = 3; uint8_t D12 = 4; uint8_t D13 = 5; 
//Register C
uint8_t D14 = 0; uint8_t D15 = 1; uint8_t D16 = 2; 
uint8_t D17 = 3; uint8_t D18 = 4; uint8_t D19 = 5; 

//input state variables
uint8_t inputStateD2  = 0; uint8_t inputStateD4  = 0; uint8_t inputStateD6  = 0; 
uint8_t inputStateD8  = 0; uint8_t inputStateD10 = 0; uint8_t inputStateD14 = 0; 

//button conditions
uint8_t flavorA_in = 0; uint8_t flavorB_in = 0; uint8_t flavorC_in = 0; 
uint8_t flavorD_in = 0; uint8_t airPump_in = 0; uint8_t airValv_in = 0; 

//relay controls
uint8_t flavorA_out = 0; uint8_t flavorB_out = 0; uint8_t flavorC_out = 0; 
uint8_t flavorD_out = 0; uint8_t airPump_out = 0; uint8_t airValv_out = 0; 


//-------------------------------------
void setup(){ 
  //set inputs/outputs (DDRx) & pull resistors (PORTx)
  //flavorA
  DDRD  &= ~(1 << D2);  //set pin as input
  PORTD |=  (1 << D2);  //set internal pullup
  DDRD  |=  (1 << D3);  //set pin as output
  //flavorB
  DDRD  &= ~(1 << D4);  //set pin as input
  PORTD |=  (1 << D4);  //set internal pullup
  DDRD  |=  (1 << D5);  //set pin as output
  //flavorC
  DDRD  &= ~(1 << D6);  //set pin as input
  PORTD |=  (1 << D6);  //set internal pullup
  DDRD  |=  (1 << D7);  //set pin as output
  //flavorD
  DDRB  &= ~(1 << D8);  //set pin as input
  PORTB |=  (1 << D8);  //set internal pullup
  DDRB  |=  (1 << D9);  //set pin as output
  //air pump
  DDRB  &= ~(1 << D10); //set pin as input
  PORTB |=  (1 << D10); //set internal pullup
  DDRB  |=  (1 << D11); //set pin as output
  //air valve
  DDRC  &= ~(1 << D14); //set pin as input
  PORTC |=  (1 << D14); //set internal pullup
  DDRC  |=  (1 << D15); //set pin as output
  //pressure sensor
  ADMUX = 0x07; //set analog input to (A7) for ADC in
                /*ADMUX bits: 7-6: 00 for internal Vref | 4: N/A | 
                5: 0 for right adjust result | 3-0: Channel Select
                ADC 3-0 Selection
                0000  ADC0 | 0101  ADC5 | 0010  ADC2 | 0111  ADC7 | 0100  ADC4
                0001  ADC1 | 0110  ADC6 | 0011  ADC3 | 1000  ADC8 |         */
  Serial.begin(9600); //set serial comm @ 9600 baud
}


//MAIN-------------------------------------
void loop(){
    //check each digital input (buttons)
    flavorA_in = dbouncer(PIND, D2 , &inputStateD2 ); //check button for flavorA
    flavorB_in = dbouncer(PIND, D4 , &inputStateD4 ); //check button for flavorB
    flavorC_in = dbouncer(PIND, D6 , &inputStateD6 ); //check button for flavorC
    flavorD_in = dbouncer(PINB, D8 , &inputStateD8 ); //check button for flavorD
    airPump_in = dbouncer(PINB, D10, &inputStateD10); //check button for airPump
    airValv_in = dbouncer(PINC, D14, &inputStateD14); //check button for airValv
    //relayControl(pinInCon, regOut, pinOut)
    relayControl(flavorA_in, &PORTD_reg, D3 , "D3 ");              //control relay for flavorA
    relayControl(flavorB_in, &PORTD_reg, D5 , "D5 ");              //control relay for flavorB
    relayControl(flavorC_in, &PORTD_reg, D7 , "D7 ");              //control relay for flavorC
    relayControl(flavorD_in, &PORTB_reg, D9 , "D9 ");              //control relay for flavorD
    relayControl(airPump_in, &PORTB_reg, D11, "D11");              //control relay for airPump
    relayControl(airValv_in, &PORTC_reg, D15, "D15");              //control relay for airValv

    //read analog voltage
    // uint16_t analogValue = pressureRead(analogPin);  //give value between 0 and 1023
    //TODO: use the voltage to control another digi output (for solenoid)
}


//BUTTON DEBOUNCE--------------------------------------------------------------------------------
//IMPORTANT: requires adding global inputState variable for EACH call in main function for proper operation!!!
//IMPORTANT: requires adding global inputState variable for EACH call in main function for proper operation!!!
/*dBounce Function uses 3 variables to run on specified input and output pins using:
    1: regIn,         sets location of input register                    i.e. P4IN_REG
    2: pinIn,         sets specific pin of selected input register       i.e. 1
    3: *inputeState,  sets location of input state main variable     i.e. &inputStateP41
                        NOTE: need uint_8 t variable in main .c file,
                        NOTE: need & in call to dereference                           */
/*Return values:  0 = no change  |  1 = SW pressed  |  2 = SW released   */

//read input, look for change, wait, read again, and change/maintain state of output
uint8_t dbouncer(uint8_t regIn, uint8_t pinIn, uint8_t *inputState){   //set input register, input pin, output register, output pin, and input state per entered values (5 variables total)
    uint8_t inputCheck = regIn & (1<<pinIn);    //initialize inputCheck to value of regIn bitwise ANDed with pinIn
                                                //(sets inputCheck to value at desired input pin)
    inputCheck = (inputCheck>>pinIn);           //bit shift inputCheck value, setting to "1" or "0" (true or false)
    // __disable_interrupt();                      //ENTER CRITICAL SECTION, disable maskable global interrupts
    // msCount = 0;                                //set TimerB0 msCount to 0 for debounce timing
    // __enable_interrupt();                       //EXIT CRITICAL SECTION, enable maskable global interrupts
    if(inputCheck != *inputState){              //ifbig input appeared to changed, wait a moment, compare again, and change output accordingly
        delay(10);
        inputCheck = regIn & (1<<pinIn);        //sets inputCheck to value at desired input pin
        inputCheck = (inputCheck>>pinIn);       //bit shift inputCheck value, setting to "1" or "0" (true or false) again
        if(inputCheck != *inputState){          //ifmid the state actually has changed, change output accordingly
            *inputState = inputCheck;           //set inputState to new value of inputCheck (1 or 0)
            if(*inputState == 0){               //iflil inputState settled low, then input goes low (onboard button currently pressed)
                return 1;                       //return 1 (button pressed)
            }else{                              //if inputState settled high, then input goes high (onboard button released)
                return 2;                       //return 2 (button released)
            }//end lil if/else
        }//end mid if
    }//end big if
    return 0;                                   //return 0 (no change)
}//end dBounce


//RELAY CONTROL---------------------------------------------------------------------
uint8_t relayControl(uint8_t pinInCon, uint8_t *regOut, uint8_t pinOut, char* pinName) {
    if(pinInCon==1){
        *regOut  |=  (1 << pinOut); //set output high on button press
        Serial.print("The button has been pressed for ");
        Serial.println(pinName);
    }else if(pinInCon==2){
        *regOut  &= ~(1 << pinOut); //set output low on button release
        Serial.print("The button has been released for ");
        Serial.println(pinName);
    }else{}
}


//read in pressure sensor voltage-------------------------------------
// uint16_t pressureRead(uint8_t pin) {
//     ADCSRA |= (1 << ADSC);        //start conversion
//     while (ADCSRA & (1 << ADSC)); //wait for conversion to finish
//     return ADC;                   //return ADC value (10-bit resolution)
// }

//Paul Litherland 24.11.20