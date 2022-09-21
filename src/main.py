from util import load_config, wifi_server
from multiplexer import Mux, Displays
import framebuf
import time
import uasyncio

class buttonInit:
  def __init__(self) -> None:
    self.b1 = None
    self.b2 = None
    self.b3 = None
    self.b4 = None
    self.b5 = None
    self.b6 = None
    self.b7 = None
    self.b8 = None

class pageConstruct(Displays, buttonInit):
    def __init__(self):
        buttonInit.__init__(self)
        self.page: str = ''
        self.base_page: str = 'homepage'
        self.current_data: dict = {}
        self.config_json = self._init_config_json()
        Displays.__init__(self, 0x70)
        
        # initiation of object
        self._extract_data_per_page(self.base_page) # it should be first init for data
        self._reg_button()
        self._init_display_start(update=True)
        
        
    def _init_config_json(self):
        data = load_config()
        return data
    
    def _switch_page(self, page: str):
        self.page = page
        
    def in_test(self, num=10):
        print(f"ini dari button {num}")
        
    def in_test_long(self, num=10):
        print(f"ini dari button long {num}")
    
    # button section
    def _reg_button(self):
        self.b1 = Mux(0, self.in_test)
        self.b2 = Mux(1, self.in_test)
        self.b3 = Mux(2, self.in_test)
        self.b4 = Mux(3, self.in_test)
        self.b5 = Mux(4, self.in_test)
        self.b6 = Mux(5, self.in_test, self.in_test_long)
        self.b7 = Mux(6, self.in_test)
        self.b8 = Mux(7, self.in_test, self.in_test_long)
    
    def button_selector(self):        
        self.b1.run(self.current_data["b1"], self.test_display_async) # chagne page to 3 pressed
        self.b2.run(self.current_data["b1"], self.test_display_async)
        self.b3.run(self.current_data["b1"], self.test_display_async)
        self.b4.run(self.current_data["b1"], self.test_display_async)
        self.b5.run(self.current_data["b1"], self.test_display_async)
        self.b6.run(self.current_data["b1"], self.test_display_async)
        self.b7.run(self.current_data["b1"], self.test_display_async)
        self.b8.run(self.current_data["b1"], self.test_display_async)
        
        
    def _extract_data_per_page(self, page):
        self.current_data = self.config_json[page]
        
    def _change_page_data(self, new_page):
        self.page = new_page
        
    # oled section
    def _center_text(self, text):
        _len = len(text)
        
        self.oled.text(text, 64 - _len*4, 50, 1)
        
    async def display_1(self):
        # display 1
        self.enable_channel(0)
        self.init_ssd1306()
    
        new_data = bytearray(self.current_data["b1"]["image"])
        fbuf = framebuf.FrameBuffer(new_data, 128, 64, framebuf.MONO_HLSB)

        self.oled.fill(0)
        self.oled.blit(fbuf, 0, -10)
        self.oled.show()
        await uasyncio.sleep_ms(10)
        
    async def display_2(self):
        # display 2
        self.enable_channel(1)
    
        new_data = bytearray(self.current_data["b1"]["image"])
        fbuf = framebuf.FrameBuffer(new_data, 128, 64, framebuf.MONO_HLSB)

        self.oled.fill(0)
        self.oled.blit(fbuf, 0, -10)
        self.oled.show()
        await uasyncio.sleep_ms(10)
    
    async def display_3(self):
        # display 3
        self.enable_channel(2)
    
        new_data = bytearray(self.current_data["b1"]["image"])
        fbuf = framebuf.FrameBuffer(new_data, 128, 64, framebuf.MONO_HLSB)

        self.oled.fill(0)
        self.oled.blit(fbuf, 0, -10)
        self.oled.show()
        await uasyncio.sleep_ms(10)
    
    async def display_4(self):
        # display 4
        self.enable_channel(3)
    
        new_data = bytearray(self.current_data["b1"]["image"])
        fbuf = framebuf.FrameBuffer(new_data, 128, 64, framebuf.MONO_HLSB)

        self.oled.fill(0)
        self.oled.blit(fbuf, 0, -10)
        self.oled.show()
        await uasyncio.sleep_ms(10)
        
    async def display_5(self):
        # display 5
        self.enable_channel(4)
    
        new_data = bytearray(self.current_data["b1"]["image"])
        fbuf = framebuf.FrameBuffer(new_data, 128, 64, framebuf.MONO_HLSB)

        self.oled.fill(0)
        self.oled.blit(fbuf, 0, -10)
        self.oled.show()
        await uasyncio.sleep_ms(10)
        
        
    async def test_display_async(self):
        await self.display_1()
        uasyncio.create_task(self.display_2())
        uasyncio.create_task(self.display_3())
        uasyncio.create_task(self.display_4())
        uasyncio.create_task(self.display_5())
        
        
    def _init_display_start(self, update=False, page: str="None"):
        if update:
            if page != "None":
                self._change_page_data(page)
                self._extract_data_per_page(page)
            
            # display 2
            self.enable_channel(1)
            
            new_data = bytearray(self.current_data["b1"]["image"])
            fbuf = framebuf.FrameBuffer(new_data, 128, 64, framebuf.MONO_HLSB)

            self.oled.fill(0)
            self.oled.blit(fbuf, 0, -10)
            self._center_text(page)
            self.oled.show()
            
            # display 3
            self.enable_channel(2)
            
            new_data = bytearray(self.current_data["b1"]["image"])
            fbuf = framebuf.FrameBuffer(new_data, 128, 64, framebuf.MONO_HLSB)

            self.oled.fill(0)
            self.oled.blit(fbuf, 0, -10)
            self._center_text(page)
            self.oled.show()
            
            # display 4
            self.enable_channel(3)
            
            new_data = bytearray(self.current_data["b1"]["image"])
            fbuf = framebuf.FrameBuffer(new_data, 128, 64, framebuf.MONO_HLSB)

            self.oled.fill(0)
            self.oled.blit(fbuf, 0, -10)
            self._center_text(page)
            self.oled.show()
            
            # display 5
            self.enable_channel(4)
            
            new_data = bytearray(self.current_data["b1"]["image"])
            fbuf = framebuf.FrameBuffer(new_data, 128, 64, framebuf.MONO_HLSB)

            self.oled.fill(0)
            self.oled.blit(fbuf, 0, -10)
            self._center_text(page)
            self.oled.show()
    
    def _display_oled(self, channel=None, bmp_data=None, text=None):
        
        if self.oled:           
            if channel and channel != 0:
                self.oled.enable_channel(channel)
                
            self.oled.oled.fill(0)
            
            if bmp_data:
                new_data = bytearray(bmp_data)
                fbuf = framebuf.FrameBuffer(new_data, 128, 64, framebuf.MONO_HLSB)
                self.oled.blit(fbuf, 0, -10)
            
            if text:
                self._center_text(text)
                
            self.oled.oled.show()
            
    async def run_forever(self):
        while True:
            try:
                self.button_selector()
                await uasyncio.seleep_ms(10)
            except Exception as e:
                pass


# wifi_server()
                
_task = pageConstruct()
uasyncio.run(_task.run_forever())