import savellysKone3 as sk3

# This is a script to create a piece of music using the savellysKone3 module.

# The piece constists of a high melody track and a low melody track plus a percussion track.

#------------high melody track-----------------

# grammar for pitch
pitch_grammar = """
$S -> $phrase0 $phrase1 $phrase2 $phrase3
$phrase0 -> $note0_0 $note0_1 $note0_2 $note0_3 $note0_4 $note0_5 $note0_6 $note0_7
$note0_0 -> 72 | 60 | 67 | 79
$note0_1 -> 75 | 63 | 70 | 82
$note0_2 -> 77 | 65 | 72 | 84
$note0_3 -> 79 | 67 | 74 | 86
$note0_4 -> 80 | 68 | 75 | 87
$note0_5 -> 82 | 70 | 77 | 89
$note0_6 -> 84 | 72 | 79 | 91
$note0_7 -> 86 | 74 | 81 | 93
$phrase1 -> $note1_0 $note1_1 $note1_2 $note1_3 $note1_4 $note1_5 $note1_6 $note1_7
$note1_0 -> 40 | 52 | 59 | 71
$note1_1 -> 42 | 54 | 61 | 73
$note1_2 -> 44 | 56 | 63 | 75
$note1_3 -> 45 | 57 | 64 | 76
$note1_4 -> 47 | 59 | 66 | 78
$note1_5 -> 49 | 61 | 68 | 80
$note1_6 -> 51 | 63 | 70 | 82
$note1_7 -> 52 | 64 | 71 | 83
$phrase2 -> $note2_0 $note2_1 $note2_2 $note2_3 $note2_4 $note2_5 $note2_6 $note2_7
$note2_0 -> 48 | 60 | 67 | 79
$note2_1 -> 50 | 62 | 69 | 81
$note2_2 -> 52 | 64 | 71 | 83
$note2_3 -> 53 | 65 | 72 | 84
$note2_4 -> 55 | 67 | 74 | 86
$note2_5 -> 57 | 69 | 76 | 88
$note2_6 -> 59 | 71 | 78 | 90
$note2_7 -> 60 | 72 | 79 | 91
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
$phrase0 -> $note0_0 $note0_1 $note0_2 $note0_3 $note0_0 $note0_1 $note0_2 $note0_3
$note0_0 -> 1 | 2 | 4 | 8
$note0_1 -> 0.8 | 1.8 | 3.8 | 7.8
$note0_2 -> 0.6 | 1.6 | 3.6 | 7.6
$note0_3 -> 0.4 | 1.4 | 3.4 | 7.4
"""

#grammar for velocity
velocity_grammar = """
$S -> $phrase0 $phrase0 $phrase0 $phrase0
$phrase0 -> $note0_0 $note0_1 $note0_2 $note0_3 $note0_0 $note0_1 $note0_2 $note0_3
$note0_0 -> 120 | 100 | 80 | 60
$note0_1 -> 110 | 90 | 70 | 50
$note0_2 -> 100 | 80 | 60 | 40
$note0_3 -> 90 | 70 | 50 | 30
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
                ioi=8.0,
                name="high melody",
                generate_every_bar=True)

song.make_bar_list()

song.make_midi_file("skAmbient2_high_melody.mid")

#------------low melody track-----------------

# grammar for pitch
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
$note1_0 -> 72 | 60 | 67 | 79
$note1_1 -> 75 | 63 | 70 | 82
$note1_2 -> 77 | 65 | 72 | 84
$note1_3 -> 79 | 67 | 74 | 86
$note1_4 -> 80 | 68 | 75 | 87
$note1_5 -> 82 | 70 | 77 | 89
$note1_6 -> 84 | 72 | 79 | 91
$note1_7 -> 86 | 74 | 81 | 93
$phrase2 -> $note2_0 $note2_1 $note2_2 $note2_3 $note2_4 $note2_5 $note2_6 $note2_7
$note2_0 -> 40 | 52 | 59 | 71
$note2_1 -> 42 | 54 | 61 | 73
$note2_2 -> 44 | 56 | 63 | 75
$note2_3 -> 45 | 57 | 64 | 76
$note2_4 -> 47 | 59 | 66 | 78
$note2_5 -> 49 | 61 | 68 | 80
$note2_6 -> 51 | 63 | 70 | 82
$note2_7 -> 52 | 64 | 71 | 83
$phrase3 -> $note3_0 $note3_1 $note3_2 $note3_3 $note3_4 $note3_5 $note3_6 $note3_7
$note3_0 -> 48 | 60 | 67 | 79
$note3_1 -> 50 | 62 | 69 | 81
$note3_2 -> 52 | 64 | 71 | 83
$note3_3 -> 53 | 65 | 72 | 84
$note3_4 -> 55 | 67 | 74 | 86
$note3_5 -> 57 | 69 | 76 | 88
$note3_6 -> 59 | 71 | 78 | 90
$note3_7 -> 60 | 72 | 79 | 91
"""

