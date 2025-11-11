"""
Tkinter GUI for savellysKone3.py

This GUI provides an easy-to-use interface for interacting with the main components
of savellysKone3.py, including:
- ListGenerator for generating pitch, duration, and velocity lists from grammars
- Bar objects for creating and manipulating musical bars
- Various operations like transpose, reverse, random modifications
- Piano roll visualization of songs
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import savellysKone3 as sk3
import midi_parser
import os
import tempfile
import sys
import subprocess


class PianoRollDisplay(tk.Canvas):
    """
    A Canvas-based widget that displays MIDI notes as a piano roll.
    
    The x-axis represents time and the y-axis represents MIDI note numbers.
    Notes are displayed as colored rectangles, with color indicating velocity.
    Note onsets are marked with a white edge.
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
        """Convert velocity (0-127) to a color based on specified ranges"""
        # Velocity ranges with corresponding colors
        if velocity <= 15:
            # Dark red (0-15)
            # Interpolate from very dark red to dark red
            normalized = velocity / 15.0
            red = int(80 + (139 - 80) * normalized)
            return f"#{red:02x}0000"
        elif velocity <= 31:
            # Dark orange (16-31)
            normalized = (velocity - 16) / 15.0
            red = int(139 + (255 - 139) * normalized)
            green = int(0 + (69 - 0) * normalized)
            return f"#{red:02x}{green:02x}00"
        elif velocity <= 47:
            # Dark yellow (32-47)
            normalized = (velocity - 32) / 15.0
            red = int(204 + (218 - 204) * normalized)
            green = int(102 + (165 - 102) * normalized)
            return f"#{red:02x}{green:02x}00"
        elif velocity <= 51:
            # Green (48-51)
            normalized = (velocity - 48) / 3.0
            green = int(100 + (155 - 100) * normalized)
            return f"#00{green:02x}00"
        elif velocity <= 63:
            # Greenish blue (52-63)
            normalized = (velocity - 52) / 11.0
            green = int(155 - (155 - 100) * normalized)
            blue = int(0 + (100 - 0) * normalized)
            return f"#00{green:02x}{blue:02x}"
        elif velocity <= 79:
            # Blue (64-79)
            normalized = (velocity - 64) / 15.0
            green = int(100 - (100 - 0) * normalized)
            blue = int(100 + (255 - 100) * normalized)
            return f"#00{green:02x}{blue:02x}"
        elif velocity <= 95:
            # Blueish violet (80-95)
            normalized = (velocity - 80) / 15.0
            red = int(0 + (138 - 0) * normalized)
            blue = 255
            return f"#{red:02x}00{blue:02x}"
        elif velocity <= 111:
            # Violet (96-111)
            normalized = (velocity - 96) / 15.0
            red = int(138 + (238 - 138) * normalized)
            blue = 255
            return f"#{red:02x}00{blue:02x}"
        else:
            # Bright indigo (112-127)
            normalized = (velocity - 112) / 15.0
            red = int(238 + (75 - 238) * normalized)
            green = int(0 + (0 - 0) * normalized)
            blue = int(255 + (130 - 255) * normalized)
            return f"#{red:02x}{green:02x}{blue:02x}"
    
    def draw_notes(self):
        """Draw all notes from the song"""
        if not self.song or not self.song.bar_list:
            return
        
        # Delete old notes (keep grid)
        self.delete("note")
        
        # Collect all notes and find time range
        all_notes = []
        max_time = 0
        min_note = 127
        max_note = 0
        velocities = []  # Track velocities for debugging
        
        for bar in self.song.bar_list:
            for note in bar.note_list:
                all_notes.append(note)
                velocities.append(note.velocity)
                note_end = note.onset + note.duration
                if note_end > max_time:
                    max_time = note_end
                if note.pitch < min_note:
                    min_note = note.pitch
                if note.pitch > max_note:
                    max_note = note.pitch
        
        # Debug: Print velocity range
        if velocities:
            print(f"Velocity range: {min(velocities)} - {max(velocities)}")
            print(f"Unique velocities: {sorted(set(velocities))}")
        
        # Update ranges if needed
        if max_time > self.max_time:
            self.max_time = max_time + 2
            self.draw_grid()
        
        # Update note range with some padding
        if all_notes:
            self.min_note = max(0, min_note - 3)
            self.max_note = min(127, max_note + 3)
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
            
            # Debug: Print first few color mappings
            if len(all_notes) <= 10 or all_notes.index(note) < 3:
                print(f"Note velocity {note.velocity} -> color {color}")
            
            # Draw the note rectangle
            self.create_rectangle(
                x1, y1, x2, y2,
                fill=color, outline='#666666',
                tags="note"
            )
            
            # Add a white edge to mark note onset
            self.create_line(
                x1, y1, x1, y2,
                fill='#ffffff', width=2,
                tags="note"
            )
    
    def update_display(self):
        """Refresh the piano roll display"""
        self.draw_grid()
        self.draw_notes()
        # Update scroll region to include all content
        self.configure(scrollregion=self.bbox("all"))


class SavellysKoneGUI:
    """Main GUI class for savellysKone3"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SavellysKone3 GUI")
        self.root.geometry("1125x700")  # 25% wider: 900 * 1.25 = 1125
        
        # Variables to store generators and bar
        self.list_generator = None
        self.current_bar = None
        self.current_song = None
        self.piano_roll = None
        
        # Variables to store generated lists
        self.generated_pitch_list = None
        self.generated_duration_list = None
        self.generated_velocity_list = None
        
        # Variables for playback
        self.sampler_process = None
        self.temp_midi_path = None
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_list_generator_tab()
        self.create_bar_manipulation_tab()
        self.create_song_modulation_tab()
        self.create_piano_roll_tab()
        
        # Create status bar at bottom
        self.create_status_bar()
    
    def create_status_bar(self):
        """Create status bar at the bottom of the window"""
        status_frame = tk.Frame(self.root, relief='sunken', borderwidth=1)
        status_frame.pack(side='bottom', fill='x')
        
        self.status_label = tk.Label(status_frame, text="Ready", 
                                      anchor='w', padx=10, pady=3)
        self.status_label.pack(side='left', fill='x', expand=True)
        
        # Add current object indicator
        self.object_status_label = tk.Label(status_frame, text="No song/bar loaded", 
                                             anchor='e', padx=10, pady=3, foreground='gray')
        self.object_status_label.pack(side='right')
    
    def update_status(self, message):
        """Update the status bar message"""
        self.status_label.config(text=message)
        self.root.after(3000, lambda: self.status_label.config(text="Ready"))
    
    def create_menu_bar(self):
        """Create the menu bar with File menu for MIDI operations"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        
        file_menu.add_command(label="Export Song to MIDI", 
                              command=self.export_song_to_midi)
        file_menu.add_command(label="Export Bar to MIDI", 
                              command=self.export_bar_to_midi)
        file_menu.add_separator()
        file_menu.add_command(label="Validate Current Song", 
                              command=self.validate_current_song)
        file_menu.add_command(label="Validate Current Bar", 
                              command=self.validate_current_bar)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def show_about(self):
        """Display about information"""
        about_text = """
SavellysKone3 GUI
Version 1.0

A comprehensive MIDI generation and manipulation tool.

Features:
  • Grammar-based list generation
  • Bar and song creation
  • Sine wave modulation
  • Piano roll visualization
  • MIDI validation
  • Real-time preview

Created with Python and Tkinter
        """
        messagebox.showinfo("About SavellysKone3", about_text)
    
    def create_list_generator_tab(self):
        """Create the ListGenerator tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="List Generator")
        
        # Create a notebook for the three grammar types
        grammar_notebook = ttk.Notebook(tab)
        grammar_notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Pitch Grammar Tab
        pitch_tab = ttk.Frame(grammar_notebook)
        grammar_notebook.add(pitch_tab, text="Pitch Grammar")
        self.create_grammar_section(pitch_tab, "pitch")
        
        # Duration Grammar Tab
        duration_tab = ttk.Frame(grammar_notebook)
        grammar_notebook.add(duration_tab, text="Duration Grammar")
        self.create_grammar_section(duration_tab, "duration")
        
        # Velocity Grammar Tab
        velocity_tab = ttk.Frame(grammar_notebook)
        grammar_notebook.add(velocity_tab, text="Velocity Grammar")
        self.create_grammar_section(velocity_tab, "velocity")
        
        # Generate All button
        generate_all_frame = ttk.Frame(tab)
        generate_all_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(generate_all_frame, text="Generate All Lists", 
                   command=self.generate_all_lists, 
                   style='Accent.TButton').pack(pady=5)
        
        ttk.Button(generate_all_frame, text="Use Generated Lists in Bar Creation", 
                   command=self.use_generated_lists).pack(pady=5)
        
        # Combined output section
        output_frame = ttk.LabelFrame(tab, text="All Generated Lists", padding=10)
        output_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.all_output_text = scrolledtext.ScrolledText(output_frame, height=8, width=80)
        self.all_output_text.pack(fill='both', expand=True)
    
    def create_grammar_section(self, parent, grammar_type):
        """Create a grammar input section for a specific type"""
        # Grammar input section
        grammar_frame = ttk.LabelFrame(parent, text=f"{grammar_type.capitalize()} Grammar Input", padding=10)
        grammar_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        ttk.Label(grammar_frame, text="Grammar String:").pack(anchor='w')
        
        # Create text widget for this grammar type
        if grammar_type == "pitch":
            self.pitch_grammar_text = scrolledtext.ScrolledText(grammar_frame, height=10, width=80)
            self.pitch_grammar_text.pack(fill='both', expand=True, pady=5)
            
            # Set default pitch grammar
            default_grammar = """$S -> $phrase01 $phrase02
$phrase01 -> $note01 $note02 $note03 $note04
$phrase02 -> $note05 $note06 $note07 $note08
$note01 -> 60
$note02 -> 62
$note03 -> 64
$note04 -> 65
$note05 -> 67
$note06 -> 69
$note07 -> 71
$note08 -> 72"""
            self.pitch_grammar_text.insert('1.0', default_grammar)
            
        elif grammar_type == "duration":
            self.duration_grammar_text = scrolledtext.ScrolledText(grammar_frame, height=10, width=80)
            self.duration_grammar_text.pack(fill='both', expand=True, pady=5)
            
            # Set default duration grammar
            default_grammar = """$S -> $phrase01 $phrase02
$phrase01 -> $dur01 $dur02 $dur03 $dur04
$phrase02 -> $dur05 $dur06 $dur07 $dur08
$dur01 -> 1.0
$dur02 -> 0.5
$dur03 -> 1.0
$dur04 -> 0.5
$dur05 -> 0.75
$dur06 -> 0.75
$dur07 -> 1.0
$dur08 -> 1.0"""
            self.duration_grammar_text.insert('1.0', default_grammar)
            
        else:  # velocity
            self.velocity_grammar_text = scrolledtext.ScrolledText(grammar_frame, height=10, width=80)
            self.velocity_grammar_text.pack(fill='both', expand=True, pady=5)
            
            # Set default velocity grammar - matches Bar Manipulation default
            default_grammar = """$S -> $phrase01 $phrase02
