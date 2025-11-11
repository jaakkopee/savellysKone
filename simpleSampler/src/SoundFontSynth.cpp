#include "SoundFontSynth.h"
#include <iostream>

SoundFontSynth::SoundFontSynth() 
    : settings(nullptr), synth(nullptr), soundFontLoaded(false), soundFontId(-1) {
    
    // Create FluidSynth settings
    settings = new_fluid_settings();
    if (!settings) {
        std::cerr << "Failed to create FluidSynth settings" << std::endl;
        return;
    }
    
    // Configure settings
    fluid_settings_setnum(settings, "synth.sample-rate", 44100.0);
    fluid_settings_setint(settings, "synth.polyphony", 32);
    
    // Create synthesizer
    synth = new_fluid_synth(settings);
    if (!synth) {
        std::cerr << "Failed to create FluidSynth synthesizer" << std::endl;
        delete_fluid_settings(settings);
        settings = nullptr;
        return;
    }
}

SoundFontSynth::~SoundFontSynth() {
    if (synth) {
        delete_fluid_synth(synth);
    }
    if (settings) {
        delete_fluid_settings(settings);
    }
}

bool SoundFontSynth::loadSoundFont(const std::string& path) {
    if (!synth) {
        return false;
    }
    
    soundFontId = fluid_synth_sfload(synth, path.c_str(), 1);
    if (soundFontId == FLUID_FAILED) {
        std::cerr << "Failed to load SoundFont: " << path << std::endl;
        return false;
    }
    
    std::cout << "Loaded SoundFont: " << path << std::endl;
    soundFontLoaded = true;
    return true;
}

void SoundFontSynth::noteOn(uint8_t note, uint8_t velocity) {
    if (synth && soundFontLoaded) {
        fluid_synth_noteon(synth, 0, note, velocity);
    }
}

void SoundFontSynth::noteOff(uint8_t note) {
    if (synth && soundFontLoaded) {
        fluid_synth_noteoff(synth, 0, note);
    }
}

void SoundFontSynth::allNotesOff() {
    if (synth && soundFontLoaded) {
        fluid_synth_all_notes_off(synth, 0);
    }
}

void SoundFontSynth::getSamples(float* leftBuffer, float* rightBuffer, size_t sampleCount) {
    if (synth && soundFontLoaded) {
        fluid_synth_write_float(synth, sampleCount, leftBuffer, 0, 1, rightBuffer, 0, 1);
    } else {
        // Return silence if not initialized
        for (size_t i = 0; i < sampleCount; ++i) {
            leftBuffer[i] = 0.0f;
            rightBuffer[i] = 0.0f;
        }
    }
}
