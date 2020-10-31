"""
First program with Microbit.
Display Hello ! on the 5x5 led matrix

Execute this command :
python build.py samples/learn-microbit-1.py
"""

import microbit

while True:
    microbit.display.scroll('Hello !')