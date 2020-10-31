"""
neopixel_random.py

Repeatedly displays random colours onto the LED strip.
"""

from random import randint

# <Includes>
from external_modules.move_mini import *
# </Includes>

move_mini = MoveMini()

while True:
    # Iterate over each LED in the strip

    for pixel_id in range(5):
        red = randint(0, 60)
        green = randint(0, 60)
        blue = randint(0, 60)

        # Assign the current LED a random red, green and blue value between 0 and 60
        move_mini.neopixel.set_pixel_color(pixel_id, (red, green, blue))

    # Display the current pixel data on the Neopixel strip
    move_mini.neopixel.show()
    sleep(0.1)
