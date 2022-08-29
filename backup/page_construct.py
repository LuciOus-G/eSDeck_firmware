
try:
    from util import load_config
    from multiplexer import Mux, Displays
    import framebuf
except Exception as e:
    print(e)

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
        self.page: str = 'homepage'
        self.base_page: str = 'homepage'
        self.current_data: dict = {}
        self.config_json = self._init_config_json()
        Displays.__init__(self, 0x70)
        
        # initiation of object
        self._extract_data_per_page() # it should be first init for data
        self._reg_button()
        self._init_display_start()
        
        
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
        self.b1 = Mux(0, self._display_oled, self.current_data["b1"], self.in_test)
        self.b2 = Mux(1, self._display_oled, self.current_data["b1"], self.in_test)
        self.b3 = Mux(2, self._display_oled, self.current_data["b1"], self.in_test)
        self.b4 = Mux(3, self._display_oled, self.current_data["b1"], self.in_test)
        self.b5 = Mux(4, self._display_oled, self.current_data["b1"], self.in_test)
        self.b6 = Mux(5, self._display_oled, self.current_data["b1"], self.in_test, self.in_test_long)
        self.b7 = Mux(6, self._display_oled, self.current_data["b1"], self.in_test)
        self.b8 = Mux(7, self._display_oled, self.current_data["b1"], self.in_test, self.in_test_long)
    
    def button_selector(self):
        self._extract_data_per_page()
        
        self.b1.run() # chagne page to 3 pressed
        self.b2.run()
        self.b3.run()
        self.b4.run()
        self.b5.run()
        self.b6.run()
        self.b7.run()
        self.b8.run()
        
        
    def _extract_data_per_page(self):
        self.current_data = self.config_json[self.page]
        
    def _change_page_data(self, new_page):
        self.page = new_page
        
    # oled section
    def _center_text(self, text):
        _len = len(text)
        
        self.oled.text(text, 64 - _len*3, 50, 1)
        
    
    def _init_display_start(self):
        self.enable_channel(0)
        self.init_ssd1306()
    
        new_data = bytearray(self.current_data["b1"]["image"])
        fbuf = framebuf.FrameBuffer(new_data, 128, 64, framebuf.MONO_HLSB)

        self.oled.fill(0)
        self.oled.blit(fbuf, 0, -10)
        self.oled.show()
        
        self.enable_channel(1)
        
        new_data = bytearray(self.current_data["b1"]["image"])
        fbuf = framebuf.FrameBuffer(new_data, 128, 64, framebuf.MONO_HLSB)

        self.oled.fill(0)
        self.oled.blit(fbuf, 0, -10)
        self._center_text("ini text")
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
            
    def run_forever(self):
        while True:
            try:
                # print(self.current_data)
                self.button_selector()
            except Exception as e:
                print(e)
                
                
                
# _task = pageConstruct()
# _task.run_forever()