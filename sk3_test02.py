from savellysKone3 import *

pitch_grammar_string = """
S -> a b b a
a -> 60 b 60 | 62 b 62 | 64 b 64 | 48 b 48 | 50 b 50
b -> 62 b 62 | 64 b 64 | 48 b 48 | 50 b 50 | 36 38 36

"""

duration_grammar_string = """
S -> a b b a
a -> 1.5 a 1.5 | 1.3 a 1.0 | 1.0 b 1.0 | 0.5 b 0.5
b -> 1.0 b 1.0 | 0.5 b 0.5 | 0.25 0.25 0.25
"""

velocity_grammar_string = """
S -> a b b a
a -> 100 b 100 | 80 b 80 | 60 b 60 | 40 b 40
b -> 100 b 100 | 80 b 80 | 60 b 60 | 40 40 40
"""

#generators

pitch_generator = ListGenerator(pitch_grammar_string, 8, "pitch")
duration_generator = ListGenerator(duration_grammar_string, 8, "duration")
velocity_generator = ListGenerator(velocity_grammar_string, 8, "velocity")

#song
song = Song(num_bars=8, ioi=2.0, pitch_generator=pitch_generator, duration_generator=duration_generator, velocity_generator=velocity_generator, generate_every_bar=True)

song.make_bar_list()

song.make_midi_file("sk3_test02_melody.mid")

#a melodic counterpoint

pitch_grammar_string = """
S -> a b b a
a -> 60 b 60 | 62 b 62 | 64 b 64 | 48 b 48 | 50 b 50
b -> 55 b 55 | 57 b 57 | 48 b 48 | 43 b 43 | 36 29 36
"""

duration_grammar_string = """
S -> a b b a
a -> 1.5 a 1.5 | 1.3 a 1.0 | 1.0 b 1.0 | 0.5 b 0.5
b -> 1.0 b 1.0 | 0.5 b 0.5 | 0.25 0.25 0.25
"""

velocity_grammar_string = """
S -> a b b a
a -> 100 b 100 | 80 b 80 | 60 b 60 | 40 b 40
b -> 100 b 100 | 80 b 80 | 60 b 60 | 40 40 40
"""

#generators

pitch_generator = ListGenerator(pitch_grammar_string, 8, "pitch")
duration_generator = ListGenerator(duration_grammar_string, 8, "duration")
velocity_generator = ListGenerator(velocity_grammar_string, 8, "velocity")

#song
song = Song(num_bars=8, ioi=2.0, pitch_generator=pitch_generator, duration_generator=duration_generator, velocity_generator=velocity_generator, generate_every_bar=True)

song.make_bar_list()

song.make_midi_file("sk3_test02_counterpoint.mid")

