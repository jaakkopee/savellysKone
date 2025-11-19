#this program uses grammars to generate midi files
#also includes some methods for modifying the generated music


from midiutil import MIDIFile
import random
import math
import musical_scales as ms
import sys
import gengramparser2 as ggp


class ListGenerator:
    def __init__(self, grammar_str, min_length=8, type="pitch"):
        self.type = type
        self.grammar = ggp.parse_grammar(grammar_str.split("\n"))
        self.min_length = min_length
        self.list = []

    def generate_list(self):
        self.list = []
        max_attempts = 100  # Prevent infinite loops
        attempts = 0
        max_length_seen = 0
        
        # Try to generate a list that meets min_length
        while len(self.list) < self.min_length:
            raw_output = ggp.generate(self.grammar, "$S", 128)  # Increased depth from 64 to 128
            self.list = raw_output.split()
            
            # Check for unexpanded non-terminals (containing $)
            unexpanded = [item for item in self.list if '$' in item]
            if unexpanded:
                print(f"WARNING ({self.type}): Grammar contains unexpanded non-terminals after depth 128")
                print(f"         Unexpanded symbols: {unexpanded[:5]}")  # Show first 5
                print(f"         Raw output: {raw_output[:100]}...")
                print(f"         This may indicate missing grammar rules or infinite recursion")
            
            # Filter out any unexpanded non-terminals
            self.list = [item for item in self.list if '$' not in item]
            
            if not self.list:
                print(f"ERROR ({self.type}): After filtering unexpanded symbols, list is empty!")
                print(f"       Raw output was: {raw_output}")
                attempts += 1
                continue
            
            # Convert to appropriate type with error handling
            conversion_errors = []
            try:
                if self.type == "pitch":
                    converted = []
                    for i, note in enumerate(self.list):
                        try:
                            val = int(note)
                            if not (0 <= val <= 127):
                                conversion_errors.append(f"Note {i}: {note} -> {val} (out of MIDI range 0-127)")
                            converted.append(val)
                        except ValueError:
                            conversion_errors.append(f"Note {i}: '{note}' cannot be converted to integer")
                            raise
                    self.list = converted
                elif self.type == "duration": 
                    converted = []
                    for i, note in enumerate(self.list):
                        try:
                            val = float(note)
                            if val < 0:
                                conversion_errors.append(f"Duration {i}: {note} -> {val} (negative duration)")
                            elif val > 100:
                                conversion_errors.append(f"Duration {i}: {note} -> {val} (unusually long)")
                            converted.append(val)
                        except ValueError:
                            conversion_errors.append(f"Duration {i}: '{note}' cannot be converted to float")
                            raise
                    self.list = converted
                elif self.type == "velocity":
                    converted = []
                    for i, note in enumerate(self.list):
                        try:
                            val = int(note)
                            if not (0 <= val <= 127):
                                conversion_errors.append(f"Velocity {i}: {note} -> {val} (out of MIDI range 0-127)")
                            converted.append(val)
                        except ValueError:
                            conversion_errors.append(f"Velocity {i}: '{note}' cannot be converted to integer")
                            raise
                    self.list = converted
                elif self.type == "ioi":
                    converted = []
                    for i, note in enumerate(self.list):
                        try:
                            val = float(note)
                            if val < 0:
                                conversion_errors.append(f"IOI {i}: {note} -> {val} (negative IOI)")
                            elif val > 100:
                                conversion_errors.append(f"IOI {i}: {note} -> {val} (unusually long)")
                            converted.append(val)
                        except ValueError:
                            conversion_errors.append(f"IOI {i}: '{note}' cannot be converted to float")
                            raise
                    self.list = converted
            except ValueError as e:
                print(f"\n{'='*60}")
                print(f"ERROR: Cannot convert grammar output to {self.type} type")
                print(f"{'='*60}")
                print(f"Raw grammar output: {raw_output[:200]}")
                print(f"After splitting: {self.list[:10]} {'...' if len(self.list) > 10 else ''}")
                if conversion_errors:
                    print(f"\nConversion errors found:")
                    for err in conversion_errors[:5]:  # Show first 5 errors
                        print(f"  • {err}")
                print(f"\nOriginal error: {str(e)}")
                print(f"Attempt {attempts + 1}/{max_attempts} - Retrying with new generation...")
                print(f"{'='*60}\n")
                self.list = []  # Reset and try again
                attempts += 1
                continue
            
            # Show warnings for out-of-range values
            if conversion_errors:
                print(f"WARNING ({self.type}): Found {len(conversion_errors)} values with issues:")
                for err in conversion_errors[:3]:
                    print(f"  • {err}")
            
            # Track the maximum length we've seen
            if len(self.list) > max_length_seen:
                max_length_seen = len(self.list)
            
            attempts += 1
            
            # If we've tried many times and can't reach min_length, pad the list
            if attempts >= max_attempts:
                print(f"WARNING: Grammar cannot generate {self.min_length} elements after {max_attempts} attempts.")
                print(f"         Maximum length seen: {max_length_seen}")
                print(f"         Padding list by repeating elements to reach min_length={self.min_length}")
                
                # Pad by repeating the list until we reach min_length
                if len(self.list) > 0:
                    while len(self.list) < self.min_length:
                        # Repeat elements from the beginning
                        elements_needed = self.min_length - len(self.list)
                        self.list.extend(self.list[:elements_needed])
                else:
                    # If list is empty, use default values
                    if self.type == "pitch":
                        self.list = [60] * self.min_length
                    elif self.type == "duration":
                        self.list = [1.0] * self.min_length
                    elif self.type == "velocity":
                        self.list = [100] * self.min_length
                    print(f"         Grammar produced empty list, using defaults")
                
                break
        
        return self.list

