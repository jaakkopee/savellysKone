# savellysKone

A Python-based MIDI generation toolkit using grammars and modulation.

## Features

- **Grammar-based MIDI Generation**: Generate musical patterns using custom grammars
- **Modulation Support**: Apply sinusoidal modulation to pitch, duration, velocity, and onset
- **Piano Roll Visualization**: Real-time visual feedback with an interactive GUI

## New: Piano Roll Display GUI

The toolkit now includes a comprehensive Piano Roll Display for visualizing MIDI data. See [PIANO_ROLL_README.md](PIANO_ROLL_README.md) for details.

### Quick Start with GUI

```bash
# Install dependencies
pip install midiutil musical-scales pillow
sudo apt-get install python3-tk  # On Ubuntu/Debian

# Run the GUI
python3 demo_piano_roll.py
```

### Quick Start with Code

```python
import savellysKone3 as sk3

# Define grammars for pitch, duration, and velocity
pitch_grammar = """
$S -> 60 62 64 65 67 69 71 72
"""

# Create generators
pitch_gen = sk3.ListGenerator(pitch_grammar, 8, "pitch")

# Create and generate a song
song = sk3.Song(pitch_generator=pitch_gen, num_bars=4, ioi=1.0)
song.make_bar_list()

# Apply modulation
song.modulate_pitch_with_sin(1.0, 5.0)

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

### piano_roll_gui.py
GUI module containing:
- `PianoRollDisplay`: Visual piano roll widget
- `MIDIGeneratorGUI`: Complete application with modulation controls

## Files

- `savellysKone.py`, `savellysKone2.py`, `savellysKone3.py` - Core MIDI generation modules
- `gengramparser.py`, `gengramparser2.py` - Grammar parsing utilities
- `piano_roll_gui.py` - Piano roll visualization GUI
- `demo_piano_roll.py` - GUI demonstration script
- Test files: `sk3Test_*.py`, `test_*.py`

## Documentation

- [Piano Roll Display Guide](PIANO_ROLL_README.md) - Comprehensive GUI documentation with screenshots

## Requirements

- Python 3.x
- midiutil
- musical-scales
- tkinter (for GUI)
- PIL/Pillow (optional, for screenshots)

## License

See repository for license information.
