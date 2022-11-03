"""
midi.py
created by Aiden McCormack on 11-03-2022
Copyright 2022, Aiden McCormack, All rights reserved.

This file initializes the midi file that gets written to output, and defines some procedures
for generating chords & scales as well as some housekeeping procedures to make this thing work.
"""

from random import randint
from music import *
from midiutil.MidiFile import MIDIFile

# initialize the midifile object with 7 tracks
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


# print some info about the track, since it is randomly generated
def info():
    print()
    print("====== BEAT INFO ======")
    print("Key = " + KEYNAME + " " + MODENAME)
    print("Tempo = " + str(TEMPO))
    prog_to_string()
    print()


# makes the syntax for writing the file out a little nicer, useful if I ever
# want to write more than one midifile for some reason
def write(filename="output.mid"):
    with open(filename, 'wb') as outf:
        midi.writeFile(outf)
    print("Wrote midi to file " + filename)


# code that outputs a scale. It was the first thing I wrote, and I might remove it since it's buggy.
def output_scale(scale, beat=0):
    for i in range(len(scale)):
        pitch = ROOT + scale[i]
        midi.addNote(1, 0, pitch, i+beat, 1, 100)
    print("output: " + str(scale))


# converts the tuple representation of a chord into a string representation
def chord_to_string(chord):
    note = chord[0]
    while note > MIDDLE_C+OCTAVE:
        note = note - OCTAVE
    note = note - MIDDLE_C
    note_id = key_id[note]
    variety = chord[1][0]
    output = note_id + " " + variety
    print(output + ", ", end="")


# uses the above method to output the beat's chord progression
def prog_to_string(p=progression):
    print("Chord progression: ", end="")
    for i in range(len(progression)):
        chord_to_string(progression[i])


# adds a chords to the file
# parameters:
    # root_note is the root note of the chord, represented by an integer number of musical half-steps
    # variety is the type of chord, set to major by default
    # beat is the beat number where the chord should be added, beginning by default
    # length is the number of beats that each note of the chord is, set to 4 (whole note) by default
    # track is the track # that the chord gets written to, I designate 1 as the chords track and this shouldn't change
    # octave is an optional modifier that shifts the chord up or down by an octave
    # threshold is a value to make the chords have better voicing, any note above it gets lowered down an octave
def add_chord(root_note=ROOT, variety=triads['maj'], beat=0, length=4, track=1, octave=0, threshold=FIFTH):
    for i in range(1, len(variety)):
        pitch = root_note + variety[i] + (OCTAVE*octave)
        if pitch > (threshold + (OCTAVE*octave)):
            pitch = pitch - OCTAVE
        midi.addNote(track, 0, pitch, beat, length, 100)


# writes a progression of chords with repeated calls of the add_chord function
# parameters:
    # prog_type is the progression to be built, which is a tuple of chord representations (see the note in music.py)
    # beat dittos above
    # space is how far apart each chord is written from the previous chord, 4 (1 measure) by default
    # length dittos above
    # track dittos above
    # octave dittos above
    # threshold dittos above
def add_progression(prog_type, beat=0, space=4, length=4, track=1, octave=0, threshold=FIFTH):
    for i in range(len(prog_type)):
        add_chord(prog_type[i][0], prog_type[i][1], beat, length, track, octave, threshold)
        beat = beat+space


# generate all possible chords based on the chromatic scale and every chord type defined in 'triads' & 'extensions'
def generate_all_chords(c=chords):
    print("Generating all chords")
    for i in range(len(intervals)):
        root_note = ROOT + i
        for j in range(len(triads)):
            triad = triads_enum[j]
            c.append((root_note, triad))
            chord = extensions_enum[j]
            c.append((root_note, chord))


# generates all possible triads within a given scale
# parameters
    # mode is the mode (major/minor) of the scale to generate.
        # ie if mode is major then the piece will generate the chords "I ii iii IV V vi viiº" based on ROOT
    # pentatonic is a boolean that enables/disables the generation to be solely on the pentatonic scale
    # c is the list storing every generated chord the beat CAN USE, should not change
def generate_triads_by_scale(mode=MODENAME, pentatonic=False, c=chords):
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


# writes a chord progression to the chords track
# parameters
    # length is the number of chords to add to the progression
    # mode is the mode (major/minor) for the progression to generate to
    # force_unique is a bool that makes the progressions a little more interesting
        # by disallowing two of the same chord consecutively
    # force_root is a bool that makes the first chord in the progression equal to the root chord
        # instead of randomly selecting it
    # p is the list storing every generated chord the beat ACTUALLY USES, should not change
        # p is a subset of c
def generate_progression(length=4, mode='all', force_unique=True, force_root=True, p=progression):
    if len(chords) == 0:
        if mode == 'all':
            generate_all_chords()
        else:
            generate_triads_by_scale(mode=mode)
    prev_index = 0
    print("Generating progression of " + str(length) + " chords")
    for i in range(length):
        index = randint(0, (len(chords))-1)
        if (i == 0) and force_root:
            progression.append(chords[0])
        elif (prev_index == index) and force_unique:
            p.append(chords[index-1])
        else:
            p.append(chords[index])
        prev_index = index
    return p
