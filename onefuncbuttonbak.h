/*-
 * This example demonstrates how to read digital signals.
 *
 * It assumes there are push buttons with pullup resistors connected to the 16
 * channels of the 74HC4067 mux.
 * 
 * ------------------------------------------------------------
 * Project: arduino-ad-mux-lib
 * Source: https://github.com/stechio/arduino-ad-mux-lib.git
 *
 * Author: Nick Lamprianidis (adaptation by Stefano Chizzolini)
 */

#include <Arduino.h>
#include "Mux.h"

using namespace admux;

/*
 * Creates a Mux instance.
 *
 * 1st argument is the SIG (signal) pin (Arduino digital input pin 3).
 * 2nd argument is the S0-S3 (channel control) pins (Arduino pins 8, 9, 10, 11).
 */
// Mux mux(Pin(4, INPUT, PinType::Digital), Pinset(14, 2, 0));

// float pressLength_milliSeconds = 0;
// int optionOne_milliSeconds = 100;
// int optionTwo_milliSeconds = 1000;


// class buttonReg{
//     public:
//         buttonReg(int8_t muxpin, Pinset pinSelector);

//     protected:
//         Mux data;
// }

int16_t buttonRegs(int8_t pinSelected, int8_t pinSelector, Pinset pinSelecting){
    byte data;
    Mux mux(Pin(pinSelector, INPUT, PinType::Digital), pinSelecting);
    data = mux.read(pinSelected);

    return data;
}

// void setup() {
//   // Serial port initialization.
//   Serial.begin(9600); while (!Serial) /* Waits for serial port to connect (needed for Leonardo only) */;
//   Serial.println(mux.channelCount());
// }

/**
 * Reads the 16 channels and reports on the serial monitor if the corresponding
 * push button is pressed.
 */
// void loop() {
//   byte data;
//   int8_t selpin = 4;
//   data = mux.read(selpin);
//   Serial.println(buttonRegs(selpin, 4, Pinset(14, 2, 0)));
//   // for (byte i = 0; i < mux.channelCount(); i++) {
//   //   data = mux.read(i) /* Reads from channel i (returns HIGH or LOW) */;

//   //   Serial.print("Push button at channel "); Serial.print(i); Serial.print(" is "); Serial.println(data == HIGH ? "pressed" : "not pressed");
//   //   Serial.print(i);
//   // }

//   while (data == HIGH ){  //if you want more resolution, lower this number
//     delay(100);

//     pressLength_milliSeconds = pressLength_milliSeconds + 100;   

//     //display how long button is has been held
//     Serial.print("ms = ");
//     Serial.println(pressLength_milliSeconds);
//     // update new data
//     data = mux.read(selpin);

//   }//close while


//   //Different if-else conditions are triggered based on the length of the button press
//   //Start with the longest time option first

//   //Option 2 - Execute the second option if the button is held for the correct amount of time
//   if (pressLength_milliSeconds >= optionTwo_milliSeconds){
//     Serial.print("op 2");      

//   } 

//   //option 1 - Execute the first option if the button is held for the correct amount of time
//   else if(pressLength_milliSeconds >= optionOne_milliSeconds){
//     Serial.print("op 1");  

//   }//close if options


//   //every time through the loop, we need to reset the pressLength_Seconds counter
//   pressLength_milliSeconds = 0;
// }