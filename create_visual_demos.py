#!/usr/bin/env python3
"""
Visual demonstration script for PianoRollDisplay
Creates multiple screenshots showing different modulation effects
"""

import sys
import time
import tkinter as tk
from piano_roll_gui import MIDIGeneratorGUI

def capture_window(root, filename):
    """Capture the window to a file"""
    root.update()
    time.sleep(0.3)
    
    try:
        from PIL import Image, ImageGrab
        
        # Get window position and size
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        w = root.winfo_width()
        h = root.winfo_height()
        
        # Add some padding
        padding = 10
        x = max(0, x - padding)
        y = max(0, y - padding)
        w += padding * 2
        h += padding * 2
        
        # Capture the window
        img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
        img.save(filename)
        print(f"Screenshot saved to {filename}")
        return True
        
    except Exception as e:
        print(f"Could not save screenshot: {e}")
        return False

def main():
    """Create visual examples of the GUI with different modulations"""
    
    # Scenario 1: No modulation (baseline)
    print("\n=== Scenario 1: Baseline (No Modulation) ===")
    root = tk.Tk()
    app = MIDIGeneratorGUI(root)
    root.update()
    time.sleep(0.5)
    capture_window(root, "/home/runner/work/savellysKone/savellysKone/screenshot_baseline.png")
    root.destroy()
    
    # Scenario 2: Pitch modulation
    print("\n=== Scenario 2: Pitch Modulation ===")
    root = tk.Tk()
    app = MIDIGeneratorGUI(root)
    app.pitch_freq.set(2.0)
    app.pitch_amp.set(8.0)
    app.apply_modulation()
    root.update()
    time.sleep(0.5)
    capture_window(root, "/home/runner/work/savellysKone/savellysKone/screenshot_pitch_mod.png")
    root.destroy()
    
    # Scenario 3: Velocity modulation
    print("\n=== Scenario 3: Velocity Modulation ===")
    root = tk.Tk()
    app = MIDIGeneratorGUI(root)
    app.velocity_freq.set(1.5)
    app.velocity_amp.set(30.0)
    app.apply_modulation()
    root.update()
    time.sleep(0.5)
    capture_window(root, "/home/runner/work/savellysKone/savellysKone/screenshot_velocity_mod.png")
    root.destroy()
    
    # Scenario 4: Combined modulation
    print("\n=== Scenario 4: Combined Modulation ===")
    root = tk.Tk()
    app = MIDIGeneratorGUI(root)
    app.pitch_freq.set(2.5)
    app.pitch_amp.set(5.0)
    app.velocity_freq.set(1.0)
    app.velocity_amp.set(25.0)
    app.duration_freq.set(1.5)
    app.duration_amp.set(0.3)
    app.onset_freq.set(2.0)
    app.onset_amp.set(0.2)
    app.apply_modulation()
    root.update()
    time.sleep(0.5)
    capture_window(root, "/home/runner/work/savellysKone/savellysKone/screenshot_combined_mod.png")
    root.destroy()
    
    print("\n=== All screenshots created successfully ===")
    print("\nFiles created:")
    print("  - screenshot_baseline.png (no modulation)")
    print("  - screenshot_pitch_mod.png (pitch modulation)")
    print("  - screenshot_velocity_mod.png (velocity modulation)")
    print("  - screenshot_combined_mod.png (all modulations)")

if __name__ == "__main__":
    main()
