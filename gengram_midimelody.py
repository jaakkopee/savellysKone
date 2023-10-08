import gengramparser as ggp
import time
import sys
import mido
import rtmidi
import threading

midi_out = rtmidi.MidiOut()
midi_out.open_virtual_port("gengram_midimelody")

class MelodyIterator(threading.Thread):
    def __init__(self, melody, start):
        threading.Thread.__init__(self)
        self.melody = melody
        self.index = start
        self.running = True

    def run(self):
        while self.running:
            note = self.melody[self.index]
            self.index += 1
            if self.index >= len(self.melody):
                self.index = 0
            midi_out.send_message(mido.Message("note_on", note=note, velocity=127).bytes())
            time.sleep(0.5)
            midi_out.send_message(mido.Message("note_off", note=note, velocity=127).bytes())

    def stop(self):
        self.running = False

def play_melody(melody):
    melody_iterator = MelodyIterator(melody, 0)
    melody_iterator.start()
    input("Press enter to stop")
    melody_iterator.stop()

def generate_melody(grammar, symbol, depth):
    melody = ggp.generate(grammar, symbol, depth)
    melody = melody.split()
    melody = [int(note) for note in melody]
    return melody

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 gengram_midimelody.py <grammar_file> <depth>")
        sys.exit(1)

    grammar_file = sys.argv[1]
    depth = int(sys.argv[2])

    with open(grammar_file) as f:
        grammar = ggp.parse_grammar(f)

    print(grammar)
    melody = generate_melody(grammar, "S", depth)
    print(melody)
    play_melody(melody)

if __name__ == "__main__":
    main()



    