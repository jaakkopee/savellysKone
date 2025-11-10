# SavellysKone3 GUI

A comprehensive graphical user interface for `savellysKone3.py` built with Tkinter. Create, manipulate, and visualize MIDI compositions with grammar-based generation and real-time modulation.

## Requirements

- Python 3.x
- tkinter (usually comes with Python)
- midiutil (`pip install midiutil`)
- savellysKone3.py (core module)
- midi_parser.py (MIDI validation)

## Usage

Run the GUI with:

```bash
python3 savellysKone3_gui.py
```

## Overview

The GUI features four main tabs:

1. **List Generator** - Generate musical parameters using grammars
2. **Bar Manipulation** - Create and modify musical bars
3. **Song Modulation** - Apply sinusoidal modulation to songs
4. **Piano Roll** - Visualize MIDI data with zoom and scroll controls

## Features

### 1. List Generator Tab

Generate musical lists (pitch, duration, or velocity) from grammar strings using a three-grammar system:

#### Three Grammar Notebooks

- **Pitch Grammar** - Define pitch sequences
- **Duration Grammar** - Define note durations
- **Velocity Grammar** - Define note velocities

Each grammar tab includes:
- **Grammar text area** - Enter your grammar rules
- **Min length spinner** - Set minimum list length (default: 8)
- **Generate button** - Create the list
- **Output display** - View the generated list

**Auto-Update Feature**: Generated lists automatically populate the Bar Manipulation tab.

#### Default Grammars

**Pitch Grammar**:
```
$S -> $phrase01 $phrase02
$phrase01 -> $note01 $note02 $note03 $note04
$phrase02 -> $note05 $note06 $note07 $note08
$note01 -> 60
$note02 -> 62
$note03 -> 64
$note04 -> 65
$note05 -> 67
$note06 -> 69
$note07 -> 71
$note08 -> 72
```

**Duration Grammar**:
```
$S -> $D1 $D2 $D3 $D4 $D5 $D6 $D7 $D8
$D1 -> 1.0
$D2 -> 0.5
$D3 -> 1.0
$D4 -> 0.5
$D5 -> 1.0
$D6 -> 0.75
$D7 -> 0.5
$D8 -> 0.25
```

**Velocity Grammar**:
```
$S -> $V1 $V2 $V3 $V4 $V5 $V6 $V7 $V8
$V1 -> 60
$V2 -> 80
$V3 -> 100
$V4 -> 90
$V5 -> 70
$V6 -> 95
$V7 -> 85
$V8 -> 110
```

### 2. Bar Manipulation Tab

Create and manipulate musical bars with comprehensive controls:

#### Creating a Bar

- **Pitch list** - Comma-separated MIDI note numbers (e.g., `60, 62, 64, 65`)
- **Duration list** - Note durations in beats (e.g., `1.0, 0.5, 1.0, 0.5`)
- **Velocity list** - Note velocities 0-127 (e.g., `60, 80, 100, 90`)
- **Onset** - Bar start time in beats (default: 0.0)
- **IOI** - Inter-Onset Interval between notes (default: 1.0)

#### Bar Operations

- **Transpose** - Shift all pitches by semitones
- **Set Duration** - Set all notes to a specific duration
- **Reverse Notes** - Reverse the note order
- **Random Pitches** - Apply random variations (±3 semitones)
- **Random Durations** - Apply random duration variations
- **Random Velocities** - Apply random velocity variations (±20)
- **Random Onsets** - Apply random timing variations

#### Display

The note table shows:
- Pitch (MIDI note number)
- Onset (time position in beats)
- Duration (note length in beats)
- Velocity (0-127)

### 3. Song Modulation Tab

Apply sinusoidal modulation to entire songs with precise control:

#### Modulation Functions

**Continuous Modulation**:
- **Modulate Pitch** - Frequency & amplitude control
- **Modulate Duration** - Frequency & amplitude control
- **Modulate Velocity** - Frequency & amplitude control
- **Modulate Onset** - Frequency & amplitude control

**Phase-Reset Modulation** (resets at each bar):
- **Modulate Pitch (Phase by Bar)** - Frequency & amplitude control
- **Modulate Duration (Phase by Bar)** - Frequency & amplitude control
- **Modulate Velocity (Phase by Bar)** - Frequency & amplitude control
- **Modulate Onset (Phase by Bar)** - Frequency & amplitude control

#### Controls for Each Function

- **Frequency slider** - 0.1 to 5.0 Hz (sine wave frequency)
- **Amplitude slider** - 0.1 to 10.0 (modulation depth)
- **Apply button** - Execute the modulation
- **Reset button** - Clear modulation and restore original song

### 4. Piano Roll Tab

Real-time visualization of MIDI data with advanced navigation:

#### Visual Features

- **2D Grid Display** - Time (X-axis) vs. Pitch (Y-axis)
- **Color-Coded Velocities** - 9 distinct velocity ranges:
  - 0-15: Red
  - 16-31: Orange
  - 32-47: Yellow
  - 48-63: Green
  - 64-79: Cyan
  - 80-95: Blue
  - 96-111: Violet
  - 112-127: Indigo
