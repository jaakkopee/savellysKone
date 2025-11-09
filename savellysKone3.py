#this program uses grammars to generate midi files
#also includes some methods for modifying the generated music


from midiutil import MIDIFile
import random
import math
import sys
import gengramparser2 as ggp
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class ListGenerator:
    def __init__(self, grammar_str, min_length=8, type="pitch"):
        self.type = type
        self.grammar = ggp.parse_grammar(grammar_str.split("\n"))
        self.min_length = min_length
        self.list = []

    def generate_list(self):
        self.list = []
        #powers_of_two = [2**i for i in range(10)]
        while (len(self.list) < self.min_length) or (len(self.list)%2 != 0):
            self.list = ggp.generate(self.grammar, "$S", 64)
            self.list = self.list.split()
            if self.type == "pitch":
                self.list = [int(note) for note in self.list]
            elif self.type == "duration": 
                self.list = [float(note) for note in self.list]
            elif self.type == "velocity":
                self.list = [int(note) for note in self.list]
        return self.list

class Note:
    def __init__(self):
        self.pitch = 60
        self.onset = 0
        self.duration = 1
        self.velocity = 100
        return    
    
class Bar:
    def __init__(self, onset=0, ioi=0.75, pitch_list=None, duration_list=None, velocity_list=None):
        self.pitch_list = pitch_list
        self.duration_list = duration_list
        self.velocity_list = velocity_list
        self.note_list = []
        self.bar_onset = onset
        self.ioi = ioi

    def make_note_list(self):
        self.note_list = []
        delta = self.bar_onset
        for i in range(len(self.pitch_list)):
            note = Note()
            note.onset = delta
            note.pitch = self.pitch_list[i]
            note.duration = self.duration_list[i]
            note.velocity = self.velocity_list[i]
            self.note_list.append(note)
            delta += self.ioi
        return
    
    def reverse_note_list(self):
        self.note_list.reverse()
        return
    
    def set_note_list_durations(self, duration):
        for note in self.note_list:
            note.duration = duration
        return
    
    def transpose_note_list(self, semitone):
        for note in self.note_list:
            note.pitch += semitone
            if note.pitch < 0:
                note.pitch = 0
            if note.pitch > 127:
                note.pitch = 127
        return
    
    def random_pitch(self):
        for i in range(len(self.note_list)):
            self.note_list[i].pitch += random.randint(-3, 3)
            if self.note_list[i].pitch < 0:
                self.note_list[i].pitch = 0
            if self.note_list[i].pitch > 127:
                self.note_list[i].pitch = 127
        return
    
    def random_onset(self):
        for i in range(len(self.note_list)):
            self.note_list[i].onset += (random.random()-0.5)*0.8
            if self.note_list[i].onset < 0:
                self.note_list[i].onset = 0
        return
    
    def random_duration(self):
        for i in range(len(self.note_list)):
            self.note_list[i].duration += (random.random()-0.5)*0.8
            if self.note_list[i].duration < 0:
                self.note_list[i].duration = 0
        return
    
    def random_velocity(self):
        for i in range(len(self.note_list)):
            self.note_list[i].velocity += random.randint(-20, 20)
            if self.note_list[i].velocity < 0:
                self.note_list[i].velocity = 0
            if self.note_list[i].velocity > 127:
                self.note_list[i].velocity = 127
        return
    
    
