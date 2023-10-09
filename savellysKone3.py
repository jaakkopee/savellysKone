#this program uses grammars to generate midi files
from midiutil import MIDIFile
import random
import math
import musical_scales as ms

class Grammar:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def __str__(self):
        return "\n".join(map(str, self.rules))

    def __repr__(self):
        return self.__str__()
    
class GrammarRule:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return self.lhs + " -> " + self.rhs

    def __repr__(self):
        return self.__str__()
    
def parse_grammar(f):
    grammar = Grammar()
    for line in f:
        line = line.strip()
        if line:
            lhs, rhs_alternatives = line.split("->")
            lhs = lhs.strip()
            alternatives = rhs_alternatives.split("|")
            alternatives = [alt.strip() for alt in alternatives]
            for alternative in alternatives:
                grammar.add_rule(GrammarRule(lhs, alternative))
    return grammar

def generate_from_symbol(grammar, symbol):
    options = [rule.rhs for rule in grammar.rules if rule.lhs == symbol]
    if options:
        return random.choice(options)
    return symbol

def generate_from_string(grammar, string):
    output = ""
    for symbol in string:
        output += generate_from_symbol(grammar, symbol)
    return output

def generate(grammar, symbol, depth):
    if depth == 0:
        return symbol
    else:
        return generate(grammar, generate_from_string(grammar, symbol), depth - 1)

pitch_grammar_str = """
S -> A B C D E F G H
A -> 60 A | 62 A | 64 | 65
B -> 68 B | 67 B | 66 | 70
C -> 72 C | 71 C | 70 | 74
D -> 76 D | 75 D | 74 | 78
E -> 80 E | 79 E | 78 | 82
F -> 84 F | 83 F | 82 | 86
G -> 88 G | 87 G | 86 | 90
H -> 92 H | 91 H | 90 | 94
"""
pitch_grammar = parse_grammar(pitch_grammar_str.split("\n"))
print(pitch_grammar)
pitch_list = []
print("generating pitch list")
while len(pitch_list) < 8:
    pitch_list = generate(pitch_grammar, "S", 64)
    pitch_list = pitch_list.split()
    pitch_list = [int(note) for note in pitch_list]

print("...done")


duration_grammar_str = """
S -> A B C D E F G H
A -> 1 A | 0.5 A | 0.25 | 0.125
B -> 1 B | 0.5 B | 0.25 | 0.125
C -> 1 C | 0.5 C | 0.25 | 0.125
D -> 1 D | 0.5 D | 0.25 | 0.125
E -> 1 E | 0.5 E | 0.25 | 0.125
F -> 1 F | 0.5 F | 0.25 | 0.125
G -> 1 G | 0.5 G | 0.25 | 0.125
H -> 1 H | 0.5 H | 0.25 | 0.125
"""
duration_grammar = parse_grammar(duration_grammar_str.split("\n"))
print(duration_grammar)
print("generating duration list")
duration_list = []
while len(duration_list) < 8:
    duration_list = generate(duration_grammar, "S", 64)
    duration_list = duration_list.split()
    duration_list = [float(note) for note in duration_list]

print("...done")

velocity_grammar_str = """
S -> A B C D E F G H
A -> 100 A | 90 A | 80 | 70
B -> 100 B | 90 B | 80 | 70
C -> 100 C | 90 C | 80 | 70
D -> 100 D | 90 D | 80 | 70
E -> 100 E | 90 E | 80 | 70
F -> 100 F | 90 F | 80 | 70
G -> 100 G | 90 G | 80 | 70
H -> 100 H | 90 H | 80 | 70
"""
velocity_grammar = parse_grammar(velocity_grammar_str.split("\n"))
print(velocity_grammar)
velocity_list = []
print("generating velocity list")
while len(velocity_list) < 8:
    velocity_list = generate(velocity_grammar, "S", 64)
    velocity_list = velocity_list.split()
    velocity_list = [int(note) for note in velocity_list]

print("...done")


#find the shortest list
shortest_list = len(pitch_list)
if len(duration_list) < shortest_list:
    shortest_list = len(duration_list)
if len(velocity_list) < shortest_list:
    shortest_list = len(velocity_list)

