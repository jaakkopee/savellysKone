#!/usr/bin/env python3
"""
Integration test: Use PianoRollDisplay with an existing test case
This demonstrates how the GUI integrates with existing savellysKone3 code
"""

import tkinter as tk
from piano_roll_gui import PianoRollDisplay
import savellysKone3 as sk3

def test_with_existing_pattern():
    """Test using the pattern from sk3Test_modulators.py"""
    
    # Setup from sk3Test_modulators.py
    pitch_grammar = """
    $S -> $phrase0 $phrase0 $phrase0 $phrase0
    $phrase0 -> 60 60 60 60 60 60 60 60
    """

    duration_grammar = """
    $S -> $phrase0 $phrase0 $phrase0 $phrase0
    $phrase0 -> 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3
    """

    velocity_grammar = """
    $S -> $phrase0 $phrase0 $phrase0 $phrase0
    $phrase0 -> 100 100 100 100 100 100 100 100
    """

    # Generators
    pitch_generator = sk3.ListGenerator(pitch_grammar, 8, "pitch")
    duration_generator = sk3.ListGenerator(duration_grammar, 8, "duration")
    velocity_generator = sk3.ListGenerator(velocity_grammar, 8, "velocity")

    # Create song
    song = sk3.Song(pitch_generator=pitch_generator,
                    duration_generator=duration_generator,
                    velocity_generator=velocity_generator,
                    num_bars=8,
                    ioi=0.5,
                    name="test modulators",
                    generate_every_bar=True)

    song.make_bar_list()

    # Apply modulations as in the original test
    song.modulate_duration_with_sin(1.0, 0.05)
    song.modulate_velocity_with_sin(1.0, 10.0)
    song.modulate_pitch_with_sin(1.0, 10.0)
    song.modulate_onset_with_sin(1.0, 0.075)
    
    # Create GUI to visualize
    root = tk.Tk()
    root.title("Integration Test: sk3Test_modulators Pattern")
    
    # Create piano roll
    piano_roll = PianoRollDisplay(root, width=900, height=500)
    piano_roll.pack(padx=10, pady=10)
    
    # Set the song
    piano_roll.set_song(song)
    
    # Update display
    root.update()
    
    # Save screenshot
    try:
        from PIL import ImageGrab
        import time
        
        time.sleep(0.5)
        root.update()
        
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        w = root.winfo_width()
        h = root.winfo_height()
        
        img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
        img.save('/home/runner/work/savellysKone/savellysKone/screenshot_integration_test.png')
        print("Integration test screenshot saved")
        
    except Exception as e:
        print(f"Could not save screenshot: {e}")
    
    root.destroy()
    
    # Also export MIDI as in original
    song.make_midi_file("/tmp/integration_test_modulators.mid")
    print("Integration test MIDI file saved to /tmp/integration_test_modulators.mid")
    print("Integration test passed successfully!")

if __name__ == "__main__":
    test_with_existing_pattern()
