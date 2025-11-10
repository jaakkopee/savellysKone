# Simple MIDI Sampler

A C++ MIDI sampler that plays MIDI files using sine wave synthesis with ADSR envelopes.

## Features

- **MIDI File Parsing**: Reads standard MIDI files (.mid)
- **Sine Wave Synthesis**: Pure sine wave audio generation
- **ADSR Envelope**: Gentle amplitude envelope (Attack, Decay, Sustain, Release)
- **Polyphony**: Supports up to 32 simultaneous voices
- **Velocity Sensitivity**: Respects MIDI note velocities
- **Real-time Playback**: Uses SFML for low-latency audio output

## Requirements

- C++17 compatible compiler
- CMake 3.16 or higher
- SFML 3.0 or higher (Audio and System modules)

## Installation

### macOS (using Homebrew)

```bash
brew install sfml cmake
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get install libsfml-dev cmake build-essential
```

### Windows

Download SFML from [https://www.sfml-dev.org/download.php](https://www.sfml-dev.org/download.php) and follow the installation instructions.

## Building

```bash
cd simpleSampler
mkdir -p build
cd build
cmake ..
make
```

### Quick Check

Verify the build and integration setup:

```bash
python3 check_integration.py
```

This will check if SimpleSampler is built and ready for GUI integration.

## Usage

```bash
./SimpleSampler path/to/your/file.mid
```

Or run without arguments to be prompted for a file path:

```bash
./SimpleSampler
```

### Integration with savellysKone3_gui

SimpleSampler can be integrated into the Python GUI for real-time playback:

```python
from sampler_player import SimpleSamplerPlayer

# Initialize player
player = SimpleSamplerPlayer()

# Play a Song object directly
temp_path, process = player.play_from_song(song, background=True)

# Or play a MIDI file
player.play_midi_file("myfile.mid")
```

See [GUI_INTEGRATION.md](GUI_INTEGRATION.md) for complete integration instructions.

### Example Script

```bash
# Run the example integration demo
python3 example_integration.py
```

This creates a savellysKone3 composition and plays it through SimpleSampler.

## Project Structure

```
simpleSampler/
├── CMakeLists.txt       # CMake build configuration
├── include/             # Header files
│   ├── AudioEngine.h    # Audio playback engine
│   ├── Envelope.h       # ADSR envelope generator
│   ├── MidiParser.h     # MIDI file parser
│   └── SineWaveSynth.h  # Sine wave synthesizer
├── src/                 # Implementation files
│   ├── AudioEngine.cpp
│   ├── Envelope.cpp
│   ├── MidiParser.cpp
│   ├── SineWaveSynth.cpp
│   └── main.cpp         # Application entry point
└── build/               # Build directory (generated)
```

## How It Works

1. **MIDI Parsing**: The `MidiParser` class reads MIDI files and extracts note events (pitch, velocity, timing, duration).

2. **Synthesis**: The `SineWaveSynth` manages multiple `Voice` instances, each generating a sine wave at the appropriate frequency for a MIDI note.

3. **Envelope**: Each voice applies an ADSR envelope to create smooth attack and release phases:
   - **Attack**: 10ms - Quick rise to peak amplitude
   - **Decay**: 100ms - Gradual decrease to sustain level
   - **Sustain**: 70% - Held amplitude while note is active
   - **Release**: 200ms - Gentle fade out after note off

4. **Audio Output**: The `AudioEngine` streams generated audio samples to SFML's audio system in real-time.

## Customization

### Adjusting the Envelope

Edit the `Envelope` constructor in `src/Envelope.cpp`:

```cpp
Envelope::Envelope()
    : attackTime(0.01),      // Attack time in seconds
      decayTime(0.1),        // Decay time in seconds
      sustainLevel(0.7),     // Sustain level (0.0-1.0)
      releaseTime(0.2)       // Release time in seconds
{ }
```

### Changing Polyphony

Modify the maximum voices in `src/main.cpp` when creating the AudioEngine:

```cpp
AudioEngine engine(44100, 64);  // 64 voices instead of default 32
```

## Troubleshooting

**"Failed to load MIDI file"**
- Ensure the file path is correct
- Verify the file is a valid MIDI format (.mid)

**No audio output**
- Check system audio settings
- Ensure SFML audio module is properly installed
- Verify audio device is not being used by another application

**Distorted audio**
- Reduce the volume multiplier in `Voice::getSample()` (currently 0.3)
- Decrease the number of simultaneous voices

## License

This project is open source and available under the MIT License.

## Author

Created with SFML and C++17.
