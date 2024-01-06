from machine import Pin
from menu import Menu
from math import ceil
import utime


class MotorStep:

    def __init__(self, in1: int, in2: int, in3: int, in4: int, menu: Menu):
        self.step_index = 0
        self.current_position = 0
        self.afficheur = menu
        self.min_step = 8
        self.min_degree = 0.70
        self.stepper_pins = [
            Pin(in1, Pin.OUT),
            Pin(in2, Pin.OUT),
            Pin(in3, Pin.OUT),
            Pin(in4, Pin.OUT)
        ]
        self.step_sequence_semi = [
            [1, 0, 0, 1],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1]
        ]

    def exec(self, direction: int, step: int, pause: int, delay: int):

        current_step = 0
        step_count = step
        count = 0

        while pause > current_step:

            for i in range(step_count):

                self.step_index = (self.step_index + direction) % len(self.step_sequence_semi)

                for pin_index in range(len(self.stepper_pins)):
                    pin_value = self.step_sequence_semi[self.step_index][pin_index]
                    self.stepper_pins[pin_index].value(pin_value)

                if count == 8:
                    if direction > 0:
                        self.current_position = self.float_sum(self.current_position, 0.70)
                    elif direction < 0:
                        self.current_position = self.float_sum(self.current_position, -0.70)
                    else:
                        self.afficheur.set_text("error direction")

                    self.display_current_position(pause, current_step)
                    count = 0

                utime.sleep(0.001)
                count += 1

            for pin_index in range(len(self.stepper_pins)):
                self.stepper_pins[pin_index].value(0)

            self.adjust_value()
            self.display_current_position(pause, current_step)

            current_step += 1
            utime.sleep(delay)

    def display_current_position(self, tt_step: int, current_step: int):
        self.afficheur.set_text("{0} deg \n{1}/{2} step".format(str(ceil(self.current_position)), str(current_step+1), str(tt_step)))

    def adjust_value(self):

        if self.current_position < 0:
            a = ceil(self.current_position) * -1
            if self.need_adjust(a):
                self.current_position = (a + 1) * -1

        else:
            a = ceil(self.current_position)
            if self.need_adjust(a):
                self.current_position = a + 1

    @staticmethod
    def float_sum(a: float, b: float):
        c = a + b
        return float("{0:.2f}".format(c))

    @staticmethod
    def need_adjust(value):
        if value % 45 > 0:
            return True
        else:
            return False
