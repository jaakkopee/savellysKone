# Piano Roll Display for savellysKone

This document describes the Piano Roll Display feature integrated into the savellysKone3_gui.py application.

## Overview

The `PianoRollDisplay` class provides a comprehensive visual representation of MIDI data with advanced navigation and validation features. It is integrated as the fourth tab in the main `savellysKone3_gui.py` application.

## Features

### 1. Visual Representation

**2D Grid Visualization**:
- **X-axis**: Time (beats)
- **Y-axis**: MIDI note numbers (48-84 by default, C3 to C6)
- Clear grid lines with highlighted C notes
- Axis labels for easy reading

**Note Visualization**:
- Notes displayed as colored rectangles
- **9-Range Velocity Color Mapping**:
  - 0-15: Red
  - 16-31: Orange (interpolated)
  - 32-47: Yellow (interpolated)
  - 48-63: Green (interpolated)
  - 64-79: Cyan (interpolated)
  - 80-95: Blue (interpolated)
  - 96-111: Violet (interpolated)
  - 112-127: Indigo
- White edge on left side indicates note-on events
- Duration clearly visible as rectangle width

### 2. Navigation Controls

**Zoom Features**:
- **Horizontal Zoom Slider**: 0.5x to 4.0x (time axis scaling)
- **Vertical Zoom Slider**: 0.5x to 4.0x (pitch axis scaling)
- **Independent Zoom Levels**: H and V zoom operate independently
- **Live Zoom Labels**: Display current zoom factor (e.g., "1.5x")
- **Reset Zoom Button**: Return to 1.0x on both axes instantly

**Scroll Features**:
- **Horizontal Scrollbar**: Navigate through time when zoomed
- **Vertical Scrollbar**: Navigate through pitch range when zoomed
- Automatic activation when content exceeds visible area
- Smooth scrolling with mouse wheel support (via Canvas)

### 3. MIDI Validation

**Visual Indicators**:
- **Colored Circle**: 
  - Green = Valid MIDI data
  - Red = Invalid MIDI data
  - Orange = No MIDI data available
- **Status Label**: Text description of validation state
- Real-time validation updates after each operation

**Validation Button**:
- "Validate MIDI" button for manual validation check
- Integrates with `midi_parser.py` for comprehensive checking
- Displays error messages with specific issue details

### 4. MIDI Export

**Export Functionality**:
- "Export MIDI" button in Piano Roll tab
- Also available in File menu (File > Export MIDI)
- Saves current composition with all modulations applied
- Standard MIDI format (.mid) compatible with all DAWs

**Export Features**:
- File dialog for save location selection
- Automatic .mid extension
- Success/error feedback via message boxes
- Validates before export (optional)

### 5. Real-time Updates

- Automatically refreshes when MIDI data changes
- Reflects modulation parameter changes instantly
- Updates after bar manipulation operations
- Responds to grammar generation

## Usage

### Running the Application

```bash
python3 savellysKone3_gui.py
```

The Piano Roll is the fourth tab in the main application.

### Using PianoRollDisplay in Your Code

```python
import tkinter as tk
from savellysKone3_gui import PianoRollDisplay
import savellysKone3 as sk3

# Create a window
root = tk.Tk()

# Create the piano roll display
piano_roll = PianoRollDisplay(root, width=800, height=400)
piano_roll.pack()

# Create and set a song
song = sk3.Song(num_bars=4, ioi=1.0)
song.make_bar_list()
piano_roll.set_song(song)

root.mainloop()
```

### Navigation Workflow

1. **View Overview**: Start at 1.0x zoom to see entire composition
2. **Zoom In**: Increase zoom (2.0x-4.0x) to examine note details
3. **Scroll**: Use scrollbars to navigate zoomed view
4. **Zoom Out**: Decrease zoom (0.5x) for compressed overview
5. **Reset**: Click "Reset Zoom" to return to default view

### Validation Workflow

1. Create or modify MIDI data in Bar Manipulation tab
2. Switch to Piano Roll tab
3. Check the validation indicator (circle + label)
4. If red, click "Validate MIDI" for detailed error information
5. Return to Bar Manipulation to fix issues
6. Re-check validation in Piano Roll

## Controls Reference

### Piano Roll Tab Controls

**Zoom Controls** (in Zoom Controls frame):
- **H Zoom Slider**: Horizontal zoom 0.5x - 4.0x
- **V Zoom Slider**: Vertical zoom 0.5x - 4.0x
- **H Zoom Label**: Shows current horizontal zoom (e.g., "H Zoom: 1.0x")
- **V Zoom Label**: Shows current vertical zoom (e.g., "V Zoom: 1.0x")
- **Reset Zoom Button**: Resets both zoom levels to 1.0x

**Scrollbars**:
- **Horizontal Scrollbar**: Below the piano roll canvas
- **Vertical Scrollbar**: Right side of the piano roll canvas

**Action Buttons**:
- **Export MIDI**: Save composition to .mid file
- **Validate MIDI**: Check MIDI data validity

**Validation Indicators**:
- **Status Circle**: Colored circle (green/red/orange)
- **Status Label**: Text description ("Valid MIDI", "Invalid MIDI", etc.)

## Implementation Details

### PianoRollDisplay Class

Located in `savellysKone3_gui.py` (lines ~30-250).

**Key Methods**:
- `__init__(parent, width, height, **kwargs)`: Initialize the canvas
- `set_song(song)`: Set the Song object to display
- `draw_notes()`: Render all notes with velocity colors
- `draw_grid()`: Draw time and pitch grid
- `velocity_to_color(velocity)`: Convert velocity to RGB color
- `update_display()`: Refresh the entire display and configure scroll region

