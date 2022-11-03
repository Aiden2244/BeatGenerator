"""
music.py
created by Aiden McCormack on 11-03-2022
Copyright 2022, Aiden McCormack, All rights reserved.

This file contains some hardcoded musical information that is useful for the entire program
"""

from random import randint

# dict relating an index to its string representation
key_id = {
    0: 'C',
    1: 'C#',
    2: 'D',
    3: 'Eb',
    4: 'E',
    5: 'F',
    6: 'F#',
    7: 'G',
    8: 'Ab',
    9: 'A',
    10: 'Bb',
    11: 'B',
    12: 'C'
}

# relates an index to a string representation of the mode
mode_id = {
    0: "major",
    1: "minor"
}

# relates a descriptive string to a corresponding musical interval, in half steps from the root
intervals = {
    'root': 0,
    'm2': 1,
    'M2': 2,
    'm3': 3,
    'M3': 4,
    'p4': 5,
    'tritone': 6,
    'p5': 7,
    'm6': 8,
    'M6': 9,
    'd7': 10,
    'M7': 11,
    'OCTAVE': 12
}

# same as above but more convenient for the program to work with internally
root = int(0)
m2 = 1
M2 = 2
m3 = 3
M3 = 4
p4 = 5
tritone = 6
p5 = 7
m6 = 8
M6 = 9
d7 = 10
M7 = 11
OCTAVE = intervals['OCTAVE']

# global variables for the entire program
KEY = randint(0, 11)
TEMPO = randint(120, 180)
KEYNAME = key_id[KEY]
MODE = randint(0, 1)
MODENAME = mode_id[MODE]
PROGRESSION_LEN = 16

# Note identifiers
MIDDLE_C = 60
ROOT = MIDDLE_C + KEY
FIFTH = ROOT + p5
FOURTH = ROOT + p4
SECOND = ROOT + M2
if MODE == 0:
    THIRD = ROOT + M3
    SIXTH = ROOT + M6
    SEVENTH = ROOT + M7
else:
    THIRD = ROOT + m3
    SIXTH = ROOT + m6
    SEVENTH = ROOT + d7

# scale blueprints: construct a scale using these hardcoded values given only a root note
scales = {
    0: (root, M2, M3, p4, p5, M6, M7, OCTAVE, "major"),
    1: (root, M2, m3, p4, p5, m6, d7, OCTAVE, "minor"),
    2: (root, M2, M3, p5, M6, OCTAVE, "major pentatonic"),
    3: (root, m3, p4, p5, d7, OCTAVE, "minor pentatonic")
}

# A bunch of stuff relating to chords
# Based on 19th century Western European harmonic analysis, aka what most of the internet thinks is "music theory"

# access chord types by scale with a variable name
chord_types_in_major = ("maj", "min", "min", "maj", "maj", "min", "dim"),
chords_types_in_minor = ("min", "dim", "maj", "min", "min", "maj", "maj"),
chords_types_in_major_pentatonic = ("maj", "min", "min", "maj", "min"),
chords_types_in_minor_pentatonic = ("min", "maj", "min", "min", "maj"),

# access chord types by scale with a tuple index
chord_builder = (("maj", "min", "min", "maj", "maj", "min", "dim"),
("min", "dim", "maj", "min", "min", "maj", "maj"),
("maj", "min", "min", "maj", "min"),
("min", "maj", "min", "min", "maj"))

# how to build the triads based on a root note
triads = {
    "maj": ("major", root, M3, p5),
    "min": ("minor", root, m3, p5),
    "aug": ("augmented", root, M3, m6),
    "dim": ("diminished", root, m3, tritone)
}

# same as above but relates it to a number instead of a string
triads_enum = {
    0: ("major", root, M3, p5),
    1: ("minor", root, m3, p5),
    2: ("augmented", root, M3, m6),
    3: ("diminished", root, m3, tritone)
}

# spicier chords
extensions = {
    "7": ('7', root, M3, p5, d7),
    "maj7": ('major 7', root, M3, p5, M7),
    "min7": ('minor 7', root, m3, p5, d7),
    "dim7": ('diminished 7', root, m3, tritone, M6)
}

# same as above but relates it to a number instead of a string
extensions_enum = {
    0: ('7', root, M3, p5, d7),
    1: ('major 7', root, M3, p5, M7),
    2: ('minor 7', root, m3, p5, d7),
    3: ('diminished 7', root, m3, tritone, M6)
}

# some hardcoded progressions
# NOTE: A chord is represented by a tuple of length 2 with structure (<root note>, <formula to build chord from root>)
progressions_hardcoded = [
     ((SECOND, extensions['min7']), (FIFTH, extensions['7']), (ROOT, extensions['maj7']), (ROOT, extensions['maj7']),
      "iim7_V7_Imaj7"),
     ((ROOT, triads['maj']), (SIXTH, triads['min']), (FOURTH, triads['maj']), (FIFTH, triads['maj']), "I_vi_IV_V"),
     ((ROOT, triads['maj']), (SIXTH, triads['min']), (SECOND, triads['min']), (FIFTH, triads['maj']), "I_iv_ii_V"),
     ((FOURTH, triads['maj']), (FIFTH, triads['maj']), (ROOT, triads['maj']), (SIXTH, triads['min']), "IV_V_I_vi"),
     ((ROOT, triads['maj']), (SECOND, triads['min']), (SIXTH, triads['min']), (FIFTH, triads['maj']), "I_ii_vi_V")
]

# the list storing every generated chord the beat can use
chords = []

# the list storing the chords actually being used by the beat
progression = []
