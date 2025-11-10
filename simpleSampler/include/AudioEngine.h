#ifndef AUDIOENGINE_H
#define AUDIOENGINE_H

#include <SFML/Audio.hpp>
#include "SineWaveSynth.h"
#include "MidiParser.h"
#include <vector>
#include <atomic>

class AudioEngine : public sf::SoundStream {
public:
    AudioEngine(uint32_t sampleRate = 44100);
    ~AudioEngine();
    
    bool loadMidiFile(const std::string& filename);
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
    SineWaveSynth synth;
    std::vector<MidiTrack> tracks;
    std::vector<int16_t> sampleBuffer;
    
    std::atomic<double> currentTime;
    std::atomic<bool> playing;
    size_t currentNoteIndex;
    
    void processNotes();
};

#endif // AUDIOENGINE_H