class Note:
    def __init__(self):
        self.pitch = 60
        self.onset = 0
        self.duration = 1
        self.velocity = 100
        return    
    
class Bar:
    def __init__(self, onset=0, ioi=0.75, pitch_list=None, duration_list=None, velocity_list=None, num_notes=None, ioi_list=None):
        self.pitch_list = pitch_list
        self.duration_list = duration_list
        self.velocity_list = velocity_list
        self.ioi_list = ioi_list if ioi_list is not None else []
        self.note_list = []
        self.bar_onset = onset
        self.ioi = ioi
        self.num_notes = num_notes  # User-specified number of notes, None = use longest list

    def make_note_list(self):
        self.note_list = []
        delta = self.bar_onset
        
        # Check for empty lists
        if not self.pitch_list or not self.duration_list or not self.velocity_list:
            print(f"WARNING: One or more parameter lists are empty!")
            return
        
        # Determine number of notes: use user-specified value if provided, otherwise use longest list
        if self.num_notes is not None:
            max_len = self.num_notes
            print(f"DEBUG: Using user-specified number of notes: {max_len}")
        else:
            # Use the LONGEST list to determine number of notes (include ioi_list if present)
            list_lengths = [len(self.pitch_list), len(self.duration_list), len(self.velocity_list)]
            if self.ioi_list:
                list_lengths.append(len(self.ioi_list))
            max_len = max(list_lengths)
            print(f"DEBUG: Using longest list length: {max_len}")
        
        # Other lists will wrap around using modulo (circular buffer)
        # Info about list cycling behavior
        all_same_length = (len(self.pitch_list) == len(self.duration_list) == len(self.velocity_list))
        if self.ioi_list:
            all_same_length = all_same_length and (len(self.ioi_list) == len(self.pitch_list))
        
        if not all_same_length:
            print(f"DEBUG: Using circular buffer - pitch:{len(self.pitch_list)}, duration:{len(self.duration_list)}, velocity:{len(self.velocity_list)}, ioi:{len(self.ioi_list) if self.ioi_list else 0}")
            print(f"       Creating {max_len} notes with lists wrapping independently")
        
        print(f"DEBUG make_note_list: bar_onset={self.bar_onset}, ioi={self.ioi}, ioi_list={'yes' if self.ioi_list else 'no'}, num_notes={max_len}")
        
        for i in range(max_len):
            note = Note()
            note.onset = delta
            # Use modulo to wrap around each list independently (circular buffer)
            note.pitch = self.pitch_list[i % len(self.pitch_list)]
            note.duration = self.duration_list[i % len(self.duration_list)]
            note.velocity = self.velocity_list[i % len(self.velocity_list)]
            self.note_list.append(note)
            if i < 3:  # Print first 3 notes
                print(f"  Note {i}: onset={note.onset}, pitch={note.pitch}, dur={note.duration}, vel={note.velocity}")
            
            # Use per-note IOI from ioi_list if available, otherwise use default self.ioi
            if self.ioi_list:
                current_ioi = self.ioi_list[i % len(self.ioi_list)]
                delta += current_ioi
            else:
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
    
    def modulate_pitch_with_sin(self, freq, amp):
        """Modulate pitch using sine wave based on absolute note onset"""
        for note in self.note_list:
            note.pitch += int(math.sin(note.onset * freq) * amp)
            if note.pitch < 0:
                note.pitch = 0
            if note.pitch > 127:
                note.pitch = 127
        return
    
    def modulate_duration_with_sin(self, freq, amp):
        """Modulate duration using sine wave based on absolute note onset"""
        for note in self.note_list:
            note.duration += math.sin(note.onset * freq) * amp
            if note.duration < 0:
                note.duration = 0
        return
    
    def modulate_velocity_with_sin(self, freq, amp):
        """Modulate velocity using sine wave based on absolute note onset"""
        for note in self.note_list:
            note.velocity += int(math.sin(note.onset * freq) * amp)
            if note.velocity < 0:
                note.velocity = 0
            if note.velocity > 127:
                note.velocity = 127
        return
    
    def modulate_onset_with_sin(self, freq, amp):
        """Modulate onset using sine wave based on absolute note onset"""
        for note in self.note_list:
            note.onset += math.sin(note.onset * freq) * amp
            if note.onset < 0:
                note.onset = 0
        return
    
    def modulate_pitch_with_sin_phase_by_bar(self, freq, amp):
        """Modulate pitch using sine wave with phase reset at bar onset"""
        for note in self.note_list:
            phase = (note.onset - self.bar_onset) * freq
            note.pitch += int(math.sin(phase) * amp)
            if note.pitch < 0:
                note.pitch = 0
            if note.pitch > 127:
                note.pitch = 127
        return
    
    def modulate_duration_with_sin_phase_by_bar(self, freq, amp):
        """Modulate duration using sine wave with phase reset at bar onset"""
        for note in self.note_list:
            phase = (note.onset - self.bar_onset) * freq
            note.duration += math.sin(phase) * amp
            if note.duration < 0:
                note.duration = 0.001
        return
    
    def modulate_velocity_with_sin_phase_by_bar(self, freq, amp):
        """Modulate velocity using sine wave with phase reset at bar onset"""
        for note in self.note_list:
            phase = (note.onset - self.bar_onset) * freq
            note.velocity += int(math.sin(phase) * amp)
            if note.velocity < 0:
                note.velocity = 0
            if note.velocity > 127:
                note.velocity = 127
        return
    
    def modulate_onset_with_sin_phase_by_bar(self, freq, amp):
        """Modulate onset using sine wave with phase reset at bar onset"""
        for note in self.note_list:
            phase = (note.onset - self.bar_onset) * freq
            note.onset += math.sin(phase) * amp
            if note.onset < 0:
                note.onset = 0
        return


