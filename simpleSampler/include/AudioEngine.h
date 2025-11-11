#ifndef AUDIOENGINE_H
#define AUDIOENGINE_H

#include <SFML/Audio.hpp>
#include "SineWaveSynth.h"
#include "SoundFontSynth.h"
#include "MidiParser.h"
#include <vector>
#include <atomic>

enum class SynthMode {
    SineWave,
    SoundFont
};

class AudioEngine : public sf::SoundStream {
public:
    AudioEngine(uint32_t sampleRate = 44100);
    ~AudioEngine();
    
    bool loadMidiFile(const std::string& filename);
    bool loadSoundFont(const std::string& path);
    void setSynthMode(SynthMode mode);
    SynthMode getSynthMode() const { return synthMode; }
    
    void start();
    void stop() override;
    void reset();
    
    bool isPlaying() const;
    double getCurrentTime() const;
    
protected:
    virtual bool onGetData(Chunk& data) override;
    virtual void onSeek(sf::Time timeOffset) override;
    
private:
    static const size_t BUFFER_SIZE = 4096;
    static const size_t CHANNEL_COUNT = 2; // Stereo
    
    uint32_t sampleRate;
    SineWaveSynth sineWaveSynth;
    SoundFontSynth soundFontSynth;
    SynthMode synthMode;
    std::vector<MidiTrack> tracks;
    std::vector<int16_t> sampleBuffer;
    std::vector<float> floatBufferLeft;
    std::vector<float> floatBufferRight;
    
    std::atomic<double> currentTime;
    std::atomic<bool> playing;
    size_t currentNoteIndex;
    
    void processNotes();
};

#endif // AUDIOENGINE_H
