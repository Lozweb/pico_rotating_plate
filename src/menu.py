import utime

from lcd import Lcd
from preset import Preset
from settings import Settings
from button import Button


class Menu:

    def __init__(self, lcd: Lcd):
        self.afficheur = lcd
        self.settings = Settings()
        self.ok_btn = Button(13)
        self.up_btn = Button(14)
        self.down_btn = Button(12)
        self.exit_btn = Button(15)
        self.is_in_settings = False
        self.main_menu = ["start", "presets", "settings"]
        self.sub_menus = [
            ["preset-1", "preset-2", "preset-3", "preset-4"],
            ["set-degree", "set-steps", "set-delay", "set-direction"],
        ]
        self.current_menu_selected = 0
        self.current_menu_start_index = 0
        self.current_menu = self.main_menu
        self.display(self.current_menu)

    def validate(self, action, sub_menu_index: int = 0):
        if action == "sub_menu":
            self.select(False, sub_menu_index)

    def action(self, action: str, values: str):
        if action == "preset_settings":
            self.settings.load_preset(values)
            self.return_home()
        else:                
            if values == "set-delay":
                
                while self.ok_btn.button_pressed():
                    utime.sleep_ms(50)
                
                self.is_in_settings = True
                while self.is_in_settings:
                            
                    self.set_text("delay : " + str(self.settings.current_preset.delay) + " sec")

                    if self.up_btn.button_pressed():
                        self.settings.current_preset.delay += 1
                        while self.up_btn.button_pressed():
                            utime.sleep_ms(50)

                    if self.down_btn.button_pressed():
                        self.settings.current_preset.delay -= 1
                        while self.down_btn.button_pressed():
                            utime.sleep_ms(50)

                    if self.ok_btn.button_pressed():
                        self.is_in_settings = False
                        self.settings.save_preset()
                        self.return_home()
                        while self.ok_btn.button_pressed():
                            utime.sleep_ms(50)

                    if self.exit_btn.button_pressed():
                        self.is_in_settings = False
                        self.return_home()
                        while self.exit_btn.button_pressed():
                            utime.sleep_ms(50)

                    utime.sleep(0.1)

    def return_home(self):
        self.current_menu = self.main_menu
        self.current_menu_start_index = 0
        self.current_menu_selected = 0
        self.display(self.current_menu)

    def select(self, is_main: bool, sub_menu_index: int = 0):
        if is_main:
            self.return_home()
        else:
            self.current_menu = self.sub_menus[sub_menu_index]
            self.current_menu_start_index = 0
            self.current_menu_selected = 0
            self.display(self.current_menu)

    def display(self, menu):
        self.afficheur.lcd.clear()
        for i in range(self.current_menu_start_index, min(len(menu), self.current_menu_start_index + 2)):
            if i == self.current_menu_selected:
                self.afficheur.lcd.putstr("*" + self.set_menu_text(menu[i]) + "\n")
            else:
                self.afficheur.lcd.putstr(" " + self.set_menu_text(menu[i]) + "\n")

    def set_menu_text(self, menu: str):
        if menu == "start":
            return menu + " " + self.settings.current_preset.name
        else:
            return menu

    def to_down(self):
        if self.current_menu_selected > 0:
            self.current_menu_selected -= 1
            if self.current_menu_selected < self.current_menu_start_index:
                self.current_menu_start_index -= 1
        self.display(self.current_menu)

    def to_up(self):
        if self.current_menu_selected < len(self.current_menu) - 1:
            self.current_menu_selected += 1
            if self.current_menu_selected > self.current_menu_start_index:
                self.current_menu_start_index += 1
        self.display(self.current_menu)

    def set_text(self, txt: str):
        self.afficheur.lcd.clear()
        self.afficheur.lcd.putstr(txt)

    def exit(self):
        self.select(True)

    def get_current_option_selected(self):
        return self.current_menu[self.current_menu_selected]
