#ifndef buttonreg_h
#define buttonreg_h

#include "Arduino.h"
#include "Mux.h"

using namespace admux;

extern "C" {
    typedef void (*callbackFunction)(void);
    typedef void (*parameterizedCallbackFunction)(char *);
}

class buttonReg{
    public:
        buttonReg();
        buttonReg(int8_t signalPin, Pinset pinSet, int8_t pinSelect);

        void singlePress(callbackFunction newFunc);
        void singlePressParam(parameterizedCallbackFunction newFunc, char *parameter);
        void longPress(callbackFunction newFunc);
        void longPressParam(parameterizedCallbackFunction newFunc, char *parameter);
        void tick();
        void defaultFunction();

    private:
        callbackFunction _executeFunc = NULL;
        parameterizedCallbackFunction _executeParamFunc = NULL;
        char *_singleFuncParam = NULL;

        callbackFunction _executeLongFunc = NULL;
        parameterizedCallbackFunction _executeParamLongFunc = NULL;
        char *_longPresseParamFunc = NULL;


        Mux _muxConstruct = Mux(Pin(4, INPUT, PinType::Digital), Pinset(14, 2, 0));
        int8_t _pinSelect = 0;
};

#endif