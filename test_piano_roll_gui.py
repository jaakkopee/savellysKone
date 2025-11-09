#!/usr/bin/env python3
"""
Test script for the PianoRollDisplay GUI
Takes a screenshot of the GUI for visual verification
"""

import sys
import time
import tkinter as tk
from piano_roll_gui import MIDIGeneratorGUI

def take_screenshot():
    """Run the GUI and take a screenshot"""
    root = tk.Tk()
    app = MIDIGeneratorGUI(root)
    
    # Give it time to render
    root.update()
    time.sleep(0.5)
    root.update()
    
    # Set some modulation parameters for demonstration
    app.pitch_amp.set(5.0)
    app.velocity_amp.set(20.0)
    app.duration_amp.set(0.2)
    app.apply_modulation()
    
    root.update()
    time.sleep(0.5)
    root.update()
    
    # Take screenshot using tkinter's postscript
    try:
        # Get the canvas widget
        canvas = app.piano_roll
        
        # Save as PostScript first
        ps = canvas.postscript(colormode='color')
        
        # Write to file
        with open('/tmp/piano_roll_screenshot.ps', 'w') as f:
            f.write(ps)
        
        print("Screenshot saved to /tmp/piano_roll_screenshot.ps")
        
        # Try to convert to PNG using PIL if available
        try:
            from PIL import Image
            import io
            
            # This is a workaround - we'll use a different approach
            # Let's use the screenshot from the window instead
            import PIL.ImageGrab as ImageGrab
            
            # Get window position
            x = root.winfo_rootx()
            y = root.winfo_rooty()
            w = root.winfo_width()
            h = root.winfo_height()
            
            # Capture the window
            img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
            img.save('/tmp/piano_roll_screenshot.png')
            print("PNG screenshot saved to /tmp/piano_roll_screenshot.png")
            
        except Exception as e:
            print(f"Could not save PNG: {e}")
            
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        import traceback
        traceback.print_exc()
    
    root.destroy()
    print("GUI test completed successfully")

if __name__ == "__main__":
    take_screenshot()
