"""
main.py
created by Aiden McCormack on 11-03-2022

This file handles the UI for the program and calls the functions that actually generate the output midifile
"""

from midiutil.MidiFile import MIDIFile
from random import randint
from music import *
from midi import *

add_progression(generate_progression(mode=MODENAME, length=8))
info()
write()
