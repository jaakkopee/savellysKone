# SavellysKone MIDI Validation GUI

This directory contains a MIDI generation system with real-time validation.

## Files

- **savellysKone3.py** - Core MIDI generation engine with grammar-based composition
- **savellysKone3_gui.py** - GUI application with real-time validation
- **midi_parser.py** - MIDI validation functions

## Running the GUI

To launch the GUI application:

```bash
python3 savellysKone3_gui.py
```

## Features

### GUI Controls

1. **Onset Modulation**
   - Frequency: Controls the frequency of sine wave modulation (0.1 - 5.0)
   - Amplitude: Controls the amplitude of onset time shifts (0.0 - 1.0)

2. **Duration Modulation**
   - Frequency: Controls the frequency of sine wave modulation (0.1 - 5.0)
   - Amplitude: Controls the amplitude of duration changes (0.0 - 0.5)

3. **Validation Status**
   - Real-time validation display
   - Green checkmark: All notes are valid
   - Red X: Some notes have invalid timing (duration ≤ 0)
   - Detailed error messages showing invalid note locations

### MIDI Validation

The validation system checks that all notes have valid timing:
- Each note must have duration > 0
- Notes with duration ≤ 0 are flagged as invalid
- This can occur when aggressive modulation parameters reduce note durations below zero

### Exporting MIDI

Click the "Export MIDI" button to save the current song to `gui_generated.mid`.

## Example Usage

```python
import savellysKone3 as sk3
import midi_parser

# Create a song
pitch_grammar = "$S -> 60 62 64 65"
duration_grammar = "$S -> 0.5 0.5 0.5 0.5"
velocity_grammar = "$S -> 100 100 100 100"

pitch_gen = sk3.ListGenerator(pitch_grammar, 4, "pitch")
duration_gen = sk3.ListGenerator(duration_grammar, 4, "duration")
velocity_gen = sk3.ListGenerator(velocity_grammar, 4, "velocity")

song = sk3.Song(pitch_generator=pitch_gen, duration_generator=duration_gen,
                velocity_generator=velocity_gen, num_bars=2, ioi=0.5)
song.generate_parameter_lists()
song.make_bar_list()

# Apply modulation
song.modulate_onset_with_sin(1.0, 0.1)
song.modulate_duration_with_sin(1.0, 0.05)

# Validate
is_valid, message = midi_parser.validate_song_timing(song)
print(f"Valid: {is_valid}")
print(f"Details: {message}")

# Export
song.make_midi_file("output.mid")
```

## Dependencies

- Python 3.x
- midiutil
- tkinter (for GUI)

Install dependencies:
```bash
pip install midiutil
```