#trim the lists to the shortest length
pitch_list = pitch_list[:shortest_list]
duration_list = duration_list[:shortest_list]
velocity_list = velocity_list[:shortest_list]

class Note:
    def __init__(self):
        self.pitch = 60
        self.onset = 0
        self.duration = 1
        self.velocity = 100
        return    
    
class Bar:
    def __init__(self, onset=0, ioi=0.75):
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
        self.pitch_list.reverse()
        self.duration_list.reverse()
        self.velocity_list.reverse()
        self.make_note_list()
        return
    
    def set_note_list_durations(self, duration):
        self.duration_list = []
        for i in range(len(self.pitch_list)):
            self.duration_list.append(duration)
        self.make_note_list()
        return
    
    def transpose_note_list(self, semitone):
        for i in range(len(self.pitch_list)):
            self.pitch_list[i] += semitone
        self.make_note_list()
        return
    
    def random_pitch(self):
        for i in range(len(self.pitch_list)):
            self.pitch_list[i] += random.randint(-12, 24)
        self.make_note_list()
        return
    
    def random_onset(self):
        for i in range(len(self.pitch_list)):
            self.note_list[i].onset += (random.random()-0.5)*0.8
            if self.note_list[i].onset < 0:
                self.note_list[i].onset = 0
        return
    
    def random_duration(self):
        for i in range(len(self.pitch_list)):
            self.note_list[i].duration += (random.random()-0.5)*0.8
            if self.note_list[i].duration < 0:
                self.note_list[i].duration = 0
        return
    
    def random_velocity(self):
        for i in range(len(self.pitch_list)):
            self.note_list[i].velocity += random.randint(-20, 20)
            if self.note_list[i].velocity < 0:
                self.note_list[i].velocity = 0
            if self.note_list[i].velocity > 127:
                self.note_list[i].velocity = 127
        return
    
    
class Song:
    def __init__(self, num_bars=4):
        self.bar_list = []
        self.ioi = 1.0
        self.num_bars = num_bars

    def make_bar_list(self):
        self.bar_list = []
        onset = 0
        for i in range(self.num_bars):
            bar = Bar(onset, self.ioi)
            bar.make_note_list()
            self.bar_list.append(bar)
            onset += bar.ioi*len(bar.pitch_list)
        return
    
    def make_midi_file(self, filename):
        midi_file = MIDIFile(1)
        for bar in self.bar_list:
            for note in bar.note_list:
                midi_file.addNote(0, 0, note.pitch, note.onset, note.duration, note.velocity)
        with open(filename, "wb") as output_file:
            midi_file.writeFile(output_file)
        return
    
    def reverse_bar_list(self):
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
            bar_onset = bar.bar_onset
            for note in bar.note_list:
                note.pitch += int(math.sin((note.onset+bar_onset)*freq)*amp)
                if note.pitch < 0:
                    note.pitch = 0
                if note.pitch > 127:
                    note.pitch = 127
    
    def modulate_duration_with_sin(self, freq, amp):
        for bar in self.bar_list:
            bar_onset = bar.bar_onset
            for note in bar.note_list:
                note.duration += math.sin((note.onset+bar_onset)*freq)*amp
                if note.duration < 0:
                    note.duration = 0
        return
    
    def modulate_velocity_with_sin(self, freq, amp):
        for bar in self.bar_list:
            bar_onset = bar.bar_onset
            for note in bar.note_list:
                note.velocity += int(math.sin((note.onset+bar_onset)*freq)*amp)
                if note.velocity < 0:
                    note.velocity = 0
                if note.velocity > 127:
                    note.velocity = 127

    def modulate_onset_with_sin(self, freq, amp):
        for bar in self.bar_list:
            bar_onset = bar.bar_onset
            for note in bar.note_list:
                note.onset += math.sin((note.onset+bar_onset)*freq)*amp
                if note.onset < 0:
                    note.onset = 0
        return
    
song = Song(8)
song.make_bar_list()
song.set_bar_list_durations(0.5)
song.modulate_onset_with_sin(2, 0.6)
song.make_midi_file("test_grammars.mid")
print("Done")

