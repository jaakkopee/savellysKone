# Integration Guide: SimpleSampler + savellysKone3_gui

This guide shows how to add a "Play MIDI" button to the savellysKone3_gui that uses SimpleSampler to play compositions.

## Quick Integration

### Step 1: Add the import

Add this near the top of `savellysKone3_gui.py` (after other imports):

```python
import sys
import os

# Add SimpleSampler directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'simpleSampler'))

try:
    from sampler_player import SimpleSamplerPlayer
    SAMPLER_AVAILABLE = True
except ImportError:
    SAMPLER_AVAILABLE = False
    print("SimpleSampler not available - play functionality disabled")
```

### Step 2: Initialize player in SavellysKoneGUI.__init__

Add this in the `__init__` method after initializing other attributes:

```python
# Initialize SimpleSampler player
self.sampler_player = None
if SAMPLER_AVAILABLE:
    sampler_path = os.path.join(os.path.dirname(__file__), 
                                'simpleSampler', 'build', 'SimpleSampler')
    self.sampler_player = SimpleSamplerPlayer(sampler_path)
    if not self.sampler_player.is_available():
        print(f"SimpleSampler executable not found at {sampler_path}")
        print("Please build SimpleSampler first: cd simpleSampler/build && cmake .. && make")
        self.sampler_player = None
```

### Step 3: Add play method

Add this method to the `SavellysKoneGUI` class:

```python
def play_current_song(self):
    """Play the current song using SimpleSampler"""
    if self.sampler_player is None:
        messagebox.showerror("Error", "SimpleSampler not available.\n\n"
                           "Please build SimpleSampler:\n"
                           "cd simpleSampler/build\n"
                           "cmake .. && make")
        return
    
    if self.song is None:
        messagebox.showerror("Error", "No song to play. Please create a bar first.")
        return
    
    try:
        # Stop any currently playing audio
        if self.sampler_player.is_playing():
            self.sampler_player.stop()
        
        # Create temp MIDI and play
        self.update_status("Playing MIDI with SimpleSampler...")
        temp_path, process = self.sampler_player.play_from_song(self.song, background=True)
        
        # Store temp path for cleanup later
        if not hasattr(self, 'temp_midi_files'):
            self.temp_midi_files = []
        self.temp_midi_files.append(temp_path)
        
        messagebox.showinfo("Playing", "MIDI playback started!\n\n"
                          "The audio is playing through SimpleSampler.\n"
                          "Press Ctrl+C in the terminal to stop.")
        
    except Exception as e:
        messagebox.showerror("Playback Error", f"Failed to play MIDI:\n{str(e)}")
```

### Step 4: Add cleanup method

Add this cleanup method and call it from `__del__` or window close:

```python
def cleanup_temp_files(self):
    """Clean up temporary MIDI files"""
    if hasattr(self, 'temp_midi_files'):
        for temp_file in self.temp_midi_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except:
                pass
```

### Step 5: Add Play button to Piano Roll tab

In the `create_piano_roll_tab` method, add a Play button alongside the Export button:

```python
# In the button frame where Export MIDI button is created, add:

# Play MIDI button
if self.sampler_player and self.sampler_player.is_available():
    play_button = ttk.Button(
        button_frame, 
        text="▶ Play MIDI", 
        command=self.play_current_song
    )
    play_button.pack(side=tk.LEFT, padx=5)
```

### Step 6: Optional - Add to Menu Bar

In the `create_menu_bar` method, add to the File menu:

```python
# Add to File menu, after Export MIDI:
if self.sampler_player and self.sampler_player.is_available():
    file_menu.add_command(label="Play MIDI", command=self.play_current_song)
```

## Alternative: Simple Integration (Minimal Changes)

If you want minimal changes, just add a single button somewhere in your GUI:

```python
# Anywhere in your GUI layout:
play_btn = ttk.Button(
    parent_frame,
    text="▶ Play with SimpleSampler",
    command=lambda: self.play_with_sampler()
)
play_btn.pack()

# And this method:
def play_with_sampler(self):
    if self.song is None:
        messagebox.showerror("Error", "Create a bar first")
        return
    
    # Create temp MIDI file
    import tempfile
    temp_fd, temp_path = tempfile.mkstemp(suffix='.mid')
    os.close(temp_fd)
    
    try:
        self.song.make_midi_file(temp_path)
        
        # Run SimpleSampler
        sampler_path = os.path.join(os.path.dirname(__file__), 
                                    'simpleSampler/build/SimpleSampler')
        subprocess.Popen([sampler_path, temp_path])
        
        messagebox.showinfo("Playing", "MIDI playback started!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
```

## Testing the Integration

1. Build SimpleSampler (if not already done):
```bash
cd simpleSampler/build
cmake .. && make
```

2. Run the GUI:
```bash
python3 savellysKone3_gui.py
```

3. Create a bar using the List Generator or Bar Manipulation tabs

4. Click the "Play MIDI" button

5. You should hear your composition played through sine wave synthesis!

## Troubleshooting

**"SimpleSampler not available"**
- Make sure SimpleSampler is built: `cd simpleSampler/build && make`
- Check that the executable exists at `simpleSampler/build/SimpleSampler`

**No sound when playing**
- Check system audio is not muted
- Verify SimpleSampler works standalone: `./simpleSampler/build/SimpleSampler test.mid`
- Check that SFML audio libraries are installed

**Button doesn't appear**
- Make sure `SAMPLER_AVAILABLE` is True
- Check that `self.sampler_player.is_available()` returns True
- Verify the path to SimpleSampler executable

## Complete Example Code Snippet

Here's a complete snippet you can add to your GUI class:

```python
# Add these methods to SavellysKoneGUI class:

def init_sampler(self):
    """Initialize SimpleSampler integration"""
    try:
        from sampler_player import SimpleSamplerPlayer
        sampler_path = os.path.join(os.path.dirname(__file__), 
                                    'simpleSampler', 'build', 'SimpleSampler')
        self.sampler_player = SimpleSamplerPlayer(sampler_path)
        if not self.sampler_player.is_available():
            self.sampler_player = None
    except:
        self.sampler_player = None

def play_current_composition(self):
    """Play current composition with SimpleSampler"""
    if self.sampler_player is None:
        messagebox.showwarning("SimpleSampler Unavailable", 
                              "SimpleSampler is not built or not found.")
        return
    
    if self.song is None:
        messagebox.showwarning("No Song", "Please create a song first.")
        return
    
    try:
        # Stop any playing audio
        if self.sampler_player.is_playing():
            self.sampler_player.stop()
        
        # Play the song
        temp_path, _ = self.sampler_player.play_from_song(self.song, background=True)
        self.update_status("Playing MIDI...")
        
    except Exception as e:
        messagebox.showerror("Playback Error", f"Error: {e}")
```

Then call `self.init_sampler()` in `__init__` and use `self.play_current_composition()` as your button command.
