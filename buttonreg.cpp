#include "buttonreg.h"

buttonReg::buttonReg(){}

buttonReg::buttonReg(int8_t signalPin, Pinset pinSet, int8_t pinSelect){
    _pinSelect = pinSelect;
    _muxConstruct = Mux(Pin(signalPin, INPUT, PinType::Digital), pinSet);
}

void buttonReg::singlePress(callbackFunction newFunc){
    _executeFunc = newFunc;
}

void buttonReg::singlePressParam(parameterizedCallbackFunction newFunc, char *parameter){
    _singleFuncParam = parameter;
    _executeParamFunc = newFunc;
}


void buttonReg::longPress(callbackFunction newFunc){
    _executeLongFunc = newFunc;
}

void buttonReg::longPressParam(parameterizedCallbackFunction newFunc, char *parameter){
    _longPresseParamFunc = parameter;
    _executeParamLongFunc = newFunc;
}

void buttonReg::tick(){
    float pressLength_milliSeconds = 0;
    int optionOne_milliSeconds = 100;
    int optionTwo_milliSeconds = 1000;
    byte data = _muxConstruct.read(_pinSelect);

    while (data == HIGH ){
        Serial.print(_pinSelect);
        delay(100);

        pressLength_milliSeconds = pressLength_milliSeconds + 100;
        Serial.print("ms = ");
        Serial.println(pressLength_milliSeconds);

        // update new data
        data = _muxConstruct.read(_pinSelect);

    }

    if (pressLength_milliSeconds >= optionTwo_milliSeconds){
        if (_executeLongFunc){
            _executeLongFunc();
        }else if(_executeParamLongFunc){
            _executeParamLongFunc(_longPresseParamFunc);
        }else{
            defaultFunction();
        }
    }else if(pressLength_milliSeconds >= optionOne_milliSeconds){
        if(_executeFunc){
            _executeFunc();
        }else if(_executeParamFunc){
            _executeParamFunc(_singleFuncParam);
            Serial.print(_singleFuncParam);
            Serial.print("\n");
        }else{
            defaultFunction();
        }
    }
    pressLength_milliSeconds = 0;
}

void buttonReg::defaultFunction(){
    Serial.print("no function declare\n");
}