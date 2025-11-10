#!/usr/bin/env python3
"""
Test SimpleSampler directly with a simple MIDI file.
This will help diagnose if the issue is with SimpleSampler or the integration.
"""

import sys
import os
import tempfile

# Add path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'simpleSampler'))

from sampler_player import SimpleSamplerPlayer
import savellysKone3 as sk3

print("=" * 70)
print("TESTING SIMPLESAMPLER PLAYBACK")
print("=" * 70)
print()

# Create player
player = SimpleSamplerPlayer()

# Check availability
print("1. Checking SimpleSampler availability...")
if not player.is_available():
    print(f"✗ SimpleSampler not found at: {player.sampler_path}")
    print("Please build it first:")
    print("  cd simpleSampler/build")
    print("  cmake ..")
    print("  make")
    sys.exit(1)
print(f"✓ SimpleSampler found at: {player.sampler_path}")
print()

# Create a simple test song
print("2. Creating a test song...")
pitch_list = [60, 62, 64, 65, 67, 69, 71, 72]  # C major scale
duration_list = [0.5] * 8
velocity_list = [80, 90, 100, 110, 100, 90, 80, 70]

# Create a bar
bar = sk3.Bar(onset=0, ioi=0.5, 
              pitch_list=pitch_list, 
              duration_list=duration_list, 
              velocity_list=velocity_list)
bar.make_note_list()

# Create a song
song = sk3.Song(num_bars=1, ioi=0.5)
song.bar_list = [bar]

print(f"✓ Song created with {len(song.bar_list)} bar(s)")
print(f"  Bar has {len(bar.note_list)} notes")
print()

# Export to temp MIDI file
print("3. Exporting to temporary MIDI file...")
temp_fd, temp_path = tempfile.mkstemp(suffix='.mid', prefix='test_')
os.close(temp_fd)

song.make_midi_file(temp_path)
print(f"✓ MIDI file created: {temp_path}")
print(f"  File size: {os.path.getsize(temp_path)} bytes")
print()

# Play with SimpleSampler
print("4. Playing with SimpleSampler...")
print("   (You should hear a C major scale)")
print()

try:
    # Play in foreground so we wait for it to finish
    return_code = player.play_midi_file(temp_path, background=False)
    
    if return_code == 0:
        print("✓ Playback completed successfully")
    else:
        print(f"✗ SimpleSampler returned error code: {return_code}")
    
except Exception as e:
    print(f"✗ Error during playback: {e}")
    import traceback
    traceback.print_exc()

# Clean up
print()
print("5. Cleaning up...")
if os.path.exists(temp_path):
    os.unlink(temp_path)
    print("✓ Temporary file deleted")

print()
print("=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print()
print("If you heard the C major scale, SimpleSampler is working correctly.")
print("If you didn't hear anything, check:")
print("  - System volume is up")
print("  - Audio output device is working")
print("  - SimpleSampler was built correctly")
print()
