#!/usr/bin/env python3
"""
Test the Play MIDI button integration with SimpleSampler.
This script tests the sampler_player module independently.
"""

import sys
import os

# Add simpleSampler to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'simpleSampler'))

from sampler_player import SimpleSamplerPlayer
import savellysKone3 as sk3

print("=" * 70)
print("TESTING SIMPLESAMPLER INTEGRATION")
print("=" * 70)
print()

# Test 1: Check if SimpleSampler is available
print("Test 1: Checking SimpleSampler availability")
player = SimpleSamplerPlayer()
if player.is_available():
    print(f"✓ SimpleSampler found at: {player.sampler_path}")
else:
    print(f"✗ SimpleSampler NOT found at: {player.sampler_path}")
    print("Please build SimpleSampler first:")
    print("  cd simpleSampler/build")
    print("  cmake ..")
    print("  make")
    sys.exit(1)

print()

# Test 2: Create a test song
print("Test 2: Creating a test song")
pitch_grammar = """$S -> 60 62 64 65 67 69 71 72"""
duration_grammar = """$S -> 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5"""
velocity_grammar = """$S -> 80 90 100 90 80 90 100 110"""

pitch_gen = sk3.ListGenerator(pitch_grammar, 8, "pitch")
duration_gen = sk3.ListGenerator(duration_grammar, 8, "duration")
velocity_gen = sk3.ListGenerator(velocity_grammar, 8, "velocity")

song = sk3.Song(
    pitch_generator=pitch_gen,
    duration_generator=duration_gen,
    velocity_generator=velocity_gen,
    num_bars=2,
    ioi=0.5
)
song.make_bar_list()
print("✓ Test song created with 2 bars")
print()

# Test 3: Play the song
print("Test 3: Playing the song with SimpleSampler")
print("(This will play audio - you should hear a simple ascending scale)")
print()
try:
    temp_path, process = player.play_from_song(song, background=False)
    print(f"✓ Song played successfully")
    print(f"  Temp MIDI file was: {temp_path}")
    
    # Clean up
    if os.path.exists(temp_path):
        os.unlink(temp_path)
        print(f"✓ Cleaned up temp file")
    
except Exception as e:
    print(f"✗ Error playing song: {e}")
    sys.exit(1)

print()
print("=" * 70)
print("ALL TESTS PASSED!")
print("=" * 70)
print()
print("The Play MIDI button in the GUI should work correctly.")
print("To test in the GUI:")
print("  1. Run: python3 savellysKone3_gui.py")
print("  2. Create a song (use List Generator or Bar Manipulation)")
print("  3. Go to Piano Roll tab")
print("  4. Click '▶️ Play MIDI' button")
print()