class BarCollection:
    """Collection of multiple Bar objects for manipulation and export"""
    def __init__(self, bars=None):
        self.bars = bars if bars is not None else []
    
    def add_bar(self, bar):
        """Add a Bar to the collection"""
        self.bars.append(bar)
    
    def remove_bar(self, index):
        """Remove a Bar at the given index"""
        if 0 <= index < len(self.bars):
            self.bars.pop(index)
    
    def clear(self):
        """Remove all bars"""
        self.bars = []
    
    def make_midi_file(self, filename, name="BarCollection"):
        """Export all bars to a MIDI file"""
        midi_file = MIDIFile(numTracks=1, removeDuplicates=False, deinterleave=False, 
                            adjust_origin=False, file_format=0)
        midi_file.addTempo(0, 0, 120)
        midi_file.addTrackName(0, 0, name)
        
        note_count = 0
        for bar_idx, bar in enumerate(self.bars):
            for note in bar.note_list:
                midi_file.addNote(0, 0, note.pitch, note.onset, note.duration, note.velocity)
                note_count += 1
        
        print(f"Total notes added to MIDI: {note_count}")
        with open(filename, "wb") as output_file:
            midi_file.writeFile(output_file)
        return
    
    def transpose_all(self, semitone):
        """Transpose all bars"""
        for bar in self.bars:
            bar.transpose_note_list(semitone)
    
    def reverse_all(self):
        """Reverse all bars"""
        for bar in self.bars:
            bar.reverse_note_list()
    
    def set_all_durations(self, duration):
        """Set duration for all notes in all bars"""
        for bar in self.bars:
            bar.set_note_list_durations(duration)
    
    def random_pitch_all(self):
        """Apply random pitch variation to all bars"""
        for bar in self.bars:
            bar.random_pitch()
    
    def random_onset_all(self):
        """Apply random onset variation to all bars"""
        for bar in self.bars:
            bar.random_onset()
    
    def random_duration_all(self):
        """Apply random duration variation to all bars"""
        for bar in self.bars:
            bar.random_duration()
    
    def random_velocity_all(self):
        """Apply random velocity variation to all bars"""
        for bar in self.bars:
            bar.random_velocity()
    

