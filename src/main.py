import utime
from machine import Pin
from lcd import Lcd
from button import Button
from menu import Menu
from motor import MotorStep
from settings import Settings

exit_btn = Button(15)
ok_btn = Button(13)
down_btn = Button(14)
up_btn = Button(12)

afficheur = Lcd(1, Pin(2), Pin(3), 400000, 0)
menu = Menu(
    afficheur.get_instance(),
    ["start", "settings"],
    [
        ["total degree", "nb steps", "delay", "direction"],
    ]
)
motor = MotorStep(18, 19, 20, 21, menu)
menu.select(True)
settings = Settings()

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
        selected_option = menu.get_current_option_seleceted()

        if selected_option == "settings":
            menu.validate("sub_menu", 0)

        if selected_option == "start":
            motor.exec(
                settings.direction,
                settings.get_step(),
                settings.pause,
                settings.delay
            )

        while ok_btn.button_pressed():
            utime.sleep_ms(50)

    if exit_btn.button_pressed():
        menu.exit()
        motor.current_position = 0
        while ok_btn.button_pressed():
            utime.sleep_ms(50)

    utime.sleep(0.1)
