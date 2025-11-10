# Play MIDI Button Integration

## Overview

The GUI now includes a **Play MIDI** button in the Piano Roll tab that allows you to play your compositions directly through SimpleSampler without saving the file manually.

## Features

### Play MIDI Button (▶️ Play MIDI)
- Located in the Piano Roll tab
- Plays the current song using SimpleSampler with sine wave synthesis
- Creates a temporary MIDI file automatically
- Plays in the background so you can continue working

### Stop Button (⏹️ Stop)
- Stops the currently playing audio
- Cleans up temporary files
- Located next to the Play button

## Requirements

### SimpleSampler Must Be Built

The SimpleSampler C++ application must be compiled before the Play button will work:

```bash
cd simpleSampler/build
cmake ..
make
```

The executable should be located at: `simpleSampler/build/SimpleSampler`

### Python Dependencies

- `subprocess` (built-in)
- `tempfile` (built-in)
- `savellysKone3.py` (already required)

## Usage

### In the GUI

1. **Create a song** using one of these methods:
   - Use the List Generator to create grammars
   - Use Bar Manipulation to create a bar
   - The song will be created automatically when you create a bar

2. **Go to the Piano Roll tab**

3. **Click "▶️ Play MIDI"**
   - The song will play through SimpleSampler
   - You'll hear sine wave synthesis with amplitude envelopes
   - A message box will confirm playback has started

4. **Click "⏹️ Stop"** to stop playback at any time

### Button Visibility

The Play and Stop buttons only appear if:
- SimpleSampler is built and available
- The executable is found at `simpleSampler/build/SimpleSampler`

If you don't see the buttons, build SimpleSampler first.

## How It Works

### Behind the Scenes

1. When you click "Play MIDI":
   - A temporary MIDI file is created in the system temp directory
   - SimpleSampler is launched with this file as an argument
   - SimpleSampler reads the MIDI and synthesizes audio using sine waves
   - The audio plays through your system's audio output

2. The process runs in the background:
   - You can continue editing while the song plays
   - Multiple clicks will stop the previous playback and start new playback
   - Temporary files are cleaned up when you click Stop

3. When you click "Stop":
   - The SimpleSampler process is terminated
   - Temporary MIDI files are deleted
   - Status bar is updated

### Technical Implementation

The integration uses the `sampler_player.py` module from the `simpleSampler` directory:

```python
# Import (with error handling)
from sampler_player import SimpleSamplerPlayer

# Create player
player = SimpleSamplerPlayer()

# Play a song
temp_path, process = player.play_from_song(song, background=True)

# Stop playback
player.stop()
```

## Error Messages

### "SimpleSampler Not Available"
- **Cause**: SimpleSampler is not built or not found
- **Solution**: Build SimpleSampler in `simpleSampler/build`

### "SimpleSampler Not Found"
- **Cause**: The executable doesn't exist at the expected path
- **Solution**: 
  ```bash
  cd simpleSampler/build
  cmake ..
  make
  ```

### "Please create a song first!"
- **Cause**: No song exists in the current session
- **Solution**: Create a bar in Bar Manipulation tab or use List Generator

## Testing

Run the test script to verify the integration:

```bash
python3 test_sampler_integration.py
```

This will:
1. Check if SimpleSampler is available
2. Create a test song
3. Play it through SimpleSampler
4. Verify the integration works

## Code Changes

### Modified Files

1. **savellysKone3_gui.py**
   - Added import for `SimpleSamplerPlayer`
   - Added `sampler_player` initialization in `__init__`
   - Added `play_current_song()` method
   - Added `stop_playback()` method
   - Added Play and Stop buttons to Piano Roll tab

### New Files

1. **test_sampler_integration.py**
   - Integration test for SimpleSampler playback

## Future Enhancements

Potential improvements:
- Volume control slider
- Loop playback option
- Playback progress indicator
- Real-time waveform visualization during playback
- Multiple playback modes (SimpleSampler vs. external MIDI player)

## Troubleshooting

**Buttons don't appear in GUI**:
- Check if SimpleSampler is built: `ls simpleSampler/build/SimpleSampler`
- Rebuild if needed: `cd simpleSampler/build && cmake .. && make`

**No sound when playing**:
- Check system volume
- Verify SimpleSampler works: `./simpleSampler/build/SimpleSampler test.mid`
- Check audio output settings

**Error on Play**:
- Ensure you've created a song first
- Check console output for detailed error messages
- Verify MIDI data is valid using Validate button

## Date

November 10, 2025
