# Savellys Kone GUI

## Overview
The Savellys Kone Music Generator now includes a comprehensive Tkinter GUI for easy music generation and modulation.

## Features

### Song Parameters
- **Song Name**: Name your generated composition
- **Number of Bars**: Define the length of your song (default: 4)
- **IOI (Inter-Onset Interval)**: Control the timing between notes (default: 0.5)

### Grammar Configuration
Define custom grammars for:
- **Pitch Grammar**: Control note pitches (MIDI values 0-127)
- **Duration Grammar**: Define note durations
- **Velocity Grammar**: Set note velocities (volume, 0-127)

### Modulation Functions

#### Duration Modulation with Sine Wave (Featured)
Apply sinusoidal modulation to note durations:
- **Frequency**: Controls the oscillation speed (default: 1.0)
- **Amplitude**: Controls the modulation intensity (default: 0.05)

#### Additional Modulation Options
- **Pitch Modulation**: Apply sine wave to pitch values
- **Velocity Modulation**: Modulate note velocities
- **Onset Modulation**: Modify note timing

### Workflow
1. Configure song parameters and grammars (or use defaults)
2. Click "Generate Song" to create the initial composition
3. Apply modulations as desired (can apply multiple)
4. Click "Save MIDI File" to export your creation

## Running the GUI

### Method 1: Direct Execution
```bash
python3 savellysKone3.py
```

### Method 2: Using Demo Script
```bash
python3 demo_gui.py
```

### Method 3: Programmatic Access
```python
from savellysKone3 import launch_gui
launch_gui()
```

## Testing

Run the test suite to verify functionality:
```bash
python3 test_gui.py
```

All tests should pass, confirming:
- GUI instantiation
- Duration modulation function
- GUI modulation methods

## Example Usage

1. **Generate a simple song:**
   - Keep default grammars or modify them
   - Set number of bars (e.g., 8)
   - Click "Generate Song"

2. **Apply duration modulation:**
   - Set Frequency: 2.0
   - Set Amplitude: 0.1
   - Click "Apply Duration Modulation"

3. **Save your work:**
   - Click "Save MIDI File"
   - Choose a location and filename

## Notes

- The GUI runs with a virtual display in testing mode
- Default grammars provide a good starting point
- Multiple modulations can be applied sequentially
- Status messages keep you informed of operations

## Requirements

- Python 3.x
- tkinter (python3-tk)
- MIDIUtil
- gengramparser2 (included in repository)
