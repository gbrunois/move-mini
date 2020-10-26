"""
neopixel_random.py
Repeatedly displays random colours onto the LED strip.
"""

from random import randint
from microbit import *

# <Includes>
from external_modules.move_mini import *
# </Includes>

move_mini = MoveMini()

while True:
    # Iterate over each LED in the strip

    for pixel_id in range(0, len(move_mini.neopixel)):
        red = randint(0, 60)
        green = randint(0, 60)
        blue = randint(0, 60)

        # Assign the current LED a random red, green and blue value between 0 and 60
        move_mini.neopixel[pixel_id] = (red, green, blue)

        # Display the current pixel data on the Neopixel strip
        move_mini.neopixel.show()
        sleep(100)
