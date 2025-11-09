#!/usr/bin/env python3
"""
Demo script to showcase the Savellys Kone GUI
This script demonstrates the duration modulation functionality
"""

from savellysKone3 import launch_gui

if __name__ == "__main__":
    print("=" * 60)
    print("Savellys Kone - Music Generator GUI")
    print("=" * 60)
    print("\nFeatures:")
    print("- Configure song parameters (name, bars, IOI)")
    print("- Define grammars for pitch, duration, and velocity")
    print("- Generate songs with the 'Generate Song' button")
    print("- Apply modulations:")
    print("  * Duration Modulation with Sine Wave (FEATURED)")
    print("  * Pitch Modulation with Sine Wave")
    print("  * Velocity Modulation with Sine Wave")
    print("  * Onset Modulation with Sine Wave")
    print("- Save generated music as MIDI files")
    print("\nLaunching GUI...")
    print("=" * 60)
    
    launch_gui()
