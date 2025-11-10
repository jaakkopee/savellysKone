#!/usr/bin/env python3
"""
Test the Play MIDI button functionality with direct command execution.
This simulates what happens when you click the Play button.
"""

import os
import tempfile
import subprocess
import savellysKone3 as sk3

print("=" * 70)
print("TESTING PLAY MIDI FUNCTIONALITY")
print("=" * 70)
print()

# Step 1: Check SimpleSampler
print("1. Checking SimpleSampler executable...")
sampler_path = os.path.join(os.path.dirname(__file__), 
                           'simpleSampler', 'build', 'SimpleSampler')
print(f"   Looking for: {sampler_path}")

if not os.path.isfile(sampler_path):
    print(f"✗ SimpleSampler not found!")
    print("  Please build it:")
    print("    cd simpleSampler/build")
    print("    cmake ..")
    print("    make")
    exit(1)

print(f"✓ SimpleSampler found")
print()

# Step 2: Create a test song
print("2. Creating a test song...")
pitch_list = [60, 62, 64, 65, 67, 69, 71, 72]  # C major scale
duration_list = [0.5] * 8
velocity_list = [80, 90, 100, 110, 100, 90, 80, 70]

bar = sk3.Bar(onset=0, ioi=0.5, 
              pitch_list=pitch_list, 
              duration_list=duration_list, 
              velocity_list=velocity_list)
bar.make_note_list()

song = sk3.Song(num_bars=1, ioi=0.5)
song.bar_list = [bar]

print(f"✓ Song created with {len(song.bar_list)} bar(s)")
print(f"  First bar has {len(bar.note_list)} notes")
print()

# Step 3: Create temporary MIDI file
print("3. Creating temporary MIDI file...")
temp_fd, temp_path = tempfile.mkstemp(suffix='.mid', prefix='sk3_play_')
os.close(temp_fd)

song.make_midi_file(temp_path)
file_size = os.path.getsize(temp_path)
print(f"✓ MIDI file created: {temp_path}")
print(f"  File size: {file_size} bytes")
print()

# Step 4: Build and execute command
print("4. Building command to execute SimpleSampler...")
command = f"{sampler_path} {temp_path}"
print(f"   Command: {command}")
print()

print("5. Executing SimpleSampler...")
print("   (You should hear a C major scale playing)")
print()

try:
    # Execute in foreground to wait for completion
    result = subprocess.run(command, shell=True, 
                          capture_output=True, text=True, timeout=10)
    
    print(f"✓ SimpleSampler finished")
    print(f"  Return code: {result.returncode}")
    
    if result.stdout:
        print(f"  STDOUT: {result.stdout[:200]}")
    if result.stderr:
        print(f"  STDERR: {result.stderr[:200]}")
    
except subprocess.TimeoutExpired:
    print("⚠ SimpleSampler timed out (this might be OK if it's still playing)")
except Exception as e:
    print(f"✗ Error: {e}")

# Step 6: Cleanup
print()
print("6. Cleaning up...")
if os.path.exists(temp_path):
    os.unlink(temp_path)
    print(f"✓ Temporary file deleted")

print()
print("=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print()
print("This is exactly what happens when you click '▶️ Play MIDI' in the GUI:")
print("  1. Check if SimpleSampler exists")
print("  2. Create temp MIDI file from current song")
print("  3. Execute: ./simpleSampler/build/SimpleSampler /tmp/sk3_play_*.mid")
print("  4. SimpleSampler plays the MIDI file with sine waves")
print()
