# SimpleSampler - Synthesis Mode Feature Summary

## What Was Added

SimpleSampler now supports **two synthesis modes**:

### 1. Sine Wave Mode (Original)
- Pure sine wave synthesis
- ADSR envelope (Attack: 10ms, Decay: 100ms, Sustain: 70%, Release: 200ms)
- Lightweight, no extra dependencies
- 20% gain to prevent distortion with polyphony

### 2. SoundFont Mode (New!)
- High-quality sampled piano sound
- Uses FluidSynth library
- Motif ES6 Concert Piano SoundFont (12MB, included)
- Professional audio quality

## Usage

### Command Line

**Sine Wave (Default):**
```bash
./SimpleSampler song.mid
```

**SoundFont (Piano):**
```bash
./SimpleSampler song.mid --soundfont
# or
./SimpleSampler song.mid -sf
```

### Python Wrapper

```python
from sampler_player import SimpleSamplerPlayer

# Sine wave mode
player = SimpleSamplerPlayer(use_soundfont=False)
player.play_midi_file("song.mid")

# SoundFont mode  
player = SimpleSamplerPlayer(use_soundfont=True)
player.play_midi_file("song.mid")
```

## Files Modified/Added

### New Files:
- `include/SoundFontSynth.h` - SoundFont synthesizer interface
- `src/SoundFontSynth.cpp` - FluidSynth wrapper implementation
- `USAGE.md` - Comprehensive usage documentation

### Modified Files:
- `CMakeLists.txt` - Added FluidSynth dependency
- `include/AudioEngine.h` - Added SynthMode enum and mode selection
- `src/AudioEngine.cpp` - Dual synthesis path (sine wave / SoundFont)
- `src/main.cpp` - Added command-line argument parsing for mode selection
- `sampler_player.py` - Added `use_soundfont` parameter

## Dependencies

**New Requirement:**
- FluidSynth 2.5+ (installed via `brew install fluidsynth`)

**Existing Requirements:**
- SFML 3.0+
- C++17 compiler

## Implementation Details

### AudioEngine Changes
- `SynthMode` enum with `SineWave` and `SoundFont` values
- Dual synthesis paths in `onGetData()`:
  - Sine wave: Real-time sample generation per note
  - SoundFont: Batch rendering via FluidSynth
- Mode selection via `setSynthMode()`
- Both synthesizers initialized, mode switches which one is used

### SoundFontSynth Class
- Wraps FluidSynth C API in C++ interface
- Handles SF2 file loading
- Manages note on/off events via MIDI channels
- Provides stereo float buffer output
- 32-voice polyphony (same as sine wave mode)

### Main Program Flow
1. Parse command-line arguments for `--soundfont` flag
2. If SoundFont requested:
   - Attempt to load SF2 file from `build/soundfonts/` or `soundfonts/`
   - Set mode to SoundFont if successful
   - Fall back to sine wave if loading fails
3. Load MIDI file
4. Start playback with selected mode

## Audio Quality Comparison

| Aspect | Sine Wave | SoundFont |
|--------|-----------|-----------|
| Sound | Synthetic, clean | Realistic piano |
| Quality | Basic | Professional |
| File Size | ~200KB binary | +12MB SF2 file |
| CPU Usage | Very low | Low-Medium |
| Dependencies | SFML only | SFML + FluidSynth |
| Use Case | Development/Testing | Production/Demo |

## Testing Results

Both modes tested successfully with `test.mid`:
- ✅ Sine wave mode plays with envelope-shaped tones
- ✅ SoundFont mode plays with realistic piano sound
- ✅ Polyphony works in both modes
- ✅ Note timing accurate in both modes
- ✅ Volume levels appropriate (no clipping)

## Integration Notes

For GUI integration, add a checkbox or toggle:
```python
# Example GUI code
self.soundfont_enabled = tk.BooleanVar(value=False)
tk.Checkbutton(frame, text="Use Piano Sound", 
               variable=self.soundfont_enabled).pack()

# When playing:
player = SimpleSamplerPlayer(use_soundfont=self.soundfont_enabled.get())
```

## Known Issues

1. FluidSynth warning about channel 9 (drums) - **harmless, can be ignored**
2. SoundFont file must be exactly named "Motif ES6 Concert Piano(12Mb).SF2"
3. First note may have slight latency in SoundFont mode (FluidSynth initialization)

## Future Enhancements

Possible improvements:
- Support for multiple SoundFonts (user selection)
- Instrument/program change support
- Reverb/chorus effects in SoundFont mode
- Volume control per mode
- Export to WAV file

## Performance

Both modes:
- Sample rate: 44100 Hz
- Polyphony: 32 voices
- Latency: ~93ms
- CPU usage: < 5% on Apple Silicon

SoundFont mode adds minimal CPU overhead thanks to FluidSynth's efficient rendering.
