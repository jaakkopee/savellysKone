import savellysKone3 as sk
import random
import os
import time

#----bass line ------
# grammar for pitch
pitch_grammar = """
$S -> $phrase0 | $phrase1 | $phrase2 | $phrase3
$phrase0 -> $subphrase0_0 $subphrase0_1
$subphrase0_0 -> $note0_0 $note0_1 $note0_2 $note0_3 $note0_4 $note0_5 $note0_6 $note0_7
$note0_0 -> 48 | 60 | 55 | 67
$note0_1 -> 52 | 64 | 59 | 71
$note0_2 -> 56 | 68 | 63 | 75
$note0_3 -> 60 | 72 | 67 | 79
$note0_4 -> 64 | 76 | 71 | 83
$note0_5 -> 68 | 80 | 75 | 87
$note0_6 -> 72 | 84 | 79 | 91
$note0_7 -> 76 | 88 | 83 | 95
$subphrase0_1 -> $note1_0 $note1_1 $note1_2 $note1_3 $note1_4 $note1_5 $note1_6 $note1_7
$note1_0 -> 48 | 60 | 55 | 67
$note1_1 -> 52 | 64 | 59 | 71
$note1_2 -> 56 | 68 | 63 | 75
$note1_3 -> 60 | 72 | 67 | 79
$note1_4 -> 64 | 76 | 71 | 83
$note1_5 -> 68 | 80 | 75 | 87
$note1_6 -> 72 | 84 | 79 | 91
$note1_7 -> 76 | 88 | 83 | 95
$phrase1 -> $subphrase1_0 $subphrase1_1
$subphrase1_0 -> $note2_0 $note2_1 $note2_2 $note2_3 $note2_4 $note2_5 $note2_6 $note2_7
$note2_0 -> 48 | 60 | 55 | 67
$note2_1 -> 52 | 64 | 59 | 71
$note2_2 -> 56 | 68 | 63 | 75
$note2_3 -> 60 | 72 | 67 | 79
$note2_4 -> 64 | 76 | 71 | 83
$note2_5 -> 68 | 80 | 75 | 87
$note2_6 -> 72 | 84 | 79 | 91
$note2_7 -> 76 | 88 | 83 | 95
$subphrase1_1 -> $note3_0 $note3_1 $note3_2 $note3_3 $note3_4 $note3_5 $note3_6 $note3_7
$note3_0 -> 69 | 81 | 76 | 88
$note3_1 -> 73 | 85 | 80 | 92
$note3_2 -> 77 | 89 | 84 | 96
$note3_3 -> 81 | 93 | 88 | 100
$note3_4 -> 84 | 96 | 91 | 103
$note3_5 -> 88 | 100 | 95 | 107
$note3_6 -> 92 | 104 | 99 | 111
$note3_7 -> 96 | 108 | 103 | 115
$phrase2 -> $subphrase2_0 $subphrase2_1
$subphrase2_0 -> $note4_0 $note4_1 $note4_2 $note4_3 $note4_4 $note4_5 $note4_6 $note4_7
$note4_0 -> 32 | 44 | 39 | 51
$note4_1 -> 36 | 48 | 43 | 55
$note4_2 -> 40 | 52 | 47 | 59
$note4_3 -> 44 | 56 | 51 | 63
$note4_4 -> 48 | 60 | 55 | 67
$note4_5 -> 52 | 64 | 59 | 71
$note4_6 -> 56 | 68 | 63 | 75
$note4_7 -> 60 | 72 | 67 | 79
$subphrase2_1 -> $note5_0 $note5_1 $note5_2 $note5_3 $note5_4 $note5_5 $note5_6 $note5_7
$note5_0 -> 36 | 48 | 43 | 55
$note5_1 -> 40 | 52 | 47 | 59
$note5_2 -> 44 | 56 | 51 | 63
$note5_3 -> 48 | 60 | 55 | 67
$note5_4 -> 52 | 64 | 59 | 71
$note5_5 -> 56 | 68 | 63 | 75
$note5_6 -> 60 | 72 | 67 | 79
$note5_7 -> 64 | 76 | 71 | 83
$phrase3 -> $subphrase3_0 $subphrase3_1
$subphrase3_0 -> $note6_0 $note6_1 $note6_2 $note6_3 $note6_4 $note6_5 $note6_6 $note6_7
$note6_0 -> 61 | 73 | 68 | 80
$note6_1 -> 65 | 77 | 72 | 84
$note6_2 -> 69 | 81 | 76 | 88
$note6_3 -> 73 | 85 | 80 | 92
$note6_4 -> 77 | 89 | 84 | 96
$note6_5 -> 81 | 93 | 88 | 100
$note6_6 -> 85 | 97 | 92 | 104
$note6_7 -> 89 | 101 | 96 | 108
$subphrase3_1 -> $note7_0 $note7_1 $note7_2 $note7_3 $note7_4 $note7_5 $note7_6 $note7_7
$note7_0 -> 52 | 64 | 59 | 71
$note7_1 -> 56 | 68 | 63 | 75
$note7_2 -> 60 | 72 | 67 | 79
$note7_3 -> 64 | 76 | 71 | 83
$note7_4 -> 68 | 80 | 75 | 87
$note7_5 -> 72 | 84 | 79 | 91
$note7_6 -> 76 | 88 | 83 | 95
$note7_7 -> 80 | 92 | 87 | 99
"""

#grammar for duration
duration_grammar = """
$S -> $phrase0 $phrase0 $phrase0 $phrase0 $phrase0 $phrase0 $phrase0 $phrase0
$phrase0 -> $subphrase0_0 $subphrase0_1
$subphrase0_0 -> $dur0 $dur0 $dur0 $dur0 $dur0 $dur0 $dur0 $dur0
$dur0 -> 0.5 | 0.25 | 0.75 | 1.0
$subphrase0_1 -> $dur1 $dur1 $dur1 $dur1 $dur1 $dur1 $dur1 $dur1
$dur1 -> 0.25 | 0.5 | 0.75 | 1.0
"""

#grammar for velocity
velocity_grammar = """
$S -> $phrase0 $phrase0 $phrase0 $phrase0 $phrase0 $phrase0 $phrase0 $phrase0
$phrase0 -> $subphrase0_0 $subphrase0_1
$subphrase0_0 -> $velocity_0 $velocity_0 $velocity_0 $velocity_0 $velocity_0 $velocity_0 $velocity_0 $velocity_0
$velocity_0 -> 127 | 100 | 80 | 60
$subphrase0_1 -> $velocity_1 $velocity_1 $velocity_1 $velocity_1 $velocity_1 $velocity_1 $velocity_1 $velocity_1
$velocity_1 -> 100 | 80 | 60 | 40
"""

#Generators for pitch, duration and articulation
pitch_generator = sk.ListGenerator(grammar_str=pitch_grammar, min_length=8, type="pitch")
duration_generator = sk.ListGenerator(grammar_str=duration_grammar, min_length=8, type="duration")
velocity_generator = sk.ListGenerator(grammar_str=velocity_grammar, min_length=8, type="velocity")

#Create a song object
song = sk.Song(name="grovbaslin_modulated",
               num_bars=12, ioi=1.0,
               pitch_generator=pitch_generator,
               duration_generator=duration_generator,
               velocity_generator=velocity_generator,
               generate_every_bar=True)

#Generate the song
song.make_bar_list()
song.modulate_onset_with_sin_phase_by_bar(amp=0.32, freq=2.5)
song.make_midi_file(filename="grovbaslin_modulated.mid")

