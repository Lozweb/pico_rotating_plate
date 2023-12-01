from machine import Pin


class Button:

    def __init__(self, pin):
        self.pin_button = pin
        self.button = Pin(self.pin_button, Pin.IN, Pin.PULL_UP)

    def button_pressed(self):
        if self.button.value() == 0:
            return True
        else:
            return False
