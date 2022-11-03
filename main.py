from midiutil.MidiFile import MIDIFile
from random import randint

# important variables for the whole program

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
    11: 'B'
}

mode_id = {
    0: "major",
    1: "minor"
}

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

scales = {
    0: (root, M2, M3, p4, p5, M6, M7, OCTAVE, "major"),
    1: (root, M2, m3, p4, p5, m6, d7, OCTAVE, "minor"),
    2: (root, M2, M3, p5, M6, OCTAVE, "major pentatonic"),
    3: (root, m3, p4, p5, d7, OCTAVE, "minor pentatonic")
}

chord_types_in_major = ("maj", "min", "min", "maj", "maj", "min", "dim"),
chords_types_in_minor = ("min", "dim", "maj", "min", "min", "maj", "maj"),
chords_types_in_major_pentatonic = ("maj", "min", "min", "maj", "min"),
chords_types_in_minor_pentatonic = ("min", "maj", "min", "min", "maj"),

chord_builder = (("maj", "min", "min", "maj", "maj", "min", "dim"),
("min", "dim", "maj", "min", "min", "maj", "maj"),
("maj", "min", "min", "maj", "min"),
("min", "maj", "min", "min", "maj"))

triads = {
    "maj": ("major", root, M3, p5),
    "min": ("minor", root, m3, p5),
    "aug": ("augmented", root, M3, m6),
    "dim": ("diminished", root, m3, tritone)
}

triads_enum = {
    0: ("major", root, M3, p5),
    1: ("minor", root, m3, p5),
    2: ("augmented", root, M3, m6),
    3: ("diminished", root, m3, tritone)
}

extensions = {
    "7": ('7', root, M3, p5, d7),
    "maj7": ('major 7', root, M3, p5, M7),
    "min7": ('minor 7', root, m3, p5, d7),
    "dim7": ('diminished 7', root, m3, tritone, M6)
}

extensions_enum = {
    0: ('7', root, M3, p5, d7),
    1: ('major 7', root, M3, p5, M7),
    2: ('minor 7', root, m3, p5, d7),
    3: ('diminished 7', root, m3, tritone, M6)
}


# Global track vars
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


progressions_hardcoded = [
     ((SECOND, extensions['min7']), (FIFTH, extensions['7']), (ROOT, extensions['maj7']), (ROOT, extensions['maj7']),
      "iim7_V7_Imaj7"),
     ((ROOT, triads['maj']), (SIXTH, triads['min']), (FOURTH, triads['maj']), (FIFTH, triads['maj']), "I_vi_IV_V"),
     ((ROOT, triads['maj']), (SIXTH, triads['min']), (SECOND, triads['min']), (FIFTH, triads['maj']), "I_iv_ii_V"),
     ((FOURTH, triads['maj']), (FIFTH, triads['maj']), (ROOT, triads['maj']), (SIXTH, triads['min']), "IV_V_I_vi"),
     ((ROOT, triads['maj']), (SECOND, triads['min']), (SIXTH, triads['min']), (FIFTH, triads['maj']), "I_ii_vi_V")
]

chords = []


def generate_all_chords(c=chords):
    print("Generating all chords")
    for i in range(len(intervals)):
        root_note = ROOT + i
        for j in range(len(triads)):
            triad = triads_enum[j]
            c.append((root_note, triad))
            chord = extensions_enum[j]
            c.append((root_note, chord))


def generate_triads_by_scale(c=chords, mode=MODENAME, pentatonic=False):
    selector = 0
    if pentatonic:
        selector = selector + 2
        print("Pentatonic scale selected")
    if mode == 'minor':
        selector = selector + 1
        print("Generating chords based on minor scale")
    elif mode == 'major':
        print("Generating chords based on major scale")
    blueprint = chord_builder[selector]
    scale = scales[selector]

    for i in range(len(blueprint)):
        chord_id = blueprint[i]
        root_note = ROOT + scale[i]
        triad = triads[chord_id]
        c.append((root_note, triad))


def generate_progression(length=4, mode='all', force_unique=True, force_root=True):
    if len(chords) == 0:
        if mode == 'all':
            generate_all_chords()
        else:
            generate_triads_by_scale(mode=mode)
    progression = []
    prev_index = 0
    for i in range(length):
        index = randint(0, (len(chords))-1)
        if (i == 0) and force_root:
            progression.append(chords[0])
        elif (prev_index == index) and force_unique:
            progression.append(chords[index-1])
        else:
            progression.append(chords[index])
        prev_index = index
    return progression


# midifile
midi = MIDIFile(7)
midi.addTrackName(0, 0, "Bass")
midi.addTrackName(1, 0, "Chords")
midi.addTrackName(2, 0, "Kick")
midi.addTrackName(3, 0, "Snare")
midi.addTrackName(4, 0, "Hi_hat")
midi.addTrackName(5, 0, "Arpeggio")
midi.addTrackName(6, 0, "Solo")
for i in range(7):
    midi.addTempo(i, 0, TEMPO)


# some functions
def info():
    print("Key = " + KEYNAME + " " + MODENAME)
    print("Tempo = " + str(TEMPO))


def write(filename="output.mid"):
    with open(filename, 'wb') as outf:
        midi.writeFile(outf)


def output_scale(scale, beat=0):
    for i in range(len(scale)):
        pitch = ROOT + scale[i]
        midi.addNote(1, 0, pitch, i+beat, 1, 100)
    print("output: " + str(scale))


def add_chord(root_note=ROOT, variety=triads['maj'], beat=0, length=4, track=1, octave=0, threshold=FIFTH):
    for i in range(1, len(variety)):
        pitch = root_note + variety[i] + octave
        if pitch > (threshold + (OCTAVE*octave)):
            pitch = pitch - OCTAVE
        midi.addNote(track, 0, pitch, beat, length, 100)


def add_progression(prog_type, beat=0, space=4, length=4, track=1, octave=0, threshold=FIFTH):
    for i in range(len(prog_type)):
        add_chord(prog_type[i][0], prog_type[i][1], beat, length, track, octave, threshold)
        beat = beat+space


add_progression(generate_progression(mode=MODENAME, length=8))
info()
write()
