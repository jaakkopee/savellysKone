#ifndef SINEWAVESYNTH_H
#define SINEWAVESYNTH_H

#include "Envelope.h"
#include <cmath>
#include <memory>
#include <vector>

class Voice {
public:
    Voice();
    
    void noteOn(uint8_t midiNote, uint8_t velocity, double currentTime);
    void noteOff(double currentTime);
    bool isActive() const;
    
    double getSample(double currentTime, uint32_t sampleRate);
    
private:
    uint8_t midiNote;
    uint8_t velocity;
    double frequency;
    double phase;
    bool active;
    Envelope envelope;
    
    double midiNoteToFrequency(uint8_t note);
};

class SineWaveSynth {
public:
    SineWaveSynth(uint32_t sampleRate = 44100, size_t maxVoices = 32);
    ~SineWaveSynth();
    
    void noteOn(uint8_t midiNote, uint8_t velocity, double currentTime);
    void noteOff(uint8_t midiNote, double currentTime);
    void allNotesOff();
    
    double getSample(double currentTime);
    
private:
    uint32_t sampleRate;
    std::vector<std::unique_ptr<Voice>> voices;
    
    Voice* findFreeVoice();
    Voice* findVoiceWithNote(uint8_t midiNote);
};

#endif // SINEWAVESYNTH_H
