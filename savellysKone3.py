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
        self.generate_parameter_lists()
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
            # Calculate the phase reset for each bar
            phase_reset = bar.bar_onset * freq * 2 * math.pi
            for note in bar.note_list:
                # Calculate the phase with phase reset at the onset of each bar
                phase = note.onset * freq * 2 * math.pi + phase_reset
                note.pitch += int(math.sin(phase) * amp)
                if note.pitch < 0:
                    note.pitch = 0
                if note.pitch > 127:
                    note.pitch = 127

        return
    

    def modulate_duration_with_sin_phase_by_bar(self, freq, amp):
        for bar in self.bar_list:
            # Calculate the phase reset for each bar
            phase_reset = bar.bar_onset * freq * 2 * math.pi
            for note in bar.note_list:
                # Calculate the phase with phase reset at the onset of each bar
                phase = note.onset * freq * 2 * math.pi + phase_reset
                note.duration += math.sin(phase) * amp
                if note.duration < 0:
                    note.duration = 0

        return
        
    
    def modulate_velocity_with_sin_phase_by_bar(self, freq, amp):
        for bar in self.bar_list:
            # Calculate the phase reset for each bar
            phase_reset = bar.bar_onset * freq * 2 * math.pi
            for note in bar.note_list:
                # Calculate the phase with phase reset at the onset of each bar
                phase = note.onset * freq * 2 * math.pi + phase_reset
                note.velocity += int(math.sin(phase) * amp)
                if note.velocity < 0:
                    note.velocity = 0
                if note.velocity > 127:
                    note.velocity = 127

        return

    def modulate_onset_with_sin_phase_by_bar(self, freq, amp):
        for bar in self.bar_list:
            # Calculate the phase reset for each bar
            phase_reset = bar.bar_onset * freq * 2 * math.pi
            for note in bar.note_list:
                # Calculate the phase with phase reset at the onset of each bar
                phase = note.onset * freq * 2 * math.pi + phase_reset
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

