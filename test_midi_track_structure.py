#!/usr/bin/env python3
"""
Test MIDI file generation to verify track structure.
"""

import savellysKone3 as sk3
import os

print("=" * 70)
print("TESTING MIDI FILE TRACK STRUCTURE")
print("=" * 70)
print()

# Create a simple song
print("1. Creating a test song...")
pitch_list = [60, 62, 64, 65]
duration_list = [1.0, 1.0, 1.0, 1.0]
velocity_list = [100, 100, 100, 100]

bar = sk3.Bar(onset=0, ioi=1.0,
              pitch_list=pitch_list,
              duration_list=duration_list,
              velocity_list=velocity_list)
bar.make_note_list()

song = sk3.Song(name="Test Track Structure", num_bars=1, ioi=1.0)
song.bar_list = [bar]

print(f"✓ Song created: '{song.name}'")
print(f"  Bars: {len(song.bar_list)}")
print(f"  Notes in first bar: {len(bar.note_list)}")
print()

# Generate MIDI file
print("2. Generating MIDI file...")
test_file = "test_track_structure.mid"
song.make_midi_file(test_file)

if os.path.exists(test_file):
    file_size = os.path.getsize(test_file)
    print(f"✓ MIDI file created: {test_file}")
    print(f"  File size: {file_size} bytes")
else:
    print(f"✗ MIDI file was not created!")
    exit(1)

print()

# Try to parse it with our MIDI parser
print("3. Checking MIDI file structure with midi_parser...")
try:
    import midi_parser
    parser = midi_parser.MIDIParser(test_file)
    parser.parse()
    
    print(f"✓ MIDI file parsed successfully")
    print(f"  Format: {parser.format_type}")
    print(f"  Number of tracks: {parser.num_tracks}")
    print(f"  Ticks per beat: {parser.ticks_per_beat}")
    print(f"  Total note events: {len(parser.note_events)}")
    
    # Check validation
    is_valid, errors = parser.validate()
    if is_valid:
        print(f"✓ MIDI file is valid")
    else:
        print(f"✗ MIDI file has {len(errors)} validation error(s)")
        for error in errors[:3]:
            print(f"  - {error.message}")
    
except ImportError:
    print("  (midi_parser not available, skipping validation)")
except Exception as e:
    print(f"✗ Error parsing MIDI file: {e}")

print()

# Display track info using midiutil inspection
print("4. Inspecting MIDI file structure...")
try:
    from midiutil import MIDIFile
    
    # Read the file back
    with open(test_file, 'rb') as f:
        # We can't easily read it back with midiutil, so let's use hex dump
        f.seek(0)
        header = f.read(14)  # MIDI header is 14 bytes
        
        # Parse header
        if header[:4] == b'MThd':
            print("✓ Valid MIDI header found")
            format_type = int.from_bytes(header[8:10], 'big')
            num_tracks = int.from_bytes(header[10:12], 'big')
            division = int.from_bytes(header[12:14], 'big')
            
            print(f"  Format type: {format_type}")
            print(f"  Number of tracks in header: {num_tracks}")
            print(f"  Division (ticks per quarter note): {division}")
            
            if num_tracks == 1:
                print("✓ MIDI file has exactly 1 track (track 0 with notes)")
            else:
                print(f"⚠ MIDI file has {num_tracks} tracks")
        else:
            print("✗ Invalid MIDI header")
            
except Exception as e:
    print(f"  Error inspecting file: {e}")

print()

# Cleanup
print("5. Cleaning up...")
if os.path.exists(test_file):
    os.unlink(test_file)
    print(f"✓ Test file deleted")

print()
print("=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print()
print("Expected result: 1 track (track 0) containing all the notes")
print()
