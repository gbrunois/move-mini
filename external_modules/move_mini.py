from time import sleep

from neopixel_mini import NeoPixel
from microbit import *

# <Includes>
from external_modules.servo import *
# </Includes>


class MoveMini:
    """
    Move class for Move:mini robot https://kitronik.co.uk/products/5623-servolite-board-for-move-mini
    """

    _micro_sec_in_asecond = 1000000
    _distance_per_sec = 100
    _number_of_degrees_per_sec = 200

    def __init__(self):
        self.neopixel = NeoPixel(AdaFruit_NeoPixel.NeoPixel(pin0, 5))
        self.servo_0 = Servo(pin1)  # Right Servo Control
        self.servo_1 = Servo(pin2)  # Left Servo Control

    def drive_forward(self, distance: int):
        self.servo_0.write_angle(0)
        self.servo_1.write_angle(180)
        time_to_wait = distance * self._micro_sec_in_asecond / self._distance_per_sec
        self.wait_micro_secondes(time_to_wait)

        self.servo_0.stop()
        self.servo_1.stop()

    def turn_left(self, angle: int):
        self.servo_0.write_angle(45)
        self.servo_1.write_angle(45)
        time_to_wait = (
            angle * self._micro_sec_in_asecond / self._number_of_degrees_per_sec
        )
        self.wait_micro_secondes(time_to_wait)

        self.servo_0.stop()
        self.servo_1.stop()

    def turn_right(self, angle: int):
        self.servo_0.write_angle(135)
        self.servo_1.write_angle(135)
        time_to_wait = (
            angle * self._micro_sec_in_asecond / self._number_of_degrees_per_sec
        )
        self.wait_micro_secondes(time_to_wait)

        self.servo_0.stop()
        self.servo_1.stop()

    def wait_micro_secondes(self, time_to_wait: float):
        sleep(time_to_wait / 1000)
