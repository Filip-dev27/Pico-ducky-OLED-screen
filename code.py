import time
import board
import busio
import displayio
import terminalio
import digitalio
from adafruit_display_text import label
from adafruit_displayio_ssd1306 import SSD1306
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode


displayio.release_displays()
i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = SSD1306(display_bus, width=128, height=64)


time.sleep(1)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)


def show_text(text, scale=1, color=0xFFFFFF):
   
    splash = displayio.Group()
    display.show(splash)
    
  
    text_area = label.Label(terminalio.FONT, text=text, color=color, scale=scale)
    text_area.x = 10
    text_area.y = 30 if scale == 1 else 20
    splash.append(text_area)
    
    display.refresh()

show_text("Pico-Ducky", scale=2)
time.sleep(2)

try:
    with open("/payload.dd", "r") as file:
        payload = file.readlines()
        
    for line in payload:
        line = line.strip()
        if line.startswith("DELAY"):
            delay_time = int(line.split()[1]) / 1000
            show_text(f"Delay: {delay_time}s")
            time.sleep(delay_time)
        elif line.startswith("STRING"):
            text = line[7:]
            show_text(f"Typing: {text}")
            keyboard_layout.write(text)
        elif line.startswith("ENTER"):
            show_text("Pressing ENTER")
            keyboard.press(Keycode.ENTER)
            keyboard.release_all()
        else:
            show_text(f"Cmd: {line}")
            
            
except OSError:
    show_text("Error: No payload.dd")
    time.sleep(2)

show_text("Done!")