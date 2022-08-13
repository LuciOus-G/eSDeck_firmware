
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
// #include "onefuncbutton.h"
#include "Mux.h"
#include "buttonreg.h"

#define UDP_PORT 10086
#define PINSET Pinset(3,2,0)
#define SIGNAl 16 // D0

using namespace admux;

String host = "192.168.100.11";
uint16_t port = 50500;
WiFiClient client;


void fClicked(char *s)
{
  Serial.print("Click:");
  Serial.println((char *)s);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);


  WiFi.begin("apapihaus", "didonghaus");

  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());

}

void loop() {
  buttonReg button_1 = buttonReg(SIGNAl, PINSET, 1);
  buttonReg button_2 = buttonReg(SIGNAl, PINSET, 0);

  button_1.singlePressParam(fClicked, " me");
  button_2.singlePress(testnoaparam);

  button_1.tick();
  button_2.tick();

  // put your main code here, to run repeatedly:
  // 
  // Serial.println(buttonRegs(0, 4, Pinset(14, 2, 0)) == LOW);
  // while(!client.connect(host, port)){
  //   delay(500);
  //   Serial.print(".");
  //   Serial.print(client.connect(host, port));
  // }
}



// int button = 4; //D2(gpio4)
// bool buttonState = 1;
// int mili = 0;
// void setup() {
//   Serial.begin(115200);
// pinMode(button, INPUT_PULLUP);
// }
// void loop() {
// bool CurrentState = digitalRead(button); // put your main code here, to run repeatedly:
// Serial.print(CurrentState);
// Serial.print("\n");
// if (CurrentState == buttonState)
// {
// //  Serial.print("preesed\n");
//  while(CurrentState == 1){
//    // DO NOTHING
//    mili += 100;
//    Serial.print("hold press\n");
//    Serial.print(digitalRead(button));
//    Serial.print("\n");
//    Serial.print(mili);
//    Serial.print("\n");

//    if(mili >= 1000){
//      Serial.print("other func\n");
//        CurrentState = 0;
//        mili = 0;
//      }
//    delay(500);
//  }
// }
// if (buttonState==0)
// {
// // Serial.print("unpreesed\n"); 
// delay(1000);
// }
// }

void test(void *text){
  Serial.println((char *)text);
}

void testnoaparam(){
  Serial.print("masuk sini no param");
}