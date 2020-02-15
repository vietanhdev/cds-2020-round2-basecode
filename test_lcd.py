from platform_modules.lcd_driver import LCD
import time
import datetime
import config

lcd = LCD(config.LCD_ADDRESS)

while True:
    lcd.lcd_clear()
    lcd.lcd_display_string("This is LCD code", 1)
    lcd.lcd_display_string("From Viet Anh", 2)
    lcd.lcd_display_string("W: vietanhdev.com", 3)
    lcd.lcd_display_string(str(datetime.datetime.now().time()), 4)
    time.sleep(1)