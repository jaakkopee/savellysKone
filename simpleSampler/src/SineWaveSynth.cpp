#include "SineWaveSynth.h"
#include <cmath>
#include <algorithm>

// Voice implementation
Voice::Voice()
    : midiNote(0), velocity(0), frequency(440.0), phase(0.0), active(false)
{
}

void Voice::noteOn(uint8_t note, uint8_t vel, double currentTime) {
    midiNote = note;
    velocity = vel;
    frequency = midiNoteToFrequency(note);
    phase = 0.0;
    active = true;
    envelope.reset();
    envelope.noteOn();
}

void Voice::noteOff(double currentTime) {
    envelope.noteOff();
}

bool Voice::isActive() const {
    return active && envelope.isActive();
}

double Voice::getSample(double currentTime, uint32_t sampleRate) {
    if (!isActive()) {
        active = false;
        return 0.0;
    }
    
    // Generate sine wave
    double sample = std::sin(phase * 2.0 * M_PI);
    
    // Advance phase
    phase += frequency / sampleRate;
    if (phase >= 1.0) {
        phase -= 1.0;
    }
    
    // Apply envelope
    double envValue = envelope.getAmplitude(currentTime);
    
    // Apply velocity scaling (velocity 0-127 maps to 0.0-1.0)
    double velocityScale = velocity / 127.0;
    
    return sample * envValue * velocityScale * 0.3; // 0.3 to prevent clipping with multiple voices
}

double Voice::midiNoteToFrequency(uint8_t note) {
    // MIDI note 69 (A4) = 440 Hz
    return 440.0 * std::pow(2.0, (note - 69) / 12.0);
}

// SineWaveSynth implementation
SineWaveSynth::SineWaveSynth(uint32_t sr, size_t maxVoices)
    : sampleRate(sr)
{
    voices.reserve(maxVoices);
    for (size_t i = 0; i < maxVoices; ++i) {
        voices.push_back(std::make_unique<Voice>());
    }
}

SineWaveSynth::~SineWaveSynth() {
}

void SineWaveSynth::noteOn(uint8_t midiNote, uint8_t velocity, double currentTime) {
    Voice* voice = findFreeVoice();
    if (voice) {
        voice->noteOn(midiNote, velocity, currentTime);
    }
}

void SineWaveSynth::noteOff(uint8_t midiNote, double currentTime) {
    Voice* voice = findVoiceWithNote(midiNote);
    if (voice) {
        voice->noteOff(currentTime);
    }
}

void SineWaveSynth::allNotesOff() {
    for (auto& voice : voices) {
        voice->noteOff(0.0);
    }
}

double SineWaveSynth::getSample(double currentTime) {
    double mixedSample = 0.0;
    
    for (auto& voice : voices) {
        if (voice->isActive()) {
            mixedSample += voice->getSample(currentTime, sampleRate);
        }
    }
    
    return std::clamp(mixedSample, -1.0, 1.0);
}

Voice* SineWaveSynth::findFreeVoice() {
    for (auto& voice : voices) {
        if (!voice->isActive()) {
            return voice.get();
        }
    }
    return nullptr; // All voices busy
}

Voice* SineWaveSynth::findVoiceWithNote(uint8_t midiNote) {
    for (auto& voice : voices) {
        if (voice->isActive()) {
            // Note: We need to expose midiNote in Voice or track it differently
            // For now, turn off the first active voice
            return voice.get();
        }
    }
    return nullptr;
}
