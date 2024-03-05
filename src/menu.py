import utime

from lcd import Lcd


class Menu:

    def __init__(self, lcd: Lcd, main_menu, sub_menus):
        self.afficheur = lcd
        self.main_menu = main_menu
        self.sub_menus = sub_menus
        self.current_menu_selected = 0
        self.current_menu_start_index = 0
        self.current_menu = main_menu

    def select(self, is_main: bool, sub_menu_index: int = 0):
        if is_main:
            self.current_menu = self.main_menu
            self.current_menu_start_index = 0
            self.current_menu_selected = 0
            self.display(self.current_menu)
        else:
            self.current_menu = self.sub_menus[sub_menu_index]
            self.current_menu_start_index = 0
            self.current_menu_selected = 0
            self.display(self.current_menu)

    def display(self, menu):
        self.afficheur.lcd.clear()
        for i in range(self.current_menu_start_index, min(len(menu), self.current_menu_start_index + 2)):
            if i == self.current_menu_selected:
                self.afficheur.lcd.putstr("* " + menu[i] + "\n")
            else:
                self.afficheur.lcd.putstr("  " + menu[i] + "\n")

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

    def validate(self, action, sub_menu_index: int = 0):
        if action == "sub_menu":
            self.select(False, sub_menu_index)

        if action == "presets_selection":
            self.set_text("Presets selection")
            utime.sleep(2)
            self.exit()

        if action == "settings_selection":
            self.set_text("Settings selection")
            utime.sleep(2)
            self.exit()

    def exit(self):
        self.select(True)

    def get_current_option_selected(self):
        return self.current_menu[self.current_menu_selected]
