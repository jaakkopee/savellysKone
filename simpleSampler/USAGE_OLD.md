# Usage Example

The SimpleSampler has been successfully built! The executable is located at:

```
build/SimpleSampler
```

## Running the Sampler

### Option 1: With command-line argument

```bash
cd build
./SimpleSampler path/to/your/midi/file.mid
```

### Option 2: Interactive mode

```bash
cd build
./SimpleSampler
```

Then enter the path to your MIDI file when prompted.

## Testing with Python-Generated MIDI

Since you have Python MIDI generation scripts in the parent directory (savellysKone3.py), you can:

1. Generate a MIDI file using your Python scripts:
```bash
cd ..
python3 savellysKone3.py  # or any other script that generates .mid files
```

2. Play it with SimpleSampler:
```bash
cd simpleSampler/build
./SimpleSampler ../path_to_generated_file.mid
```

## Features in Action

The sampler will:
- Parse your MIDI file and extract all note events
- Play each note using pure sine wave synthesis
- Apply a gentle ADSR envelope to each note:
  - **Attack**: Quick 10ms fade-in
  - **Decay**: 100ms transition to sustain level
  - **Sustain**: Held at 70% amplitude
  - **Release**: Smooth 200ms fade-out
- Respect note velocities (louder/softer notes)
- Support up to 32 simultaneous voices (polyphony)

## What You'll Hear

The output is intentionally simple - pure sine waves give a clean, electronic sound similar to early synthesizers. The ADSR envelope prevents clicks and creates smooth note transitions.

## Tips

- For best results, use MIDI files with clear melodic content
- The sampler works with any standard MIDI file format 0 or 1
- Press Ctrl+C to stop playback at any time
- Playback timing is displayed in real-time

## Next Steps

Try generating MIDI with your Python tools and playing it with this sampler to hear your programmatic compositions!