class Song:
    def __init__(self, name="skTrack", num_bars=4, ioi=1.0, pitch_generator=None, duration_generator=None, velocity_generator=None, generate_every_bar=False):
        self.name = name
        self.bar_list = []
        self.ioi = ioi
        self.num_bars = num_bars
        self.pitch_generator = pitch_generator
        self.duration_generator = duration_generator
        self.velocity_generator = velocity_generator
        self.pitch_list = []
        self.duration_list = []
        self.velocity_list = []
        self.generate_every_bar = generate_every_bar

    def generate_parameter_lists(self):
        if self.pitch_generator:
            self.pitch_list = self.pitch_generator.generate_list()
        else:
            self.pitch_list = [60]*8
        if self.duration_generator:
            self.duration_list = self.duration_generator.generate_list()
        else:
            self.duration_list = [1]*8
        if self.velocity_generator:
            self.velocity_list = self.velocity_generator.generate_list()
        else:
            self.velocity_list = [100]*8

        #find shortest list
        min_length = min(len(self.pitch_list), len(self.duration_list), len(self.velocity_list))
        #truncate lists
        self.pitch_list = self.pitch_list[:min_length]
        self.duration_list = self.duration_list[:min_length]
        self.velocity_list = self.velocity_list[:min_length]

        return

    def make_bar_list(self):
        self.bar_list = []
        onset = 0
        for i in range(self.num_bars):
            if self.generate_every_bar:
                self.generate_parameter_lists()
            bar = Bar(onset, self.ioi, self.pitch_list, self.duration_list, self.velocity_list)
            bar.make_note_list()
            self.bar_list.append(bar)
            onset += bar.ioi*len(bar.note_list)
        return
    
    def make_midi_file(self, filename):
        midi_file = MIDIFile(1)
        midi_file.addTrackName(0, 0, self.name)
        for bar in self.bar_list:
            for note in bar.note_list:
                midi_file.addNote(0, 0, note.pitch, note.onset, note.duration, note.velocity)
        with open(filename, "wb") as output_file:
            midi_file.writeFile(output_file)
        return
    
    def reverse_bar_list(self):
        #not tested, probably buggy and not work
        self.bar_list.reverse()
        for bar in self.bar_list:
            bar.reverse_note_list()
        return
    
    def set_bar_list_durations(self, duration):
        for bar in self.bar_list:
            bar.set_note_list_durations(duration)
        return
    
    def transpose_bar_list(self, semitone):
        for bar in self.bar_list:
            bar.transpose_note_list(semitone)
        return
    
    def random_pitch(self):
        for bar in self.bar_list:
            bar.random_pitch()
        return
    
    def random_onset(self):
        for bar in self.bar_list:
            bar.random_onset()
        return
    
    def random_duration(self):
        for bar in self.bar_list:
            bar.random_duration()
        return
    
    def random_velocity(self):
        for bar in self.bar_list:
            bar.random_velocity()
        return
    
    def random_bar_order(self):
        random.shuffle(self.bar_list)
        return
    
    def modulate_pitch_with_sin(self, freq, amp):
        for bar in self.bar_list:
            for note in bar.note_list:
                note.pitch += int(math.sin((note.onset)*freq)*amp)
                if note.pitch < 0:
                    note.pitch = 0
                if note.pitch > 127:
                    note.pitch = 127
    
    def modulate_duration_with_sin(self, freq, amp):
        for bar in self.bar_list:
            for note in bar.note_list:
                note.duration += math.sin((note.onset)*freq)*amp
                if note.duration < 0:
                    note.duration = 0
        return
    
    def modulate_velocity_with_sin(self, freq, amp):
        for bar in self.bar_list:
            for note in bar.note_list:
                note.velocity += int(math.sin((note.onset)*freq)*amp)
                if note.velocity < 0:
                    note.velocity = 0
                if note.velocity > 127:
                    note.velocity = 127

    def modulate_onset_with_sin(self, freq, amp):
        for bar in self.bar_list:
            for note in bar.note_list:
                note.onset += math.sin((note.onset)*freq)*amp
                if note.onset < 0:
                    note.onset = 0
        return
    
    def modulate_pitch_with_sin_phase_by_bar(self, freq, amp):
        for bar in self.bar_list:
            for note in bar.note_list:
                # Calculate the phase with phase reset at the onset of each bar
                phase = (note.onset-bar.bar_onset) * freq
                note.pitch += int(math.sin(phase) * amp)
                if note.pitch < 0:
                    note.pitch = 0
                if note.pitch > 127:
                    note.pitch = 127

        return
    

    def modulate_duration_with_sin_phase_by_bar(self, freq, amp):
        for bar in self.bar_list:
            for note in bar.note_list:
                # Calculate the phase with phase reset at the onset of each bar
                phase = (note.onset-bar.bar_onset) * freq
                note.duration += math.sin(phase) * amp
                if note.duration < 0:
                    note.duration = 0.001

        return
        
    
    def modulate_velocity_with_sin_phase_by_bar(self, freq, amp):
        for bar in self.bar_list:
            for note in bar.note_list:
                # Calculate the phase with phase reset at the onset of each bar
                phase = (note.onset-bar.bar_onset) * freq
                note.velocity += int(math.sin(phase) * amp)
                if note.velocity < 0:
                    note.velocity = 0
                if note.velocity > 127:
                    note.velocity = 127

        return

    def modulate_onset_with_sin_phase_by_bar(self, freq, amp):
        for bar in self.bar_list:
            for note in bar.note_list:
                # Calculate the phase with phase reset at the onset of each bar
                phase = (note.onset-bar.bar_onset) * freq
                note.onset += math.sin(phase) * amp
                if note.onset < 0:
                    note.onset = 0
        return
    


