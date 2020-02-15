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

# Save last value of buttons
last_button_1 = False
last_button_2 = False
last_button_3 = False
last_button_4 = False
last_button_ss1 = False
last_button_ss2 = False

while True:
    lcd.lcd_clear()
    lcd.lcd_display_string("UI testing", 1)
    lcd.lcd_display_string("Button status: ", 2)
    button_values = [gs.button_1, gs.button_2, gs.button_3, gs.button_4, gs.button_ss1, gs.button_ss2]
    button_values = list(map(int, button_values)) 
    lcd.lcd_display_string("{} {} {} {} {} {}".format(*button_values), 3)
    
    # Determine pressed buttons
    pressed_buttons = []
    if gs.button_1 and not last_button_1:
        pressed_buttons.append("1")
    if gs.button_2 and not last_button_2:
        pressed_buttons.append("2")
    if gs.button_3 and not last_button_3:
        pressed_buttons.append("3")
    if gs.button_4 and not last_button_4:
        pressed_buttons.append("4")
    if gs.button_ss1 and not last_button_ss1:
        pressed_buttons.append("S1")
    if gs.button_ss2 and not last_button_ss2:
        pressed_buttons.append("S2")

    if pressed_buttons:
        lcd.lcd_display_string("Pressed:" + ",".join(pressed_buttons), 4)

    # Update values
    last_button_1 = gs.button_1
    last_button_2 = gs.button_2
    last_button_3 = gs.button_3
    last_button_4 = gs.button_4
    last_button_ss1 = gs.button_ss1
    last_button_ss2 = gs.button_ss2

    time.sleep(1)


button_reader.join()