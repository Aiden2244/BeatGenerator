"""
main.py
created by Aiden McCormack on 10-31-2022
Copyright 2022, Aiden McCormack, All rights reserved.

This file handles the UI for the program and calls the functions that actually generate the output midifile
"""

from midi import *

add_progression(generate_progression(mode=MODENAME))
info()
write()