$phrase01 -> $vel01 $vel02 $vel03 $vel04
$phrase02 -> $vel05 $vel06 $vel07 $vel08
$vel01 -> 60
$vel02 -> 80
$vel03 -> 100
$vel04 -> 90
$vel05 -> 70
$vel06 -> 95
$vel07 -> 85
$vel08 -> 110"""
            self.velocity_grammar_text.insert('1.0', default_grammar)
        
        # Parameters frame
        params_frame = ttk.Frame(grammar_frame)
        params_frame.pack(fill='x', pady=5)
        
        ttk.Label(params_frame, text="Minimum Length:").pack(side='left', padx=5)
        
        if grammar_type == "pitch":
            self.pitch_min_length_var = tk.StringVar(value="8")
            ttk.Entry(params_frame, textvariable=self.pitch_min_length_var, width=10).pack(side='left', padx=5)
            # Generate Every Bar checkbox
            self.pitch_geb_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(params_frame, text="Generate Every Bar (GEB)", 
                           variable=self.pitch_geb_var,
                           command=self.update_geb_status).pack(side='left', padx=20)
            # Generate button for this specific grammar
            self.pitch_generate_button = ttk.Button(grammar_frame, text="Generate Pitch List", 
                       command=lambda: self.generate_single_list("pitch"))
            self.pitch_generate_button.pack(pady=5)
        elif grammar_type == "duration":
            self.duration_min_length_var = tk.StringVar(value="8")
            ttk.Entry(params_frame, textvariable=self.duration_min_length_var, width=10).pack(side='left', padx=5)
            # Generate Every Bar checkbox
            self.duration_geb_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(params_frame, text="Generate Every Bar (GEB)", 
                           variable=self.duration_geb_var,
                           command=self.update_geb_status).pack(side='left', padx=20)
            # Generate button for this specific grammar
            self.duration_generate_button = ttk.Button(grammar_frame, text="Generate Duration List", 
                       command=lambda: self.generate_single_list("duration"))
            self.duration_generate_button.pack(pady=5)
        else:  # velocity
            self.velocity_min_length_var = tk.StringVar(value="8")
            ttk.Entry(params_frame, textvariable=self.velocity_min_length_var, width=10).pack(side='left', padx=5)
            # Generate Every Bar checkbox
            self.velocity_geb_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(params_frame, text="Generate Every Bar (GEB)", 
                           variable=self.velocity_geb_var,
                           command=self.update_geb_status).pack(side='left', padx=20)
            # Generate button for this specific grammar
            self.velocity_generate_button = ttk.Button(grammar_frame, text="Generate Velocity List", 
                       command=lambda: self.generate_single_list("velocity"))
            self.velocity_generate_button.pack(pady=5)
        
        # Output section for this grammar
        output_frame = ttk.LabelFrame(parent, text=f"Generated {grammar_type.capitalize()} List", padding=10)
        output_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        if grammar_type == "pitch":
            self.pitch_output_text = scrolledtext.ScrolledText(output_frame, height=5, width=80)
            self.pitch_output_text.pack(fill='both', expand=True)
        elif grammar_type == "duration":
            self.duration_output_text = scrolledtext.ScrolledText(output_frame, height=5, width=80)
            self.duration_output_text.pack(fill='both', expand=True)
        else:  # velocity
            self.velocity_output_text = scrolledtext.ScrolledText(output_frame, height=5, width=80)
            self.velocity_output_text.pack(fill='both', expand=True)
        
    def create_bar_manipulation_tab(self):
        """Create the Bar Manipulation tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Bar Manipulation")
        
        # Bar creation section
        creation_frame = ttk.LabelFrame(tab, text="Create Bar", padding=10)
        creation_frame.pack(fill='x', padx=10, pady=5)
        
        # Pitch list input
        pitch_frame = ttk.Frame(creation_frame)
        pitch_frame.pack(fill='x', pady=2)
        self.pitch_label = ttk.Label(pitch_frame, text="Pitch List (comma-separated):")
        self.pitch_label.pack(side='left', padx=5)
        self.pitch_list_var = tk.StringVar(value="60, 62, 64, 65, 67, 69, 71, 72")
        ttk.Entry(pitch_frame, textvariable=self.pitch_list_var, width=50).pack(side='left', padx=5)
        
        # Duration list input
        duration_frame = ttk.Frame(creation_frame)
        duration_frame.pack(fill='x', pady=2)
        self.duration_label = ttk.Label(duration_frame, text="Duration List (comma-separated):")
        self.duration_label.pack(side='left', padx=5)
        self.duration_list_var = tk.StringVar(value="1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0")
        ttk.Entry(duration_frame, textvariable=self.duration_list_var, width=50).pack(side='left', padx=5)
        
        # Velocity list input
        velocity_frame = ttk.Frame(creation_frame)
        velocity_frame.pack(fill='x', pady=2)
        self.velocity_label = ttk.Label(velocity_frame, text="Velocity List (comma-separated):")
        self.velocity_label.pack(side='left', padx=5)
        self.velocity_list_var = tk.StringVar(value="60, 80, 100, 90, 70, 95, 85, 110")
        ttk.Entry(velocity_frame, textvariable=self.velocity_list_var, width=50).pack(side='left', padx=5)
        
        # Bar parameters
        params_frame = ttk.Frame(creation_frame)
        params_frame.pack(fill='x', pady=5)
        
        ttk.Label(params_frame, text="Onset:").pack(side='left', padx=5)
        self.onset_var = tk.StringVar(value="0")
        ttk.Entry(params_frame, textvariable=self.onset_var, width=10).pack(side='left', padx=5)
        
        ttk.Label(params_frame, text="IOI (Inter-Onset Interval):").pack(side='left', padx=5)
        self.ioi_var = tk.StringVar(value="0.75")
        ttk.Entry(params_frame, textvariable=self.ioi_var, width=10).pack(side='left', padx=5)
        
        ttk.Button(creation_frame, text="Create Bar", 
                   command=self.create_bar).pack(pady=5)
        
        # Bar operations section
        operations_frame = ttk.LabelFrame(tab, text="Bar Operations", padding=10)
        operations_frame.pack(fill='x', padx=10, pady=5)
        
        # Transpose operation
        transpose_frame = ttk.Frame(operations_frame)
        transpose_frame.pack(fill='x', pady=2)
        ttk.Label(transpose_frame, text="Transpose (semitones):").pack(side='left', padx=5)
        self.transpose_var = tk.StringVar(value="0")
        ttk.Entry(transpose_frame, textvariable=self.transpose_var, width=10).pack(side='left', padx=5)
        ttk.Button(transpose_frame, text="Apply Transpose", 
                   command=self.transpose_bar).pack(side='left', padx=5)
        
        # Duration setting
        duration_op_frame = ttk.Frame(operations_frame)
        duration_op_frame.pack(fill='x', pady=2)
        ttk.Label(duration_op_frame, text="Set Duration:").pack(side='left', padx=5)
        self.set_duration_var = tk.StringVar(value="1.0")
        ttk.Entry(duration_op_frame, textvariable=self.set_duration_var, width=10).pack(side='left', padx=5)
        ttk.Button(duration_op_frame, text="Apply Duration", 
                   command=self.set_duration).pack(side='left', padx=5)
        
        # Other operations buttons
        button_frame = ttk.Frame(operations_frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="Reverse Notes", 
                   command=self.reverse_notes).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Random Pitches", 
                   command=self.random_pitches).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Random Durations", 
                   command=self.random_durations).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Random Velocities", 
                   command=self.random_velocities).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Random Onsets", 
                   command=self.random_onsets).pack(side='left', padx=5)
        
        # Bar display section
        display_frame = ttk.LabelFrame(tab, text="Current Bar", padding=10)
        display_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.bar_display = scrolledtext.ScrolledText(display_frame, height=15, width=80)
        self.bar_display.pack(fill='both', expand=True)
        
        # Bar export section
        bar_export_frame = ttk.Frame(display_frame)
        bar_export_frame.pack(fill='x', pady=5)
        
        ttk.Button(bar_export_frame, text="Export Bar to MIDI", 
                   command=self.export_bar_to_midi).pack(side='left', padx=5)
        ttk.Button(bar_export_frame, text="Validate Bar", 
                   command=self.validate_current_bar).pack(side='left', padx=5)
    
    def generate_single_list(self, grammar_type):
        """Generate a list using ListGenerator for a specific grammar type"""
        try:
            # Get grammar string and parameters based on type
            if grammar_type == "pitch":
                grammar_str = self.pitch_grammar_text.get('1.0', 'end-1c')
                min_length = int(self.pitch_min_length_var.get())
                output_widget = self.pitch_output_text
            elif grammar_type == "duration":
                grammar_str = self.duration_grammar_text.get('1.0', 'end-1c')
                min_length = int(self.duration_min_length_var.get())
                output_widget = self.duration_output_text
            else:  # velocity
                grammar_str = self.velocity_grammar_text.get('1.0', 'end-1c')
                min_length = int(self.velocity_min_length_var.get())
                output_widget = self.velocity_output_text
            
            # Create ListGenerator
            generator = sk3.ListGenerator(grammar_str, min_length, grammar_type)
            
            # Generate list
            generated_list = generator.generate_list()
            
            # Store the generated list
            if grammar_type == "pitch":
                self.generated_pitch_list = generated_list
                # Update Bar Manipulation tab
                pitch_str = ", ".join(str(p) for p in generated_list)
                self.pitch_list_var.set(pitch_str)
            elif grammar_type == "duration":
                self.generated_duration_list = generated_list
                # Update Bar Manipulation tab
                duration_str = ", ".join(str(d) for d in generated_list)
                self.duration_list_var.set(duration_str)
            else:  # velocity
                self.generated_velocity_list = generated_list
                # Update Bar Manipulation tab
                velocity_str = ", ".join(str(v) for v in generated_list)
                self.velocity_list_var.set(velocity_str)
            
            # Display result
            output_widget.delete('1.0', 'end')
            output_widget.insert('1.0', f"Generated {grammar_type} list:\n")
            output_widget.insert('end', f"{generated_list}\n\n")
            output_widget.insert('end', f"Length: {len(generated_list)}")
            
            # Update status
            self.update_status(f"{grammar_type.capitalize()} list generated and transferred to Bar Manipulation")
            
            messagebox.showinfo("Success", f"{grammar_type.capitalize()} list generated!\nLength: {len(generated_list)}\n\nBar Manipulation tab updated.")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid parameter value: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating {grammar_type} list: {str(e)}")
    
    def update_geb_status(self):
        """Update the labels in Bar Manipulation tab to show GEB status"""
        # Check which lists have GEB enabled
        pitch_geb = self.pitch_geb_var.get() if hasattr(self, 'pitch_geb_var') else False
        duration_geb = self.duration_geb_var.get() if hasattr(self, 'duration_geb_var') else False
        velocity_geb = self.velocity_geb_var.get() if hasattr(self, 'velocity_geb_var') else False
        
        # Update labels
        if hasattr(self, 'pitch_label'):
            pitch_text = "Pitch List (comma-separated)" + (" [GEB]" if pitch_geb else "") + ":"
            self.pitch_label.config(text=pitch_text)
        
        if hasattr(self, 'duration_label'):
            duration_text = "Duration List (comma-separated)" + (" [GEB]" if duration_geb else "") + ":"
            self.duration_label.config(text=duration_text)
        
        if hasattr(self, 'velocity_label'):
            velocity_text = "Velocity List (comma-separated)" + (" [GEB]" if velocity_geb else "") + ":"
            self.velocity_label.config(text=velocity_text)
        
        # Enable/disable generate buttons and clear lists based on GEB status
        if hasattr(self, 'pitch_generate_button'):
            self.pitch_generate_button.config(state='disabled' if pitch_geb else 'normal')
            if pitch_geb:
                # Clear generated pitch list in grammar tab
                if hasattr(self, 'pitch_output_text'):
                    self.pitch_output_text.delete('1.0', 'end')
                    self.pitch_output_text.insert('1.0', 'GEB - List will be generated for each bar')
                # Clear pitch list in bar manipulation tab
                if hasattr(self, 'pitch_list_var'):
                    self.pitch_list_var.set('GEB')
        
        if hasattr(self, 'duration_generate_button'):
            self.duration_generate_button.config(state='disabled' if duration_geb else 'normal')
            if duration_geb:
                # Clear generated duration list in grammar tab
                if hasattr(self, 'duration_output_text'):
                    self.duration_output_text.delete('1.0', 'end')
                    self.duration_output_text.insert('1.0', 'GEB - List will be generated for each bar')
                # Clear duration list in bar manipulation tab
                if hasattr(self, 'duration_list_var'):
                    self.duration_list_var.set('GEB')
        
        if hasattr(self, 'velocity_generate_button'):
            self.velocity_generate_button.config(state='disabled' if velocity_geb else 'normal')
            if velocity_geb:
                # Clear generated velocity list in grammar tab
                if hasattr(self, 'velocity_output_text'):
                    self.velocity_output_text.delete('1.0', 'end')
                    self.velocity_output_text.insert('1.0', 'GEB - List will be generated for each bar')
                # Clear velocity list in bar manipulation tab
                if hasattr(self, 'velocity_list_var'):
                    self.velocity_list_var.set('GEB')
    
    def generate_all_lists(self):
        """Generate all three lists (pitch, duration, velocity)"""
        try:
            # Generate pitch list
            self.generate_single_list("pitch")
            # Generate duration list
            self.generate_single_list("duration")
            # Generate velocity list
            self.generate_single_list("velocity")
            
            # Display all lists in combined output
            self.all_output_text.delete('1.0', 'end')
            self.all_output_text.insert('1.0', "=== ALL GENERATED LISTS ===\n\n")
            
            if hasattr(self, 'generated_pitch_list'):
                self.all_output_text.insert('end', f"Pitch List ({len(self.generated_pitch_list)} items):\n")
                self.all_output_text.insert('end', f"{self.generated_pitch_list}\n\n")
            
            if hasattr(self, 'generated_duration_list'):
                self.all_output_text.insert('end', f"Duration List ({len(self.generated_duration_list)} items):\n")
                self.all_output_text.insert('end', f"{self.generated_duration_list}\n\n")
            
            if hasattr(self, 'generated_velocity_list'):
                self.all_output_text.insert('end', f"Velocity List ({len(self.generated_velocity_list)} items):\n")
                self.all_output_text.insert('end', f"{self.generated_velocity_list}\n")
            
            # Update status
            self.update_status("All lists generated and transferred to Bar Manipulation tab")
            
            # Don't show multiple messageboxes since generate_single_list already shows them
            # Just show final confirmation
            self.root.after(100, lambda: messagebox.showinfo("Success", 
                "All lists generated successfully!\n\nBar Manipulation tab has been updated with all three lists."))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating all lists: {str(e)}")
    
    def use_generated_lists(self):
        """Transfer generated lists to Bar Manipulation tab"""
        try:
            if not all(hasattr(self, attr) for attr in ['generated_pitch_list', 'generated_duration_list', 'generated_velocity_list']):
                messagebox.showwarning("Warning", "Please generate all three lists first!")
                return
            
            # Convert lists to comma-separated strings
            pitch_str = ", ".join(str(p) for p in self.generated_pitch_list)
            duration_str = ", ".join(str(d) for d in self.generated_duration_list)
            velocity_str = ", ".join(str(v) for v in self.generated_velocity_list)
            
            # Update the Bar Manipulation tab input fields
            self.pitch_list_var.set(pitch_str)
            self.duration_list_var.set(duration_str)
            self.velocity_list_var.set(velocity_str)
            
            # Switch to Bar Manipulation tab
            self.notebook.select(1)  # Index 1 is Bar Manipulation tab
            
            messagebox.showinfo("Success", "Generated lists transferred to Bar Manipulation tab!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error using generated lists: {str(e)}")
    
    def create_bar(self):
        """Create a Bar object"""
        try:
            # Check if any parameter has GEB enabled
            pitch_geb = self.pitch_geb_var.get() if hasattr(self, 'pitch_geb_var') else False
            duration_geb = self.duration_geb_var.get() if hasattr(self, 'duration_geb_var') else False
            velocity_geb = self.velocity_geb_var.get() if hasattr(self, 'velocity_geb_var') else False
            
            # Block bar creation only if ALL parameters are GEB
            all_geb = pitch_geb and duration_geb and velocity_geb
            
            if all_geb:
                messagebox.showwarning("All Parameters GEB", 
                    "Cannot create bar manually because all parameters (Pitch, Duration, Velocity) have Generate Every Bar (GEB) enabled.\n\n" +
                    "Please disable GEB for at least one parameter in the List Generator tab, or create a Song instead.")
                return
            
            # Parse lists - for GEB parameters, generate them on the fly
            if pitch_geb:
                # Generate pitch list from grammar
                pitch_grammar = self.pitch_grammar_text.get('1.0', 'end-1c')
                pitch_min_length = int(self.pitch_min_length_var.get())
                pitch_generator = sk3.ListGenerator(pitch_grammar, pitch_min_length, "pitch")
                pitch_list = pitch_generator.generate_list()
            else:
                pitch_list = [int(x.strip()) for x in self.pitch_list_var.get().split(',')]
            
            if duration_geb:
                # Generate duration list from grammar
                duration_grammar = self.duration_grammar_text.get('1.0', 'end-1c')
                duration_min_length = int(self.duration_min_length_var.get())
                duration_generator = sk3.ListGenerator(duration_grammar, duration_min_length, "duration")
                duration_list = duration_generator.generate_list()
            else:
                duration_list = [float(x.strip()) for x in self.duration_list_var.get().split(',')]
            
            if velocity_geb:
                # Generate velocity list from grammar
                velocity_grammar = self.velocity_grammar_text.get('1.0', 'end-1c')
                velocity_min_length = int(self.velocity_min_length_var.get())
                velocity_generator = sk3.ListGenerator(velocity_grammar, velocity_min_length, "velocity")
                velocity_list = velocity_generator.generate_list()
            else:
                velocity_list = [int(x.strip()) for x in self.velocity_list_var.get().split(',')]
            
            # Get parameters
            onset = float(self.onset_var.get())
            ioi = float(self.ioi_var.get())
            
            # Create Bar
            self.current_bar = sk3.Bar(onset, ioi, pitch_list, duration_list, velocity_list)
            self.current_bar.make_note_list()
            
            # Display bar
            self.display_bar()
            
            # Update status
            self.object_status_label.config(text=f"Bar loaded: {len(pitch_list)} notes", foreground='blue')
            self.update_status(f"Bar created with {len(pitch_list)} notes")
            
            messagebox.showinfo("Success", "Bar created successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error creating bar: {str(e)}")
    
    def display_bar(self):
        """Display the current bar's note list"""
        if self.current_bar is None:
            self.bar_display.delete('1.0', 'end')
            self.bar_display.insert('1.0', "No bar created yet.")
            return
        
        # Check GEB status
        pitch_geb = self.pitch_geb_var.get() if hasattr(self, 'pitch_geb_var') else False
        duration_geb = self.duration_geb_var.get() if hasattr(self, 'duration_geb_var') else False
        velocity_geb = self.velocity_geb_var.get() if hasattr(self, 'velocity_geb_var') else False
        
        self.bar_display.delete('1.0', 'end')
        self.bar_display.insert('end', f"Bar Information:\n")
        self.bar_display.insert('end', f"Onset: {self.current_bar.bar_onset}\n")
        self.bar_display.insert('end', f"IOI: {self.current_bar.ioi}\n")
        self.bar_display.insert('end', f"Number of notes: {len(self.current_bar.note_list)}\n\n")
        
        self.bar_display.insert('end', "Notes:\n")
        self.bar_display.insert('end', f"{'Index':<8}{'Pitch':<10}{'Onset':<15}{'Duration':<15}{'Velocity':<10}\n")
        self.bar_display.insert('end', "-" * 60 + "\n")
        
        for i, note in enumerate(self.current_bar.note_list):
            # Show "GEB" for parameters that have GEB enabled
            pitch_str = "GEB" if pitch_geb else str(note.pitch)
            duration_str = "GEB" if duration_geb else f"{note.duration:.2f}"
            velocity_str = "GEB" if velocity_geb else str(note.velocity)
            
            self.bar_display.insert('end', 
                f"{i:<8}{pitch_str:<10}{note.onset:<15.2f}{duration_str:<15}{velocity_str:<10}\n")
    
    def update_song_from_bar(self):
        """Update the current song with the modified bar and refresh input lists"""
        if self.current_bar is not None:
            # Extract current values from the bar's note list
            pitch_list = [note.pitch for note in self.current_bar.note_list]
            duration_list = [note.duration for note in self.current_bar.note_list]
            velocity_list = [note.velocity for note in self.current_bar.note_list]
            
            # Update the bar's own lists to stay synchronized
            self.current_bar.pitch_list = pitch_list
            self.current_bar.duration_list = duration_list
            self.current_bar.velocity_list = velocity_list
            
            # Update the input fields
            self.pitch_list_var.set(','.join(map(str, pitch_list)))
            self.duration_list_var.set(','.join(str(d) for d in duration_list))
            self.velocity_list_var.set(','.join(map(str, velocity_list)))
            
            # Update the song if it exists
            if self.current_song is not None:
                self.current_song.bar_list[0] = self.current_bar
                # Update piano roll if it's visible
                if hasattr(self, 'piano_canvas'):
                    self.update_piano_roll()
    
    def check_geb_for_operation(self, operation_type):
        """Check if GEB is enabled for parameters affected by this operation.
        Returns True if operation can proceed, False if blocked by GEB.
        Operations are only blocked if they would affect GEB parameters."""
        pitch_geb = self.pitch_geb_var.get() if hasattr(self, 'pitch_geb_var') else False
        duration_geb = self.duration_geb_var.get() if hasattr(self, 'duration_geb_var') else False
        velocity_geb = self.velocity_geb_var.get() if hasattr(self, 'velocity_geb_var') else False
        
        # Map operations to the parameters they affect
        operation_affects = {
            "transpose": ["pitch"],
            "random_pitch": ["pitch"],
            "set_duration": ["duration"],
            "random_duration": ["duration"],
            "random_velocity": ["velocity"],
            "reverse": ["pitch", "duration", "velocity"],  # reverse affects all
            "random_onset": []  # onset has no GEB
        }
        
        affected_params = operation_affects.get(operation_type, [])
        blocked = []
        
        for param in affected_params:
            if param == "pitch" and pitch_geb:
                blocked.append("Pitch (GEB)")
            elif param == "duration" and duration_geb:
                blocked.append("Duration (GEB)")
            elif param == "velocity" and velocity_geb:
                blocked.append("Velocity (GEB)")
        
        if blocked:
            messagebox.showwarning("GEB Active",
                f"This operation affects the following GEB-enabled parameters:\n\n" +
                ", ".join(blocked) + "\n\n" +
                "The operation cannot be performed on GEB parameters.\n" +
                "Disable GEB for these parameters to use this operation.")
            return False
        return True
    
    def transpose_bar(self):
        """Transpose the current bar"""
        if self.current_bar is None:
            messagebox.showwarning("Warning", "Please create a bar first!")
            return
        
        if not self.check_geb_for_operation("transpose"):
            return
        
        try:
            semitones = int(self.transpose_var.get())
            self.current_bar.transpose_note_list(semitones)
            self.update_song_from_bar()  # Update song if it exists
            self.display_bar()
            messagebox.showinfo("Success", f"Bar transposed by {semitones} semitones!")
        except ValueError:
            messagebox.showerror("Error", "Invalid semitone value!")
        except Exception as e:
            messagebox.showerror("Error", f"Error transposing bar: {str(e)}")
    
    def set_duration(self):
        """Set duration for all notes in the bar"""
        if self.current_bar is None:
            messagebox.showwarning("Warning", "Please create a bar first!")
            return
        
        if not self.check_geb_for_operation("set_duration"):
            return
        
        try:
            duration = float(self.set_duration_var.get())
            self.current_bar.set_note_list_durations(duration)
            self.update_song_from_bar()  # Update song if it exists
            self.display_bar()
            messagebox.showinfo("Success", f"Duration set to {duration} for all notes!")
        except ValueError:
            messagebox.showerror("Error", "Invalid duration value!")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting duration: {str(e)}")
    
    def reverse_notes(self):
        """Reverse the note list"""
        if self.current_bar is None:
            messagebox.showwarning("Warning", "Please create a bar first!")
            return
        
        if not self.check_geb_for_operation("reverse"):
            return
        
        try:
            self.current_bar.reverse_note_list()
            self.update_song_from_bar()  # Update song if it exists
            self.display_bar()
            messagebox.showinfo("Success", "Note list reversed!")
        except Exception as e:
            messagebox.showerror("Error", f"Error reversing notes: {str(e)}")
    
    def random_pitches(self):
        """Apply random variations to pitches"""
        if self.current_bar is None:
            messagebox.showwarning("Warning", "Please create a bar first!")
            return
        
        if not self.check_geb_for_operation("random_pitch"):
            return
        
        try:
            self.current_bar.random_pitch()
            self.update_song_from_bar()  # Update song if it exists
            self.display_bar()
            messagebox.showinfo("Success", "Random pitch variations applied!")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying random pitches: {str(e)}")
    
    def random_durations(self):
        """Apply random variations to durations"""
        if self.current_bar is None:
            messagebox.showwarning("Warning", "Please create a bar first!")
            return
        
        if not self.check_geb_for_operation("random_duration"):
            return
        
        try:
            self.current_bar.random_duration()
            self.update_song_from_bar()  # Update song if it exists
            self.display_bar()
            messagebox.showinfo("Success", "Random duration variations applied!")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying random durations: {str(e)}")
    
    def random_velocities(self):
        """Apply random variations to velocities"""
        if self.current_bar is None:
            messagebox.showwarning("Warning", "Please create a bar first!")
            return
        
        if not self.check_geb_for_operation("random_velocity"):
            return
        
        try:
            self.current_bar.random_velocity()
            self.update_song_from_bar()  # Update song if it exists
            self.display_bar()
            messagebox.showinfo("Success", "Random velocity variations applied!")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying random velocities: {str(e)}")
    
    def random_onsets(self):
        """Apply random variations to onsets"""
        if self.current_bar is None:
            messagebox.showwarning("Warning", "Please create a bar first!")
            return
        
        if not self.check_geb_for_operation("random_onset"):
            return
        
        try:
            self.current_bar.random_onset()
            self.update_song_from_bar()  # Update song if it exists
            self.display_bar()
            messagebox.showinfo("Success", "Random onset variations applied!")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying random onsets: {str(e)}")
    
    def export_bar_to_midi(self):
        """Export the current bar to a MIDI file"""
        if self.current_bar is None:
            messagebox.showwarning("Warning", "Please create a bar first!")
            return
        
        try:
            # Ask user for file location
            filename = filedialog.asksaveasfilename(
                defaultextension=".mid",
                filetypes=[("MIDI files", "*.mid"), ("All files", "*.*")],
                title="Export Bar to MIDI"
            )
            
            if not filename:  # User cancelled
                return
            
            # Create a temporary song with just this bar
            temp_song = sk3.Song(name="TempBar", num_bars=1)
            temp_song.bar_list = [self.current_bar]
            temp_song.make_midi_file(filename)
            
            # Validate the exported file
            is_valid = self.validate_midi_file(filename)
            
            self.update_status(f"Bar exported to {os.path.basename(filename)}")
            
            if is_valid:
                messagebox.showinfo("Success", f"Bar exported to {filename}\nMIDI validation: PASSED ✓")
            else:
                messagebox.showwarning("Warning", f"Bar exported to {filename}\nMIDI validation: FAILED ✗\nCheck validation details in Song Modulation tab.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting bar: {str(e)}")
    
    def validate_current_bar(self):
        """Validate the current bar by exporting it to a temporary file"""
        if self.current_bar is None:
            messagebox.showwarning("Warning", "Please create a bar first!")
            return
        
        try:
            # Create a temporary MIDI file
            with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as tmp_file:
                tmp_filename = tmp_file.name
            
            # Create temporary song and export
            temp_song = sk3.Song(name="TempBar", num_bars=1)
            temp_song.bar_list = [self.current_bar]
            temp_song.make_midi_file(tmp_filename)
            
            # Validate the file
            is_valid = self.validate_midi_file(tmp_filename)
            
            # Clean up temp file
            try:
                os.unlink(tmp_filename)
            except:
                pass
            
            # Show result
            if is_valid:
                messagebox.showinfo("Validation Result", "Bar MIDI data is VALID ✓")
            else:
                messagebox.showwarning("Validation Result", "Bar MIDI data is INVALID ✗\nCheck validation details in Song Modulation tab.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error validating bar: {str(e)}")
    
    def create_song_modulation_tab(self):
        """Create the Song Modulation tab for sine modulation functions"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Song Modulation")
        
        # MIDI Validation Status Bar at the top
        status_bar = tk.Frame(tab, bg='#f0f0f0', relief='ridge', borderwidth=2)
        status_bar.pack(fill='x', padx=10, pady=5)
        
        status_inner = tk.Frame(status_bar, bg='#f0f0f0')
        status_inner.pack(fill='x', padx=10, pady=8)
        
        tk.Label(status_inner, text="MIDI Validation:", bg='#f0f0f0', 
                 font=('Arial', 11, 'bold')).pack(side='left', padx=5)
        
        # Large graphic indicator
        self.validation_indicator_large = tk.Canvas(status_inner, width=50, height=50, 
                                                     bg='#f0f0f0', highlightthickness=3, 
                                                     highlightbackground='#666666')
        self.validation_indicator_large.pack(side='left', padx=10)
        
        # Draw initial gray circle (not validated)
        self.validation_circle_large = self.validation_indicator_large.create_oval(
            5, 5, 45, 45, fill='#999999', outline='#666666', width=3
        )
        
        # Status text
        self.validation_status_label_large = tk.Label(status_inner, text="Not Validated", 
                                                       bg='#f0f0f0', foreground='#666666', 
                                                       font=('Arial', 14, 'bold'))
        self.validation_status_label_large.pack(side='left', padx=10)
        
        # Song creation section
        creation_frame = ttk.LabelFrame(tab, text="Create Song", padding=10)
        creation_frame.pack(fill='x', padx=10, pady=5)
        
        # Song parameters
        params_frame = ttk.Frame(creation_frame)
        params_frame.pack(fill='x', pady=2)
        
        ttk.Label(params_frame, text="Song Name:").pack(side='left', padx=5)
        self.song_name_var = tk.StringVar(value="MySong")
        ttk.Entry(params_frame, textvariable=self.song_name_var, width=20).pack(side='left', padx=5)
        
        ttk.Label(params_frame, text="Number of Bars:").pack(side='left', padx=5)
        self.num_bars_var = tk.StringVar(value="4")
        ttk.Entry(params_frame, textvariable=self.num_bars_var, width=10).pack(side='left', padx=5)
        
        ttk.Label(params_frame, text="IOI:").pack(side='left', padx=5)
        self.song_ioi_var = tk.StringVar(value="0.75")
        ttk.Entry(params_frame, textvariable=self.song_ioi_var, width=10).pack(side='left', padx=5)
        
        # List length behavior selector
        list_behavior_frame = ttk.Frame(creation_frame)
        list_behavior_frame.pack(fill='x', pady=5)
        ttk.Label(list_behavior_frame, text="Uneven list lengths:").pack(side='left', padx=5)
        self.list_length_behavior_var = tk.StringVar(value="truncate")
        ttk.Radiobutton(list_behavior_frame, text="Truncate to shortest", 
                       variable=self.list_length_behavior_var, value="truncate").pack(side='left', padx=5)
        ttk.Radiobutton(list_behavior_frame, text="Loop to longest", 
                       variable=self.list_length_behavior_var, value="loop_longest").pack(side='left', padx=5)
        ttk.Radiobutton(list_behavior_frame, text="Loop to matching bar", 
                       variable=self.list_length_behavior_var, value="loop_bar").pack(side='left', padx=5)
        
        ttk.Button(creation_frame, text="Create Song", 
                   command=self.create_song).pack(pady=5)
        
        # Modulation section - modulate_*_with_sin
        mod_sin_frame = ttk.LabelFrame(tab, text="Sine Modulation (Continuous Phase)", padding=10)
        mod_sin_frame.pack(fill='x', padx=10, pady=5)
        
        # Pitch modulation with sin
        pitch_sin_frame = ttk.Frame(mod_sin_frame)
        pitch_sin_frame.pack(fill='x', pady=2)
        ttk.Label(pitch_sin_frame, text="Modulate Pitch:").pack(side='left', padx=5)
        ttk.Label(pitch_sin_frame, text="Freq:").pack(side='left', padx=5)
        self.pitch_sin_freq_var = tk.StringVar(value="1.0")
        ttk.Entry(pitch_sin_frame, textvariable=self.pitch_sin_freq_var, width=10).pack(side='left', padx=5)
        ttk.Label(pitch_sin_frame, text="Amp:").pack(side='left', padx=5)
        self.pitch_sin_amp_var = tk.StringVar(value="5")
        ttk.Entry(pitch_sin_frame, textvariable=self.pitch_sin_amp_var, width=10).pack(side='left', padx=5)
        ttk.Button(pitch_sin_frame, text="Apply", 
                   command=self.modulate_pitch_sin).pack(side='left', padx=5)
        
        # Duration modulation with sin
        duration_sin_frame = ttk.Frame(mod_sin_frame)
        duration_sin_frame.pack(fill='x', pady=2)
        ttk.Label(duration_sin_frame, text="Modulate Duration:").pack(side='left', padx=5)
        ttk.Label(duration_sin_frame, text="Freq:").pack(side='left', padx=5)
        self.duration_sin_freq_var = tk.StringVar(value="1.0")
        ttk.Entry(duration_sin_frame, textvariable=self.duration_sin_freq_var, width=10).pack(side='left', padx=5)
        ttk.Label(duration_sin_frame, text="Amp:").pack(side='left', padx=5)
        self.duration_sin_amp_var = tk.StringVar(value="0.3")
        ttk.Entry(duration_sin_frame, textvariable=self.duration_sin_amp_var, width=10).pack(side='left', padx=5)
        ttk.Button(duration_sin_frame, text="Apply", 
                   command=self.modulate_duration_sin).pack(side='left', padx=5)
        
        # Velocity modulation with sin
        velocity_sin_frame = ttk.Frame(mod_sin_frame)
        velocity_sin_frame.pack(fill='x', pady=2)
        ttk.Label(velocity_sin_frame, text="Modulate Velocity:").pack(side='left', padx=5)
        ttk.Label(velocity_sin_frame, text="Freq:").pack(side='left', padx=5)
        self.velocity_sin_freq_var = tk.StringVar(value="1.0")
        ttk.Entry(velocity_sin_frame, textvariable=self.velocity_sin_freq_var, width=10).pack(side='left', padx=5)
        ttk.Label(velocity_sin_frame, text="Amp:").pack(side='left', padx=5)
        self.velocity_sin_amp_var = tk.StringVar(value="20")
        ttk.Entry(velocity_sin_frame, textvariable=self.velocity_sin_amp_var, width=10).pack(side='left', padx=5)
        ttk.Button(velocity_sin_frame, text="Apply", 
                   command=self.modulate_velocity_sin).pack(side='left', padx=5)
        
        # Onset modulation with sin
        onset_sin_frame = ttk.Frame(mod_sin_frame)
        onset_sin_frame.pack(fill='x', pady=2)
        ttk.Label(onset_sin_frame, text="Modulate Onset:").pack(side='left', padx=5)
        ttk.Label(onset_sin_frame, text="Freq:").pack(side='left', padx=5)
        self.onset_sin_freq_var = tk.StringVar(value="1.0")
        ttk.Entry(onset_sin_frame, textvariable=self.onset_sin_freq_var, width=10).pack(side='left', padx=5)
        ttk.Label(onset_sin_frame, text="Amp:").pack(side='left', padx=5)
        self.onset_sin_amp_var = tk.StringVar(value="0.1")
        ttk.Entry(onset_sin_frame, textvariable=self.onset_sin_amp_var, width=10).pack(side='left', padx=5)
        ttk.Button(onset_sin_frame, text="Apply", 
                   command=self.modulate_onset_sin).pack(side='left', padx=5)
        
        # Modulation section - modulate_*_with_sin_phase_by_bar
        mod_bar_frame = ttk.LabelFrame(tab, text="Sine Modulation (Phase Reset Per Bar)", padding=10)
        mod_bar_frame.pack(fill='x', padx=10, pady=5)
        
        # Pitch modulation with sin phase by bar
        pitch_bar_frame = ttk.Frame(mod_bar_frame)
        pitch_bar_frame.pack(fill='x', pady=2)
        ttk.Label(pitch_bar_frame, text="Modulate Pitch:").pack(side='left', padx=5)
        ttk.Label(pitch_bar_frame, text="Freq:").pack(side='left', padx=5)
        self.pitch_bar_freq_var = tk.StringVar(value="1.0")
        ttk.Entry(pitch_bar_frame, textvariable=self.pitch_bar_freq_var, width=10).pack(side='left', padx=5)
        ttk.Label(pitch_bar_frame, text="Amp:").pack(side='left', padx=5)
        self.pitch_bar_amp_var = tk.StringVar(value="5")
        ttk.Entry(pitch_bar_frame, textvariable=self.pitch_bar_amp_var, width=10).pack(side='left', padx=5)
        ttk.Button(pitch_bar_frame, text="Apply", 
                   command=self.modulate_pitch_bar).pack(side='left', padx=5)
        
        # Duration modulation with sin phase by bar
        duration_bar_frame = ttk.Frame(mod_bar_frame)
        duration_bar_frame.pack(fill='x', pady=2)
        ttk.Label(duration_bar_frame, text="Modulate Duration:").pack(side='left', padx=5)
        ttk.Label(duration_bar_frame, text="Freq:").pack(side='left', padx=5)
        self.duration_bar_freq_var = tk.StringVar(value="1.0")
        ttk.Entry(duration_bar_frame, textvariable=self.duration_bar_freq_var, width=10).pack(side='left', padx=5)
        ttk.Label(duration_bar_frame, text="Amp:").pack(side='left', padx=5)
        self.duration_bar_amp_var = tk.StringVar(value="0.3")
        ttk.Entry(duration_bar_frame, textvariable=self.duration_bar_amp_var, width=10).pack(side='left', padx=5)
        ttk.Button(duration_bar_frame, text="Apply", 
                   command=self.modulate_duration_bar).pack(side='left', padx=5)
        
        # Velocity modulation with sin phase by bar
        velocity_bar_frame = ttk.Frame(mod_bar_frame)
        velocity_bar_frame.pack(fill='x', pady=2)
        ttk.Label(velocity_bar_frame, text="Modulate Velocity:").pack(side='left', padx=5)
        ttk.Label(velocity_bar_frame, text="Freq:").pack(side='left', padx=5)
        self.velocity_bar_freq_var = tk.StringVar(value="1.0")
        ttk.Entry(velocity_bar_frame, textvariable=self.velocity_bar_freq_var, width=10).pack(side='left', padx=5)
        ttk.Label(velocity_bar_frame, text="Amp:").pack(side='left', padx=5)
        self.velocity_bar_amp_var = tk.StringVar(value="20")
        ttk.Entry(velocity_bar_frame, textvariable=self.velocity_bar_amp_var, width=10).pack(side='left', padx=5)
        ttk.Button(velocity_bar_frame, text="Apply", 
                   command=self.modulate_velocity_bar).pack(side='left', padx=5)
        
        # Onset modulation with sin phase by bar
        onset_bar_frame = ttk.Frame(mod_bar_frame)
        onset_bar_frame.pack(fill='x', pady=2)
        ttk.Label(onset_bar_frame, text="Modulate Onset:").pack(side='left', padx=5)
        ttk.Label(onset_bar_frame, text="Freq:").pack(side='left', padx=5)
        self.onset_bar_freq_var = tk.StringVar(value="1.0")
        ttk.Entry(onset_bar_frame, textvariable=self.onset_bar_freq_var, width=10).pack(side='left', padx=5)
        ttk.Label(onset_bar_frame, text="Amp:").pack(side='left', padx=5)
        self.onset_bar_amp_var = tk.StringVar(value="0.1")
        ttk.Entry(onset_bar_frame, textvariable=self.onset_bar_amp_var, width=10).pack(side='left', padx=5)
        ttk.Button(onset_bar_frame, text="Apply", 
                   command=self.modulate_onset_bar).pack(side='left', padx=5)
        
        # Song display section
        display_frame = ttk.LabelFrame(tab, text="Current Song", padding=10)
        display_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.song_display = scrolledtext.ScrolledText(display_frame, height=15, width=80)
        self.song_display.pack(fill='both', expand=True)
        
        # MIDI Export and Validation section
        export_frame = ttk.LabelFrame(tab, text="MIDI Export & Validation", padding=10)
        export_frame.pack(fill='x', padx=10, pady=5)
        
        button_frame = ttk.Frame(export_frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="Export to MIDI", 
                   command=self.export_song_to_midi).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Validate MIDI", 
                   command=self.validate_current_song).pack(side='left', padx=5)
        
        # Validation status indicator
        status_frame = ttk.Frame(export_frame)
        status_frame.pack(fill='x', pady=5)
        
        ttk.Label(status_frame, text="MIDI Validation Status:").pack(side='left', padx=5)
        
        # Create a canvas for the graphic indicator
        self.validation_indicator = tk.Canvas(status_frame, width=30, height=30, 
                                               bg='white', highlightthickness=2, 
                                               highlightbackground='gray')
        self.validation_indicator.pack(side='left', padx=5)
        
        # Draw initial gray circle (not validated)
        self.validation_circle = self.validation_indicator.create_oval(
            5, 5, 25, 25, fill='gray', outline='darkgray', width=2
        )
        
        self.validation_status_label = ttk.Label(status_frame, text="Not validated", 
                                                  foreground='gray', font=('Arial', 10, 'bold'))
        self.validation_status_label.pack(side='left', padx=5)
        
        # Validation details
        validation_detail_frame = ttk.LabelFrame(tab, text="Validation Details", padding=10)
        validation_detail_frame.pack(fill='x', padx=10, pady=5)
        
        self.validation_detail_text = scrolledtext.ScrolledText(validation_detail_frame, height=5, width=80)
        self.validation_detail_text.pack(fill='both', expand=True)
    
    def create_song(self):
        """Create a Song object"""
        try:
            # Check for GEB status
            pitch_geb = self.pitch_geb_var.get() if hasattr(self, 'pitch_geb_var') else False
            duration_geb = self.duration_geb_var.get() if hasattr(self, 'duration_geb_var') else False
            velocity_geb = self.velocity_geb_var.get() if hasattr(self, 'velocity_geb_var') else False
            
            # Get song parameters
            name = self.song_name_var.get()
            num_bars = int(self.num_bars_var.get())
            ioi = float(self.song_ioi_var.get())
            
            # Determine if we need to use generate_every_bar
            generate_every_bar = pitch_geb or duration_geb or velocity_geb
            
            # Create generators for GEB parameters
            pitch_generator = None
            duration_generator = None
            velocity_generator = None
            
            if pitch_geb:
                # Create pitch generator from grammar
                pitch_grammar = self.pitch_grammar_text.get('1.0', 'end-1c')
                pitch_min_length = int(self.pitch_min_length_var.get())
                pitch_generator = sk3.ListGenerator(pitch_grammar, pitch_min_length, "pitch")
            
            if duration_geb:
                # Create duration generator from grammar
                duration_grammar = self.duration_grammar_text.get('1.0', 'end-1c')
                duration_min_length = int(self.duration_min_length_var.get())
                duration_generator = sk3.ListGenerator(duration_grammar, duration_min_length, "duration")
            
            if velocity_geb:
                # Create velocity generator from grammar
                velocity_grammar = self.velocity_grammar_text.get('1.0', 'end-1c')
                velocity_min_length = int(self.velocity_min_length_var.get())
                velocity_generator = sk3.ListGenerator(velocity_grammar, velocity_min_length, "velocity")
            
            # Get list length behavior
            list_length_behavior = self.list_length_behavior_var.get()
            
            # Create Song with or without generators
            self.current_song = sk3.Song(
                name=name, 
                num_bars=num_bars, 
                ioi=ioi,
                pitch_generator=pitch_generator,
                duration_generator=duration_generator,
                velocity_generator=velocity_generator,
                generate_every_bar=generate_every_bar,
                list_length_behavior=list_length_behavior
            )
            
            # For non-GEB parameters, parse and set the lists BEFORE making bars
            # These will be used by all bars when GEB is not enabled for that parameter
            if not pitch_geb:
                pitch_list = [int(x.strip()) for x in self.pitch_list_var.get().split(',')]
                self.current_song.pitch_list = pitch_list
            
            if not duration_geb:
                duration_list = [float(x.strip()) for x in self.duration_list_var.get().split(',')]
                self.current_song.duration_list = duration_list
            
            if not velocity_geb:
                velocity_list = [int(x.strip()) for x in self.velocity_list_var.get().split(',')]
                self.current_song.velocity_list = velocity_list
            
            # Only generate parameter lists if we're using GEB or if lists aren't already set
            # When generate_every_bar=False and lists are manually set, don't call generate_parameter_lists
            # because it would override our manually set lists with defaults
            if generate_every_bar:
                # GEB is enabled - lists will be generated per bar in make_bar_list()
                pass
            elif pitch_generator or duration_generator or velocity_generator:
                # We have generators but not using GEB - generate once
                self.current_song.generate_parameter_lists()
            # else: lists are already set manually above, don't generate
            
            # Create bars - if generate_every_bar is True, 
            # make_bar_list() will call generate_parameter_lists() for each bar
            self.current_song.make_bar_list()
            
            # Debug: Print actual number of bars created
            print(f"DEBUG: Created {len(self.current_song.bar_list)} bars (expected {num_bars})")
            print(f"DEBUG: List lengths - pitch: {len(self.current_song.pitch_list)}, duration: {len(self.current_song.duration_list)}, velocity: {len(self.current_song.velocity_list)}")
            if self.current_song.bar_list:
                print(f"DEBUG: First bar has {len(self.current_song.bar_list[0].note_list)} notes")
                print(f"DEBUG: Last bar onset: {self.current_song.bar_list[-1].bar_onset}")
            
            # Display song
            self.display_song()
            
            # Update piano roll if it exists
            if self.piano_roll:
                self.piano_roll.set_song(self.current_song)
            
            # Automatically validate the song
            try:
                with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as tmp_file:
                    tmp_filename = tmp_file.name
                self.current_song.make_midi_file(tmp_filename)
                is_valid = self.validate_midi_file(tmp_filename)
                try:
                    os.unlink(tmp_filename)
                except:
                    pass
            except:
                pass  # Validation is optional
            
            # Update status
            total_notes = sum(len(bar.note_list) for bar in self.current_song.bar_list)
            geb_status = " (GEB)" if generate_every_bar else ""
            self.object_status_label.config(text=f"Song: {name} ({num_bars} bars, {total_notes} notes){geb_status}", 
                                            foreground='green')
            self.update_status(f"Song '{name}' created with {num_bars} bars{geb_status}")
            
            messagebox.showinfo("Success", f"Song '{name}' created with {num_bars} bars!{geb_status}")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error creating song: {str(e)}")
    
    def display_song(self):
        """Display the current song's information"""
        if self.current_song is None:
            self.song_display.delete('1.0', 'end')
            self.song_display.insert('1.0', "No song created yet.")
            return
        
        self.song_display.delete('1.0', 'end')
        self.song_display.insert('1.0', f"Song Information:\n")
        self.song_display.insert('end', f"Name: {self.current_song.name}\n")
        self.song_display.insert('end', f"Number of Bars: {len(self.current_song.bar_list)}\n")
        self.song_display.insert('end', f"IOI: {self.current_song.ioi}\n\n")
        
        total_notes = sum(len(bar.note_list) for bar in self.current_song.bar_list)
        self.song_display.insert('end', f"Total Notes: {total_notes}\n\n")
        
        self.song_display.insert('end', "Bar Details:\n")
        for i, bar in enumerate(self.current_song.bar_list):
            self.song_display.insert('end', f"Bar {i+1}: {len(bar.note_list)} notes, onset={bar.bar_onset:.2f}\n")
    
    # Sine modulation methods (continuous phase)
    def modulate_pitch_sin(self):
        """Apply sine modulation to pitch"""
        if self.current_song is None:
            messagebox.showwarning("Warning", "Please create a song first!")
            return
        
        try:
            freq = float(self.pitch_sin_freq_var.get())
            amp = float(self.pitch_sin_amp_var.get())
            self.current_song.modulate_pitch_with_sin(freq, amp)
            self.display_song()
            if self.piano_roll:
                self.piano_roll.update_display()
            messagebox.showinfo("Success", f"Pitch modulated with sine (freq={freq}, amp={amp})!")
        except ValueError:
            messagebox.showerror("Error", "Invalid frequency or amplitude value!")
        except Exception as e:
            messagebox.showerror("Error", f"Error modulating pitch: {str(e)}")
    
    def modulate_duration_sin(self):
        """Apply sine modulation to duration"""
        if self.current_song is None:
            messagebox.showwarning("Warning", "Please create a song first!")
            return
        
        try:
            freq = float(self.duration_sin_freq_var.get())
            amp = float(self.duration_sin_amp_var.get())
            self.current_song.modulate_duration_with_sin(freq, amp)
            self.display_song()
            if self.piano_roll:
                self.piano_roll.update_display()
            messagebox.showinfo("Success", f"Duration modulated with sine (freq={freq}, amp={amp})!")
        except ValueError:
            messagebox.showerror("Error", "Invalid frequency or amplitude value!")
        except Exception as e:
            messagebox.showerror("Error", f"Error modulating duration: {str(e)}")
    
    def modulate_velocity_sin(self):
        """Apply sine modulation to velocity"""
        if self.current_song is None:
            messagebox.showwarning("Warning", "Please create a song first!")
            return
        
        try:
            freq = float(self.velocity_sin_freq_var.get())
            amp = float(self.velocity_sin_amp_var.get())
            self.current_song.modulate_velocity_with_sin(freq, amp)
            self.display_song()
            if self.piano_roll:
                self.piano_roll.update_display()
            messagebox.showinfo("Success", f"Velocity modulated with sine (freq={freq}, amp={amp})!")
        except ValueError:
            messagebox.showerror("Error", "Invalid frequency or amplitude value!")
        except Exception as e:
            messagebox.showerror("Error", f"Error modulating velocity: {str(e)}")
    
    def modulate_onset_sin(self):
        """Apply sine modulation to onset"""
        if self.current_song is None:
            messagebox.showwarning("Warning", "Please create a song first!")
            return
        
        try:
            freq = float(self.onset_sin_freq_var.get())
            amp = float(self.onset_sin_amp_var.get())
            self.current_song.modulate_onset_with_sin(freq, amp)
            self.display_song()
            if self.piano_roll:
                self.piano_roll.update_display()
            messagebox.showinfo("Success", f"Onset modulated with sine (freq={freq}, amp={amp})!")
        except ValueError:
            messagebox.showerror("Error", "Invalid frequency or amplitude value!")
        except Exception as e:
            messagebox.showerror("Error", f"Error modulating onset: {str(e)}")
    
    # Sine modulation methods (phase reset per bar)
    def modulate_pitch_bar(self):
        """Apply sine modulation to pitch with phase reset per bar"""
        if self.current_song is None:
            messagebox.showwarning("Warning", "Please create a song first!")
            return
        
        try:
            freq = float(self.pitch_bar_freq_var.get())
            amp = float(self.pitch_bar_amp_var.get())
            self.current_song.modulate_pitch_with_sin_phase_by_bar(freq, amp)
            self.display_song()
            if self.piano_roll:
                self.piano_roll.update_display()
            messagebox.showinfo("Success", f"Pitch modulated with sine per bar (freq={freq}, amp={amp})!")
        except ValueError:
            messagebox.showerror("Error", "Invalid frequency or amplitude value!")
        except Exception as e:
            messagebox.showerror("Error", f"Error modulating pitch: {str(e)}")
    
    def modulate_duration_bar(self):
        """Apply sine modulation to duration with phase reset per bar"""
        if self.current_song is None:
            messagebox.showwarning("Warning", "Please create a song first!")
            return
        
        try:
            freq = float(self.duration_bar_freq_var.get())
            amp = float(self.duration_bar_amp_var.get())
            self.current_song.modulate_duration_with_sin_phase_by_bar(freq, amp)
            self.display_song()
            if self.piano_roll:
                self.piano_roll.update_display()
            messagebox.showinfo("Success", f"Duration modulated with sine per bar (freq={freq}, amp={amp})!")
        except ValueError:
            messagebox.showerror("Error", "Invalid frequency or amplitude value!")
        except Exception as e:
            messagebox.showerror("Error", f"Error modulating duration: {str(e)}")
    
    def modulate_velocity_bar(self):
        """Apply sine modulation to velocity with phase reset per bar"""
        if self.current_song is None:
            messagebox.showwarning("Warning", "Please create a song first!")
            return
        
        try:
            freq = float(self.velocity_bar_freq_var.get())
            amp = float(self.velocity_bar_amp_var.get())
            self.current_song.modulate_velocity_with_sin_phase_by_bar(freq, amp)
            self.display_song()
            if self.piano_roll:
                self.piano_roll.update_display()
            messagebox.showinfo("Success", f"Velocity modulated with sine per bar (freq={freq}, amp={amp})!")
        except ValueError:
            messagebox.showerror("Error", "Invalid frequency or amplitude value!")
        except Exception as e:
            messagebox.showerror("Error", f"Error modulating velocity: {str(e)}")
    
    def modulate_onset_bar(self):
        """Apply sine modulation to onset with phase reset per bar"""
        if self.current_song is None:
            messagebox.showwarning("Warning", "Please create a song first!")
            return
        
        try:
            freq = float(self.onset_bar_freq_var.get())
            amp = float(self.onset_bar_amp_var.get())
            self.current_song.modulate_onset_with_sin_phase_by_bar(freq, amp)
            self.display_song()
            if self.piano_roll:
                self.piano_roll.update_display()
            messagebox.showinfo("Success", f"Onset modulated with sine per bar (freq={freq}, amp={amp})!")
        except ValueError:
            messagebox.showerror("Error", "Invalid frequency or amplitude value!")
        except Exception as e:
            messagebox.showerror("Error", f"Error modulating onset: {str(e)}")
    
    def export_song_to_midi(self):
        """Export the current song to a MIDI file"""
        if self.current_song is None:
            messagebox.showwarning("Warning", "Please create a song first!")
            return
        
        try:
            # Ask user for file location
            filename = filedialog.asksaveasfilename(
                defaultextension=".mid",
                filetypes=[("MIDI files", "*.mid"), ("All files", "*.*")],
                title="Export Song to MIDI"
            )
            
            if not filename:  # User cancelled
                return
            
            # Export the song
            self.current_song.make_midi_file(filename)
            
            # Automatically validate the exported file
            self.validate_midi_file(filename)
            
            self.update_status(f"Song exported to {os.path.basename(filename)}")
            messagebox.showinfo("Success", f"Song exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting MIDI: {str(e)}")
    
    def validate_current_song(self):
        """Validate the current song by exporting it to a temporary file"""
        if self.current_song is None:
            messagebox.showwarning("Warning", "Please create a song first!")
            return
        
        try:
            # Create a temporary MIDI file
            with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as tmp_file:
                tmp_filename = tmp_file.name
            
            # Export song to temp file
            self.current_song.make_midi_file(tmp_filename)
            
            # Validate the file
            self.validate_midi_file(tmp_filename)
            
            # Clean up temp file
            try:
                os.unlink(tmp_filename)
            except:
                pass
                
        except Exception as e:
            messagebox.showerror("Error", f"Error validating song: {str(e)}")
    
    def validate_midi_file(self, filepath):
        """Validate a MIDI file and update the status indicator"""
        try:
            # Create parser
            parser = midi_parser.MIDIParser(filepath)
            
            # Parse and validate
            parser.parse()
            is_valid, errors = parser.validate()
            
            # Update status indicator
            if is_valid:
                # Green indicator for valid MIDI
                self.validation_indicator.itemconfig(self.validation_circle, 
                                                      fill='#00ff00', outline='#00aa00')
                self.validation_indicator.config(highlightbackground='#00aa00')
                self.validation_status_label.config(text="✓ VALID", foreground='green')
                
                # Update large indicator
                self.validation_indicator_large.itemconfig(self.validation_circle_large, 
                                                            fill='#00ff00', outline='#00aa00')
                self.validation_indicator_large.config(highlightbackground='#00aa00', bg='#e0ffe0')
                self.validation_status_label_large.config(text="✓ VALID", foreground='#008800', bg='#e0ffe0')
                
                self.validation_detail_text.delete('1.0', 'end')
                self.validation_detail_text.insert('1.0', "MIDI data is valid!\n\n")
                self.validation_detail_text.insert('end', f"Total note events: {len(parser.note_events)}\n")
                self.validation_detail_text.insert('end', "All note-on events have corresponding note-off events.\n")
                self.validation_detail_text.insert('end', "All timings are correct.")
            else:
                # Red indicator for invalid MIDI
                self.validation_indicator.itemconfig(self.validation_circle, 
                                                      fill='#ff0000', outline='#aa0000')
                self.validation_indicator.config(highlightbackground='#aa0000')
                self.validation_status_label.config(text="✗ INVALID", foreground='red')
                
                # Update large indicator
                self.validation_indicator_large.itemconfig(self.validation_circle_large, 
                                                            fill='#ff0000', outline='#aa0000')
                self.validation_indicator_large.config(highlightbackground='#aa0000', bg='#ffe0e0')
                self.validation_status_label_large.config(text="✗ INVALID", foreground='#aa0000', bg='#ffe0e0')
                
                self.validation_detail_text.delete('1.0', 'end')
                self.validation_detail_text.insert('1.0', f"Found {len(errors)} validation error(s):\n\n")
                
                for idx, error in enumerate(errors, 1):
                    self.validation_detail_text.insert('end', 
                        f"{idx}. [{error.error_type}] Note {error.note}, Channel {error.channel}\n")
                    self.validation_detail_text.insert('end', f"   {error.message}\n\n")
            
            return is_valid
            
        except Exception as e:
            # Orange indicator for error
            self.validation_indicator.itemconfig(self.validation_circle, 
                                                  fill='#ffaa00', outline='#aa6600')
            self.validation_indicator.config(highlightbackground='#aa6600')
            self.validation_status_label.config(text="✗ ERROR", foreground='orange')
            
            # Update large indicator
            self.validation_indicator_large.itemconfig(self.validation_circle_large, 
                                                        fill='#ffaa00', outline='#aa6600')
            self.validation_indicator_large.config(highlightbackground='#aa6600', bg='#fff0e0')
            self.validation_status_label_large.config(text="✗ ERROR", foreground='#aa6600', bg='#fff0e0')
            
            self.validation_detail_text.delete('1.0', 'end')
            self.validation_detail_text.insert('1.0', f"Error during validation:\n{str(e)}")
            return False
    
    def play_current_song(self):
        """Play the current song using SimpleSampler"""
        if self.current_song is None:
            messagebox.showwarning("Warning", "Please create a song first!\n\n"
                                 "Use the Bar Manipulation tab to create a bar,\n"
                                 "or use the List Generator to generate grammars.")
            return
        
        try:
            # Path to SimpleSampler
            sampler_path = os.path.join(os.path.dirname(__file__), 
                                       'simpleSampler', 'build', 'SimpleSampler')
            
            # Check if SimpleSampler exists
            if not os.path.isfile(sampler_path):
                messagebox.showerror("SimpleSampler Not Found", 
                                   f"SimpleSampler executable not found at:\n"
                                   f"{sampler_path}\n\n"
                                   f"Please build SimpleSampler:\n"
                                   f"cd simpleSampler/build\n"
                                   f"cmake ..\n"
                                   f"make")
                return
            
            # Create a temporary MIDI file
            temp_fd, temp_path = tempfile.mkstemp(suffix='.mid', prefix='sk3_play_')
            os.close(temp_fd)
            
            # Export song to temp MIDI file
            print(f"Creating temporary MIDI file: {temp_path}")
            self.current_song.make_midi_file(temp_path)
            print(f"MIDI file created, size: {os.path.getsize(temp_path)} bytes")
            
            # Build command string - MIDI file must come first!
            command = f'"{sampler_path}" "{temp_path}"'
            
            # Add soundfont if checkbox is checked and path is set
            if hasattr(self, 'use_soundfont_var') and self.use_soundfont_var.get():
                if hasattr(self, 'soundfont_path_var') and self.soundfont_path_var.get():
                    soundfont_path = self.soundfont_path_var.get()
                    if os.path.isfile(soundfont_path):
                        command = f'"{sampler_path}" "{temp_path}" -sf "{soundfont_path}"'
                        print(f"Using SoundFont: {soundfont_path}")
                    else:
                        print(f"Warning: SoundFont file not found: {soundfont_path}")
            
            print(f"Executing: {command}")
            
            # Execute SimpleSampler in background
            # Don't capture stdout/stderr to allow audio to work properly
            import subprocess
            process = subprocess.Popen(command, shell=True)
            
            # Store for cleanup
            self.temp_midi_path = temp_path
            self.sampler_process = process
            
            self.update_status(f"Playing MIDI file with SimpleSampler...")
            messagebox.showinfo("Playing", 
                              f"Playing song through SimpleSampler!\n\n"
                              f"Command: {os.path.basename(sampler_path)} {os.path.basename(temp_path)}")
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"ERROR playing MIDI:\n{error_details}")
            messagebox.showerror("Error", f"Error playing MIDI:\n\n{str(e)}\n\nCheck console for details.")
    
    def stop_playback(self):
        """Stop the currently playing MIDI"""
        try:
            if hasattr(self, 'sampler_process') and self.sampler_process:
                if self.sampler_process.poll() is None:  # Process is still running
                    self.sampler_process.terminate()
                    try:
                        self.sampler_process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        self.sampler_process.kill()
                    print("SimpleSampler process stopped")
                    self.update_status("Playback stopped")
                else:
                    self.update_status("Nothing is playing")
                
                # Clean up temp file if it exists
                if hasattr(self, 'temp_midi_path') and os.path.exists(self.temp_midi_path):
                    try:
                        os.unlink(self.temp_midi_path)
                        print(f"Cleaned up temp file: {self.temp_midi_path}")
                    except:
                        pass
            else:
                self.update_status("Nothing is playing")
        except Exception as e:
            messagebox.showerror("Error", f"Error stopping playback: {str(e)}")
    
    def show_sampler_instructions(self):
        """Show instructions for building SimpleSampler"""
        instructions = """SimpleSampler - Audio Playback Setup

SimpleSampler is a C++ MIDI player that uses sine wave synthesis.
To enable the Play MIDI button, you need to build it first.

Build Instructions:
-------------------

1. Open Terminal and navigate to the project directory:
   cd {project_dir}

2. Navigate to the SimpleSampler build directory:
   cd simpleSampler/build

3. Run CMake to generate build files:
   cmake ..

4. Build the executable:
   make

5. Verify the build:
   ls SimpleSampler

The Play MIDI button will appear automatically once SimpleSampler 
is built successfully.

Requirements:
-------------
- CMake (install with: brew install cmake)
- SFML (install with: brew install sfml)
- C++ compiler (Xcode Command Line Tools)

For more details, see: simpleSampler/README.md
""".format(project_dir=os.path.dirname(os.path.abspath(__file__)))
        
        messagebox.showinfo("SimpleSampler Build Instructions", instructions)
    
    def toggle_soundfont(self):
        """Handle soundfont checkbox toggle - open file browser when checked"""
        if self.use_soundfont_var.get():
            # Checkbox was just checked - open file browser
            soundfonts_dir = os.path.join(os.path.dirname(__file__), 'simpleSampler', 'soundfonts')
            # Create directory if it doesn't exist
            if not os.path.exists(soundfonts_dir):
                soundfonts_dir = os.path.join(os.path.dirname(__file__), 'simpleSampler', 'build', 'soundfonts')
            if not os.path.exists(soundfonts_dir):
                soundfonts_dir = os.path.dirname(__file__)
            
            filename = filedialog.askopenfilename(
                title="Select SoundFont File",
                filetypes=[("SoundFont Files", "*.sf2"), ("All Files", "*.*")],
                initialdir=soundfonts_dir
            )
            if filename:
                self.soundfont_path_var.set(filename)
                self.update_status(f"SoundFont selected: {os.path.basename(filename)}")
            else:
                # User cancelled - uncheck the checkbox
                self.use_soundfont_var.set(False)
        else:
            # Checkbox was unchecked - clear the soundfont path
            self.soundfont_path_var.set("")
            self.update_status("SoundFont disabled - using sine wave synthesis")
    
    def create_piano_roll_tab(self):
        """Create the Piano Roll Visualization tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Piano Roll")
        
        # Control frame at the top
        control_frame = ttk.LabelFrame(tab, text="Piano Roll Controls", padding=10)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Buttons for updating display
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="Show Current Song", 
                   command=self.show_song_in_piano_roll).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Show Current Bar", 
                   command=self.show_bar_in_piano_roll).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear Piano Roll", 
                   command=self.clear_piano_roll).pack(side='left', padx=5)
        
        # Separator
        ttk.Separator(button_frame, orient='vertical').pack(side='left', fill='y', padx=10, pady=5)
        
        # MIDI Export button
        ttk.Button(button_frame, text="💾 Save Song as MIDI", 
                   command=self.export_song_to_midi).pack(side='left', padx=5)
        
        # Play MIDI button - check if SimpleSampler exists
        sampler_path = os.path.join(os.path.dirname(__file__), 
                                   'simpleSampler', 'build', 'SimpleSampler')
        if os.path.isfile(sampler_path):
            ttk.Button(button_frame, text="▶️ Play MIDI", 
                       command=self.play_current_song).pack(side='left', padx=5)
            ttk.Button(button_frame, text="⏹️ Stop", 
                       command=self.stop_playback).pack(side='left', padx=5)
            
            # Soundfont checkbox
            self.use_soundfont_var = tk.BooleanVar(value=False)
            self.soundfont_path_var = tk.StringVar(value="")
            ttk.Checkbutton(button_frame, text="Use SoundFont", 
                           variable=self.use_soundfont_var,
                           command=self.toggle_soundfont).pack(side='left', padx=(10,5))
        else:
            # Show message when SimpleSampler is not available
            sampler_status = ttk.Label(button_frame, 
                                      text="⚠️ SimpleSampler not available", 
                                      foreground='orange')
            sampler_status.pack(side='left', padx=5)
            # Add clickable link/button to show build instructions
            ttk.Button(button_frame, text="ℹ️ Build Instructions", 
                       command=self.show_sampler_instructions).pack(side='left', padx=5)
        
        # Note range controls
        range_frame = ttk.Frame(control_frame)
        range_frame.pack(fill='x', pady=5)
        
        ttk.Label(range_frame, text="Min Note:").pack(side='left', padx=5)
        self.min_note_var = tk.StringVar(value="48")
        ttk.Entry(range_frame, textvariable=self.min_note_var, width=10).pack(side='left', padx=5)
        
        ttk.Label(range_frame, text="Max Note:").pack(side='left', padx=5)
        self.max_note_var = tk.StringVar(value="84")
        ttk.Entry(range_frame, textvariable=self.max_note_var, width=10).pack(side='left', padx=5)
        
        ttk.Label(range_frame, text="Max Time:").pack(side='left', padx=5)
        self.max_time_var = tk.StringVar(value="32")
        ttk.Entry(range_frame, textvariable=self.max_time_var, width=10).pack(side='left', padx=5)
        
        ttk.Button(range_frame, text="Update Range", 
                   command=self.update_piano_roll_range).pack(side='left', padx=5)
        
        # Zoom controls
        zoom_frame = ttk.Frame(control_frame)
        zoom_frame.pack(fill='x', pady=5)
        
        ttk.Label(zoom_frame, text="Horizontal Zoom:").pack(side='left', padx=5)
        self.h_zoom_var = tk.DoubleVar(value=1.0)
        h_zoom_slider = ttk.Scale(zoom_frame, from_=0.5, to=4.0, orient='horizontal',
                                   variable=self.h_zoom_var, command=self.update_piano_roll_zoom,
                                   length=200)
        h_zoom_slider.pack(side='left', padx=5)
        self.h_zoom_label = ttk.Label(zoom_frame, text="1.0x")
        self.h_zoom_label.pack(side='left', padx=5)
        
        ttk.Label(zoom_frame, text="Vertical Zoom:").pack(side='left', padx=20)
        self.v_zoom_var = tk.DoubleVar(value=1.0)
        v_zoom_slider = ttk.Scale(zoom_frame, from_=0.5, to=4.0, orient='horizontal',
                                   variable=self.v_zoom_var, command=self.update_piano_roll_zoom,
                                   length=200)
        v_zoom_slider.pack(side='left', padx=5)
        self.v_zoom_label = ttk.Label(zoom_frame, text="1.0x")
        self.v_zoom_label.pack(side='left', padx=5)
        
        ttk.Button(zoom_frame, text="Reset Zoom", 
                   command=self.reset_piano_roll_zoom).pack(side='left', padx=20)
        
        # Piano roll display frame
        display_frame = ttk.LabelFrame(tab, text="Piano Roll Display", padding=10)
        display_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create scrollable canvas container
        canvas_container = ttk.Frame(display_frame)
        canvas_container.pack(fill='both', expand=True)
        
        # Add scrollbars
        h_scrollbar = ttk.Scrollbar(canvas_container, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        v_scrollbar = ttk.Scrollbar(canvas_container, orient='vertical')
        v_scrollbar.pack(side='right', fill='y')
        
        # Create piano roll display with scrolling support
        self.piano_roll = PianoRollDisplay(canvas_container, width=800, height=400,
                                            xscrollcommand=h_scrollbar.set,
                                            yscrollcommand=v_scrollbar.set)
        self.piano_roll.pack(side='left', fill='both', expand=True)
        
        # Configure scrollbars
        h_scrollbar.config(command=self.piano_roll.xview)
        v_scrollbar.config(command=self.piano_roll.yview)
        
        # Store initial dimensions for zoom
        self.piano_roll_base_width = 800
        self.piano_roll_base_height = 400
        
        # Info label
        info_frame = ttk.Frame(display_frame)
        info_frame.pack(fill='x', pady=5)
        
        ttk.Label(info_frame, text="Velocity colors: Red (0-15) → Orange (16-31) → Yellow (32-47) → Green (48-51) → Cyan (52-63) → Blue (64-79) → Blue-Violet (80-95) → Violet (96-111) → Indigo (112-127)", 
                  font=('Arial', 9)).pack(side='left', padx=5)
        ttk.Label(info_frame, text="White edges mark note onsets", 
                  font=('Arial', 9)).pack(side='left', padx=20)
    
    def show_song_in_piano_roll(self):
        """Display the current song in the piano roll"""
        if self.current_song is None:
            messagebox.showwarning("Warning", "Please create a song first!")
            return
        
        try:
            self.piano_roll.set_song(self.current_song)
            messagebox.showinfo("Success", "Song displayed in piano roll!")
        except Exception as e:
            messagebox.showerror("Error", f"Error displaying song: {str(e)}")
    
    def show_bar_in_piano_roll(self):
        """Display the current bar in the piano roll"""
        if self.current_bar is None:
            messagebox.showwarning("Warning", "Please create a bar first!")
            return
        
        try:
            # Create a temporary song with just this bar
            temp_song = sk3.Song(name="TempBar", num_bars=1)
            temp_song.bar_list = [self.current_bar]
            self.piano_roll.set_song(temp_song)
            messagebox.showinfo("Success", "Bar displayed in piano roll!")
        except Exception as e:
            messagebox.showerror("Error", f"Error displaying bar: {str(e)}")
    
    def clear_piano_roll(self):
        """Clear the piano roll display"""
        try:
            self.piano_roll.song = None
            self.piano_roll.draw_grid()
            messagebox.showinfo("Success", "Piano roll cleared!")
        except Exception as e:
            messagebox.showerror("Error", f"Error clearing piano roll: {str(e)}")
    
    def update_piano_roll_range(self):
        """Update the piano roll display range"""
        try:
            min_note = int(self.min_note_var.get())
            max_note = int(self.max_note_var.get())
            max_time = float(self.max_time_var.get())
            
            if min_note < 0 or min_note > 127:
                raise ValueError("Min note must be between 0 and 127")
            if max_note < 0 or max_note > 127:
                raise ValueError("Max note must be between 0 and 127")
            if min_note >= max_note:
                raise ValueError("Min note must be less than max note")
            if max_time <= 0:
                raise ValueError("Max time must be positive")
            
            self.piano_roll.min_note = min_note
            self.piano_roll.max_note = max_note
            self.piano_roll.max_time = max_time
            self.piano_roll.update_display()
            
            messagebox.showinfo("Success", "Piano roll range updated!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid range: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating range: {str(e)}")
    
    def update_piano_roll_zoom(self, event=None):
        """Update piano roll zoom based on slider values"""
        try:
            h_zoom = self.h_zoom_var.get()
            v_zoom = self.v_zoom_var.get()
            
            # Update labels
            self.h_zoom_label.config(text=f"{h_zoom:.1f}x")
            self.v_zoom_label.config(text=f"{v_zoom:.1f}x")
            
            # Calculate new dimensions
            new_width = int(self.piano_roll_base_width * h_zoom)
            new_height = int(self.piano_roll_base_height * v_zoom)
            
            # Update piano roll dimensions
            self.piano_roll.config(width=new_width, height=new_height)
            self.piano_roll.display_width = new_width
            self.piano_roll.display_height = new_height
            
            # Recalculate grid dimensions
            self.piano_roll.grid_width = new_width - self.piano_roll.left_margin - self.piano_roll.right_margin
            self.piano_roll.grid_height = new_height - self.piano_roll.top_margin - self.piano_roll.bottom_margin
            
            # Configure scroll region
            self.piano_roll.configure(scrollregion=self.piano_roll.bbox("all"))
            
            # Redraw
            self.piano_roll.update_display()
            
        except Exception as e:
            print(f"Error updating zoom: {str(e)}")
    
    def reset_piano_roll_zoom(self):
        """Reset piano roll zoom to 1.0x"""
        self.h_zoom_var.set(1.0)
        self.v_zoom_var.set(1.0)
        self.update_piano_roll_zoom()
        messagebox.showinfo("Success", "Zoom reset to 1.0x")


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = SavellysKoneGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
