#!/usr/bin/env python3
"""
Test script to verify SimpleSampler availability checking works correctly.
This doesn't require tkinter.
"""

import sys
import os

# Add simpleSampler to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'simpleSampler'))

print("=" * 70)
print("TESTING SIMPLESAMPLER AVAILABILITY DETECTION")
print("=" * 70)
print()

# Test 1: Try to import sampler_player
print("Test 1: Importing sampler_player module")
try:
    from sampler_player import SimpleSamplerPlayer
    SAMPLER_AVAILABLE = True
    print("✓ sampler_player module imported successfully")
except ImportError as e:
    SAMPLER_AVAILABLE = False
    SimpleSamplerPlayer = None
    print(f"✗ sampler_player module import failed: {e}")

print()

# Test 2: Check if SimpleSampler executable exists
print("Test 2: Checking SimpleSampler executable")
if SAMPLER_AVAILABLE:
    try:
        player = SimpleSamplerPlayer()
        if player.is_available():
            print(f"✓ SimpleSampler executable found at: {player.sampler_path}")
            print(f"✓ Play MIDI buttons WILL appear in GUI")
        else:
            print(f"✗ SimpleSampler executable NOT found at: {player.sampler_path}")
            print(f"✗ Warning message WILL appear in GUI")
            print()
            print("To fix this, build SimpleSampler:")
            print("  cd simpleSampler/build")
            print("  cmake ..")
            print("  make")
    except Exception as e:
        print(f"✗ Error checking SimpleSampler: {e}")
        print(f"✗ Warning message WILL appear in GUI")
else:
    print("✗ Cannot check (module not imported)")
    print(f"✗ Warning message WILL appear in GUI")

print()
print("=" * 70)
print("WHAT THE GUI WILL SHOW:")
print("=" * 70)
print()

if SAMPLER_AVAILABLE and SimpleSamplerPlayer and SimpleSamplerPlayer().is_available():
    print("In the Piano Roll tab, you will see:")
    print("  • ▶️ Play MIDI button")
    print("  • ⏹️ Stop button")
else:
    print("In the Piano Roll tab, you will see:")
    print("  • ⚠️ SimpleSampler not available (orange warning)")
    print("  • ℹ️ Build Instructions button")
    print()
    print("Clicking 'Build Instructions' will show:")
    print("  - How to install dependencies (cmake, sfml)")
    print("  - Step-by-step build instructions")
    print("  - Path to README for more details")

print()
