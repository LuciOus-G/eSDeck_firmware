import json
import network

def load_config(data = 'data.json') -> dict:
    # load the config json
    data = open(data, 'r')
    data_to_json = json.load(data)
    
    return data_to_json

# wifi config
def wifi_client(ssid: str, passw: str):
    sta_if = network.WLAN(network.STA_IF)
    
    sta_if.active(True)
    sta_if.connect(
        ssid,
        passw
    )
    
    while not sta_if.isconnected():
        pass
    
    if sta_if.isconnected():
        return sta_if
    else:
        return False
    
def wifi_server():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="eSDeck", password="1234567890")
    