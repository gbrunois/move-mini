"""
Simple robot rotation
"""
from microbit import *

# <Includes>
from external_modules.move_mini import *
# </Includes>

move_mini = MoveMini()

while True:
    move_mini.turn_left(90)
    sleep(2000)
    move_mini.drive_forward(100)
    sleep(2000)
    move_mini.turn_right(90)
    sleep(2000)
    move_mini.drive_forward(100)
