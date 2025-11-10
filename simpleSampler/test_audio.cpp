#include <SFML/Audio.hpp>
#include <iostream>
#include <cmath>
#include <vector>
#include <cstdint>

class TestTone : public sf::SoundStream {
private:
    std::vector<int16_t> samples;
    double phase;
    const unsigned int sampleRate = 44100;
    const unsigned int bufferSize = 2048;
    
public:
    TestTone() : phase(0.0) {
        samples.resize(bufferSize * 2); // Stereo
        std::vector<sf::SoundChannel> channelMap = {sf::SoundChannel::FrontLeft, sf::SoundChannel::FrontRight};
        sf::SoundStream::initialize(2, sampleRate, channelMap);
    }
    
    void startPlaying() {
        sf::SoundStream::play();
    }
    
private:
    virtual bool onGetData(Chunk& data) override {
        static int count = 0;
        count++;
        if (count == 1) {
            std::cout << "Generating 440Hz test tone..." << std::endl;
        }
        
        // Generate 440Hz sine wave
        for (unsigned int i = 0; i < bufferSize; ++i) {
            double sample = std::sin(phase * 2.0 * M_PI) * 0.5; // 50% volume
            phase += 440.0 / sampleRate;
            if (phase >= 1.0) phase -= 1.0;
            
            int16_t value = static_cast<int16_t>(sample * 32767);
            samples[i * 2] = value;     // Left
            samples[i * 2 + 1] = value; // Right
        }
        
        data.samples = samples.data();
        data.sampleCount = samples.size();
        return true;
    }
    
    virtual void onSeek(sf::Time) override {}
};

int main() {
    std::cout << "SFML Audio Test - 440Hz Tone" << std::endl;
    std::cout << "You should hear a tone. Press Ctrl+C to stop." << std::endl;
    
    TestTone tone;
    tone.startPlaying();
    
    std::cout << "Playing..." << std::endl;
    
    // Wait forever
    while (true) {
        sf::sleep(sf::seconds(1));
    }
    
    return 0;
}
