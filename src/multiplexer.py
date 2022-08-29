from machine import I2C, Pin
import ustruct

class Mux:
    def __init__(self, channel_id: int, short_func, long_func=False):
        self.S0 = Pin(14, Pin.OUT)
        self.S1 = Pin(12, Pin.OUT)
        self.S2 = Pin(13, Pin.OUT)
        self.signal = Pin(16, Pin.IN)
        self._reset()
        self.current_bits = "000"
        self.state = False
        self.long_mili = 0
        self.Msignal = 16
        self.long_time = 700
        self.channel_id = channel_id
        self.short_func = short_func
        self.long_func = long_func

    def _reset(self):
        self.S0.off()
        self.S1.off()
        self.S2.off()

    def _bits_to_channel(self, bits):
        return int("000" + "".join([str(x) for x in "".join(reversed(bits))]), 2)

    def _channel_to_bits(self, channel_id):
        return "".join(reversed("{:0>{w}}".format(bin(channel_id)[2:], w=3)))

    def _switch_pins_with_bits(self, bits):
        s0, s1, s2 = [int(x) for x in tuple(bits)]
        self.S0(s0)
        self.S1(s1)
        self.S2(s2)

    def run(self, b_data,  oled_func=None):
        bits = self._channel_to_bits(self.channel_id)
        self._switch_pins_with_bits(bits)
        self.current_bits = bits        
              
        # TODO: if type page, get all image display and update the display
            
        while self.signal.value():
            print(self.long_mili)
            self.long_mili += 1
        if not self.signal.value():
            if self.long_mili <= self.long_time and self.long_mili != 0:
                if b_data.get("type", None) == 'page':
                    print("masuk typr page")
                    if oled_func:
                        oled_func(update=True, page=b_data.get("topage", None))
                else:
                    self.short_func()
            elif self.long_mili >= self.long_time:
                if self.long_func:
                    if b_data.get("type", None) == 'page':
                        print("masuk typr page")
                        if oled_func:
                            oled_func(update=True, page=b_data.get("topage", None))
                    else:
                        self.long_func()
            self.long_mili = 0


class Displays:
    def __init__(self, address) -> None:
        self.address = address
        self.scl = Pin(5)
        self.sda = Pin(4)
        self.i2c = I2C(scl=self.scl, sda=self.sda)
        self.oled = None
        self.error = []
        
    def _scan(self) -> list:
        return self.i2c.scan()
    
    def _readfrom(self):
        return self.i2c.readfrom(self.address, 1)
    
    def enable_channel(self, channel):
        self.i2c.writeto(self.address, ustruct.pack('B',1 << channel))
        
        if self.oled:
            self.oled.init_display()
    
    def init_ssd1306(self):
        import ssd1306
        self.oled = ssd1306.SSD1306_I2C(128, 64, self.i2c)
    
error = []
    
