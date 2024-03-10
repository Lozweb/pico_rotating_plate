import re
import utime
from machine import Pin
from lcd import Lcd
from menu import Menu
from motor import MotorStep

afficheur = Lcd(1, Pin(2), Pin(3), 400000, 0)
menu = Menu(afficheur)
motor = MotorStep(18, 19, 20, 21, menu)

while True:

    in_settings = False

    if menu.down_btn.button_pressed() and menu.is_in_settings is False:
        menu.to_down()
        while menu.down_btn.button_pressed():
            utime.sleep_ms(50)

    if menu.up_btn.button_pressed() and menu.is_in_settings is False:
        menu.to_up()
        while menu.exit_btn.button_pressed():
            utime.sleep_ms(50)

    if menu.ok_btn.button_pressed() and menu.is_in_settings is False:
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

        while menu.ok_btn.button_pressed():
            utime.sleep_ms(50)

    if menu.exit_btn.button_pressed() and menu.is_in_settings is False:
        menu.exit()
        motor.current_position = 0
        while menu.ok_btn.button_pressed():
            utime.sleep_ms(50)

    utime.sleep(0.1)
