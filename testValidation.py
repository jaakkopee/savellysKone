"""
Test script to demonstrate MIDI validation functionality.
This script creates songs with different modulation parameters and validates them.
"""

import savellysKone3 as sk3
import midi_parser

print("="*60)
print("MIDI Validation Test")
print("="*60)

# Define grammars
pitch_grammar = """
$S -> $phrase0 $phrase0
$phrase0 -> 60 62 64 65 67 69 71 72
"""

duration_grammar = """
$S -> $phrase0 $phrase0
$phrase0 -> 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25
"""

velocity_grammar = """
$S -> $phrase0 $phrase0
$phrase0 -> 100 100 100 100 100 100 100 100
"""

# Create generators
pitch_generator = sk3.ListGenerator(pitch_grammar, 8, "pitch")
duration_generator = sk3.ListGenerator(duration_grammar, 8, "duration")
velocity_generator = sk3.ListGenerator(velocity_grammar, 8, "velocity")

# Test 1: Song without modulation (should be valid)
print("\nTest 1: Song without modulation")
print("-" * 60)
song = sk3.Song(
    pitch_generator=pitch_generator,
    duration_generator=duration_generator,
    velocity_generator=velocity_generator,
    num_bars=4,
    ioi=0.5,
    name="Test - No Modulation"
)
song.generate_parameter_lists()
song.make_bar_list()

is_valid, message = midi_parser.validate_song_timing(song)
print(f"Status: {midi_parser.get_validation_status(song)}")
print(f"Details: {message}")

# Test 2: Song with moderate modulation (should be valid)
print("\nTest 2: Song with moderate modulation")
print("-" * 60)
song = sk3.Song(
    pitch_generator=pitch_generator,
    duration_generator=duration_generator,
    velocity_generator=velocity_generator,
    num_bars=4,
    ioi=0.5,
    name="Test - Moderate Modulation"
)
song.generate_parameter_lists()
song.make_bar_list()
song.modulate_onset_with_sin(1.0, 0.1)
song.modulate_duration_with_sin(1.0, 0.05)

is_valid, message = midi_parser.validate_song_timing(song)
print(f"Status: {midi_parser.get_validation_status(song)}")
print(f"Details: {message}")

# Test 3: Song with aggressive modulation (may be invalid)
print("\nTest 3: Song with aggressive modulation")
print("-" * 60)
song = sk3.Song(
    pitch_generator=pitch_generator,
    duration_generator=duration_generator,
    velocity_generator=velocity_generator,
    num_bars=4,
    ioi=0.5,
    name="Test - Aggressive Modulation"
)
song.generate_parameter_lists()
song.make_bar_list()
song.modulate_onset_with_sin(2.0, 0.2)
song.modulate_duration_with_sin(4.5, 0.5)

is_valid, message = midi_parser.validate_song_timing(song)
print(f"Status: {midi_parser.get_validation_status(song)}")
print(f"Details: {message}")

# Test 4: Song with very aggressive modulation (should be invalid)
print("\nTest 4: Song with very aggressive duration modulation")
print("-" * 60)
song = sk3.Song(
    pitch_generator=pitch_generator,
    duration_generator=duration_generator,
    velocity_generator=velocity_generator,
    num_bars=4,
    ioi=0.5,
    name="Test - Very Aggressive Modulation"
)
song.generate_parameter_lists()
song.make_bar_list()
song.modulate_duration_with_sin(5.0, 0.5)

is_valid, message = midi_parser.validate_song_timing(song)
print(f"Status: {midi_parser.get_validation_status(song)}")
print(f"Details: {message}")

print("\n" + "="*60)
print("All tests completed!")
print("="*60)
