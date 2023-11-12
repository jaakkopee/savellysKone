import savellysKone3 as sk3

# This is a script to create a piece of music using the savellysKone3 module.

#----bass line ------
# grammar for pitch
pitch_grammar = """
$S -> $phrase0 | $phrase1 | $phrase2 | $phrase3
$phrase0 -> $note0_0 $note0_1 $note0_2 $note0_3 $note0_4 $note0_5 $note0_6 $note0_7
$note0_0 -> 36 | 48 | 43 | 55
$note0_1 -> 40 | 52 | 47 | 59
$note0_2 -> 44 | 56 | 51 | 63
$note0_3 -> 48 | 60 | 55 | 67
$note0_4 -> 52 | 64 | 59 | 71
$note0_5 -> 56 | 68 | 63 | 75
$note0_6 -> 60 | 72 | 67 | 79
$note0_7 -> 64 | 76 | 71 | 83
$phrase1 -> $note1_0 $note1_1 $note1_2 $note1_3 $note1_4 $note1_5 $note1_6 $note1_7
$note1_0 -> 32 | 44 | 39 | 51
$note1_1 -> 36 | 48 | 43 | 55
$note1_2 -> 40 | 52 | 47 | 59
$note1_3 -> 44 | 56 | 51 | 63
$note1_4 -> 48 | 60 | 55 | 67
$note1_5 -> 52 | 64 | 59 | 71
$note1_6 -> 56 | 68 | 63 | 75
$note1_7 -> 60 | 72 | 67 | 79
$phrase2 -> $note2_0 $note2_1 $note2_2 $note2_3 $note2_4 $note2_5 $note2_6 $note2_7
$note2_0 -> 40 | 52 | 47 | 59
$note2_1 -> 44 | 56 | 51 | 63
$note2_2 -> 48 | 60 | 55 | 67
$note2_3 -> 52 | 64 | 59 | 71
$note2_4 -> 56 | 68 | 63 | 75
$note2_5 -> 60 | 72 | 67 | 79
$note2_6 -> 64 | 76 | 71 | 83
$note2_7 -> 68 | 80 | 75 | 87
$phrase3 -> $note3_0 $note3_1 $note3_2 $note3_3 $note3_4 $note3_5 $note3_6 $note3_7
$note3_0 -> 39 | 51 | 46 | 58
$note3_1 -> 43 | 55 | 50 | 62
$note3_2 -> 47 | 59 | 54 | 66
$note3_3 -> 51 | 63 | 58 | 70
$note3_4 -> 55 | 67 | 62 | 74
$note3_5 -> 59 | 71 | 66 | 78
$note3_6 -> 63 | 75 | 70 | 82
$note3_7 -> 67 | 79 | 74 | 86
"""

#grammar for duration
duration_grammar = """
$S -> $phrase0 | $phrase0 | $phrase0 | $phrase0 | $phrase0 | $phrase0 | $phrase0 | $phrase0
$phrase0 -> 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1 | 0.2 0.2 0.2 0.2 0.2 0.2 
"""

#grammar for velocity
velocity_grammar = """
$S -> $phrase0 | $phrase1 | $phrase2 | $phrase3
$phrase0 -> 100 100 100 100 100 100 100 100 | 80 80 80 80 80 80 80 80 | 60 60 60 60 60 60 60 60
$phrase1 -> 100 100 100 100 100 100 100 100 | 80 80 80 80 80 80 80 80 | 60 60 60 60 60 60 60 60
$phrase2 -> 100 100 100 100 100 100 100 100 | 80 80 80 80 80 80 80 80 | 60 60 60 60 60 60 60 60
$phrase3 -> 100 100 100 100 100 100 100 100 | 80 80 80 80 80 80 80 80 | 60 60 60 60 60 60 60 60
"""

#generators for pitch, duration and velocity
pitch_generator = sk3.ListGenerator(pitch_grammar, 8, "pitch")
duration_generator = sk3.ListGenerator(duration_grammar, 8, "duration")
velocity_generator = sk3.ListGenerator(velocity_grammar, 8, "velocity")

# create a track
song = sk3.Song(num_bars=16, ioi=0.75, generate_every_bar=True, pitch_generator=pitch_generator, duration_generator=duration_generator, velocity_generator=velocity_generator, name="bassline02")
song.make_bar_list()
song.modulate_velocity_with_sin_phase_by_bar(freq=1.5, amp=0.3)
song.modulate_onset_with_sin_phase_by_bar(freq=0.75, amp=0.8)
song.make_midi_file("bassline02_2.mid")