- **White Note-On Markers** - Left edge indicates note start
- **Grid Lines** - Clear time and pitch divisions

#### Navigation Controls

**Zoom Controls**:
- **Horizontal Zoom** - Slider: 0.5x to 4.0x (time axis)
- **Vertical Zoom** - Slider: 0.5x to 4.0x (pitch axis)
- **Reset Zoom** - Return to 1.0x on both axes
- **Live Labels** - Display current zoom levels

**Scroll Controls**:
- **Horizontal Scrollbar** - Navigate through time
- **Vertical Scrollbar** - Navigate through pitch range
- Automatic activation when content exceeds visible area

#### Export and Validation

- **Export MIDI** - Save current composition to .mid file
- **Validate MIDI** - Check MIDI data integrity
- **Visual Indicators**:
  - Green circle = Valid MIDI data
  - Red circle = Invalid MIDI data
  - Orange circle = No MIDI data
- **Status Labels** - Text feedback on MIDI validity

## Menu Bar

### File Menu

- **Export MIDI** - Save composition to MIDI file
- **Validate MIDI** - Check MIDI data validity
- **Exit** - Close the application

### Help Menu

- **About** - Display application information

## Status Bar

Bottom status bar displays:
- Current Song object status
- Current Bar object status
- Real-time feedback on operations

## Workflow Examples

### Example 1: Generate and Visualize a Composition

1. Go to **List Generator** tab
2. Click **Generate** in each grammar tab (Pitch, Duration, Velocity)
3. Switch to **Bar Manipulation** tab (lists auto-populated)
4. Click **Create Bar**
5. Go to **Piano Roll** tab to visualize
6. Adjust zoom and scroll to inspect details

### Example 2: Apply Modulation and Export

1. Create a bar (see Example 1)
2. Go to **Song Modulation** tab
3. Adjust **Modulate Pitch** frequency to 1.0, amplitude to 5.0
4. Click **Apply** under Modulate Pitch
5. Go to **Piano Roll** tab to see the modulated result
6. Use **File > Export MIDI** to save

### Example 3: Explore with Random Variations

1. In **Bar Manipulation** tab, enter your base lists
2. Click **Create Bar**
3. Try **Random Pitches** to add melodic variation
4. Try **Random Velocities** to add dynamic variation
5. View results in **Piano Roll** tab
6. Use zoom to examine detailed changes

## Advanced Features

### Grammar System

The grammar parser supports:
- Non-terminal symbols (prefixed with `$`)
- Terminal symbols (numbers for pitch/velocity, decimals for duration)
- Recursive rules
- Multiple expansions per rule

### MIDI Validation

The integrated MIDI parser validates:
- Note pitch ranges (0-127)
- Velocity values (0-127)
- Duration values (> 0)
- Onset times (≥ 0)
- Overall MIDI file structure

Visual feedback via colored indicators in the Piano Roll tab.

### Velocity Color Mapping

The 9-range color system provides intuitive visual feedback:
- **Red to Orange** (0-31): Very soft dynamics
- **Yellow to Green** (32-63): Soft to medium dynamics
- **Cyan to Blue** (64-95): Medium to loud dynamics
- **Violet to Indigo** (96-127): Very loud dynamics

Colors interpolate smoothly within each range for precise representation.

## Keyboard Shortcuts

- **Cmd/Ctrl + Q** - Quit application (via menu)
- Tab navigation between input fields
- Enter key to activate focused buttons

## Tips

- **Use Auto-Update**: Generate grammars first, they populate Bar Manipulation automatically
- **Zoom Before Export**: Verify details with zoom before exporting MIDI
- **Reset Modulation**: Always available to restore original composition
- **Validate Often**: Check MIDI validity before export to catch errors early
- **Independent Zoom**: Use different H/V zoom levels for different perspectives
- **Phase-Reset Modulation**: Use "by bar" variants for rhythmic consistency across bars

## Troubleshooting

**GUI won't start**:
- Verify tkinter is installed: `python3 -c "import tkinter"`
- Check Python version: `python3 --version` (requires 3.x)

**MIDI export fails**:
- Click "Validate MIDI" to identify issues
- Check for invalid note values in Bar Manipulation tab
- Ensure a bar has been created before exporting

**Piano roll shows all one color**:
- Check velocity values have variation (not all the same)
- Default velocity list includes variation: `60, 80, 100, 90, 70, 95, 85, 110`

**Zoom/scroll not working**:
- Ensure content is generated (create a bar first)
- Reset zoom to 1.0x if display seems frozen
- Scrollbars activate only when content exceeds visible area

## Notes

- All operations provide visual feedback via status bar and message boxes
- Invalid inputs display descriptive error messages
- The piano roll updates automatically after operations
- MIDI files are exported in standard MIDI format compatible with all DAWs
- Grammar generation uses randomization - results vary each time
