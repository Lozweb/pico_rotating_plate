from machine import Pin
from menu import Menu
import utime


class MotorStep:

    def __init__(self, in1: int, in2: int, in3: int, in4: int, menu: Menu):

        self.afficheur = menu
        self.step_index = 0
        self.current_position = 0
        self.deg_by_cycle = 0.703125

        self.stepper_pins = [
            Pin(in1, Pin.OUT),
            Pin(in2, Pin.OUT),
            Pin(in3, Pin.OUT),
            Pin(in4, Pin.OUT)
        ]
        self.step_sequence = [
            [1, 0, 0, 1],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1]
        ]

    def reset_stepper_pins(self):
        for pin_index in range(len(self.stepper_pins)):
            self.stepper_pins[pin_index].value(0)

    def set_stepper_pins(self, direction: int):
        self.step_index = (self.step_index + direction) % len(self.step_sequence)
        for pin_index in range(len(self.stepper_pins)):
            self.stepper_pins[pin_index].value(self.step_sequence[self.step_index][pin_index])

    def exec(self, direction: int, degree_target: int, tt_user_step: int, delay: int):

        current_user_step = 0
        total_step_count = 0
        current_cycle_step = 0
        step_target = self.degree_to_step(degree_target) // tt_user_step

        while current_user_step < tt_user_step:

            for i in range(step_target + 1):
                self.set_stepper_pins(direction)
                if current_cycle_step == 8:
                    self.set_current_position(direction)
                    current_cycle_step = 0
                    self.display_current_position(tt_user_step, current_user_step)

                current_cycle_step += 1
                total_step_count += 1
                utime.sleep(0.001)

            current_user_step += 1
            utime.sleep(delay)

        self.reset_stepper_pins()

    @staticmethod
    def degree_to_step(degree: int):
        return int(degree * 11.377777778)

    def set_current_position(self, direction: int):
        self.current_position = self.current_position + (self.deg_by_cycle * direction)

    def display_current_position(self, tt_step: int, current_step: int):
        self.afficheur.set_text(
            "{0} d\n{1}/{2} step".format(str(int(self.current_position)), str(current_step+1), str(tt_step)))