#----strings-----
# grammar for pitch
pitch_grammar = """
$S -> $phrase0 | $phrase1 | $phrase2 | $phrase3
$phrase0 -> $note0_0 $note0_1 $note0_2 $note0_3 $note0_4 $note0_5 $note0_6 $note0_7
$note0_0 -> 48 | 60 | 55 | 67
$note0_1 -> 52 | 64 | 59 | 71
$note0_2 -> 56 | 68 | 63 | 75
$note0_3 -> 60 | 72 | 67 | 79
$note0_4 -> 64 | 76 | 71 | 83
$note0_5 -> 68 | 80 | 75 | 87
$note0_6 -> 72 | 84 | 79 | 91
$note0_7 -> 76 | 88 | 83 | 95
$phrase1 -> $note1_0 $note1_1 $note1_2 $note1_3 $note1_4 $note1_5 $note1_6 $note1_7
$note1_0 -> 48 | 60 | 55 | 67
$note1_1 -> 52 | 64 | 59 | 71
$note1_2 -> 56 | 68 | 63 | 75
$note1_3 -> 60 | 72 | 67 | 79
$note1_4 -> 64 | 76 | 71 | 83
$note1_5 -> 68 | 80 | 75 | 87
$note1_6 -> 72 | 84 | 79 | 91
$note1_7 -> 76 | 88 | 83 | 95
$phrase2 -> $note2_0 $note2_1 $note2_2 $note2_3 $note2_4 $note2_5 $note2_6 $note2_7
$note2_0 -> 48 | 60 | 55 | 67
$note2_1 -> 52 | 64 | 59 | 71
$note2_2 -> 56 | 68 | 63 | 75
$note2_3 -> 60 | 72 | 67 | 79
$note2_4 -> 64 | 76 | 71 | 83
$note2_5 -> 68 | 80 | 75 | 87
$note2_6 -> 72 | 84 | 79 | 91
$note2_7 -> 76 | 88 | 83 | 95
$phrase3 -> $note3_0 $note3_1 $note3_2 $note3_3 $note3_4 $note3_5 $note3_6 $note3_7
$note3_0 -> 48 | 60 | 55 | 67
$note3_1 -> 52 | 64 | 59 | 71
$note3_2 -> 56 | 68 | 63 | 75
$note3_3 -> 60 | 72 | 67 | 79
$note3_4 -> 64 | 76 | 71 | 83
$note3_5 -> 68 | 80 | 75 | 87
$note3_6 -> 72 | 84 | 79 | 91
$note3_7 -> 76 | 88 | 83 | 95
"""

#grammar for duration
duration_grammar = """
$S -> $phrase0 $phrase0 $phrase0 $phrase0 $phrase0 $phrase0 $phrase0 $phrase0
$phrase0 -> 2.75 2.75 2.75 2.75 2.75 2.75 2.75 2.75
"""

#grammar for velocity
velocity_grammar = """
$S -> $phrase0 | $phrase1 | $phrase2 | $phrase3
$phrase0 -> 100 100 100 100 100 100 100 100 | 80 80 80 80 80 80 80 80 | 60 60 60 60 60 60 60 60
$phrase1 -> 100 100 100 100 100 100 100 100 | 80 80 80 80 80 80 80 80 | 60 60 60 60 60 60 60 60
$phrase2 -> 100 100 100 100 100 100 100 100 | 80 80 80 80 80 80 80 80 | 60 60 60 60 60 60 60 60
$phrase3 -> 100 100 100 100 100 100 100 100 | 80 80 80 80 80 80 80 80 | 60 60 60 60 60 60 60 60
"""

#generators for pitch, duration and velocity
pitch_generator = sk3.ListGenerator(pitch_grammar, 8, "pitch")
duration_generator = sk3.ListGenerator(duration_grammar, 8, "duration")
velocity_generator = sk3.ListGenerator(velocity_grammar, 8, "velocity")

# create a track
song = sk3.Song(num_bars=16, ioi=3.0, generate_every_bar=True, pitch_generator=pitch_generator, duration_generator=duration_generator, velocity_generator=velocity_generator, name="strings01")
song.make_bar_list()
song.modulate_velocity_with_sin_phase_by_bar(freq=1.5, amp=0.3)
song.modulate_onset_with_sin_phase_by_bar(freq=0.75, amp=0.8)
song.make_midi_file("strings01_2.mid")

#-----bass02-----
# grammar for pitch
pitch_grammar = """
$S -> $phrase0 | $phrase0 | $phrase0 | $phrase0 | $phrase0 | $phrase0 | $phrase0 | $phrase0
$phrase0 -> $note0_0 $note0_1 $note0_2 $note0_3 $note0_4 $note0_5 $note0_6 $note0_7
$note0_0 -> 36
$note0_1 -> 36
$note0_2 -> 36
$note0_3 -> 36
$note0_4 -> 42
$note0_5 -> 36
$note0_6 -> 36
$note0_7 -> 36
"""

#grammar for duration
duration_grammar = """
$S -> 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1
"""

#grammar for velocity
velocity_grammar = """
$S -> 100 100 100 100 100 100 100 100
"""

#generators for pitch, duration and velocity
pitch_generator = sk3.ListGenerator(pitch_grammar, 8, "pitch")
duration_generator = sk3.ListGenerator(duration_grammar, 8, "duration")
velocity_generator = sk3.ListGenerator(velocity_grammar, 8, "velocity")


# create a track
song = sk3.Song(num_bars=16, ioi=0.25, generate_every_bar=True, pitch_generator=pitch_generator, duration_generator=duration_generator, velocity_generator=velocity_generator, name="bass02")
song.make_bar_list()
song.modulate_velocity_with_sin_phase_by_bar(freq=1.5, amp=0.3)
song.modulate_onset_with_sin_phase_by_bar(freq=0.75, amp=0.8)
song.make_midi_file("bass02_2.mid")
