import savellysKone as sk


song = sk.Song()
sk.globalToneList = [36, 36, 42, 38]
song.generateBars(8, 4, 0.3, 0.25, True, 1.5, 8.4, True, 1.5, 0.23, True, 0.666, 48)
grammar = [i for i in range(len(song.barList))]
song.addGrammar(grammar)

song.writeMidiFile("Rumputesti10.mid", tempo=128)
