#include "AudioEngine.h"
#include <iostream>
#include <algorithm>

AudioEngine::AudioEngine(uint32_t sr)
    : sampleRate(sr),
      synth(sr),
      currentTime(0.0),
      playing(false),
      currentNoteIndex(0)
{
    sampleBuffer.resize(BUFFER_SIZE * CHANNEL_COUNT);
    // SFML 3.0 requires channel map
    std::vector<sf::SoundChannel> channelMap = {sf::SoundChannel::FrontLeft, sf::SoundChannel::FrontRight};
    initialize(CHANNEL_COUNT, sampleRate, channelMap);
}

AudioEngine::~AudioEngine() {
    stop();
}

bool AudioEngine::loadMidiFile(const std::string& filename) {
    MidiParser parser;
    if (!parser.loadFile(filename)) {
        std::cerr << "Failed to load MIDI file" << std::endl;
        return false;
    }
    
    tracks = parser.getTracks();
    
    if (tracks.empty()) {
        std::cerr << "No tracks found in MIDI file" << std::endl;
        return false;
    }
    
    std::cout << "Loaded " << tracks.size() << " track(s)" << std::endl;
    
    // Sort all notes by start time for easier playback
    for (auto& track : tracks) {
        std::sort(track.notes.begin(), track.notes.end(),
                  [](const MidiNote& a, const MidiNote& b) {
                      return a.startTime < b.startTime;
                  });
    }
    
    return true;
}

void AudioEngine::start() {
    if (!tracks.empty()) {
        playing = true;
        currentTime = 0.0;
        currentNoteIndex = 0;
        play();
    }
}

void AudioEngine::stop() {
    sf::SoundStream::stop();
    playing = false;
    synth.allNotesOff();
}

void AudioEngine::reset() {
    stop();
    currentTime = 0.0;
    currentNoteIndex = 0;
}

bool AudioEngine::isPlaying() const {
    return playing;
}

double AudioEngine::getCurrentTime() const {
    return currentTime;
}

bool AudioEngine::onGetData(Chunk& data) {
    if (!playing) {
        return false;
    }
    
    // Generate audio samples
    for (size_t i = 0; i < BUFFER_SIZE; ++i) {
        processNotes();
        
        double sample = synth.getSample(currentTime);
        
        // Convert to 16-bit integer range
        int16_t sampleValue = static_cast<int16_t>(sample * 32767.0);
        
        // Stereo output (same signal on both channels)
        sampleBuffer[i * 2] = sampleValue;     // Left
        sampleBuffer[i * 2 + 1] = sampleValue; // Right
        
        currentTime = currentTime + (1.0 / sampleRate);
    }
    
    data.samples = sampleBuffer.data();
    data.sampleCount = sampleBuffer.size();
    
    return true;
}

void AudioEngine::onSeek(sf::Time timeOffset) {
    currentTime = timeOffset.asSeconds();
    currentNoteIndex = 0;
    synth.allNotesOff();
}

void AudioEngine::processNotes() {
    if (tracks.empty()) {
        return;
    }
    
    // Process all tracks
    for (auto& track : tracks) {
        for (size_t i = 0; i < track.notes.size(); ++i) {
            const MidiNote& note = track.notes[i];
            
            // Trigger note on
            if (note.startTime <= currentTime && 
                note.startTime > (currentTime - (1.0 / sampleRate))) {
                synth.noteOn(note.pitch, note.velocity, currentTime - note.startTime);
            }
            
            // Trigger note off
            double noteEndTime = note.startTime + note.duration;
            if (noteEndTime <= currentTime && 
                noteEndTime > (currentTime - (1.0 / sampleRate))) {
                synth.noteOff(note.pitch, currentTime - noteEndTime);
            }
        }
    }
}