class SavellysKoneGUI:
    def __init__(self, root, test_mode=False):
        self.root = root
        self.root.title("Savellys Kone - Music Generator")
        self.root.geometry("800x900")
        
        self.song = None
        self.test_mode = test_mode  # Disable messageboxes in test mode
        
        # Create main container with scrollbar
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        row = 0
        
        # Song Parameters Section
        ttk.Label(main_frame, text="Song Parameters", font=('Arial', 12, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        
        ttk.Label(main_frame, text="Song Name:").grid(row=row, column=0, sticky=tk.W)
        self.name_var = tk.StringVar(value="generated_song")
        ttk.Entry(main_frame, textvariable=self.name_var, width=40).grid(row=row, column=1, sticky=tk.W, padx=5)
        row += 1
        
        ttk.Label(main_frame, text="Number of Bars:").grid(row=row, column=0, sticky=tk.W)
        self.num_bars_var = tk.StringVar(value="4")
        ttk.Entry(main_frame, textvariable=self.num_bars_var, width=20).grid(row=row, column=1, sticky=tk.W, padx=5)
        row += 1
        
        ttk.Label(main_frame, text="IOI (Inter-Onset Interval):").grid(row=row, column=0, sticky=tk.W)
        self.ioi_var = tk.StringVar(value="0.5")
        ttk.Entry(main_frame, textvariable=self.ioi_var, width=20).grid(row=row, column=1, sticky=tk.W, padx=5)
        row += 1
        
        # Grammar Section
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        ttk.Label(main_frame, text="Grammars", font=('Arial', 12, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        
        # Pitch Grammar
        ttk.Label(main_frame, text="Pitch Grammar:").grid(row=row, column=0, sticky=tk.W)
        row += 1
        self.pitch_grammar_text = tk.Text(main_frame, height=6, width=60)
        self.pitch_grammar_text.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5)
        self.pitch_grammar_text.insert('1.0', """$S -> $phrase0 $phrase0 $phrase0 $phrase0
$phrase0 -> 60 62 64 65 67 69 71 72""")
        row += 1
        
        # Duration Grammar
        ttk.Label(main_frame, text="Duration Grammar:").grid(row=row, column=0, sticky=tk.W, pady=(10, 0))
        row += 1
        self.duration_grammar_text = tk.Text(main_frame, height=6, width=60)
        self.duration_grammar_text.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5)
        self.duration_grammar_text.insert('1.0', """$S -> $phrase0 $phrase0 $phrase0 $phrase0
$phrase0 -> 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5""")
        row += 1
        
        # Velocity Grammar
        ttk.Label(main_frame, text="Velocity Grammar:").grid(row=row, column=0, sticky=tk.W, pady=(10, 0))
        row += 1
        self.velocity_grammar_text = tk.Text(main_frame, height=6, width=60)
        self.velocity_grammar_text.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5)
        self.velocity_grammar_text.insert('1.0', """$S -> $phrase0 $phrase0 $phrase0 $phrase0
$phrase0 -> 100 100 100 100 100 100 100 100""")
        row += 1
        
        # Generate Song Button
        ttk.Button(main_frame, text="Generate Song", command=self.generate_song).grid(row=row, column=0, columnspan=2, pady=10)
        row += 1
        
        # Modulation Section
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        ttk.Label(main_frame, text="Modulation Functions", font=('Arial', 12, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        
        # Duration Modulation with Sin (FEATURED)
        frame_dur = ttk.LabelFrame(main_frame, text="Duration Modulation with Sine Wave", padding="10")
        frame_dur.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        ttk.Label(frame_dur, text="Frequency:").grid(row=0, column=0, sticky=tk.W)
        self.dur_freq_var = tk.StringVar(value="1.0")
        ttk.Entry(frame_dur, textvariable=self.dur_freq_var, width=15).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(frame_dur, text="Amplitude:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.dur_amp_var = tk.StringVar(value="0.05")
        ttk.Entry(frame_dur, textvariable=self.dur_amp_var, width=15).grid(row=0, column=3, sticky=tk.W, padx=5)
        
        ttk.Button(frame_dur, text="Apply Duration Modulation", command=self.apply_duration_modulation).grid(row=1, column=0, columnspan=4, pady=(10, 0))
        
        # Pitch Modulation with Sin
        frame_pitch = ttk.LabelFrame(main_frame, text="Pitch Modulation with Sine Wave", padding="10")
        frame_pitch.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        ttk.Label(frame_pitch, text="Frequency:").grid(row=0, column=0, sticky=tk.W)
        self.pitch_freq_var = tk.StringVar(value="1.0")
        ttk.Entry(frame_pitch, textvariable=self.pitch_freq_var, width=15).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(frame_pitch, text="Amplitude:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.pitch_amp_var = tk.StringVar(value="10.0")
        ttk.Entry(frame_pitch, textvariable=self.pitch_amp_var, width=15).grid(row=0, column=3, sticky=tk.W, padx=5)
        
        ttk.Button(frame_pitch, text="Apply Pitch Modulation", command=self.apply_pitch_modulation).grid(row=1, column=0, columnspan=4, pady=(10, 0))
        
        # Velocity Modulation with Sin
        frame_vel = ttk.LabelFrame(main_frame, text="Velocity Modulation with Sine Wave", padding="10")
        frame_vel.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        ttk.Label(frame_vel, text="Frequency:").grid(row=0, column=0, sticky=tk.W)
        self.vel_freq_var = tk.StringVar(value="1.0")
        ttk.Entry(frame_vel, textvariable=self.vel_freq_var, width=15).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(frame_vel, text="Amplitude:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.vel_amp_var = tk.StringVar(value="10.0")
        ttk.Entry(frame_vel, textvariable=self.vel_amp_var, width=15).grid(row=0, column=3, sticky=tk.W, padx=5)
        
        ttk.Button(frame_vel, text="Apply Velocity Modulation", command=self.apply_velocity_modulation).grid(row=1, column=0, columnspan=4, pady=(10, 0))
        
        # Onset Modulation with Sin
        frame_onset = ttk.LabelFrame(main_frame, text="Onset Modulation with Sine Wave", padding="10")
        frame_onset.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        ttk.Label(frame_onset, text="Frequency:").grid(row=0, column=0, sticky=tk.W)
        self.onset_freq_var = tk.StringVar(value="1.0")
        ttk.Entry(frame_onset, textvariable=self.onset_freq_var, width=15).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(frame_onset, text="Amplitude:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.onset_amp_var = tk.StringVar(value="0.075")
        ttk.Entry(frame_onset, textvariable=self.onset_amp_var, width=15).grid(row=0, column=3, sticky=tk.W, padx=5)
        
        ttk.Button(frame_onset, text="Apply Onset Modulation", command=self.apply_onset_modulation).grid(row=1, column=0, columnspan=4, pady=(10, 0))
        
        # Save Section
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        ttk.Button(main_frame, text="Save MIDI File", command=self.save_midi).grid(row=row, column=0, columnspan=2, pady=10)
        row += 1
        
        # Status Label
        self.status_var = tk.StringVar(value="Ready. Click 'Generate Song' to start.")
        ttk.Label(main_frame, textvariable=self.status_var, foreground="blue").grid(row=row, column=0, columnspan=2, pady=5)
    
    def generate_song(self):
        try:
            # Get parameters
            name = self.name_var.get()
            num_bars = int(self.num_bars_var.get())
            ioi = float(self.ioi_var.get())
            
            # Get grammars
            pitch_grammar = self.pitch_grammar_text.get('1.0', tk.END).strip()
            duration_grammar = self.duration_grammar_text.get('1.0', tk.END).strip()
            velocity_grammar = self.velocity_grammar_text.get('1.0', tk.END).strip()
            
            # Create generators
            pitch_generator = ListGenerator(pitch_grammar, 8, "pitch")
            duration_generator = ListGenerator(duration_grammar, 8, "duration")
            velocity_generator = ListGenerator(velocity_grammar, 8, "velocity")
            
            # Create song
            self.song = Song(
                name=name,
                num_bars=num_bars,
                ioi=ioi,
                pitch_generator=pitch_generator,
                duration_generator=duration_generator,
                velocity_generator=velocity_generator,
                generate_every_bar=True
            )
            
            self.song.generate_parameter_lists()
            self.song.make_bar_list()
            
            self.status_var.set(f"Song '{name}' generated successfully with {num_bars} bars!")
            if not self.test_mode:
                messagebox.showinfo("Success", f"Song generated successfully!\nBars: {num_bars}\nIOI: {ioi}")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            if not self.test_mode:
                messagebox.showerror("Error", f"Failed to generate song:\n{str(e)}")
    
    def apply_duration_modulation(self):
        if self.song is None:
            if not self.test_mode:
                messagebox.showwarning("Warning", "Please generate a song first!")
            return
        
        try:
            freq = float(self.dur_freq_var.get())
            amp = float(self.dur_amp_var.get())
            
            self.song.modulate_duration_with_sin(freq, amp)
            
            self.status_var.set(f"Duration modulation applied (freq={freq}, amp={amp})")
            if not self.test_mode:
                messagebox.showinfo("Success", f"Duration modulation applied!\nFrequency: {freq}\nAmplitude: {amp}")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            if not self.test_mode:
                messagebox.showerror("Error", f"Failed to apply duration modulation:\n{str(e)}")
    
    def apply_pitch_modulation(self):
        if self.song is None:
            messagebox.showwarning("Warning", "Please generate a song first!")
            return
        
        try:
            freq = float(self.pitch_freq_var.get())
            amp = float(self.pitch_amp_var.get())
            
            self.song.modulate_pitch_with_sin(freq, amp)
            
            self.status_var.set(f"Pitch modulation applied (freq={freq}, amp={amp})")
            messagebox.showinfo("Success", f"Pitch modulation applied!\nFrequency: {freq}\nAmplitude: {amp}")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to apply pitch modulation:\n{str(e)}")
    
    def apply_velocity_modulation(self):
        if self.song is None:
            messagebox.showwarning("Warning", "Please generate a song first!")
            return
        
        try:
            freq = float(self.vel_freq_var.get())
            amp = float(self.vel_amp_var.get())
            
            self.song.modulate_velocity_with_sin(freq, amp)
            
            self.status_var.set(f"Velocity modulation applied (freq={freq}, amp={amp})")
            messagebox.showinfo("Success", f"Velocity modulation applied!\nFrequency: {freq}\nAmplitude: {amp}")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to apply velocity modulation:\n{str(e)}")
    
    def apply_onset_modulation(self):
        if self.song is None:
            messagebox.showwarning("Warning", "Please generate a song first!")
            return
        
        try:
            freq = float(self.onset_freq_var.get())
            amp = float(self.onset_amp_var.get())
            
            self.song.modulate_onset_with_sin(freq, amp)
            
            self.status_var.set(f"Onset modulation applied (freq={freq}, amp={amp})")
            messagebox.showinfo("Success", f"Onset modulation applied!\nFrequency: {freq}\nAmplitude: {amp}")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to apply onset modulation:\n{str(e)}")
    
    def save_midi(self):
        if self.song is None:
            messagebox.showwarning("Warning", "Please generate a song first!")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".mid",
                filetypes=[("MIDI files", "*.mid"), ("All files", "*.*")],
                initialfile=f"{self.song.name}.mid"
            )
            
            if filename:
                self.song.make_midi_file(filename)
                self.status_var.set(f"MIDI file saved: {filename}")
                messagebox.showinfo("Success", f"MIDI file saved successfully!\n{filename}")
        
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to save MIDI file:\n{str(e)}")


def launch_gui():
    """Launch the Tkinter GUI for Savellys Kone"""
    root = tk.Tk()
    app = SavellysKoneGUI(root)
    root.mainloop()
    
    
if __name__=="__main__":
    # Launch GUI by default
    launch_gui()


