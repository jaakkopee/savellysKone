from midiutil import MIDIFile
import random
# create MIDI file with one track
midi_file = MIDIFile(numTracks=1)


class Note:
    def __init__(self):
        self.pitch = 60
        self.alkuaika = 0
        self.duration = 1
        self.dyn = 10
        return

class Bar:
    def __init__(self):
        self.noteList = []
        self.duration = 8
        return
    
    def fillNoteList(self, toneList):
        isku = 10
        delta = 0
        for t in toneList:
            tn = Note()
            tn.pitch = t
            tn.dyn=isku
            tn.alkuaika = delta
            self.noteList.append(tn)
            isku+=10
            delta+=1
        return

    def transposeNoteList(self, semitone):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].pitch+=semitone
        return
    
    def tnlRandom(self):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].pitch+=random.randint(-12, 24)
        return
    

tahti = Bar()
tahti.fillNoteList([60,60,60,64,62,62,62,65])
tahti.transposeNoteList(6)
tahti.tnlRandom()

tahti2 = Bar()
tahti2.fillNoteList([60,60,60,64,62,62,62,65])
tahti2.tnlRandom()

tahti3 = Bar()
tahti3.fillNoteList([60,60,60,64,62,62,62,65])

bars = [tahti, tahti2, tahti3]
gra = [0,0,1,1,2,2,1,1,0]

talku = 0
for g in gra:
    currentbar = bars[g]
    tahdinalkuaika=talku
    for n in currentbar.noteList:
        midi_file.addNote(0,0,n.pitch, n.alkuaika+tahdinalkuaika, n.duration, n.dyn)
    talku+=currentbar.duration

# write MIDI data to a file
with open("output.mid", "wb") as f:
    midi_file.writeFile(f)
