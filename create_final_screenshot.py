#!/usr/bin/env python3
"""
Create a final showcase screenshot demonstrating all GUI features
"""

import time
import tkinter as tk
from piano_roll_gui import MIDIGeneratorGUI

def create_final_screenshot():
    """Create a comprehensive screenshot showing the full GUI"""
    
    root = tk.Tk()
    app = MIDIGeneratorGUI(root)
    
    # Set up interesting modulation parameters
    app.pitch_freq.set(1.5)
    app.pitch_amp.set(7.0)
    app.velocity_freq.set(2.0)
    app.velocity_amp.set(30.0)
    app.duration_freq.set(1.0)
    app.duration_amp.set(0.25)
    app.onset_freq.set(1.8)
    app.onset_amp.set(0.15)
    
    # Apply and update
    app.apply_modulation()
    root.update()
    time.sleep(0.5)
    root.update()
    
    # Take screenshot
    try:
        from PIL import ImageGrab
        
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        w = root.winfo_width()
        h = root.winfo_height()
        
        # Add padding
        padding = 5
        img = ImageGrab.grab(bbox=(x-padding, y-padding, x+w+padding, y+h+padding))
        img.save('/home/runner/work/savellysKone/savellysKone/screenshot_final.png')
        print("Final screenshot saved to screenshot_final.png")
        
    except Exception as e:
        print(f"Could not save screenshot: {e}")
    
    root.destroy()

if __name__ == "__main__":
    create_final_screenshot()
