import savellysKone3 as sk3

#test modulators

#grammars

#grammar for pitch
pitch_grammar = """
$S -> $phrase0 $phrase1 $phrase2 $phrase3
$phrase0 -> $note0_0 $note0_1 $note0_2 $note0_3 $note0_4 $note0_5 $note0_6 $note0_7
$note0_0 -> 36 | 48 | 55 | 67
$note0_1 -> 38 | 50 | 57 | 69
$note0_2 -> 40 | 52 | 59 | 71
$note0_3 -> 41 | 53 | 60 | 72
$note0_4 -> 43 | 55 | 62 | 74
$note0_5 -> 45 | 57 | 64 | 76
$note0_6 -> 47 | 59 | 66 | 78
$note0_7 -> 48 | 60 | 67 | 79

$phrase1 -> $note1_0 $note1_1 $note1_2 $note1_3 $note1_4 $note1_5 $note1_6 $note1_7
$note1_0 -> 36 | 48 | 55 | 67
$note1_1 -> 38 | 50 | 57 | 69
$note1_2 -> 40 | 52 | 59 | 71
$note1_3 -> 41 | 53 | 60 | 72
$note1_4 -> 43 | 55 | 62 | 74
$note1_5 -> 45 | 57 | 64 | 76
$note1_6 -> 47 | 59 | 66 | 78
$note1_7 -> 48 | 60 | 67 | 79

$phrase2 -> $note2_0 $note2_1 $note2_2 $note2_3 $note2_4 $note2_5 $note2_6 $note2_7
$note2_0 -> 36 | 48 | 55 | 67
$note2_1 -> 38 | 50 | 57 | 69
$note2_2 -> 40 | 52 | 59 | 71
$note2_3 -> 41 | 53 | 60 | 72
$note2_4 -> 43 | 55 | 62 | 74
$note2_5 -> 45 | 57 | 64 | 76
$note2_6 -> 47 | 59 | 66 | 78
$note2_7 -> 48 | 60 | 67 | 79

$phrase3 -> $note3_0 $note3_1 $note3_2 $note3_3 $note3_4 $note3_5 $note3_6 $note3_7
$note3_0 -> 36 | 48 | 55 | 67
$note3_1 -> 38 | 50 | 57 | 69
$note3_2 -> 40 | 52 | 59 | 71
$note3_3 -> 41 | 53 | 60 | 72
$note3_4 -> 43 | 55 | 62 | 74
$note3_5 -> 45 | 57 | 64 | 76
$note3_6 -> 47 | 59 | 66 | 78
$note3_7 -> 48 | 60 | 67 | 79

"""

#grammar for duration
duration_grammar = """
$S -> $phrase0 $phrase0 $phrase0 $phrase0
$phrase0 -> 0.25 0.75 0.25 0.75 0.25 0.75 0.25 0.75
"""

#grammar for velocity
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
                ioi=2.0,
                name="test modulators",
                generate_every_bar=True)

song.make_bar_list()

song.modulate_duration_with_sin_phase_by_bar(3.0, 0.03)
song.modulate_velocity_with_sin_phase_by_bar(1.0, 0.1)

song.modulate_onset_with_sin_phase_by_bar(3.0, 0.08)

song.make_midi_file("shadypopsgenerated.mid")

