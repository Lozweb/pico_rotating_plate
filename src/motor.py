from machine import Pin
from menu import Menu
import utime


class MotorStep:

    def __init__(self, in1: int, in2: int, in3: int, in4: int, menu: Menu):
        # get lcd instance to write data on screen
        self.afficheur = menu

        # data
        self.step_index = 0
        self.current_position = 0
        self.deg_by_cycle = 0.703125

        # stepper config micro Pin: id, mode
        self.stepper_pins = [
            Pin(in1, Pin.OUT),
            Pin(in2, Pin.OUT),
            Pin(in3, Pin.OUT),
            Pin(in4, Pin.OUT)
        ]
        # stepper sequence mode execute
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
            # set all pins to mode out (off)
            self.stepper_pins[pin_index].value(0)

    def set_stepper_pins(self, direction: int):
        # get step sequence index to set stepper
        # step_index = (3 + 1) % 8 = 4
        self.step_index = (self.step_index + direction) % len(self.step_sequence)
        for pin_index in range(len(self.stepper_pins)):
            self.stepper_pins[pin_index].value(self.step_sequence[self.step_index][pin_index])

    def exec(self, direction: int, step_target: int, tt_user_step: int, delay: int):

        current_user_step = 0
        total_step_count = 0
        current_cycle_step = 0

        while current_user_step < tt_user_step:

            for i in range(step_target + 1):

                # set stepper for next step motor execute
                self.set_stepper_pins(direction)

                if current_cycle_step == 8:
                    self.set_current_position(direction)
                    current_cycle_step = 0
                    # in for loop but exec only 8th loop better performance
                    self.display_current_position(tt_user_step, current_user_step, total_step_count)

                # in for loop exec anytime and decrease performance
                # self.display_current_position(tt_user_step, current_user_step, total_step_count)
                current_cycle_step += 1
                total_step_count += 1
                utime.sleep(0.001)

            current_user_step += 1
            utime.sleep(delay)

        self.reset_stepper_pins()

    def degree_to_step(self, degree: int):
        print(self.current_position)

    def set_current_position(self, direction: int):
        self.current_position = self.current_position + (self.deg_by_cycle * direction)

    def display_current_position(self, tt_step: int, current_step: int, count: int):
        self.afficheur.set_text(
            "{0} d {3} \n{1}/{2} step".format(str(self.current_position), str(current_step), str(tt_step), str(count)))