# try:
#     pass        
    
    # display = Displays(address=0x70)
    
    # display.enable_channel(0)
    # display.init_ssd1306()
    
    # data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 63, 248, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 255, 255, 192, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 255, 255, 240, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 255, 255, 248, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 255, 255, 255, 255, 253, 255, 224, 0, 0, 0, 0, 0, 0, 0, 0, 127, 255, 255, 255, 255, 255, 255, 248, 0, 0, 0, 0, 0, 0, 0, 0, 96, 3, 0, 1, 255, 255, 128, 30, 0, 0, 0, 0, 0, 0, 0, 0, 192, 0, 0, 0, 31, 254, 63, 199, 0, 0, 0, 0, 0, 0, 0, 0, 207, 252, 127, 255, 199, 249, 255, 243, 0, 0, 0, 0, 0, 0, 0, 0, 111, 252, 127, 255, 243, 243, 255, 249, 0, 0, 0, 0, 0, 0, 0, 0, 111, 252, 127, 255, 251, 231, 255, 253, 0, 0, 0, 0, 0, 0, 0, 0, 111, 252, 127, 255, 249, 143, 255, 252, 0, 0, 0, 0, 0, 0, 0, 0, 111, 248, 127, 255, 253, 159, 255, 252, 0, 0, 0, 0, 0, 0, 0, 0, 111, 248, 127, 255, 252, 63, 249, 252, 0, 0, 0, 0, 0, 0, 0, 0, 111, 248, 63, 199, 252, 63, 243, 252, 0, 0, 0, 0, 0, 0, 0, 0, 103, 248, 63, 195, 254, 127, 227, 253, 0, 0, 0, 0, 0, 0, 0, 0, 103, 248, 63, 203, 254, 127, 195, 253, 0, 0, 0, 0, 0, 0, 0, 0, 103, 248, 63, 195, 254, 255, 193, 251, 0, 0, 0, 0, 0, 0, 0, 0, 103, 248, 63, 199, 252, 255, 192, 99, 0, 0, 0, 0, 0, 0, 0, 0, 103, 248, 63, 255, 252, 255, 128, 15, 0, 0, 0, 0, 0, 0, 0, 0, 103, 240, 63, 255, 252, 255, 144, 255, 0, 0, 0, 0, 0, 0, 0, 0, 103, 240, 63, 255, 248, 255, 192, 1, 0, 0, 0, 0, 0, 0, 0, 0, 103, 240, 63, 255, 248, 255, 195, 253, 0, 0, 0, 0, 0, 0, 0, 0, 103, 240, 63, 255, 240, 255, 193, 253, 0, 0, 0, 0, 0, 0, 0, 0, 111, 244, 63, 255, 224, 255, 225, 249, 0, 0, 0, 0, 0, 0, 0, 0, 111, 252, 63, 255, 140, 255, 225, 249, 0, 0, 0, 0, 0, 0, 0, 0, 111, 252, 63, 220, 60, 127, 241, 249, 0, 0, 0, 0, 0, 0, 0, 0, 239, 252, 63, 192, 124, 127, 253, 249, 0, 0, 0, 0, 0, 0, 0, 0, 143, 252, 63, 192, 0, 127, 255, 249, 0, 0, 0, 0, 0, 0, 0, 0, 15, 252, 63, 192, 0, 63, 255, 249, 0, 0, 0, 0, 0, 0, 0, 0, 15, 252, 127, 192, 0, 31, 255, 249, 0, 0, 0, 0, 0, 0, 0, 0, 15, 252, 127, 192, 0, 15, 255, 249, 0, 0, 0, 0, 0, 0, 0, 0, 15, 254, 127, 224, 0, 7, 255, 249, 0, 0, 0, 0, 0, 0, 0, 0, 143, 252, 127, 224, 0, 1, 255, 253, 0, 0, 0, 0, 0, 0, 0, 0, 207, 248, 127, 239, 224, 0, 63, 253, 0, 0, 0, 0, 0, 0, 0, 0, 192, 2, 0, 15, 255, 192, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 127, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 63, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 127, 255, 255, 240, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 255, 255, 240, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 255, 255, 224, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 255, 255, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 127, 252, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # new_data = bytearray(data)
    
    # fbuf = framebuf.FrameBuffer(new_data, 128, 64, framebuf.MONO_HLSB)
    # display.oled.fill(0)
    # display.oled.blit(fbuf, 0, 0)
    # display.oled.show()
    
    # display.enable_channel(1)
    
    # display.oled.fill(0)
    # display.oled.text("Display 2", 0, 0, 1)
    # display.oled.show()
    
# except Exception as e:
#     error.append(e)

# def load_conf():
#     return load_config()["homepage"]

# def change_image():
    
#     display = Displays(address=0x70)
#     display.enable_channel(0)
#     display.init_ssd1306()
#     data = load_conf()["image"]
#     new_data = bytearray(data)
#     fbuf = framebuf.FrameBuffer(new_data, 128, 64, framebuf.MONO_HLSB)

#     display.oled.fill(0)
#     display.oled.blit(fbuf, 0, 0)
#     display.oled.show()

#     display.enable_channel(1)

#     display.oled.fill(0)
#     display.oled.text("Display 2", 0, 0, 1)
#     display.oled.show()

# while True:
#     try:
#         print(error)
#     except Exception as e:
#         print(e)