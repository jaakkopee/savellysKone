"""
PianoRollDisplay - A Tkinter-based GUI for visualizing MIDI data
This module provides a piano roll visualization that displays MIDI notes
with support for modulation parameter adjustments.
"""

import tkinter as tk
from tkinter import ttk
import savellysKone3 as sk3


class PianoRollDisplay(tk.Canvas):
    """
    A Canvas-based widget that displays MIDI notes as a piano roll.
    
    The x-axis represents time and the y-axis represents MIDI note numbers.
    Notes are displayed as colored rectangles, with color indicating velocity.
    """
    
    def __init__(self, parent, width=800, height=400, **kwargs):
        super().__init__(parent, width=width, height=height, bg='#1a1a1a', **kwargs)
        
        # Display dimensions
        self.display_width = width
        self.display_height = height
        
        # MIDI note range to display (default: 2 octaves around middle C)
        self.min_note = 48  # C3
        self.max_note = 84  # C6
        
        # Time range (in beats)
        self.min_time = 0
        self.max_time = 32
        
        # Margins for labels
        self.left_margin = 40
        self.right_margin = 20
        self.top_margin = 20
        self.bottom_margin = 40
        
        # Calculate drawable area
        self.grid_width = self.display_width - self.left_margin - self.right_margin
        self.grid_height = self.display_height - self.top_margin - self.bottom_margin
        
        # Song data
        self.song = None
        
        # Draw the initial grid
        self.draw_grid()
        
    def set_song(self, song):
        """Set the Song object to visualize"""
        self.song = song
        self.update_display()
        
    def draw_grid(self):
        """Draw the background grid with axis labels"""
        # Clear canvas
        self.delete("all")
        
        # Draw background
        self.create_rectangle(
            self.left_margin, self.top_margin,
            self.left_margin + self.grid_width,
            self.top_margin + self.grid_height,
            fill='#0a0a0a', outline='#333333'
        )
        
        # Draw horizontal grid lines (for each MIDI note)
        note_range = self.max_note - self.min_note
        for i in range(note_range + 1):
            note_num = self.min_note + i
            y = self.top_margin + self.grid_height - (i * self.grid_height / note_range)
            
            # Highlight C notes (every 12 semitones from C)
            if (note_num % 12) == 0:  # C notes
                color = '#444444'
                width = 2
            else:
                color = '#222222'
                width = 1
                
            self.create_line(
                self.left_margin, y,
                self.left_margin + self.grid_width, y,
                fill=color, width=width
            )
            
            # Draw note labels for C notes
            if (note_num % 12) == 0:
                octave = (note_num // 12) - 1
                label = f"C{octave}"
                self.create_text(
                    self.left_margin - 5, y,
                    text=label, fill='#888888',
                    anchor='e', font=('Arial', 8)
                )
        
        # Draw vertical grid lines (for time)
        time_range = self.max_time - self.min_time
        num_time_divisions = 16
        for i in range(num_time_divisions + 1):
            time_val = self.min_time + (i * time_range / num_time_divisions)
            x = self.left_margin + (i * self.grid_width / num_time_divisions)
            
            # Every 4th line is darker
            if i % 4 == 0:
                color = '#444444'
                width = 2
            else:
                color = '#222222'
                width = 1
                
            self.create_line(
                x, self.top_margin,
                x, self.top_margin + self.grid_height,
                fill=color, width=width
            )
            
            # Draw time labels
            if i % 2 == 0:
                self.create_text(
                    x, self.top_margin + self.grid_height + 10,
                    text=f"{time_val:.1f}", fill='#888888',
                    anchor='n', font=('Arial', 8)
                )
        
        # Draw axis labels
        self.create_text(
            self.left_margin + self.grid_width // 2,
            self.display_height - 5,
            text="Time (beats)", fill='#aaaaaa',
            font=('Arial', 10, 'bold')
        )
        
        self.create_text(
            10, self.top_margin + self.grid_height // 2,
            text="MIDI Note", fill='#aaaaaa',
            angle=90, font=('Arial', 10, 'bold')
        )
    
    def note_to_y(self, note_num):
        """Convert MIDI note number to y-coordinate"""
        note_range = self.max_note - self.min_note
        normalized = (note_num - self.min_note) / note_range
        return self.top_margin + self.grid_height - (normalized * self.grid_height)
    
    def time_to_x(self, time):
        """Convert time to x-coordinate"""
        time_range = self.max_time - self.min_time
        normalized = (time - self.min_time) / time_range
        return self.left_margin + (normalized * self.grid_width)
    
    def velocity_to_color(self, velocity):
        """Convert velocity (0-127) to a color"""
        # Map velocity to color gradient from dark blue to bright yellow
        if velocity < 1:
            return '#111111'  # Very dark for silent notes
        
        normalized = velocity / 127.0
        
        if normalized < 0.25:
            # Dark blue to blue
            intensity = int(normalized * 4 * 128)
            return f"#{0:02x}{0:02x}{intensity:02x}"
        elif normalized < 0.5:
            # Blue to cyan
            intensity = int((normalized - 0.25) * 4 * 255)
            return f"#{0:02x}{intensity:02x}{255:02x}"
        elif normalized < 0.75:
            # Cyan to green
            blue = int((0.75 - normalized) * 4 * 255)
            return f"#{0:02x}{255:02x}{blue:02x}"
        else:
            # Green to yellow
            red = int((normalized - 0.75) * 4 * 255)
            return f"#{red:02x}{255:02x}{0:02x}"
    
    def draw_notes(self):
        """Draw all notes from the song"""
        if not self.song or not self.song.bar_list:
            return
        
        # Delete old notes (keep grid)
        self.delete("note")
        
        # Collect all notes and find time range
        all_notes = []
        max_time = 0
        for bar in self.song.bar_list:
            for note in bar.note_list:
                all_notes.append(note)
                note_end = note.onset + note.duration
                if note_end > max_time:
                    max_time = note_end
        
        # Update time range if needed
        if max_time > self.max_time:
            self.max_time = max_time + 2
            self.draw_grid()
        
        # Draw each note
        for note in all_notes:
            x1 = self.time_to_x(note.onset)
            x2 = self.time_to_x(note.onset + note.duration)
            
            # Note height represents a semitone
            y_center = self.note_to_y(note.pitch)
            note_height = self.grid_height / (self.max_note - self.min_note)
            y1 = y_center - note_height / 2
            y2 = y_center + note_height / 2
            
            # Get color based on velocity
            color = self.velocity_to_color(note.velocity)
            
            # Draw the note rectangle
            self.create_rectangle(
                x1, y1, x2, y2,
                fill=color, outline='#666666',
                tags="note"
            )
            
            # Add a brighter edge to show note-on
            self.create_line(
                x1, y1, x1, y2,
                fill='#ffffff', width=2,
                tags="note"
            )
    
    def update_display(self):
        """Refresh the piano roll display"""
        self.draw_grid()
        self.draw_notes()


class MIDIGeneratorGUI:
    """
    Main GUI application for MIDI generation with piano roll visualization.
    Provides controls for modulation parameters and real-time visualization.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("MIDI Generator with Piano Roll Display")
        self.root.geometry("1000x700")
        
        # Initialize song
        self.song = None
        self.initialize_song()
        
        # Create main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="MIDI Piano Roll Visualizer",
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=10)
        
        # Piano roll display
        self.piano_roll = PianoRollDisplay(main_frame, width=960, height=400)
        self.piano_roll.grid(row=1, column=0, pady=10)
        
        # Control panel
        self.create_control_panel(main_frame)
        
        # Initial display
        self.update_visualization()
        
    def initialize_song(self):
        """Create a default song with some notes"""
        pitch_grammar = """
        $S -> $phrase0 $phrase0 $phrase0 $phrase0
        $phrase0 -> 60 62 64 65 67 69 71 72
        """
        
        duration_grammar = """
        $S -> $phrase0 $phrase0 $phrase0 $phrase0
        $phrase0 -> 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5
        """
        
        velocity_grammar = """
        $S -> $phrase0 $phrase0 $phrase0 $phrase0
        $phrase0 -> 80 90 100 110 100 90 80 70
        """
        
        pitch_generator = sk3.ListGenerator(pitch_grammar, 8, "pitch")
        duration_generator = sk3.ListGenerator(duration_grammar, 8, "duration")
        velocity_generator = sk3.ListGenerator(velocity_grammar, 8, "velocity")
        
        self.song = sk3.Song(
            name="PianoRollDemo",
            num_bars=4,
            ioi=1.0,
            pitch_generator=pitch_generator,
            duration_generator=duration_generator,
            velocity_generator=velocity_generator,
            generate_every_bar=False
        )
        
        self.song.generate_parameter_lists()
        self.song.make_bar_list()
        
    def create_control_panel(self, parent):
        """Create the control panel with modulation parameters"""
        control_frame = ttk.LabelFrame(parent, text="Modulation Controls", padding="10")
        control_frame.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.E))
        
        # Variables for modulation parameters
        self.pitch_freq = tk.DoubleVar(value=1.0)
        self.pitch_amp = tk.DoubleVar(value=0.0)
        self.duration_freq = tk.DoubleVar(value=1.0)
        self.duration_amp = tk.DoubleVar(value=0.0)
        self.velocity_freq = tk.DoubleVar(value=1.0)
        self.velocity_amp = tk.DoubleVar(value=0.0)
        self.onset_freq = tk.DoubleVar(value=1.0)
        self.onset_amp = tk.DoubleVar(value=0.0)
        
        # Pitch modulation controls
        ttk.Label(control_frame, text="Pitch Modulation:").grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Label(control_frame, text="Freq:").grid(row=0, column=1)
        ttk.Scale(control_frame, from_=0.1, to=5.0, variable=self.pitch_freq,
                  orient=tk.HORIZONTAL, length=150, command=self.on_param_change).grid(row=0, column=2)
        ttk.Label(control_frame, textvariable=self.pitch_freq).grid(row=0, column=3)
        ttk.Label(control_frame, text="Amp:").grid(row=0, column=4)
        ttk.Scale(control_frame, from_=0, to=12, variable=self.pitch_amp,
                  orient=tk.HORIZONTAL, length=150, command=self.on_param_change).grid(row=0, column=5)
        ttk.Label(control_frame, textvariable=self.pitch_amp).grid(row=0, column=6)
        
        # Duration modulation controls
        ttk.Label(control_frame, text="Duration Modulation:").grid(row=1, column=0, sticky=tk.W, padx=5)
        ttk.Label(control_frame, text="Freq:").grid(row=1, column=1)
        ttk.Scale(control_frame, from_=0.1, to=5.0, variable=self.duration_freq,
                  orient=tk.HORIZONTAL, length=150, command=self.on_param_change).grid(row=1, column=2)
        ttk.Label(control_frame, textvariable=self.duration_freq).grid(row=1, column=3)
        ttk.Label(control_frame, text="Amp:").grid(row=1, column=4)
        ttk.Scale(control_frame, from_=0, to=1.0, variable=self.duration_amp,
                  orient=tk.HORIZONTAL, length=150, command=self.on_param_change).grid(row=1, column=5)
        ttk.Label(control_frame, textvariable=self.duration_amp).grid(row=1, column=6)
        
        # Velocity modulation controls
        ttk.Label(control_frame, text="Velocity Modulation:").grid(row=2, column=0, sticky=tk.W, padx=5)
        ttk.Label(control_frame, text="Freq:").grid(row=2, column=1)
        ttk.Scale(control_frame, from_=0.1, to=5.0, variable=self.velocity_freq,
                  orient=tk.HORIZONTAL, length=150, command=self.on_param_change).grid(row=2, column=2)
        ttk.Label(control_frame, textvariable=self.velocity_freq).grid(row=2, column=3)
        ttk.Label(control_frame, text="Amp:").grid(row=2, column=4)
        ttk.Scale(control_frame, from_=0, to=50, variable=self.velocity_amp,
                  orient=tk.HORIZONTAL, length=150, command=self.on_param_change).grid(row=2, column=5)
        ttk.Label(control_frame, textvariable=self.velocity_amp).grid(row=2, column=6)
        
        # Onset modulation controls
        ttk.Label(control_frame, text="Onset Modulation:").grid(row=3, column=0, sticky=tk.W, padx=5)
        ttk.Label(control_frame, text="Freq:").grid(row=3, column=1)
        ttk.Scale(control_frame, from_=0.1, to=5.0, variable=self.onset_freq,
                  orient=tk.HORIZONTAL, length=150, command=self.on_param_change).grid(row=3, column=2)
        ttk.Label(control_frame, textvariable=self.onset_freq).grid(row=3, column=3)
        ttk.Label(control_frame, text="Amp:").grid(row=3, column=4)
        ttk.Scale(control_frame, from_=0, to=1.0, variable=self.onset_amp,
                  orient=tk.HORIZONTAL, length=150, command=self.on_param_change).grid(row=3, column=5)
        ttk.Label(control_frame, textvariable=self.onset_amp).grid(row=3, column=6)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=4, column=0, columnspan=7, pady=10)
        
        ttk.Button(button_frame, text="Reset Modulation", 
                   command=self.reset_modulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Regenerate Song", 
                   command=self.regenerate_song).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export MIDI", 
                   command=self.export_midi).pack(side=tk.LEFT, padx=5)
        
    def on_param_change(self, *args):
        """Called when any modulation parameter changes"""
        self.apply_modulation()
        
    def apply_modulation(self):
        """Apply modulation parameters to the song and update display"""
        # Regenerate the song to start fresh
        self.song.generate_parameter_lists()
        self.song.make_bar_list()
        
        # Apply modulations if amplitudes are non-zero
        if self.pitch_amp.get() > 0:
            self.song.modulate_pitch_with_sin(
                self.pitch_freq.get(),
                self.pitch_amp.get()
            )
        
        if self.duration_amp.get() > 0:
            self.song.modulate_duration_with_sin(
                self.duration_freq.get(),
                self.duration_amp.get()
            )
        
        if self.velocity_amp.get() > 0:
            self.song.modulate_velocity_with_sin(
                self.velocity_freq.get(),
                self.velocity_amp.get()
            )
        
        if self.onset_amp.get() > 0:
            self.song.modulate_onset_with_sin(
                self.onset_freq.get(),
                self.onset_amp.get()
            )
        
        # Update the visualization
        self.update_visualization()
        
    def update_visualization(self):
        """Update the piano roll display"""
        self.piano_roll.set_song(self.song)
        
    def reset_modulation(self):
        """Reset all modulation parameters to zero"""
        self.pitch_amp.set(0.0)
        self.duration_amp.set(0.0)
        self.velocity_amp.set(0.0)
        self.onset_amp.set(0.0)
        self.apply_modulation()
        
    def regenerate_song(self):
        """Generate a new song"""
        self.initialize_song()
        self.apply_modulation()
        
    def export_midi(self):
        """Export the current song to a MIDI file"""
        filename = "piano_roll_output.mid"
        self.song.make_midi_file(filename)
        print(f"MIDI file exported to: {filename}")


def main():
    """Run the MIDI Generator GUI application"""
    root = tk.Tk()
    app = MIDIGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