class Song:
    def __init__(self, name="skTrack", num_bars=4, ioi=1.0, pitch_generator=None, duration_generator=None, velocity_generator=None, ioi_generator=None, generate_every_bar=False, bar_collection=None):
        self.name = name
        self.bar_list = []
        self.ioi = ioi
        self.num_bars = num_bars
        self.pitch_generator = pitch_generator
        self.duration_generator = duration_generator
        self.velocity_generator = velocity_generator
        self.ioi_generator = ioi_generator
        self.pitch_list = []
        self.duration_list = []
        self.velocity_list = []
        self.ioi_list = []
        self.generate_every_bar = generate_every_bar
        self.bar_collection = bar_collection  # Optional BarCollection to use instead of generating

    def generate_parameter_lists(self):
        if self.pitch_generator:
            self.pitch_list = self.pitch_generator.generate_list()
            print(f"    Generated pitch_list: {len(self.pitch_list)} notes")
        else:
            self.pitch_list = [60]*8
            print(f"    Using default pitch_list: {len(self.pitch_list)} notes")
        if self.duration_generator:
            self.duration_list = self.duration_generator.generate_list()
            print(f"    Generated duration_list: {len(self.duration_list)} notes")
        else:
            self.duration_list = [1]*8
            print(f"    Using default duration_list: {len(self.duration_list)} notes")
        if self.velocity_generator:
            self.velocity_list = self.velocity_generator.generate_list()
            print(f"    Generated velocity_list: {len(self.velocity_list)} notes")
        else:
            self.velocity_list = [100]*8
            print(f"    Using default velocity_list: {len(self.velocity_list)} notes")
        if self.ioi_generator:
            self.ioi_list = self.ioi_generator.generate_list()
            print(f"    Generated ioi_list: {len(self.ioi_list)} values")
        else:
            self.ioi_list = []
            print(f"    Using default IOI (0.5 seconds per note)")

        print(f"    Lists: pitch={len(self.pitch_list)}, duration={len(self.duration_list)}, velocity={len(self.velocity_list)}, ioi={len(self.ioi_list)}")
        print(f"    Using circular buffer for bars (lists wrap independently)")

        return

    def make_bar_list(self):
        self.bar_list = []
        
        # If a BarCollection was provided, use those bars instead of generating
        if self.bar_collection is not None:
            print(f"DEBUG make_bar_list: Using BarCollection with {len(self.bar_collection.bars)} bars")
            self.bar_list = self.bar_collection.bars.copy()
            
            # Recalculate bar onsets so each bar starts where the previous one ends
            onset = 0
            for i, bar in enumerate(self.bar_list):
                old_onset = bar.bar_onset
                bar.bar_onset = onset
                
                # Update all note onsets in the bar
                onset_delta = onset - old_onset
                for note in bar.note_list:
                    note.onset += onset_delta
                
                # Calculate where next bar should start (end of current bar)
                if bar.note_list:
                    last_note_onset = bar.note_list[-1].onset
                    onset = last_note_onset + bar.ioi
                    print(f"  Bar {i}: onset={bar.bar_onset:.3f}, last_note={last_note_onset:.3f}, next_onset={onset:.3f}")
                else:
                    print(f"  Bar {i}: empty bar, onset={onset}")
            
            return
        
        # Otherwise, generate bars as usual
        onset = 0
        print(f"DEBUG make_bar_list: num_bars={self.num_bars}, song.ioi={self.ioi}, generate_every_bar={self.generate_every_bar}")
        for i in range(self.num_bars):
            if self.generate_every_bar:
                self.generate_parameter_lists()
                print(f"  Bar {i}: Generated lists - pitch:{len(self.pitch_list)}, duration:{len(self.duration_list)}, velocity:{len(self.velocity_list)}, ioi:{len(self.ioi_list)}")
            bar = Bar(onset, self.ioi, self.pitch_list, self.duration_list, self.velocity_list, ioi_list=self.ioi_list)
            bar.make_note_list()
            self.bar_list.append(bar)
            prev_onset = onset
            onset += bar.ioi*len(bar.note_list)
            print(f"  Bar {i}: onset was {prev_onset}, added {bar.ioi}*{len(bar.note_list)}={bar.ioi*len(bar.note_list)}, new onset={onset}")
        return
    
    def make_midi_file(self, filename):
        # Create MIDI file with 1 track, format 0 (single track)
        # Disable removeDuplicates to ensure all notes are written
        midi_file = MIDIFile(numTracks=1, removeDuplicates=False, deinterleave=False, 
                            adjust_origin=False, file_format=0)
        # Add tempo to track 0
        midi_file.addTempo(0, 0, 120)
        # Add track name
        midi_file.addTrackName(0, 0, self.name)
        # Add notes to track 0, channel 0
        # Debug: Print onset times for first few bars
        note_count = 0
        notes_at_time = {}  # Track how many notes at each onset
        for bar_idx, bar in enumerate(self.bar_list):
            if bar_idx < 3:  # Print first 3 bars for debugging
                print(f"Bar {bar_idx}: bar_onset={bar.bar_onset}, num_notes={len(bar.note_list)}")
                if bar.note_list:
                    print(f"  First note onset: {bar.note_list[0].onset}, Last note onset: {bar.note_list[-1].onset}")
            for note_idx, note in enumerate(bar.note_list):
                # Track notes at same time
                onset_key = round(note.onset, 3)
                if onset_key not in notes_at_time:
                    notes_at_time[onset_key] = []
                notes_at_time[onset_key].append((note.pitch, bar_idx, note_idx))
                
                midi_file.addNote(0, 0, note.pitch, note.onset, note.duration, note.velocity)
                note_count += 1
        
        # Check for overlapping notes
        print(f"Total notes added to MIDI: {note_count}")
        overlaps = {k: v for k, v in notes_at_time.items() if len(v) > 1}
        if overlaps:
            print(f"WARNING: Found {len(overlaps)} onset times with multiple notes:")
            for onset, notes_list in list(overlaps.items())[:5]:  # Show first 5
                print(f"  Onset {onset}: {len(notes_list)} notes - {notes_list}")
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
    
    
    
