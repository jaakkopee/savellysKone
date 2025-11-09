#!/usr/bin/env python3
"""
Piano Roll GUI Demo
This demonstrates the PianoRollDisplay class integrated with the MIDI generator.

The GUI features:
1. Real-time piano roll visualization of MIDI notes
2. Interactive controls for modulation parameters (pitch, duration, velocity, onset)
3. Automatic refresh when parameters change
4. Visual representation of note states with color-coded velocities
5. Clear grid lines and axis labels
"""

from piano_roll_gui import main

if __name__ == "__main__":
    print("Starting Piano Roll GUI Demo...")
    print("\nFeatures:")
    print("- Piano roll display showing MIDI notes over time")
    print("- X-axis: Time (beats)")
    print("- Y-axis: MIDI note numbers")
    print("- Color-coded notes: Blue (low velocity) to Yellow (high velocity)")
    print("- White edge indicates note-on events")
    print("\nControls:")
    print("- Pitch Modulation: Modulate note pitches with a sine wave")
    print("- Duration Modulation: Modulate note durations")
    print("- Velocity Modulation: Modulate note velocities (affects color)")
    print("- Onset Modulation: Modulate note timing")
    print("- Reset Modulation: Clear all modulations")
    print("- Regenerate Song: Create a new random pattern")
    print("- Export MIDI: Save current pattern to MIDI file")
    print("\nAdjust the frequency and amplitude sliders to see changes in real-time!")
    print("\n" + "="*60 + "\n")
    
    main()
