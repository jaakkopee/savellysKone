#ifndef MIDIPARSER_H
#define MIDIPARSER_H

#include <vector>
#include <string>
#include <cstdint>

struct MidiNote {
    uint8_t pitch;      // MIDI note number (0-127)
    uint8_t velocity;   // Note velocity (0-127)
    double startTime;   // Start time in seconds
    double duration;    // Duration in seconds
};

struct MidiTrack {
    std::vector<MidiNote> notes;
    uint32_t tempo;     // Microseconds per quarter note
};

class MidiParser {
public:
    MidiParser();
    ~MidiParser();
    
    bool loadFile(const std::string& filename);
    const std::vector<MidiTrack>& getTracks() const;
    uint16_t getTicksPerQuarterNote() const;
    
private:
    std::vector<MidiTrack> tracks;
    uint16_t ticksPerQuarterNote;
    
    bool parseHeader(const std::vector<uint8_t>& data, size_t& offset);
    bool parseTrack(const std::vector<uint8_t>& data, size_t& offset, MidiTrack& track);
    uint32_t readVariableLength(const std::vector<uint8_t>& data, size_t& offset);
    uint32_t read32BitBE(const std::vector<uint8_t>& data, size_t offset);
    uint16_t read16BitBE(const std::vector<uint8_t>& data, size_t offset);
};

#endif // MIDIPARSER_H