**Velocity Color Algorithm**:
```python
def velocity_to_color(self, velocity):
    # Define 9 velocity ranges with distinct colors
    ranges = [
        (0, 15, (255, 0, 0)),      # Red
        (16, 31, (255, 128, 0)),   # Orange
        (32, 47, (255, 255, 0)),   # Yellow
        (48, 63, (0, 255, 0)),     # Green
        (64, 79, (0, 255, 255)),   # Cyan
        (80, 95, (0, 0, 255)),     # Blue
        (96, 111, (128, 0, 255)),  # Violet
        (112, 127, (75, 0, 130))   # Indigo
    ]
    
    # Find range and interpolate
    for min_vel, max_vel, color in ranges:
        if min_vel <= velocity <= max_vel:
            # Interpolation logic...
            return color_hex
```

**Zoom Implementation**:
- Base dimensions: 800x400 pixels
- Scaled dimensions: `base * zoom_factor`
- Canvas reconfigured with `config(width=new_width, height=new_height)`
- Scroll region updated: `configure(scrollregion=bbox("all"))`

**Scroll Region**:
- Automatically calculated from canvas bounding box
- Updated in `update_display()` method
- Synchronized with zoom changes

### Integration with Main GUI

The PianoRollDisplay is integrated into `SavellysKoneGUI` class:

```python
class SavellysKoneGUI:
    def __init__(self, root):
        # ... other initialization ...
        self.create_piano_roll_tab()
        
    def create_piano_roll_tab(self):
        # Create PianoRollDisplay
        self.piano_roll = PianoRollDisplay(canvas_container, width=800, height=400)
        
        # Create zoom controls
        h_zoom_var = tk.DoubleVar(value=1.0)
        v_zoom_var = tk.DoubleVar(value=1.0)
        
        # Create scrollbars
        h_scrollbar = ttk.Scrollbar(canvas_container, orient="horizontal", 
                                    command=self.piano_roll.xview)
        v_scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", 
                                    command=self.piano_roll.yview)
        
        # Configure piano roll with scrollbars
        self.piano_roll.configure(xscrollcommand=h_scrollbar.set,
                                 yscrollcommand=v_scrollbar.set)
```

## Advanced Features

### Color Interpolation

Within each velocity range, colors interpolate smoothly:
- Provides 9 distinct visual regions
- Smooth gradients within each region
- Easy to distinguish velocity differences at a glance

### Automatic Updates

The piano roll updates automatically when:
- New bar is created in Bar Manipulation tab
- Grammar lists are generated in List Generator tab
- Modulation is applied in Song Modulation tab
- Any operation modifies the Song object

### Performance Optimization

- Efficient canvas drawing with batched operations
- Grid drawn once, notes redrawn on updates
- Scroll region calculated only when needed
- Zoom operations reconfigure canvas without full redraw

## Troubleshooting

**Piano roll shows all notes the same color**:
- Check that velocity values vary in your bar
- Default velocity list has variation: `60, 80, 100, 90, 70, 95, 85, 110`
- Use Bar Manipulation > Random Velocities to add variation

**Scrollbars don't appear**:
- Scrollbars only appear when zoomed beyond visible area
- Try increasing zoom to 2.0x or higher
- Ensure a bar with notes has been created

**Zoom seems stuck**:
- Click "Reset Zoom" to return to 1.0x
- Check that both sliders are responsive
- Verify a song object exists (create a bar first)

**Validation always shows orange**:
- Orange indicates no MIDI data
- Create a bar in Bar Manipulation tab first
- Check that the Song object has bars

**Export MIDI fails**:
- Validate MIDI first to identify issues
- Ensure bar contains valid note data
- Check file permissions in save directory

## Related Files

- `savellysKone3_gui.py` - Main application containing PianoRollDisplay
- `midi_parser.py` - MIDI validation module
- `savellysKone3.py` - Core Song/Bar/Note classes
- `README_GUI.md` - Complete GUI documentation

## See Also

- [README_GUI.md](README_GUI.md) - Full GUI user guide
- [README.md](README.md) - Project overview
- [MIDI_PARSER_README.md](MIDI_PARSER_README.md) - MIDI parser documentation

The `PianoRollDisplay` class extends `tkinter.Canvas` and provides:

- **Grid Drawing**: Draws a grid with time and note axes
- **Note Rendering**: Converts MIDI note data to visual rectangles
- **Color Mapping**: Maps velocity values to color gradients
- **Coordinate Conversion**: Transforms MIDI data to screen coordinates
- **Auto-refresh**: Updates display when song data changes

### Integration with savellysKone3

The GUI integrates seamlessly with the existing `savellysKone3` module:

- Uses `Song`, `Bar`, and `Note` classes
- Supports all modulation methods:
  - `modulate_pitch_with_sin()`
  - `modulate_duration_with_sin()`
  - `modulate_velocity_with_sin()`
  - `modulate_onset_with_sin()`

## Requirements

- Python 3.x
- tkinter (python3-tk)
- midiutil
- musical-scales
- PIL (Pillow) - optional, for screenshots

Install dependencies:
```bash
pip install midiutil musical-scales pillow
sudo apt-get install python3-tk  # On Ubuntu/Debian
```

## Design Decisions

1. **Color Scheme**: Dark background (#1a1a1a) with colored notes for better visibility
2. **Velocity Mapping**: Blue to yellow gradient provides intuitive visual feedback
3. **Note-on Indication**: White edge on left side clearly marks note start
4. **Grid Lines**: C notes highlighted for musical context
5. **Real-time Updates**: Immediate feedback when modulation parameters change

## Future Enhancements

Potential improvements:
- Multiple track support
- Zoom controls for time/pitch axes
- Note editing capabilities
- Playback integration
- MIDI file import
- Customizable color schemes
