from savellysKone3 import *

pitch_grammar_string = """
S -> a b c d
a -> A B C D
b -> E F G H
c -> I J K L
d -> M N O P
A -> 40 44 48 40 | 40 32 36 40
B -> 36 40 44 36 | 36 28 32 36
C -> 32 36 40 32 | 32 24 28 32
D -> 28 32 36 28 | 28 20 24 28
E -> 44 48 52 44 | 44 36 40 44
F -> 40 44 48 40 | 40 32 36 40
G -> 36 40 44 36 | 36 28 32 36
H -> 32 36 40 32 | 32 24 28 32
I -> 48 52 56 48 | 48 40 44 48
J -> 44 48 60 44 | 44 36 64 44
K -> 40 44 48 40 | 40 32 36 40
L -> 36 40 44 36 | 36 28 32 36
M -> 52 56 60 52 | 52 44 48 52
N -> 48 52 56 48 | 48 40 44 48
O -> 44 48 52 44 | 44 36 40 44
P -> 40 44 48 40 | 40 32 36 40
"""

duration_grammar_string = """
S -> a b c d
a -> A B C D
b -> A B C D
c -> A B C D
d -> A B C D
A -> 0.3 0.2 0.1 0.05
B -> 0.3 0.2 0.1 0.05
C -> 0.3 0.2 0.1 0.05
D -> 0.3 0.2 0.1 0.05
"""

velocity_grammar_string = """
S -> a b c d
a -> A B C D
b -> A B C D
c -> A B C D
d -> A B C D
A -> 100 127 100 127
B -> 100 127 90 100
C -> 100 127 80 100
D -> 100 127 70 100
"""

#generators
pitch_generator = ListGenerator(pitch_grammar_string, 16, "pitch")
duration_generator = ListGenerator(duration_grammar_string, 16, "duration")
velocity_generator = ListGenerator(velocity_grammar_string, 16, "velocity")

#song
song = Song(num_bars=16, ioi=0.5, pitch_generator=pitch_generator, duration_generator=duration_generator, velocity_generator=velocity_generator, generate_every_bar=True)
song.make_bar_list()
song.modulate_onset_with_sin_phase_by_bar(0.6, 0.8)
#song.modulate_pitch_with_sin_phase_by_bar(1.0, 1.8)
#song.modulate_velocity_with_sin_phase_by_bar(0.333, 1.8)
#song.modulate_duration_with_sin_phase_by_bar(0.5, 0.01)

#render
song.make_midi_file("sk3_test01.mid")