#grammar for duration
duration_grammar = """
$S -> $phrase0 $phrase0 $phrase0 $phrase0
$phrase0 -> $note0_0 $note0_1 $note0_2 $note0_3 $note0_0 $note0_1 $note0_2 $note0_3
$note0_0 -> 1 | 2 | 4 | 8
$note0_1 -> 0.8 | 1.8 | 3.8 | 7.8
$note0_2 -> 0.6 | 1.6 | 3.6 | 7.6
$note0_3 -> 0.4 | 1.4 | 3.4 | 7.4
"""

#grammar for velocity
velocity_grammar = """
$S -> $phrase0 $phrase0 $phrase0 $phrase0
$phrase0 -> $note0_0 $note0_1 $note0_2 $note0_3 $note0_0 $note0_1 $note0_2 $note0_3
$note0_0 -> 120 | 100 | 80 | 60
$note0_1 -> 110 | 90 | 70 | 50
$note0_2 -> 100 | 80 | 60 | 40
$note0_3 -> 90 | 70 | 50 | 30
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
                ioi=8.0,
                name="low melody",
                generate_every_bar=True)

song.make_bar_list()

song.make_midi_file("skAmbient2_low_melody.mid")

#------------percussion track-----------------

# grammar for pitch (percussion, General MIDI mapping)
pitch_grammar = """
$S -> $phrase0 $phrase1
$phrase0 -> $note0_0 $note0_1 $note0_2 $note0_3
$note0_0 -> 35 | 36 | 37 | 38
$note0_1 -> 39 | 40 | 41 | 42
$note0_2 -> 43 | 44 | 45 | 46
$note0_3 -> 47 | 48 | 49 | 50
$phrase1 -> $note1_0 $note1_1 $note1_2 $note1_3
$note1_0 -> 51 | 52 | 53 | 54
$note1_1 -> 55 | 56 | 57 | 58
$note1_2 -> 59 | 60 | 61 | 62
$note1_3 -> 63 | 64 | 65 | 66
"""

#grammar for duration
duration_grammar = """
$S -> $phrase0 $phrase0
$phrase0 -> 0.1 0.1 0.1 0.1
"""

#grammar for velocity
velocity_grammar = """
$S -> $phrase0 $phrase0
$phrase0 -> 100 100 100 100
"""

#generators for pitch, duration and velocity
pitch_generator = sk3.ListGenerator(pitch_grammar, 4, "pitch")
duration_generator = sk3.ListGenerator(duration_grammar, 4, "duration")
velocity_generator = sk3.ListGenerator(velocity_grammar, 4, "velocity")

# create a track
song = sk3.Song(pitch_generator=pitch_generator,
                duration_generator=duration_generator,
                velocity_generator=velocity_generator,
                num_bars=64,
                ioi=0.5,
                name="percussion",
                generate_every_bar=True)

song.make_bar_list()

song.make_midi_file("skAmbient2_percussion.mid")
