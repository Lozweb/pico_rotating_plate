import re
import utime
from machine import Pin
from lcd import Lcd
from button import Button
from menu import Menu
from motor import MotorStep

exit_btn = Button(15)
ok_btn = Button(13)
down_btn = Button(12)
up_btn = Button(14)

afficheur = Lcd(1, Pin(2), Pin(3), 400000, 0)
menu = Menu(afficheur)
motor = MotorStep(18, 19, 20, 21, menu)

while True:

    if down_btn.button_pressed():
        menu.to_down()
        while down_btn.button_pressed():
            utime.sleep_ms(50)

    if up_btn.button_pressed():
        menu.to_up()
        while exit_btn.button_pressed():
            utime.sleep_ms(50)

    if ok_btn.button_pressed():
        selected_option = menu.get_current_option_selected()

        if selected_option == "start":
            motor.exec(
                menu.settings.current_preset.direction,
                menu.settings.current_preset.tt_degree,
                menu.settings.current_preset.pause,
                menu.settings.current_preset.delay
            )

        elif selected_option == "presets":
            menu.validate("sub_menu", 0)

        elif selected_option == "settings":
            menu.validate("sub_menu", 1)

        else:
            reg_preset = re.compile("preset-[0-9]")
            reg_settings = re.compile("set-[a-z]*")
            
            if reg_preset.match(selected_option):
                menu.action("preset_settings", selected_option)

            if reg_settings.match(selected_option):
                menu.action("settings", selected_option)

        while ok_btn.button_pressed():
            utime.sleep_ms(50)

    if exit_btn.button_pressed():
        menu.exit()
        motor.current_position = 0
        while ok_btn.button_pressed():
            utime.sleep_ms(50)

    utime.sleep(0.1)
