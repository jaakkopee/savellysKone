#ifndef SOUNDFONTSYNTH_H
#define SOUNDFONTSYNTH_H

#include <fluidsynth.h>
#include <string>
#include <memory>

class SoundFontSynth {
public:
    SoundFontSynth();
    ~SoundFontSynth();
    
    bool loadSoundFont(const std::string& path);
    void noteOn(uint8_t note, uint8_t velocity);
    void noteOff(uint8_t note);
    void allNotesOff();
    
    // Get audio samples
    void getSamples(float* leftBuffer, float* rightBuffer, size_t sampleCount);
    
    bool isLoaded() const { return soundFontLoaded; }
    
private:
    fluid_settings_t* settings;
    fluid_synth_t* synth;
    bool soundFontLoaded;
    int soundFontId;
};

#endif // SOUNDFONTSYNTH_H
