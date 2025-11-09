#!/usr/bin/env python3
"""
GUI for savellysKone3 modulation functionalities
This application provides a user interface to apply various modulation effects
to generated MIDI songs using sinusoidal functions.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import savellysKone3 as sk3


class ModulationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SavellysKone3 Modulation GUI")
        self.root.geometry("600x600")
        
        # Initialize song variable
        self.song = None
        
        # Create the main UI
        self.create_widgets()
        
    def create_widgets(self):
        """Create all UI widgets"""
        
        # Title label
        title_label = tk.Label(
            self.root, 
            text="SavellysKone3 Modulation Interface",
            font=("Arial", 16, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Generate a song first, then apply modulations",
            font=("Arial", 10),
            pady=5
        )
        instructions.pack()
        
        # Song generation section
        generation_frame = ttk.LabelFrame(self.root, text="Song Generation", padding=10)
        generation_frame.pack(fill="x", padx=10, pady=5)
        
        generate_button = ttk.Button(
            generation_frame,
            text="Generate Song",
            command=self.generate_song
        )
        generate_button.pack()
        
        # Pitch Modulation Section
        pitch_frame = ttk.LabelFrame(self.root, text="Pitch Modulation with Sin", padding=10)
        pitch_frame.pack(fill="x", padx=10, pady=5)
        
        # Pitch frequency
        pitch_freq_frame = tk.Frame(pitch_frame)
        pitch_freq_frame.pack(fill="x", pady=2)
        tk.Label(pitch_freq_frame, text="Frequency:", width=15, anchor="w").pack(side="left")
        self.pitch_freq_entry = ttk.Entry(pitch_freq_frame, width=20)
        self.pitch_freq_entry.pack(side="left", padx=5)
        self.pitch_freq_entry.insert(0, "1.0")
        
        # Pitch amplitude
        pitch_amp_frame = tk.Frame(pitch_frame)
        pitch_amp_frame.pack(fill="x", pady=2)
        tk.Label(pitch_amp_frame, text="Amplitude:", width=15, anchor="w").pack(side="left")
        self.pitch_amp_entry = ttk.Entry(pitch_amp_frame, width=20)
        self.pitch_amp_entry.pack(side="left", padx=5)
        self.pitch_amp_entry.insert(0, "10.0")
        
        # Pitch apply button
        pitch_button = ttk.Button(
            pitch_frame,
            text="Apply Pitch Modulation",
            command=self.apply_pitch_modulation
        )
        pitch_button.pack(pady=5)
        
        # Velocity Modulation Section
        velocity_frame = ttk.LabelFrame(self.root, text="Velocity Modulation with Sin", padding=10)
        velocity_frame.pack(fill="x", padx=10, pady=5)
        
        # Velocity frequency
        velocity_freq_frame = tk.Frame(velocity_frame)
        velocity_freq_frame.pack(fill="x", pady=2)
        tk.Label(velocity_freq_frame, text="Frequency:", width=15, anchor="w").pack(side="left")
        self.velocity_freq_entry = ttk.Entry(velocity_freq_frame, width=20)
        self.velocity_freq_entry.pack(side="left", padx=5)
        self.velocity_freq_entry.insert(0, "1.0")
        
        # Velocity amplitude
        velocity_amp_frame = tk.Frame(velocity_frame)
        velocity_amp_frame.pack(fill="x", pady=2)
        tk.Label(velocity_amp_frame, text="Amplitude:", width=15, anchor="w").pack(side="left")
        self.velocity_amp_entry = ttk.Entry(velocity_amp_frame, width=20)
        self.velocity_amp_entry.pack(side="left", padx=5)
        self.velocity_amp_entry.insert(0, "10.0")
        
        # Velocity apply button
        velocity_button = ttk.Button(
            velocity_frame,
            text="Apply Velocity Modulation",
            command=self.apply_velocity_modulation
        )
        velocity_button.pack(pady=5)
        
        # Onset (Temporal) Modulation Section
        onset_frame = ttk.LabelFrame(self.root, text="Onset (Temporal) Modulation with Sin", padding=10)
        onset_frame.pack(fill="x", padx=10, pady=5)
        
        # Onset frequency
        onset_freq_frame = tk.Frame(onset_frame)
        onset_freq_frame.pack(fill="x", pady=2)
        tk.Label(onset_freq_frame, text="Frequency:", width=15, anchor="w").pack(side="left")
        self.onset_freq_entry = ttk.Entry(onset_freq_frame, width=20)
        self.onset_freq_entry.pack(side="left", padx=5)
        self.onset_freq_entry.insert(0, "1.0")
        
        # Onset amplitude
        onset_amp_frame = tk.Frame(onset_frame)
        onset_amp_frame.pack(fill="x", pady=2)
        tk.Label(onset_amp_frame, text="Amplitude:", width=15, anchor="w").pack(side="left")
        self.onset_amp_entry = ttk.Entry(onset_amp_frame, width=20)
        self.onset_amp_entry.pack(side="left", padx=5)
        self.onset_amp_entry.insert(0, "0.075")
        
        # Onset apply button
        onset_button = ttk.Button(
            onset_frame,
            text="Apply Onset Modulation",
            command=self.apply_onset_modulation
        )
        onset_button.pack(pady=5)
        
        # Export section
        export_frame = ttk.LabelFrame(self.root, text="Export MIDI", padding=10)
        export_frame.pack(fill="x", padx=10, pady=5)
        
        export_button = ttk.Button(
            export_frame,
            text="Save MIDI File",
            command=self.save_midi_file
        )
        export_button.pack()
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Ready - Generate a song to begin",
            relief=tk.SUNKEN,
            anchor="w",
            bg="#f0f0f0",
            pady=5
        )
        self.status_label.pack(fill="x", side="bottom", padx=10, pady=5)
        
    def generate_song(self):
        """Generate a basic song for testing modulations"""
        try:
            # Define simple grammars for testing
            pitch_grammar = """
            $S -> $phrase0 $phrase0 $phrase0 $phrase0
            $phrase0 -> 60 60 60 60 60 60 60 60
            """
            
            duration_grammar = """
            $S -> $phrase0 $phrase0 $phrase0 $phrase0
            $phrase0 -> 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3
            """
            
            velocity_grammar = """
            $S -> $phrase0 $phrase0 $phrase0 $phrase0
            $phrase0 -> 100 100 100 100 100 100 100 100
            """
            
            # Create generators
            pitch_generator = sk3.ListGenerator(pitch_grammar, 8, "pitch")
            duration_generator = sk3.ListGenerator(duration_grammar, 8, "duration")
            velocity_generator = sk3.ListGenerator(velocity_grammar, 8, "velocity")
            
            # Create song
            self.song = sk3.Song(
                pitch_generator=pitch_generator,
                duration_generator=duration_generator,
                velocity_generator=velocity_generator,
                num_bars=8,
                ioi=0.5,
                name="GUI Generated Song",
                generate_every_bar=True
            )
            
            # Generate the bar list
            self.song.make_bar_list()
            
            self.status_label.config(text="Song generated successfully! Apply modulations or save MIDI.")
            messagebox.showinfo("Success", "Song generated successfully!\nYou can now apply modulations.")
            
        except Exception as e:
            self.status_label.config(text=f"Error generating song: {str(e)}")
            messagebox.showerror("Error", f"Failed to generate song:\n{str(e)}")
    
    def apply_pitch_modulation(self):
        """Apply pitch modulation with sin"""
        if self.song is None:
            messagebox.showwarning("Warning", "Please generate a song first!")
            return
        
        try:
            freq = float(self.pitch_freq_entry.get())
            amp = float(self.pitch_amp_entry.get())
            
            self.song.modulate_pitch_with_sin(freq, amp)
            
            self.status_label.config(text=f"Pitch modulation applied (freq={freq}, amp={amp})")
            messagebox.showinfo("Success", f"Pitch modulation applied!\nFrequency: {freq}\nAmplitude: {amp}")
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numeric values for frequency and amplitude")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply pitch modulation:\n{str(e)}")
    
    def apply_velocity_modulation(self):
        """Apply velocity modulation with sin"""
        if self.song is None:
            messagebox.showwarning("Warning", "Please generate a song first!")
            return
        
        try:
            freq = float(self.velocity_freq_entry.get())
            amp = float(self.velocity_amp_entry.get())
            
            self.song.modulate_velocity_with_sin(freq, amp)
            
            self.status_label.config(text=f"Velocity modulation applied (freq={freq}, amp={amp})")
            messagebox.showinfo("Success", f"Velocity modulation applied!\nFrequency: {freq}\nAmplitude: {amp}")
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numeric values for frequency and amplitude")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply velocity modulation:\n{str(e)}")
    
    def apply_onset_modulation(self):
        """Apply onset (temporal) modulation with sin"""
        if self.song is None:
            messagebox.showwarning("Warning", "Please generate a song first!")
            return
        
        try:
            freq = float(self.onset_freq_entry.get())
            amp = float(self.onset_amp_entry.get())
            
            self.song.modulate_onset_with_sin(freq, amp)
            
            self.status_label.config(text=f"Onset modulation applied (freq={freq}, amp={amp})")
            messagebox.showinfo("Success", f"Onset modulation applied!\nFrequency: {freq}\nAmplitude: {amp}")
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numeric values for frequency and amplitude")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply onset modulation:\n{str(e)}")
    
    def save_midi_file(self):
        """Save the current song as a MIDI file"""
        if self.song is None:
            messagebox.showwarning("Warning", "Please generate a song first!")
            return
        
        try:
            # Ask user for filename
            filename = filedialog.asksaveasfilename(
                defaultextension=".mid",
                filetypes=[("MIDI files", "*.mid"), ("All files", "*.*")],
                initialfile="modulated_song.mid"
            )
            
            if filename:
                self.song.make_midi_file(filename)
                self.status_label.config(text=f"MIDI file saved: {filename}")
                messagebox.showinfo("Success", f"MIDI file saved successfully:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save MIDI file:\n{str(e)}")


def main():
    """Main entry point for the GUI application"""
    root = tk.Tk()
    app = ModulationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
