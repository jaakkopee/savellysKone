"""
Test script for MIDI parser validation functionality.

This script creates test MIDI files with both valid and invalid note timing,
then validates them using the midi_parser module.
"""

import mido
import os
import sys
from midi_parser import MIDIParser, validate_midi_file


def create_valid_midi_file(filepath):
    """
    Create a valid MIDI file with correct note timing.
    Note-on events occur before their corresponding note-off events.
    """
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Add some valid notes
    # Note: time is delta time (time since last event)
    track.append(mido.Message('note_on', note=60, velocity=64, time=0))
    track.append(mido.Message('note_off', note=60, velocity=0, time=100))
    
    track.append(mido.Message('note_on', note=64, velocity=80, time=50))
    track.append(mido.Message('note_off', note=64, velocity=0, time=100))
    
    track.append(mido.Message('note_on', note=67, velocity=100, time=50))
    track.append(mido.Message('note_off', note=67, velocity=0, time=100))
    
    mid.save(filepath)
    print(f"Created valid MIDI file: {filepath}")


def create_invalid_midi_file_missing_noteoff(filepath):
    """
    Create an invalid MIDI file with missing note-off events.
    """
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Note that never gets turned off
    track.append(mido.Message('note_on', note=60, velocity=64, time=0))
    
    # Another note
    track.append(mido.Message('note_on', note=64, velocity=80, time=100))
    track.append(mido.Message('note_off', note=64, velocity=0, time=100))
    
    mid.save(filepath)
    print(f"Created invalid MIDI file (missing note_off): {filepath}")


def create_invalid_midi_file_missing_noteon(filepath):
    """
    Create an invalid MIDI file with note-off without corresponding note-on.
    """
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Note off without note on
    track.append(mido.Message('note_off', note=60, velocity=0, time=100))
    
    # Valid note
    track.append(mido.Message('note_on', note=64, velocity=80, time=100))
    track.append(mido.Message('note_off', note=64, velocity=0, time=100))
    
    mid.save(filepath)
    print(f"Created invalid MIDI file (missing note_on): {filepath}")


def create_invalid_midi_file_double_noteon(filepath):
    """
    Create an invalid MIDI file with double note-on without note-off in between.
    """
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Two note-on events without note-off
    track.append(mido.Message('note_on', note=60, velocity=64, time=0))
    track.append(mido.Message('note_on', note=60, velocity=80, time=100))
    track.append(mido.Message('note_off', note=60, velocity=0, time=100))
    
    mid.save(filepath)
    print(f"Created invalid MIDI file (double note_on): {filepath}")


def run_tests():
    """
    Run all test cases for MIDI parser validation.
    """
    print("=" * 70)
    print("MIDI Parser Validation Test Suite")
    print("=" * 70)
    
    # Create test directory
    test_dir = "/tmp/midi_parser_tests"
    os.makedirs(test_dir, exist_ok=True)
    
    # Test 1: Valid MIDI file
    print("\n" + "=" * 70)
    print("TEST 1: Valid MIDI file")
    print("=" * 70)
    valid_file = os.path.join(test_dir, "valid.mid")
    create_valid_midi_file(valid_file)
    result1 = validate_midi_file(valid_file, verbose=True)
    print(f"Result: {'PASS' if result1 else 'FAIL'}")
    
    # Test 2: Missing note-off
    print("\n" + "=" * 70)
    print("TEST 2: Invalid MIDI file - Missing note_off")
    print("=" * 70)
    invalid_file1 = os.path.join(test_dir, "missing_noteoff.mid")
    create_invalid_midi_file_missing_noteoff(invalid_file1)
    result2 = validate_midi_file(invalid_file1, verbose=True)
    print(f"Result: {'PASS' if not result2 else 'FAIL'} (Expected to find errors)")
    
    # Test 3: Missing note-on
    print("\n" + "=" * 70)
    print("TEST 3: Invalid MIDI file - Missing note_on")
    print("=" * 70)
    invalid_file2 = os.path.join(test_dir, "missing_noteon.mid")
    create_invalid_midi_file_missing_noteon(invalid_file2)
    result3 = validate_midi_file(invalid_file2, verbose=True)
    print(f"Result: {'PASS' if not result3 else 'FAIL'} (Expected to find errors)")
    
    # Test 4: Double note-on
    print("\n" + "=" * 70)
    print("TEST 4: Invalid MIDI file - Double note_on")
    print("=" * 70)
    invalid_file3 = os.path.join(test_dir, "double_noteon.mid")
    create_invalid_midi_file_double_noteon(invalid_file3)
    result4 = validate_midi_file(invalid_file3, verbose=True)
    print(f"Result: {'PASS' if not result4 else 'FAIL'} (Expected to find errors)")
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Test 1 (Valid file): {'PASS' if result1 else 'FAIL'}")
    print(f"Test 2 (Missing note_off): {'PASS' if not result2 else 'FAIL'}")
    print(f"Test 3 (Missing note_on): {'PASS' if not result3 else 'FAIL'}")
    print(f"Test 4 (Double note_on): {'PASS' if not result4 else 'FAIL'}")
    
    all_passed = result1 and not result2 and not result3 and not result4
    print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("=" * 70)
    
    return all_passed


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
