#!/usr/bin/env python3
"""
Test script for the Savellys Kone GUI
Tests that the GUI can be instantiated and the modulate_duration_with_sin function
can be called through the GUI interface.
"""

import tkinter as tk
from savellysKone3 import SavellysKoneGUI, Song, ListGenerator


def test_gui_instantiation():
    """Test that the GUI can be created without errors"""
    print("Testing GUI instantiation...")
    root = tk.Tk()
    try:
        app = SavellysKoneGUI(root, test_mode=True)
        print("✓ GUI instantiated successfully")
        
        # Verify that the duration modulation fields exist
        assert app.dur_freq_var is not None, "Duration frequency variable not found"
        assert app.dur_amp_var is not None, "Duration amplitude variable not found"
        print("✓ Duration modulation fields exist")
        
        # Verify default values
        assert app.dur_freq_var.get() == "1.0", "Default frequency should be 1.0"
        assert app.dur_amp_var.get() == "0.05", "Default amplitude should be 0.05"
        print("✓ Default values are correct")
        
        root.destroy()
        print("✓ GUI destroyed successfully")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        root.destroy()
        return False


def test_duration_modulation_function():
    """Test that the modulate_duration_with_sin function works correctly"""
    print("\nTesting modulate_duration_with_sin function...")
    
    # Create a simple song
    pitch_grammar = "$S -> 60 60 60 60"
    duration_grammar = "$S -> 0.5 0.5 0.5 0.5"
    velocity_grammar = "$S -> 100 100 100 100"
    
    pitch_gen = ListGenerator(pitch_grammar, 4, "pitch")
    duration_gen = ListGenerator(duration_grammar, 4, "duration")
    velocity_gen = ListGenerator(velocity_grammar, 4, "velocity")
    
    song = Song(
        name="test_song",
        num_bars=2,
        ioi=0.5,
        pitch_generator=pitch_gen,
        duration_generator=duration_gen,
        velocity_generator=velocity_gen,
        generate_every_bar=True
    )
    
    song.generate_parameter_lists()
    song.make_bar_list()
    
    # Store original durations
    original_durations = []
    for bar in song.bar_list:
        for note in bar.note_list:
            original_durations.append(note.duration)
    
    print(f"  Original durations: {original_durations}")
    
    # Apply modulation
    freq = 1.0
    amp = 0.05
    song.modulate_duration_with_sin(freq, amp)
    
    # Check that durations have changed
    modulated_durations = []
    for bar in song.bar_list:
        for note in bar.note_list:
            modulated_durations.append(note.duration)
    
    print(f"  Modulated durations: {modulated_durations}")
    
    # Verify that at least some durations changed
    durations_changed = any(
        abs(orig - mod) > 0.001 
        for orig, mod in zip(original_durations, modulated_durations)
    )
    
    if durations_changed:
        print("✓ Duration modulation applied successfully")
        return True
    else:
        print("✗ Durations did not change")
        return False


def test_gui_modulation_methods_exist():
    """Test that the GUI has all required modulation methods"""
    print("\nTesting GUI modulation methods...")
    
    root = tk.Tk()
    try:
        app = SavellysKoneGUI(root, test_mode=True)
        
        # Check that all modulation methods exist
        assert hasattr(app, 'apply_duration_modulation'), "apply_duration_modulation method missing"
        assert hasattr(app, 'apply_pitch_modulation'), "apply_pitch_modulation method missing"
        assert hasattr(app, 'apply_velocity_modulation'), "apply_velocity_modulation method missing"
        assert hasattr(app, 'apply_onset_modulation'), "apply_onset_modulation method missing"
        print("✓ All modulation methods exist")
        
        # Check that duration modulation variables have correct default values
        assert app.dur_freq_var.get() == "1.0", "Duration frequency default incorrect"
        assert app.dur_amp_var.get() == "0.05", "Duration amplitude default incorrect"
        print("✓ Duration modulation parameters accessible")
        
        root.quit()
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        try:
            root.quit()
            root.destroy()
        except:
            pass
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Savellys Kone GUI Test Suite")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("GUI Instantiation", test_gui_instantiation()))
    results.append(("Duration Modulation Function", test_duration_modulation_function()))
    results.append(("GUI Modulation Methods", test_gui_modulation_methods_exist()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        exit(0)
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        exit(1)
