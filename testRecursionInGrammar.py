import savellysKone3 as sk3

# Updated: This grammar previously had left recursion ($phrase0 -> $phrase0 ...)
# which would cause infinite loops. Changed to valid right recursion.
pitch_grammar = """
$S -> $phrase0
$phrase0 -> 55 $phrase0 | 66 $phrase0 | 77 $phrase0 | 55 | 66 | 77
"""

#grammar for duration
duration_grammar = """
$S -> $phrase0
$phrase0 -> 0.25 0.75 0.25 0.75 0.25 0.75 0.25 0.75
"""

#grammar for velocity
velocity_grammar = """
$S -> $phrase0
$phrase0 -> 100 72 62 52 100 66 127 55
"""

pitch_generator = sk3.ListGenerator(pitch_grammar, 3, "pitch")
duration_generator = sk3.ListGenerator(duration_grammar, 3, "duration")
velocity_generator = sk3.ListGenerator(velocity_grammar, 3, "velocity")

song = sk3.Song(pitch_generator=pitch_generator,
                duration_generator=duration_generator,
                velocity_generator=velocity_generator,
                num_bars=6,
                ioi=2.0,
                name="test recursion in grammar",
                generate_every_bar=True)

print("generating bars...")
song.make_bar_list()
print ("...bars generated")

song.make_midi_file("testRecursionInGrammar.mid")
