# SimpleSampler Usage Guide

## Overview
SimpleSampler is a MIDI file player with two synthesis modes:
1. **Sine Wave Mode** - Simple sine wave synthesis with ADSR envelope
2. **SoundFont Mode** - High-quality piano sound using the Motif ES6 Concert Piano SoundFont

## Command Line Usage

### Sine Wave Mode (Default)
```bash
./SimpleSampler path/to/file.mid
```

### SoundFont Mode (Piano Sound)
```bash
./SimpleSampler path/to/file.mid --soundfont
# or
./SimpleSampler path/to/file.mid -sf
```

## Python Wrapper Usage

### Basic Usage

```python
from sampler_player import SimpleSamplerPlayer

# Create player with sine waves
player = SimpleSamplerPlayer()
player.play_midi_file("song.mid", background=True)

# Create player with SoundFont
player = SimpleSamplerPlayer(use_soundfont=True)
player.play_midi_file("song.mid", background=True)

# Stop playback
player.stop()
```

### With savellysKone3

```python
import savellysKone3 as sk3
from sampler_player import play_song

# Create a song
pitch_grammar = "$S -> 60 62 64 65 67 69 71 72"
pitch_gen = sk3.ListGenerator(pitch_grammar, 8, "pitch")
song = sk3.Song(pitch_generator=pitch_gen, num_bars=4, ioi=0.5)
song.make_bar_list()

# Play with sine waves
temp_path, player = play_song(song, use_soundfont=False)

# Or play with piano sound
temp_path, player = play_song(song, use_soundfont=True)

# Clean up when done
import os
os.unlink(temp_path)
```

## Synthesis Modes

### Sine Wave Mode
- **Pros**: Lightweight, no dependencies beyond SFML
- **Cons**: Simple sound, less realistic
- **Best for**: Testing, debugging, minimal audio footprint
- **Settings**:
  - Polyphony: 32 voices
  - ADSR Envelope:
    - Attack: 10ms
    - Decay: 100ms
    - Sustain: 70%
    - Release: 200ms
  - Gain: 20% (to prevent clipping with multiple voices)

### SoundFont Mode
- **Pros**: High-quality piano sound, realistic
- **Cons**: Requires FluidSynth library and SF2 file (~12MB)
- **Best for**: Production, presentations, realistic playback
- **Settings**:
  - Polyphony: 32 voices
  - Sample Rate: 44100 Hz
  - SoundFont: Motif ES6 Concert Piano (included)

## SoundFont Location

The SoundFont file should be located at:
```
simpleSampler/build/soundfonts/Motif ES6 Concert Piano(12Mb).SF2
```

Or:
```
simpleSampler/soundfonts/Motif ES6 Concert Piano(12Mb).SF2
```

SimpleSampler will check both locations.

## Interactive Mode

If you run SimpleSampler without arguments, it will prompt you:

```bash
./SimpleSampler

# Prompts:
# Enter MIDI file path: [enter path]
# Use SoundFont? (y/n): [y or n]
```

## Requirements

### For Sine Wave Mode
- SFML 3.0+ (Audio and System modules)
- C++17 compiler

### For SoundFont Mode
- All of the above, plus:
- FluidSynth 2.5+
- SoundFont file (.SF2)

Install FluidSynth on macOS:
```bash
brew install fluidsynth
```

## Building

```bash
cd simpleSampler
mkdir -p build
cd build
cmake ..
make
```

## Integration with savellysKone3_gui

Add a toggle or dropdown in your GUI to let users choose synthesis mode:

```python
# In your GUI code
from sampler_player import SimpleSamplerPlayer

class YourGUI:
    def __init__(self):
        self.player = SimpleSamplerPlayer()
        self.use_soundfont = False  # Toggle this based on UI control
        
    def on_synth_mode_changed(self, use_soundfont):
        """Called when user changes synthesis mode"""
        self.use_soundfont = use_soundfont
        self.player = SimpleSamplerPlayer(use_soundfont=use_soundfont)
    
    def play_current_song(self):
        """Play the current song with selected synthesis mode"""
        temp_path, _ = self.player.play_from_song(self.current_song)
        # Store temp_path to clean up later
        self.temp_midi_file = temp_path
```

## Troubleshooting

### No Sound
1. Check system volume is not muted
2. Verify correct audio output device is selected
3. For SoundFont mode, ensure FluidSynth is installed: `brew list fluidsynth`

### SoundFont Not Found
1. Check that the SF2 file exists in `build/soundfonts/` or `soundfonts/`
2. Verify the filename matches exactly (including spaces)
3. SimpleSampler will fall back to sine wave mode if SoundFont loading fails

### FluidSynth Warning
If you see: `fluidsynth: warning: No preset found on channel 9`
- This is normal - channel 9 is typically for drums in MIDI
- Piano notes will still play correctly

## Performance

- Both modes support 32-voice polyphony
- Sample rate: 44100 Hz
- Buffer size: 4096 samples
- Latency: ~93ms (acceptable for offline rendering/playback)

## Audio Quality Comparison

**Sine Wave**: Pure mathematical sine waves with envelope shaping. Clear but synthetic sound.

**SoundFont**: Sampled piano with realistic attack, body, and release. Professional quality.

Choose based on your needs:
- Development/testing → Sine Wave
- Demos/presentations → SoundFont
- Production → SoundFont
