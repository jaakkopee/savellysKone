#this program uses grammars to generate midi files
#also includes some methods for modifying the generated music


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
    

class ListGenerator:
    def __init__(self, grammar_str, min_length=8, type="pitch"):
        self.type = type
        self.grammar = parse_grammar(grammar_str.split("\n"))
        self.min_length = min_length
        self.list = []

    def generate_list(self):
        self.list = []
        powers_of_two = [2**i for i in range(10)]
        while (len(self.list) < self.min_length) or (len(self.list) not in powers_of_two):
            self.list = generate(self.grammar, "S", 64)
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
    def __init__(self, num_bars=4, ioi=1.0, pitch_generator=None, duration_generator=None, velocity_generator=None, generate_every_bar=False):
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
            for note in bar.note_list:
                note.pitch += int(math.sin((note.onsett)*freq)*amp)
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
                note.pitch += int(math.sin((note.onset+bar.bar_onset)*freq)*amp)
                if note.pitch < 0:
                    note.pitch = 0
                if note.pitch > 127:
                    note.pitch = 127

    def modulate_duration_with_sin_phase_by_bar(self, freq, amp):
        for bar in self.bar_list:
            for note in bar.note_list:
                note.duration += math.sin((note.onset+bar.bar_onset)*freq)*amp
                if note.duration < 0:
                    note.duration = 0
        return
    
    def modulate_velocity_with_sin_phase_by_bar(self, freq, amp):
        for bar in self.bar_list:
            for note in bar.note_list:
                note.velocity += int(math.sin((note.onset+bar.bar_onset)*freq)*amp)
                if note.velocity < 0:
                    note.velocity = 0
                if note.velocity > 127:
                    note.velocity = 127

    def modulate_onset_with_sin_phase_by_bar(self, freq, amp):
        for bar in self.bar_list:
            for note in bar.note_list:
                note.onset += math.sin((note.onset+bar.bar_onset)*freq)*amp
                if note.onset < 0:
                    note.onset = 0
        return
    
    
if __name__=="__main__":
    #a simple bass line
    pitch_grammar_str = """
    S -> A A A A A A A A
    A -> 60 A | 60 B | 60
    B -> 62 B | 62 C | 64 C | 66
    C -> 63 | A

    """

    duration_grammar_str = """
    S -> A A A A A A A A
    A -> 0.1 A | 0.11 B | 0.111
    B -> 0.25 B | 0.25
    """

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

    #generators
    pitch_generator = ListGenerator(pitch_grammar_str, 16, "pitch")
    #generators can be None, in which case a default list is used
    #Note lists produced by default are all 60, 1.0, 100
    #leaving any of the generators as None will use the default values for that parameter
    #these values can be changed via the Song class
    duration_generator = ListGenerator(duration_grammar_str, 16, "duration")
    velocity_generator = ListGenerator(velocity_grammar_str, 16, "velocity")

    #make the song
    song = Song(num_bars=16, ioi=0.5, pitch_generator=pitch_generator, duration_generator=duration_generator, velocity_generator=velocity_generator, generate_every_bar=False)
    song.make_bar_list() #this is the method that actually generates the song
    #all the methods below can be used to modify the song plus some untested ones.
    #song.set_bar_list_durations(0.2)
    #song.modulate_duration_with_sin(1, 0.1)
    #song.modulate_onset_with_sin(1, 0.06) #add sway
    #song.modulate_onset_with_sin(1.5, 0.06) #add sway another way
    #song.modulate_onset_with_sin_phase_by_bar(0.5, 0.6) #add groove with phase reset by bar onset
    #song.modulate_velocity_with_sin(1, 10)
    #custom transpose algorithm
    pitch = 0
    sign = 1
    for bar in song.bar_list:
        bar.transpose_note_list(pitch*sign)
        sign *= -1
        pitch += 1
        pitch %= 4

    
    song.make_midi_file("testPow2LimitBassLine.mid")

    #a simple melody
    pitch_grammar_str = """
    S -> A A A A
    A -> 60 A | 60 B | 60
    B -> 62 B | 62 C
    C -> 64 C | 64 D
    D -> 65 D | 65 E
    E -> 67 E | 67 F
    F -> 69 F | 69 G
    G -> 71 G | 71
    """

    duration_grammar_str = """
    S -> A A A A
    A -> 0.1 A | 0.11 B | 0.111
    B -> 0.25 B | 0.25
    """ 

    velocity_grammar_str = """
    S -> A B C D
    A -> 100 A | 90 A | 80 | 70
    B -> 100 B | 90 B | 80 | 70
    C -> 100 C | 90 C | 80 | 70
    D -> 100 D | 90 D | 80 | 70
    """

    #generators
    pitch_generator = ListGenerator(pitch_grammar_str, 16, "pitch")
    duration_generator = ListGenerator(duration_grammar_str, 16, "duration")
    velocity_generator = ListGenerator(velocity_grammar_str, 16, "velocity")

    #make the song
    song = Song(num_bars=16, ioi=1.0, pitch_generator=pitch_generator, duration_generator=duration_generator, velocity_generator=velocity_generator, generate_every_bar=False)
    song.make_bar_list()
    song.set_bar_list_durations(0.3)
    #song.modulate_onset_with_sin_phase_by_bar(0.5, 0.6) #add groove with phase reset by bar onset

    #custom transpose algorithm
    pitch = 0
    sign = 1
    for bar in song.bar_list:
        bar.transpose_note_list(pitch*sign)
        sign *= -1
        pitch += 1
        pitch %= 4


    song.make_midi_file("testPow2LimitMelody.mid")


    
