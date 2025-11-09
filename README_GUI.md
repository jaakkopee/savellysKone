# SavellysKone3 GUI

A graphical user interface for `savellysKone3.py` built with Tkinter.

## Requirements

- Python 3.x
- tkinter (usually comes with Python)
- midiutil (`pip install midiutil`)

## Usage

Run the GUI with:

```bash
python3 savellysKone3_gui.py
```

## Features

### List Generator Tab

Generate musical lists (pitch, duration, or velocity) from grammar strings:

1. **Enter a grammar string** - Define your grammar rules in the text area
2. **Set minimum length** - Specify the minimum length for the generated list
3. **Select type** - Choose between pitch, duration, or velocity
4. **Click "Generate List"** - View the generated list in the output area

Example grammar:
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

### Bar Manipulation Tab

Create and manipulate musical bars:

1. **Create a Bar**
   - Enter comma-separated lists for pitches, durations, and velocities
   - Set onset time and IOI (Inter-Onset Interval)
   - Click "Create Bar"

2. **Operations**
   - **Transpose**: Shift all pitches by a number of semitones
   - **Set Duration**: Set all notes to a specific duration
   - **Reverse Notes**: Reverse the order of notes
   - **Random Pitches**: Apply random variations to pitches (±3 semitones)
   - **Random Durations**: Apply random variations to durations
   - **Random Velocities**: Apply random variations to velocities (±20)
   - **Random Onsets**: Apply random variations to onset times

3. **View Results**
   - The current bar's notes are displayed in a table format
   - Shows pitch, onset, duration, and velocity for each note

## Examples

### Generate a Pitch Sequence

1. Go to the "List Generator" tab
2. Enter your pitch grammar
3. Set minimum length to 8
4. Select "pitch" as type
5. Click "Generate List"

### Create and Modify a Musical Bar

1. Go to the "Bar Manipulation" tab
2. Enter pitch list: `60, 62, 64, 65, 67, 69, 71, 72`
3. Enter duration list: `1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0`
4. Enter velocity list: `100, 100, 100, 100, 100, 100, 100, 100`
5. Click "Create Bar"
6. Try operations like:
   - Transpose by 5 semitones
   - Apply random pitches
   - Reverse the note order

## Notes

- All operations provide visual feedback through message boxes
- Invalid inputs will display error messages
- The bar display updates automatically after each operation
