#include "AudioEngine.h"
#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <iomanip>
#include <filesystem>

int main(int argc, char* argv[]) {
    std::cout << "===========================================\n";
    std::cout << "     Simple MIDI Sampler    \n";
    std::cout << "===========================================\n\n";
    
    std::string midiFile;
    bool useSoundFont = false;
    std::string soundFontPath;
    
    if (argc > 1) {
        midiFile = argv[1];
        // Check for --soundfont or -sf flag
        if (argc > 2) {
            std::string arg2 = argv[2];
            if (arg2 == "--soundfont" || arg2 == "-sf") {
                useSoundFont = true;
                // Check if a SoundFont path is provided after the flag
                if (argc > 3) {
                    soundFontPath = argv[3];
                }
            }
        }
    } else {
        std::cout << "Usage: " << argv[0] << " <midi_file.mid> [-sf <soundfont.sf2>]" << std::endl;
        std::cout << "       " << argv[0] << " <midi_file.mid> [--soundfont <soundfont.sf2>]" << std::endl;
        std::cout << "Enter MIDI file path: ";
        std::getline(std::cin, midiFile);
        
        std::cout << "Use SoundFont? (y/n): ";
        std::string answer;
        std::getline(std::cin, answer);
        useSoundFont = (answer == "y" || answer == "Y");
        
        if (useSoundFont) {
            std::cout << "Enter SoundFont path (or leave empty for default): ";
            std::getline(std::cin, soundFontPath);
        }
    }
    
    AudioEngine engine(44100);
    
    // Configure synthesis mode
    if (useSoundFont) {
        std::string sfPath;
        
        // If user provided a specific SoundFont path, use it
        if (!soundFontPath.empty()) {
            sfPath = soundFontPath;
        } else {
            // Look for default SoundFont in ./soundfonts directory
            sfPath = "soundfonts/Motif ES6 Concert Piano(12Mb).SF2";
            if (!std::filesystem::exists(sfPath)) {
                sfPath = "build/soundfonts/Motif ES6 Concert Piano(12Mb).SF2";
            }
        }
        
        if (std::filesystem::exists(sfPath)) {
            std::cout << "Loading SoundFont: " << sfPath << std::endl;
            if (engine.loadSoundFont(sfPath)) {
                engine.setSynthMode(SynthMode::SoundFont);
                std::cout << "SoundFont loaded successfully" << std::endl;
            } else {
                std::cerr << "Failed to load SoundFont, falling back to sine wave" << std::endl;
                useSoundFont = false;
            }
        } else {
            std::cerr << "SoundFont file not found: " << sfPath << std::endl;
            std::cerr << "Falling back to sine wave synthesis" << std::endl;
            useSoundFont = false;
        }
    }
    
    if (!useSoundFont) {
        std::cout << "Using sine wave synthesis with ADSR envelope" << std::endl;
        engine.setSynthMode(SynthMode::SineWave);
    }
    
    std::cout << "\nLoading MIDI file: " << midiFile << std::endl;
    
    if (!engine.loadMidiFile(midiFile)) {
        std::cerr << "Failed to load MIDI file. Exiting." << std::endl;
        return 1;
    }
    
    std::cout << "\nStarting playback..." << std::endl;
    std::cout << "Press Ctrl+C to stop\n" << std::endl;
    
    engine.start();
    
    std::cout << "Audio stream started, playing..." << std::endl;
    
    // Keep playing until user interrupts
    while (engine.isPlaying()) {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        
        // Print current time
        std::cout << "\rTime: " << std::fixed << std::setprecision(2) 
                  << engine.getCurrentTime() << "s" << std::flush;
    }
    
    std::cout << "\n\nPlayback finished." << std::endl;
    
    return 0;
}
