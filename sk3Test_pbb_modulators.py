import savellysKone3 as sk3

#test modulators

#grammars
pitch_grammar = """
$S -> $phrase0 $phrase0 $phrase0 $phrase0
$phrase0 -> 60 60 60 60 60 60 60 60
"""

duration_grammar = """
$S -> $phrase0 $phrase0 $phrase0 $phrase0
$phrase0 -> 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5
"""

velocity_grammar = """
$S -> $phrase0 $phrase0 $phrase0 $phrase0
$phrase0 -> 100 100 100 100 100 100 100 100
"""

#generators for pitch, duration and velocity
pitch_generator = sk3.ListGenerator(pitch_grammar, 8, "pitch")
duration_generator = sk3.ListGenerator(duration_grammar, 8, "duration")
velocity_generator = sk3.ListGenerator(velocity_grammar, 8, "velocity")

# create a track
song = sk3.Song(pitch_generator=pitch_generator,
                duration_generator=duration_generator,
                velocity_generator=velocity_generator,
                num_bars=8,
                ioi=0.5,
                name="test modulators",
                generate_every_bar=True)

song.make_bar_list()

song.modulate_duration_with_sin_phase_by_bar(1.0, 0.3)
song.modulate_velocity_with_sin_phase_by_bar(1.0, 30.0)
song.modulate_pitch_with_sin_phase_by_bar(1.0, 30.0)
song.modulate_onset_with_sin_phase_by_bar(1.0, 0.6)

song.make_midi_file("sk3Test_modulators.mid")
