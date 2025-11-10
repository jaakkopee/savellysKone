#include "MidiParser.h"
#include <fstream>
#include <iostream>
#include <cstring>

MidiParser::MidiParser()
    : ticksPerQuarterNote(480)
{
}

MidiParser::~MidiParser() {
}

bool MidiParser::loadFile(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    if (!file.is_open()) {
        std::cerr << "Failed to open MIDI file: " << filename << std::endl;
        return false;
    }
    
    // Read entire file into memory
    std::vector<uint8_t> data((std::istreambuf_iterator<char>(file)),
                               std::istreambuf_iterator<char>());
    file.close();
    
    if (data.size() < 14) {
        std::cerr << "File too small to be a valid MIDI file" << std::endl;
        return false;
    }
    
    size_t offset = 0;
    
    // Parse header
    if (!parseHeader(data, offset)) {
        return false;
    }
    
    // Parse tracks
    tracks.clear();
    while (offset < data.size()) {
        MidiTrack track;
        if (parseTrack(data, offset, track)) {
            tracks.push_back(track);
        } else {
            break;
        }
    }
    
    return !tracks.empty();
}

const std::vector<MidiTrack>& MidiParser::getTracks() const {
    return tracks;
}

uint16_t MidiParser::getTicksPerQuarterNote() const {
    return ticksPerQuarterNote;
}

bool MidiParser::parseHeader(const std::vector<uint8_t>& data, size_t& offset) {
    // Check for "MThd" chunk ID
    if (std::memcmp(&data[offset], "MThd", 4) != 0) {
        std::cerr << "Invalid MIDI header" << std::endl;
        return false;
    }
    offset += 4;
    
    uint32_t headerLength = read32BitBE(data, offset);
    offset += 4;
    
    if (headerLength < 6) {
        std::cerr << "Header length too small" << std::endl;
        return false;
    }
    
    uint16_t format = read16BitBE(data, offset);
    offset += 2;
    
    uint16_t numTracks = read16BitBE(data, offset);
    offset += 2;
    
    ticksPerQuarterNote = read16BitBE(data, offset);
    offset += 2;
    
    // Skip any extra header data
    offset += (headerLength - 6);
    
    std::cout << "MIDI Format: " << format << std::endl;
    std::cout << "Number of tracks: " << numTracks << std::endl;
    std::cout << "Ticks per quarter note: " << ticksPerQuarterNote << std::endl;
    
    return true;
}

bool MidiParser::parseTrack(const std::vector<uint8_t>& data, size_t& offset, MidiTrack& track) {
    if (offset + 8 > data.size()) {
        return false;
    }
    
    // Check for "MTrk" chunk ID
    if (std::memcmp(&data[offset], "MTrk", 4) != 0) {
        std::cerr << "Invalid track header at offset " << offset << std::endl;
        return false;
    }
    offset += 4;
    
    uint32_t trackLength = read32BitBE(data, offset);
    offset += 4;
    
    size_t trackEnd = offset + trackLength;
    
    uint32_t absoluteTime = 0;
    uint8_t runningStatus = 0;
    uint32_t tempo = 500000; // Default tempo: 120 BPM
    track.tempo = tempo;
    
    std::vector<std::pair<uint32_t, uint8_t>> activeNotes; // (start tick, note number)
    
    while (offset < trackEnd) {
        // Read delta time
        uint32_t deltaTime = readVariableLength(data, offset);
        absoluteTime += deltaTime;
        
        if (offset >= data.size()) break;
        
        uint8_t statusByte = data[offset];
        
        // Handle running status
        if (statusByte < 0x80) {
            statusByte = runningStatus;
        } else {
            offset++;
            runningStatus = statusByte;
        }
        
        uint8_t messageType = statusByte & 0xF0;
        uint8_t channel = statusByte & 0x0F;
        
        if (messageType == 0x90) { // Note On
            if (offset + 1 >= data.size()) break;
            uint8_t note = data[offset++];
            uint8_t velocity = data[offset++];
            
            if (velocity > 0) {
                activeNotes.push_back({absoluteTime, note});
            } else {
                // Velocity 0 is note off
                for (auto it = activeNotes.begin(); it != activeNotes.end(); ++it) {
                    if (it->second == note) {
                        MidiNote midiNote;
                        midiNote.pitch = note;
                        midiNote.velocity = 64; // Default velocity for note off
                        midiNote.startTime = (it->first * tempo / (double)ticksPerQuarterNote) / 1000000.0;
                        midiNote.duration = ((absoluteTime - it->first) * tempo / (double)ticksPerQuarterNote) / 1000000.0;
                        track.notes.push_back(midiNote);
                        activeNotes.erase(it);
                        break;
                    }
                }
            }
        } else if (messageType == 0x80) { // Note Off
            if (offset + 1 >= data.size()) break;
            uint8_t note = data[offset++];
            uint8_t velocity = data[offset++];
            
            for (auto it = activeNotes.begin(); it != activeNotes.end(); ++it) {
                if (it->second == note) {
                    MidiNote midiNote;
                    midiNote.pitch = note;
                    midiNote.velocity = velocity;
                    midiNote.startTime = (it->first * tempo / (double)ticksPerQuarterNote) / 1000000.0;
                    midiNote.duration = ((absoluteTime - it->first) * tempo / (double)ticksPerQuarterNote) / 1000000.0;
                    track.notes.push_back(midiNote);
                    activeNotes.erase(it);
                    break;
                }
            }
        } else if (messageType == 0xA0 || messageType == 0xB0 || messageType == 0xE0) {
            // Aftertouch, Control Change, Pitch Bend - skip 2 bytes
            offset += 2;
        } else if (messageType == 0xC0 || messageType == 0xD0) {
            // Program Change, Channel Pressure - skip 1 byte
            offset += 1;
        } else if (statusByte == 0xFF) { // Meta event
            if (offset >= data.size()) break;
            uint8_t metaType = data[offset++];
            uint32_t metaLength = readVariableLength(data, offset);
            
            if (metaType == 0x51 && metaLength == 3) { // Set Tempo
                tempo = (data[offset] << 16) | (data[offset+1] << 8) | data[offset+2];
                track.tempo = tempo;
            }
            
            offset += metaLength;
        } else if (statusByte == 0xF0 || statusByte == 0xF7) { // SysEx
            uint32_t sysexLength = readVariableLength(data, offset);
            offset += sysexLength;
        }
    }
    
    offset = trackEnd;
    
    std::cout << "Parsed track with " << track.notes.size() << " notes" << std::endl;
    
    return true;
}

uint32_t MidiParser::readVariableLength(const std::vector<uint8_t>& data, size_t& offset) {
    uint32_t value = 0;
    uint8_t byte;
    
    do {
        if (offset >= data.size()) break;
        byte = data[offset++];
        value = (value << 7) | (byte & 0x7F);
    } while (byte & 0x80);
    
    return value;
}

uint32_t MidiParser::read32BitBE(const std::vector<uint8_t>& data, size_t offset) {
    return (data[offset] << 24) | (data[offset+1] << 16) | 
           (data[offset+2] << 8) | data[offset+3];
}

uint16_t MidiParser::read16BitBE(const std::vector<uint8_t>& data, size_t offset) {
    return (data[offset] << 8) | data[offset+1];
}
