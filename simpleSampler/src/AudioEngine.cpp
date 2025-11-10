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
        std::cout << "AudioEngine::start() called" << std::endl;
        std::cout << "Tracks: " << tracks.size() << std::endl;
        std::cout << "Total notes: ";
        for (const auto& track : tracks) {
            std::cout << track.notes.size() << " ";
        }
        std::cout << std::endl;
        
        playing = true;
        currentTime = 0.0;
        currentNoteIndex = 0;
        play();
        
        std::cout << "SFML play() called, status: " << static_cast<int>(getStatus()) << std::endl;
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
    static int bufferCount = 0;
    static bool firstCall = true;
    
    if (firstCall) {
        std::cout << "onGetData() called for the first time!" << std::endl;
        firstCall = false;
    }
    
    if (!playing) {
        std::cout << "onGetData() - not playing, returning false" << std::endl;
        return false;
    }
    
    bufferCount++;
    if (bufferCount % 100 == 0) {
        std::cout << "Generated " << bufferCount << " audio buffers" << std::endl;
    }
    
    static int nonZeroSampleCount = 0;
    static int sustainSampleCount = 0;
    
    // Generate audio samples
    for (size_t i = 0; i < BUFFER_SIZE; ++i) {
        processNotes();
        
        double sample = synth.getSample(currentTime);
        
        // Debug: Check for non-zero samples
        if (sample != 0.0 && nonZeroSampleCount < 5) {
            std::cout << "Non-zero sample: " << sample << " at time " << currentTime << std::endl;
            nonZeroSampleCount++;
        }
        
        // Debug: Check for sustained samples (after attack phase)
        if (currentTime > 0.05 && currentTime < 0.1 && std::abs(sample) > 0.1 && sustainSampleCount < 3) {
            std::cout << "SUSTAIN sample: " << sample << " at time " << currentTime << std::endl;
            sustainSampleCount++;
        }
        
        // Convert to 16-bit integer range
        int16_t sampleValue = static_cast<int16_t>(sample * 32767.0);
        
        // Stereo output (same signal on both channels)
        sampleBuffer[i * 2] = sampleValue;     // Left
        sampleBuffer[i * 2 + 1] = sampleValue; // Right
        
        currentTime = currentTime + (1.0 / sampleRate);
    }
    
    data.samples = sampleBuffer.data();
    data.sampleCount = sampleBuffer.size();
    
    // Keep playing (return true) - user will stop manually
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
    
    static int noteOnCount = 0;
    static int noteOffCount = 0;
    
    // Process all tracks
    for (auto& track : tracks) {
        for (size_t i = 0; i < track.notes.size(); ++i) {
            const MidiNote& note = track.notes[i];
            
            // Trigger note on
            if (note.startTime <= currentTime && 
                note.startTime > (currentTime - (1.0 / sampleRate))) {
                synth.noteOn(note.pitch, note.velocity, 0.0);
                noteOnCount++;
                if (noteOnCount <= 10) {
                    std::cout << "Note ON: pitch=" << (int)note.pitch 
                              << " vel=" << (int)note.velocity 
                              << " time=" << currentTime << std::endl;
                }
            }
            
            // Trigger note off
            double noteEndTime = note.startTime + note.duration;
            if (noteEndTime <= currentTime && 
                noteEndTime > (currentTime - (1.0 / sampleRate))) {
                synth.noteOff(note.pitch, 0.0);
                noteOffCount++;
                if (noteOffCount <= 10) {
                    std::cout << "Note OFF: pitch=" << (int)note.pitch 
                              << " time=" << currentTime << std::endl;
                }
            }
        }
    }
}
