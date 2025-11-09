"""
GUI application for savellysKone3 with MIDI validation integration.
This GUI allows users to adjust onset and duration modulation parameters
and validates the resulting MIDI in real-time.
"""

import tkinter as tk
from tkinter import ttk
import savellysKone3 as sk3
import midi_parser


class SavellysKoneGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SavellysKone - MIDI Generator with Validation")
        self.root.geometry("600x500")
        
        # Create default song
        self.song = None
        self.create_default_song()
        
        # Create GUI elements
        self.create_widgets()
        
        # Initial validation
        self.update_validation()
    
    def create_default_song(self):
        """Create a default song for testing modulation"""
        pitch_grammar = """
        $S -> $phrase0 $phrase0 $phrase0 $phrase0
        $phrase0 -> 60 62 64 65 67 69 71 72
        """
        
        duration_grammar = """
        $S -> $phrase0 $phrase0 $phrase0 $phrase0
        $phrase0 -> 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25
        """
        
        velocity_grammar = """
        $S -> $phrase0 $phrase0 $phrase0 $phrase0
        $phrase0 -> 100 100 100 100 100 100 100 100
        """
        
        pitch_generator = sk3.ListGenerator(pitch_grammar, 8, "pitch")
        duration_generator = sk3.ListGenerator(duration_grammar, 8, "duration")
        velocity_generator = sk3.ListGenerator(velocity_grammar, 8, "velocity")
        
        self.song = sk3.Song(
            pitch_generator=pitch_generator,
            duration_generator=duration_generator,
            velocity_generator=velocity_generator,
            num_bars=4,
            ioi=0.5,
            name="GUI Test Song",
            generate_every_bar=True
        )
        self.song.generate_parameter_lists()
        self.song.make_bar_list()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="MIDI Modulation Controls", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Onset Modulation Section
        onset_frame = ttk.LabelFrame(main_frame, text="Onset Modulation", padding="10")
        onset_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(onset_frame, text="Frequency:").grid(row=0, column=0, sticky=tk.W)
        self.onset_freq_var = tk.DoubleVar(value=1.0)
        self.onset_freq_scale = ttk.Scale(onset_frame, from_=0.1, to=5.0, 
                                          variable=self.onset_freq_var,
                                          orient=tk.HORIZONTAL, length=300,
                                          command=self.on_modulation_change)
        self.onset_freq_scale.grid(row=0, column=1, padx=5)
        self.onset_freq_label = ttk.Label(onset_frame, text="1.00")
        self.onset_freq_label.grid(row=0, column=2)
        
        ttk.Label(onset_frame, text="Amplitude:").grid(row=1, column=0, sticky=tk.W)
        self.onset_amp_var = tk.DoubleVar(value=0.1)
        self.onset_amp_scale = ttk.Scale(onset_frame, from_=0.0, to=1.0, 
                                         variable=self.onset_amp_var,
                                         orient=tk.HORIZONTAL, length=300,
                                         command=self.on_modulation_change)
        self.onset_amp_scale.grid(row=1, column=1, padx=5)
        self.onset_amp_label = ttk.Label(onset_frame, text="0.10")
        self.onset_amp_label.grid(row=1, column=2)
        
        # Duration Modulation Section
        duration_frame = ttk.LabelFrame(main_frame, text="Duration Modulation", padding="10")
        duration_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(duration_frame, text="Frequency:").grid(row=0, column=0, sticky=tk.W)
        self.duration_freq_var = tk.DoubleVar(value=1.0)
        self.duration_freq_scale = ttk.Scale(duration_frame, from_=0.1, to=5.0, 
                                             variable=self.duration_freq_var,
                                             orient=tk.HORIZONTAL, length=300,
                                             command=self.on_modulation_change)
        self.duration_freq_scale.grid(row=0, column=1, padx=5)
        self.duration_freq_label = ttk.Label(duration_frame, text="1.00")
        self.duration_freq_label.grid(row=0, column=2)
        
        ttk.Label(duration_frame, text="Amplitude:").grid(row=1, column=0, sticky=tk.W)
        self.duration_amp_var = tk.DoubleVar(value=0.05)
        self.duration_amp_scale = ttk.Scale(duration_frame, from_=0.0, to=0.5, 
                                            variable=self.duration_amp_var,
                                            orient=tk.HORIZONTAL, length=300,
                                            command=self.on_modulation_change)
        self.duration_amp_scale.grid(row=1, column=1, padx=5)
        self.duration_amp_label = ttk.Label(duration_frame, text="0.05")
        self.duration_amp_label.grid(row=1, column=2)
        
        # Validation Status Section
        validation_frame = ttk.LabelFrame(main_frame, text="Validation Status", padding="10")
        validation_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.status_label = ttk.Label(validation_frame, text="Valid", 
                                      font=('Arial', 20, 'bold'),
                                      foreground='green')
        self.status_label.grid(row=0, column=0, pady=5)
        
        self.status_canvas = tk.Canvas(validation_frame, width=100, height=100, 
                                       bg='white', highlightthickness=1)
        self.status_canvas.grid(row=1, column=0, pady=5)
        
        self.details_text = tk.Text(validation_frame, height=6, width=60, 
                                    wrap=tk.WORD, state=tk.DISABLED)
        self.details_text.grid(row=2, column=0, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Reset to Default", 
                  command=self.reset_parameters).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Export MIDI", 
                  command=self.export_midi).grid(row=0, column=1, padx=5)
    
    def on_modulation_change(self, event=None):
        """Called when any modulation parameter changes"""
        # Update labels
        self.onset_freq_label.config(text=f"{self.onset_freq_var.get():.2f}")
        self.onset_amp_label.config(text=f"{self.onset_amp_var.get():.2f}")
        self.duration_freq_label.config(text=f"{self.duration_freq_var.get():.2f}")
        self.duration_amp_label.config(text=f"{self.duration_amp_var.get():.2f}")
        
        # Recreate song with current parameters
        self.create_default_song()
        
        # Apply modulations
        self.song.modulate_onset_with_sin(
            self.onset_freq_var.get(), 
            self.onset_amp_var.get()
        )
        self.song.modulate_duration_with_sin(
            self.duration_freq_var.get(), 
            self.duration_amp_var.get()
        )
        
        # Validate and update display
        self.update_validation()
    
    def update_validation(self):
        """Update the validation status display"""
        is_valid, message = midi_parser.validate_song_timing(self.song)
        status = "Valid" if is_valid else "Invalid"
        
        # Update status label
        self.status_label.config(
            text=status,
            foreground='green' if is_valid else 'red'
        )
        
        # Update canvas (visual indicator)
        self.status_canvas.delete("all")
        color = 'green' if is_valid else 'red'
        self.status_canvas.create_oval(10, 10, 90, 90, fill=color, outline=color)
        
        if is_valid:
            # Draw checkmark
            self.status_canvas.create_line(30, 50, 45, 65, width=3, fill='white')
            self.status_canvas.create_line(45, 65, 70, 30, width=3, fill='white')
        else:
            # Draw X
            self.status_canvas.create_line(30, 30, 70, 70, width=3, fill='white')
            self.status_canvas.create_line(70, 30, 30, 70, width=3, fill='white')
        
        # Update details text
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(1.0, message)
        self.details_text.config(state=tk.DISABLED)
    
    def reset_parameters(self):
        """Reset all parameters to default values"""
        self.onset_freq_var.set(1.0)
        self.onset_amp_var.set(0.1)
        self.duration_freq_var.set(1.0)
        self.duration_amp_var.set(0.05)
        self.on_modulation_change()
    
    def export_midi(self):
        """Export the current song to a MIDI file"""
        filename = "gui_generated.mid"
        self.song.make_midi_file(filename)
        
        # Show confirmation
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title("Export Complete")
        confirm_window.geometry("300x100")
        ttk.Label(confirm_window, text=f"MIDI file exported to:\n{filename}", 
                 font=('Arial', 10)).pack(pady=20)
        ttk.Button(confirm_window, text="OK", 
                  command=confirm_window.destroy).pack()


def main():
    """Main entry point for the GUI application"""
    root = tk.Tk()
    app = SavellysKoneGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