if __name__=="__main__":
    
    #generate a song
    pitch_grammar_str = """
    $S -> $phrase01 $phrase02 $phrase03 $phrase04
    $phrase01 -> $note01 $note02 $note03 $note04
    $phrase02 -> $note05 $note06 $note07 $note08
    $phrase03 -> $note09 $note10 $note11 $note12
    $phrase04 -> $note13 $note14 $note15 $note16
    $note01 -> 60
    $note02 -> 62
    $note03 -> 64
    $note04 -> 65
    $note05 -> 67
    $note06 -> 69
    $note07 -> 71
    $note08 -> 72
    $note09 -> 74
    $note10 -> 76
    $note11 -> 77
    $note12 -> 79
    $note13 -> 81
    $note14 -> 83
    $note15 -> 84
    $note16 -> 86
    """

    duration_grammar_str = """
    $S -> $phrase01 $phrase01 $phrase01 $phrase01
    $phrase01 -> $duration01 $duration02 $duration03 $duration04
    $duration01 -> 0.6
    $duration02 -> 0.8
    $duration03 -> 1.0
    $duration04 -> 1.2
    """

    velocity_grammar_str = """
    $S -> $phrase01 $phrase01 $phrase01 $phrase01
    $phrase01 -> $velocity01 $velocity02 $velocity03 $velocity04
    $velocity01 -> 100
    $velocity02 -> 110
    $velocity03 -> 120
    $velocity04 -> 127
    """

    pitch_generator = ListGenerator(pitch_grammar_str, 8, "pitch")
    duration_generator = ListGenerator(duration_grammar_str, 8, "duration")
    velocity_generator = ListGenerator(velocity_grammar_str, 8, "velocity")

    song = Song(name="ionic_upwards", num_bars=4, ioi=1.5, pitch_generator=pitch_generator, duration_generator=duration_generator, velocity_generator=velocity_generator, generate_every_bar=True)
    song.make_bar_list()
    song.make_midi_file("testGGP2.mid")

