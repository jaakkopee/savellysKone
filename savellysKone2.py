from midiutil import MIDIFile
import random, math
import musical_scales as ms
import gengramparser as ggp
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

def create_global_tonelist():
    with open("in_grammar.txt") as in_grammar_file:
        grammar = ggp.parse_grammar(in_grammar_file)
    in_grammar_file.close()
    globalToneList = ggp.generate(grammar, "S", 256)
    globalToneList = globalToneList.split()
    globalToneList = [int(note) for note in globalToneList]
    return globalToneList

globalToneList = create_global_tonelist()

class Note:
    def __init__(self):
        self.pitch = 60
        self.onset = 0
        self.duration = 1
        self.velocity = 100
        return

class Bar:
    def __init__(self, duration=8, interOnsetInterval = 1.0, onset=0):
        self.toneList = None
        self.noteList = []
        self.duration = duration
        self.interOnsetInterval = interOnsetInterval
        self.bar_onset = onset
        self.endTime = self.bar_onset + self.duration*self.interOnsetInterval
        return

    def generateNoteList(self):
        self.fillNoteList(globalToneList)
        return
        
    def fillNoteList(self, toneList):
        self.noteList=[]
        delta = self.bar_onset
        for t in toneList:
            tn = Note()
            tn.pitch = t
            tn.velocity=70
            tn.onset = delta
            tn.duration = 0.1
            self.noteList.append(tn)
            delta+=self.interOnsetInterval
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
    
    def randomOnset(self):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].onset+=(random.random()-0.5)*0.8
            if self.noteList[noteNumber].onset < 0:
                self.noteList[noteNumber].onset = 0
        return

    def randomDuration(self, factor=0.6):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].duration+=(random.random()-0.5)*factor
            if self.noteList[noteNumber].duration < 0:
                self.noteList[noteNumber].duration = 0
        return
    

    def randomVelocity(self):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].velocity+=random.randint(-5, 5)
        return
    
    def modulateNoteListOnsetsWithSinusoid(self, freq, amp):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].onset+=amp*math.sin(freq*(noteNumber/len(self.noteList)))
        return
    
    def modulateNoteListDurationsWithSinusoid(self, freq, amp):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].duration+=amp*math.sin(freq*(noteNumber/len(self.noteList)))
        return
    
    def modulateNoteListVelocitiesWithSinusoid(self, freq, amp):
        for noteNumber in range(len(self.noteList)):
            self.noteList[noteNumber].velocity+=int(round(amp*math.sin(freq*(noteNumber/len(self.noteList)))))
            if self.noteList[noteNumber].velocity > 127:
                self.noteList[noteNumber].velocity = 127
            if self.noteList[noteNumber].velocity < 0:
                self.noteList[noteNumber].velocity = 0

        return
    
class Song:
    def __init__(self, numBars=4):
        self.barList = []
        self.numBars = numBars
        return

    def generateBarList(self):
        for i in range(self.numBars):
            b = Bar(8, 1.0, i*8)
            b.generateNoteList()
            self.barList.append(b)
        return

    def reverseBarList(self):
        self.barList.reverse()
        return

    def transposeBarList(self, semitone):
        for barNumber in range(len(self.barList)):
            self.barList[barNumber].transposeNoteList(semitone)
        return

    def randomPitch(self):
        for barNumber in range(len(self.barList)):
            self.barList[barNumber].randomPitch()
        return

    def randomOnset(self):
        for barNumber in range(len(self.barList)):
            self.barList[barNumber].randomOnset()
        return

    def randomDuration(self, factor=0.6):
        for barNumber in range(len(self.barList)):
            self.barList[barNumber].randomDuration(factor)
        return

    def randomVelocity(self):
        for barNumber in range(len(self.barList)):
            self.barList[barNumber].randomVelocity()
        return

    def modulateBarListOnsetsWithSinusoid(self, freq, amp):
        for barNumber in range(len(self.barList)):
            self.barList[barNumber].modulateNoteListOnsetsWithSinusoid(freq, amp)
        return

    def modulateBarListDurationsWithSinusoid(self, freq, amp):
        for barNumber in range(len(self.barList)):
            self.barList[barNumber].modulateNoteListDurationsWithSinusoid(freq, amp)
        return

    def modulateBarListVelocitiesWithSinusoid(self, freq, amp):
        for barNumber in range(len(self.barList)):
            self.barList[barNumber].modulateNoteListVelocitiesWithSinusoid(freq, amp)
        return

    def setBarListDurations(self, duration):
        for barNumber in range(len(self.barList)):
            self.barList[barNumber].setNoteListDurations(duration)
        return
    
    def write_midi(self):
        #create your MIDI object
        mf = MIDIFile(1)
        #mf.addTrackName(0, 0, "Sample Track")
        #mf.addTempo(0, 0, 120)
        for barNumber in range(len(self.barList)):
            for noteNumber in range(len(self.barList[barNumber].noteList)):
                mf.addNote(0, 0, self.barList[barNumber].noteList[noteNumber].pitch, self.barList[barNumber].noteList[noteNumber].onset, self.barList[barNumber].noteList[noteNumber].duration, self.barList[barNumber].noteList[noteNumber].velocity)
        with open("test_gengram.mid", 'wb') as outf:
            mf.writeFile(outf)
        return
    
if __name__ == "__main__":
    s = Song(16)
    s.generateBarList()
    s.modulateBarListDurationsWithSinusoid(1, 3.0)
    s.modulateBarListOnsetsWithSinusoid(1, 2.0)
    s.modulateBarListVelocitiesWithSinusoid(2, 2.0)
    s.write_midi()