# """
# Blynk is a platform with iOS and Android apps to control
# Arduino, Raspberry Pi and the likes over the Internet.
# You can easily build graphic interfaces for all your
# projects by simply dragging and dropping widgets.
#   Downloads, docs, tutorials: http://www.blynk.cc
#   Sketch generator:           http://examples.blynk.cc
#   Blynk community:            http://community.blynk.cc
#   Social networks:            http://www.fb.com/blynkapp
#                               http://twitter.com/blynk_app
# This example shows how to initialize your ESP8266/ESP32 board
# and connect it to Blynk.
# Don't forget to change WIFI_SSID, WIFI_PASS and BLYNK_AUTH ;)
# """

# import BlynkLib
# import network
# import machine

# WIFI_SSID = 'apapihaus'
# WIFI_PASS = 'didonghaus'

# BLYNK_AUTH = '7Yojk-J6oFhRDyd6kneD6XznL_FljDiW'

# wifi = network.WLAN(network.STA_IF)
# if not wifi.isconnected():
#     print("Connecting to WiFi...")
#     wifi.active(True)
#     wifi.connect(WIFI_SSID, WIFI_PASS)
#     while not wifi.isconnected():
#         pass

# print('IP:', wifi.ifconfig()[0])

# blynk = BlynkLib.Blynk(BLYNK_AUTH)

# @blynk.on("connected")
# def blynk_connected(ping):
#     print('Blynk ready. Ping:', ping, 'ms')
    
# @blynk.on("V3")
# def v3_write_handler(value):
#     print('Current slider value: {}'.format(value[0]))

# while True:
#     blynk.run()

from machine import Pin
from machine import Timer
from ir_rx import NEC_16


def ir_callback(data, addr, ctrl):
    global ir_data
    global ir_addr
    if data > 0:
        ir_data = data
        ir_addr = addr
        print('Data {:02x} Addr {:04x}'.format(data, addr))
            
def timer_callback(timer):
    led.value( not led.value() )        

ir = NEC_16(Pin(2, Pin.IN), ir_callback)
led = Pin(2, Pin.OUT)
tim0 = Timer(0)
isLedBlinking = False
ir_data = 0
ir_addr = 0

while True:
    if ir_data > 0:
        print(ir_data)
        if ir_data == 0x16:   # 0
            led.value(0)
            if isLedBlinking==True:
                tim0.deinit()
                isLedBlinking = False
        elif ir_data == 0x0C: # 1
            led.value(1)
            if isLedBlinking==True:
                tim0.deinit()
                isLedBlinking = False
        elif ir_data == 0x18: # 2
            isLedBlinking = True
            tim0.init(period=500,
                      mode=Timer.PERIODIC,
                      callback=timer_callback)
        ir_data = 0
