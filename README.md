# savellysKone

A Python-based MIDI generation toolkit using grammars and modulation with a comprehensive GUI.

## Features

- **Grammar-based MIDI Generation**: Generate musical patterns using custom grammars for pitch, duration, and velocity
- **Modulation Support**: Apply sinusoidal modulation to pitch, duration, velocity, and onset (continuous or phase-reset)
- **Piano Roll Visualization**: Real-time visual feedback with zoom, scroll, and color-coded velocities
- **MIDI Validation**: Built-in validation with visual indicators
- **Interactive GUI**: Complete Tkinter-based interface with four main tabs

## Quick Start with GUI

```bash
# Install dependencies
pip install midiutil

# Run the main GUI
python3 savellysKone3_gui.py
```

## GUI Overview

The `savellysKone3_gui.py` application provides four main tabs:

1. **List Generator** - Three-grammar system (pitch, duration, velocity) with auto-update to Bar Manipulation
2. **Bar Manipulation** - Create and modify bars with transpose, reverse, and randomization operations
3. **Song Modulation** - Eight modulation functions with frequency/amplitude controls
4. **Piano Roll** - Visual display with 9-range velocity colors, zoom (0.5x-4.0x), and scroll controls

See [README_GUI.md](README_GUI.md) for comprehensive GUI documentation.

## Quick Start with Code

```python
import savellysKone3 as sk3

# Define grammars for pitch, duration, and velocity
pitch_grammar = """
$S -> 60 62 64 65 67 69 71 72
"""

duration_grammar = """
$S -> 1.0 0.5 1.0 0.5 1.0 0.75 0.5 0.25
"""

velocity_grammar = """
$S -> 60 80 100 90 70 95 85 110
"""

# Create generators
pitch_gen = sk3.ListGenerator(pitch_grammar, 8, "pitch")
duration_gen = sk3.ListGenerator(duration_grammar, 8, "duration")
velocity_gen = sk3.ListGenerator(velocity_grammar, 8, "velocity")

# Create and generate a song
song = sk3.Song(
    pitch_generator=pitch_gen,
    duration_generator=duration_gen,
    velocity_generator=velocity_gen,
    num_bars=4,
    ioi=1.0
)
song.make_bar_list()

# Apply modulation
song.modulate_pitch_with_sin(freq=1.0, amp=5.0)
song.modulate_velocity_with_sin(freq=2.0, amp=20.0)

# Export to MIDI
song.make_midi_file("output.mid")
```

## Core Components

### savellysKone3.py
Main module containing:
- `Note`: Represents a MIDI note (pitch, onset, duration, velocity)
- `Bar`: Collection of notes in a musical bar
- `Song`: Complete musical composition with multiple bars
- `ListGenerator`: Grammar-based parameter generation

### savellysKone3_gui.py
Complete GUI application with:
- `PianoRollDisplay`: Visual piano roll widget with zoom/scroll
- `SavellysKoneGUI`: Main application with four-tab interface
- MIDI validation integration via `midi_parser.py`
- Real-time modulation controls

### midi_parser.py
MIDI validation module with:
- `MIDIParser`: Parse and validate MIDI files
- `ValidationError`: Custom exception for validation errors
- Comprehensive error checking for note ranges and timing

## Key Features

### Three-Grammar System
- Separate grammars for pitch, duration, and velocity
- Auto-population of Bar Manipulation tab
- Default grammars with musical variation

### Song Modulation
Eight modulation functions:
- Continuous modulation: pitch, duration, velocity, onset
- Phase-reset modulation: pitch by bar, duration by bar, velocity by bar, onset by bar
- Frequency range: 0.1-5.0 Hz
- Amplitude range: 0.1-10.0

### Piano Roll Visualization
- Color-coded velocities (9 ranges: red→orange→yellow→green→cyan→blue→violet→indigo)
- Independent H/V zoom (0.5x to 4.0x)
- Horizontal and vertical scrollbars
- MIDI validation indicators (green/red/orange circles)
- Real-time updates

## Files

### Core Modules
- `savellysKone.py`, `savellysKone2.py`, `savellysKone3.py` - Evolution of MIDI generation modules
- `gengramparser.py`, `gengramparser2.py` - Grammar parsing utilities
- `midi_parser.py` - MIDI validation and parsing

### GUI Applications
- `savellysKone3_gui.py` - **Main comprehensive GUI** (recommended)
- `piano_roll_gui.py` - Standalone piano roll demonstration
- `demo_piano_roll.py` - GUI demonstration script

### Test Files
- `test_integration.py` - Integration tests
- `test_midi_parser.py` - MIDI parser tests
- `test_piano_roll_gui.py` - Piano roll GUI tests
- `sk3Test_*.py` - Various feature tests
- `verify_implementation.py` - Implementation verification

### Example Files
- `example_midi_parser_usage.py` - MIDI parser examples
- `sk01.py` - Basic examples
- `sk_new_test.py` - Testing examples
- `sk3_techno_track2.py` - Techno composition example
- Various `sk*` test files

### Utilities
- `create_final_screenshot.py` - Screenshot generation
- `create_visual_demos.py` - Visual demonstration creation

## Documentation

- [README_GUI.md](README_GUI.md) - **Comprehensive GUI documentation** with detailed feature descriptions
- [PIANO_ROLL_README.md](PIANO_ROLL_README.md) - Piano roll display guide
- [MIDI_PARSER_README.md](MIDI_PARSER_README.md) - MIDI parser documentation
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Implementation details

## Requirements

- Python 3.x
- midiutil (`pip install midiutil`)
- tkinter (for GUI, usually included with Python)

Optional:
- musical-scales (for scale utilities)
- PIL/Pillow (for screenshots)

## Installation

```bash
# Clone the repository
git clone https://github.com/jaakkopee/savellysKone.git
cd savellysKone

# Install dependencies
pip install midiutil

# Run the GUI
python3 savellysKone3_gui.py
```

## Usage Examples

### GUI Workflow
1. Launch `python3 savellysKone3_gui.py`
2. Generate lists in List Generator tab (pitch, duration, velocity)
3. Create bar in Bar Manipulation tab (auto-populated from grammars)
4. Apply modulation in Song Modulation tab
5. Visualize in Piano Roll tab with zoom/scroll
6. Export via File > Export MIDI

### Programmatic Workflow
```python
import savellysKone3 as sk3

# Quick start
song = sk3.Song(num_bars=4, ioi=1.0)
song.make_bar_list()
song.modulate_pitch_with_sin(1.0, 5.0)
song.make_midi_file("output.mid")
```

## License

See repository for license information.

## Author

Jaakko Prättälä (jaakkopee)
