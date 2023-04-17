from midiutil import MIDIFile
import random, math
import musical_scales as ms
"""
acoustic
aeolian
algerian
super locrian
augmented
bebop dominant
blues
chromatic
dorian
double harmonic
enigmatic
flamenco
romani
half-diminished
harmonic major
harmonic minor
hijaroshi
hungarian minor
hungarian major
in
insen
ionian
iwato
locrian
lydian augmented
lydian
locrian major
pentatonic major
melodic minor ascending
melodic minor descending
pentatonic minor
mixolydian
neapolitan major
neapolitan minor
octatonic c-d
octatonic c-c#
persian
phrygian dominant
phrygian
prometheus
harmonics
tritone
two-semitone tritone
ukranian dorian
whole-tone scale
yo
"""
# create MIDI file with one track
midi_file = MIDIFile(numTracks=1)

noteDict = {
    'C3': 60,
    'C#3': 61,
    'Db3': 61,
    'D3': 62,
    'D#3': 63,
    'Eb3': 63,
    'E3': 64,
    'F3': 65,
    'F#3': 66,
    'Gb3': 66,
    'G3': 67,
    'G#3': 68,
    'Ab3': 68,
    'A3': 69,
    'A#3': 70,
    'Bb3': 70,
    'B3': 71,
    'Cb3': 71,
    'B#3': 72,
    'C4': 72,
    'C#4': 73,
    'Db4': 73,
    'D4': 74,
    'D#4': 75,
    'Eb4': 75,
    'E4': 76,
    'F4': 77,
    'F#4': 78,
    'Gb4': 78,
    'G4': 79,
    'G#4': 80,
    'Ab4': 80,
    'A4': 81,
    'A#4': 82,
    'Bb4': 82,
    'B4': 83,
    'Cb4': 83,
    'B#4': 84,
    'C5': 84
}


class Note:
    def __init__(self):
        self.pitch = 60
        self.alkuaika = 0
        self.duration = 1
        self.dyn = 100
        return

class Bar:
    def __init__(self, duration=8, deltaPlus=0.75):
        self.noteList = []
        self.duration = duration
        self.deltaPlus = deltaPlus
        return

    def generateNoteList(self, noteCount, rootNote='D', scale='dorian'):
        noteColl = []
        scale = ms.scale(rootNote, scale)
        
        for i in scale:
            noteColl.append(noteDict[i.midi])

        notes=[]
        for i in range(noteCount):
            if len(notes)==0:
                notes.append(random.choice(noteColl))
            note1 = notes[-1]
            note2 = random.choice(noteColl)
            while abs(note1-note2) > 4:
                note2 = random.choice(noteColl)
            notes.append(note1)
            notes.append(note2)
        self.fillNoteList(notes)
    
    def fillNoteList(self, toneList):
        delta = 0
        for t in toneList:
            tn = Note()
            tn.pitch = t
            tn.dyn=70
            tn.alkuaika = delta
            tn.duration = 0.1
            self.noteList.append(tn)
            delta+=self.deltaPlus
        return

    def reverseNoteList(self):
        pitches = [i.pitch for i in self.noteList]
        pitches.reverse()
        for i in range(len(self.noteList)):
            self.noteList[i].pitch = pitches[i]
        return

    def setNoteListDurations(self, duration):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].duration = duration
        return
            
    def transposeNoteList(self, semitone):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].pitch+=semitone
        return
    
    def randomPitch(self):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].pitch+=random.randint(-12, 24)
        return
    
    def randomAlkuaika(self):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].alkuaika+=(random.random()-0.5)*0.8
            if self.noteList[noteNumber].alkuaika < 0:
                self.noteList[noteNumber].alkuaika = 0
        return

    def randomDuration(self, factor=0.6):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].duration+=(random.random()-0.5)*factor
            if self.noteList[noteNumber].duration < 0:
                self.noteList[noteNumber].duration = 0
        return
    

    def randomDyn(self):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].dyn+=random.randint(-5, 5)
        return
    
    def modulateNoteListAlkuaikaWithSinusoid(self, freq, amp):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].alkuaika+=amp*math.sin(freq*(noteNumber/len(self.noteList)))
        return
    
    def modulateNoteListDurationWithSinusoid(self, freq, amp):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].duration+=amp*math.sin(freq*(noteNumber/len(self.noteList)))
        return
    
    def modulateNoteListDynWithSinusoid(self, freq, amp):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].dyn+=int(round(amp*math.sin(freq*(noteNumber/len(self.noteList)))))
            if self.noteList[noteNumber].dyn > 127:
                self.noteList[noteNumber].dyn = 127
            if self.noteList[noteNumber].dyn < 0:
                self.noteList[noteNumber].dyn = 0

        return
    
class Song:
    def __init__(self):
        self.barList = []
        self.gra = []
        self.talku = 0
        return
    
    def addBars(self, bars):
        for bar in bars:
            self.barList.append(bar)
        return
    
    def addGrammar(self, grammar):
        for gra in grammar:
            self.gra.append(gra)
        return

    def generateBars(self,
                     barCount=8,
                     notesPerBar=6,
                     rootNote='D',
                     scale='dorian',
                     duration=8,
                     deltaPlus=0.75):
        
        bars = []
        
        #preliminary actions
        for i in range(barCount):
            bar = Bar(duration, deltaPlus)
            bar.generateNoteList(notesPerBar, rootNote, scale)
            bar.setNoteListDurations(0.61)
            bars.append(bar)

        #start with sinusoid modulation of alkuaika
        for barNumber in range(len(bars)):
            if barNumber%1==0:
                bars[barNumber].modulateNoteListAlkuaikaWithSinusoid(1, -0.18)


        #then sinusoid modulation of duration
        for barNumber in range(len(bars)):
            if barNumber%1==0:
                bars[barNumber].modulateNoteListDurationWithSinusoid(1, -0.61)

        #then sinusoid modulation of dyn
        for barNumber in range(len(bars)):
            if barNumber%1==0:
                bars[barNumber].modulateNoteListDynWithSinusoid(1, 20)

        #then reverse
        for barNumber in range(len(bars)):
            if barNumber%11==0:
                bars[barNumber].reverseNoteList()

        #then transpose
        for barNumber in range(len(bars)):
            if barNumber%4==0:
                bars[barNumber].transposeNoteList(7)

            if barNumber%5==0:
                bars[barNumber].transposeNoteList(-7)


        self.addBars(bars)


    def scrambleGrammar(self):
        random.shuffle(self.gra)
        return

    def transpose(self, semitone):
        for barNumber in range(len(self.barList)):
            for noteNumber in range(len(self.barList[barNumber].noteList)):
                self.barList[barNumber].noteList[noteNumber].pitch+=semitone
        return


    def outputToMidiFile(self):
        midi_file = MIDIFile(numTracks=1)
        midi_file.addTempo(0, 0, 120)
        self.talku = 0
        for g in self.gra:
            currentbar = self.barList[g]
            songTime = self.talku
            for n in currentbar.noteList:
                midi_file.addNote(0 , 0, n.pitch, n.alkuaika+songTime, n.duration, n.dyn)
            self.talku+=currentbar.duration

        return midi_file
    
    def writeMidiFile(self, filename):
        with open(filename, "wb") as output_file:
            self.outputToMidiFile().writeFile(output_file)
        return
    


if __name__ == "__main__":
    song = Song()
    song.generateBars(32, 6, 'C', 'harmonics', 4, 1.5)
    grammar = [i for i in range(len(song.barList))]
    song.addGrammar(grammar)
    song.scrambleGrammar()

    song.writeMidiFile("skTest02.mid")

