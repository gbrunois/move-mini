from microbit import *

class Servo:
    # Servo class for Continuous servo FS90R 

    def __init__(self, pin):
        self.pin = pin
        self.pin.set_analog_period(20)

    def stop(self):
        self.set_angle(90)

    def set_angle(self, degrees: float):
        # 90 : no movement
        # 0 full speed anticlockwise
        # 180 full speed clockwise
        duty = 26 + (degrees * 102) / 180
        self.pin.write_analog(duty)

class MoveMini:
    # Move class for Move:mini robot

    _micro_sec_in_asecond = 1000000
    _distance_per_sec = 100
    _number_of_degrees_per_sec = 300

    def __init__(self):
        self.servo_0 = Servo(pin1) # Right Servo Control
        self.servo_1 = Servo(pin2) # Left Servo Control

    def drive_forward(self, distance: int):
        self.servo_0.set_angle(0)
        self.servo_1.set_angle(180)
        time_to_wait = distance * self._micro_sec_in_asecond / self._distance_per_sec
        self.wait_micro_secondes(time_to_wait)

        self.servo_0.stop()
        self.servo_1.stop()

    def turn_left(self, angle: int):
        self.servo_0.set_angle(45)
        self.servo_1.set_angle(45)
        time_to_wait = angle * self._micro_sec_in_asecond / self._number_of_degrees_per_sec
        self.wait_micro_secondes(time_to_wait)

        self.servo_0.stop()
        self.servo_1.stop()

    def turn_right(self, angle: int):
        self.servo_0.set_angle(135)
        self.servo_1.set_angle(135)
        time_to_wait = angle * self._micro_sec_in_asecond / self._number_of_degrees_per_sec
        self.wait_micro_secondes(time_to_wait)

        self.servo_0.stop()
        self.servo_1.stop()

    def wait_micro_secondes(self, time_to_wait: int):
        sleep(time_to_wait / 1000)

