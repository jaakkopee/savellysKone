#include "AudioEngine.h"
#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <iomanip>

int main(int argc, char* argv[]) {
    std::cout << "===========================================\n";
    std::cout << "     Simple MIDI Sampler with Sine Waves    \n";
    std::cout << "===========================================\n\n";
    
    std::string midiFile;
    
    if (argc > 1) {
        midiFile = argv[1];
    } else {
        std::cout << "Usage: " << argv[0] << " <midi_file.mid>" << std::endl;
        std::cout << "Enter MIDI file path: ";
        std::getline(std::cin, midiFile);
    }
    
    AudioEngine engine(44100);
    
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
