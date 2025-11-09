"""
Tkinter GUI for savellysKone3.py

This GUI provides an easy-to-use interface for interacting with the main components
of savellysKone3.py, including:
- ListGenerator for generating pitch, duration, and velocity lists from grammars
- Bar objects for creating and manipulating musical bars
- Various operations like transpose, reverse, random modifications
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import savellysKone3 as sk3


class SavellysKoneGUI:
    """Main GUI class for savellysKone3"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SavellysKone3 GUI")
        self.root.geometry("900x700")
        
        # Variables to store generators and bar
        self.list_generator = None
        self.current_bar = None
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_list_generator_tab()
        self.create_bar_manipulation_tab()
        
    def create_list_generator_tab(self):
        """Create the ListGenerator tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="List Generator")
        
        # Grammar input section
        grammar_frame = ttk.LabelFrame(tab, text="Grammar Input", padding=10)
        grammar_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        ttk.Label(grammar_frame, text="Grammar String:").pack(anchor='w')
        self.grammar_text = scrolledtext.ScrolledText(grammar_frame, height=10, width=80)
        self.grammar_text.pack(fill='both', expand=True, pady=5)
        
        # Set default grammar
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
        self.grammar_text.insert('1.0', default_grammar)
        
        # Parameters frame
        params_frame = ttk.Frame(grammar_frame)
        params_frame.pack(fill='x', pady=5)
        
        ttk.Label(params_frame, text="Minimum Length:").pack(side='left', padx=5)
        self.min_length_var = tk.StringVar(value="8")
        ttk.Entry(params_frame, textvariable=self.min_length_var, width=10).pack(side='left', padx=5)
        
        ttk.Label(params_frame, text="Type:").pack(side='left', padx=5)
        self.type_var = tk.StringVar(value="pitch")
        type_combo = ttk.Combobox(params_frame, textvariable=self.type_var, 
                                   values=["pitch", "duration", "velocity"], 
                                   state="readonly", width=15)
        type_combo.pack(side='left', padx=5)
        
        # Generate button
        ttk.Button(grammar_frame, text="Generate List", 
                   command=self.generate_list).pack(pady=5)
        
        # Output section
        output_frame = ttk.LabelFrame(tab, text="Generated List", padding=10)
        output_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=8, width=80)
        self.output_text.pack(fill='both', expand=True)
        
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
        ttk.Label(pitch_frame, text="Pitch List (comma-separated):").pack(side='left', padx=5)
        self.pitch_list_var = tk.StringVar(value="60, 62, 64, 65, 67, 69, 71, 72")
        ttk.Entry(pitch_frame, textvariable=self.pitch_list_var, width=50).pack(side='left', padx=5)
        
        # Duration list input
        duration_frame = ttk.Frame(creation_frame)
        duration_frame.pack(fill='x', pady=2)
        ttk.Label(duration_frame, text="Duration List (comma-separated):").pack(side='left', padx=5)
        self.duration_list_var = tk.StringVar(value="1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0")
        ttk.Entry(duration_frame, textvariable=self.duration_list_var, width=50).pack(side='left', padx=5)
        
        # Velocity list input
        velocity_frame = ttk.Frame(creation_frame)
        velocity_frame.pack(fill='x', pady=2)
        ttk.Label(velocity_frame, text="Velocity List (comma-separated):").pack(side='left', padx=5)
        self.velocity_list_var = tk.StringVar(value="100, 100, 100, 100, 100, 100, 100, 100")
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
    
    def generate_list(self):
        """Generate a list using ListGenerator"""
        try:
            # Get grammar string
            grammar_str = self.grammar_text.get('1.0', 'end-1c')
            
            # Get parameters
            min_length = int(self.min_length_var.get())
            list_type = self.type_var.get()
            
            # Create ListGenerator
            self.list_generator = sk3.ListGenerator(grammar_str, min_length, list_type)
            
            # Generate list
            generated_list = self.list_generator.generate_list()
            
            # Display result
            self.output_text.delete('1.0', 'end')
            self.output_text.insert('1.0', f"Generated {list_type} list:\n")
            self.output_text.insert('end', f"{generated_list}\n\n")
            self.output_text.insert('end', f"Length: {len(generated_list)}")
            
            messagebox.showinfo("Success", f"List generated successfully!\nLength: {len(generated_list)}")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid parameter value: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating list: {str(e)}")
    
    def create_bar(self):
        """Create a Bar object"""
        try:
            # Parse lists
            pitch_list = [int(x.strip()) for x in self.pitch_list_var.get().split(',')]
            duration_list = [float(x.strip()) for x in self.duration_list_var.get().split(',')]
            velocity_list = [int(x.strip()) for x in self.velocity_list_var.get().split(',')]
            
            # Get parameters
            onset = float(self.onset_var.get())
            ioi = float(self.ioi_var.get())
            
            # Create Bar
            self.current_bar = sk3.Bar(onset, ioi, pitch_list, duration_list, velocity_list)
            self.current_bar.make_note_list()
            
            # Display bar
            self.display_bar()
            
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
        
        self.bar_display.delete('1.0', 'end')
        self.bar_display.insert('1.0', f"Bar Information:\n")
        self.bar_display.insert('end', f"Onset: {self.current_bar.bar_onset}\n")
        self.bar_display.insert('end', f"IOI: {self.current_bar.ioi}\n")
        self.bar_display.insert('end', f"Number of notes: {len(self.current_bar.note_list)}\n\n")
        
        self.bar_display.insert('end', "Notes:\n")
        self.bar_display.insert('end', f"{'Index':<8}{'Pitch':<10}{'Onset':<15}{'Duration':<15}{'Velocity':<10}\n")
        self.bar_display.insert('end', "-" * 60 + "\n")
        
        for i, note in enumerate(self.current_bar.note_list):
            self.bar_display.insert('end', 
                f"{i:<8}{note.pitch:<10}{note.onset:<15.2f}{note.duration:<15.2f}{note.velocity:<10}\n")
    
    def transpose_bar(self):
        """Transpose the current bar"""
        if self.current_bar is None:
            messagebox.showwarning("Warning", "Please create a bar first!")
            return
        
        try:
            semitones = int(self.transpose_var.get())
            self.current_bar.transpose_note_list(semitones)
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
        
        try:
            duration = float(self.set_duration_var.get())
            self.current_bar.set_note_list_durations(duration)
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
        
        try:
            self.current_bar.reverse_note_list()
            self.display_bar()
            messagebox.showinfo("Success", "Note list reversed!")
        except Exception as e:
            messagebox.showerror("Error", f"Error reversing notes: {str(e)}")
    
    def random_pitches(self):
        """Apply random variations to pitches"""
        if self.current_bar is None:
            messagebox.showwarning("Warning", "Please create a bar first!")
            return
        
        try:
            self.current_bar.random_pitch()
            self.display_bar()
            messagebox.showinfo("Success", "Random pitch variations applied!")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying random pitches: {str(e)}")
    
    def random_durations(self):
        """Apply random variations to durations"""
        if self.current_bar is None:
            messagebox.showwarning("Warning", "Please create a bar first!")
            return
        
        try:
            self.current_bar.random_duration()
            self.display_bar()
            messagebox.showinfo("Success", "Random duration variations applied!")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying random durations: {str(e)}")
    
    def random_velocities(self):
        """Apply random variations to velocities"""
        if self.current_bar is None:
            messagebox.showwarning("Warning", "Please create a bar first!")
            return
        
        try:
            self.current_bar.random_velocity()
            self.display_bar()
            messagebox.showinfo("Success", "Random velocity variations applied!")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying random velocities: {str(e)}")
    
    def random_onsets(self):
        """Apply random variations to onsets"""
        if self.current_bar is None:
            messagebox.showwarning("Warning", "Please create a bar first!")
            return
        
        try:
            self.current_bar.random_onset()
            self.display_bar()
            messagebox.showinfo("Success", "Random onset variations applied!")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying random onsets: {str(e)}")


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = SavellysKoneGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
