from platform_modules.lcd_driver import LCD
from platform_modules.button_reader import ButtonReader
import time
import datetime
import config
import global_storage as gs

# Init LCD
lcd = LCD(config.LCD_ADDRESS)

# Init button reader
button_reader = ButtonReader()
button_reader.start()

while True:
    lcd.lcd_clear()
    lcd.lcd_display_string("UI testing", 1)
    lcd.lcd_display_string("Button status: ", 2)
    button_values = [gs.button_1, gs.button_2, gs.button_3, gs.button_4, gs.button_ss1, gs.button_ss2]
    button_values = list(map(int, button_values)) 
    lcd.lcd_display_string("{} {} {} {} {} {}".format(*button_values), 3)
    lcd.lcd_display_string(str(datetime.datetime.now().time()), 4)
    time.sleep(2)


button_reader.join()