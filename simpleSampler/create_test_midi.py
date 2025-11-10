#!/usr/bin/env python3
"""
Create a simple test MIDI file for testing SimpleSampler audio output.
"""

from midiutil import MIDIFile

# Create MIDI file with 1 track
midi = MIDIFile(1)

track = 0
channel = 0
tempo = 120

midi.addTempo(track, 0, tempo)

# Add a simple C major scale
notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C, D, E, F, G, A, B, C
time = 0

for note in notes:
    midi.addNote(track, channel, note, time, duration=1, volume=100)
    time += 1

# Write to file
with open('test.mid', 'wb') as f:
    midi.writeFile(f)

print("Created test.mid with C major scale")
print("Test with: ./build/SimpleSampler test.mid")
