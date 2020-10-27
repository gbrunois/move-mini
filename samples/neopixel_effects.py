"""
neopixel_effects.py
Repeatedly displays random colours onto the LED strip.
"""
# <Includes>
from external_modules.move_mini import *
# </Includes>


move_mini = MoveMini()

neopixel_effects = NeoPixelEffects(move_mini.neopixel)

while True:
    neopixel_effects.rainbow_cycle(0.001) # rainbow cycle with 1ms delay per step
    sleep(0.2)
