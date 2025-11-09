"""
MIDI Parser and Validator

This module provides functionality to parse MIDI files and validate note timing.
Specifically, it checks that each note-on event occurs before its corresponding 
note-off event, ensuring the correctness of MIDI data.
"""

import mido
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class NoteEvent:
    """Represents a single note event with timing information."""
    note: int
    channel: int
    velocity: int
    time: float
    event_type: str  # 'note_on' or 'note_off'


@dataclass
class ValidationError:
    """Represents a validation error found in MIDI data."""
    note: int
    channel: int
    error_type: str
    message: str
    timestamp: Optional[float] = None


class MIDIParser:
    """
    Parser for MIDI files that extracts and validates note timing information.
    """
    
    def __init__(self, filepath: str):
        """
        Initialize the MIDI parser with a file path.
        
        Args:
            filepath: Path to the MIDI file to parse
        """
        self.filepath = filepath
        self.midi_file = None
        self.note_events = []
        self.validation_errors = []
    
    def parse(self) -> List[NoteEvent]:
        """
        Parse the MIDI file and extract note timing information.
        
        Returns:
            List of NoteEvent objects containing timing information
            
        Raises:
            FileNotFoundError: If the MIDI file doesn't exist
            IOError: If the file cannot be read
        """
        try:
            self.midi_file = mido.MidiFile(self.filepath)
        except FileNotFoundError:
            raise FileNotFoundError(f"MIDI file not found: {self.filepath}")
        except Exception as e:
            raise IOError(f"Error reading MIDI file: {e}")
        
        self.note_events = []
        
        # Process all tracks
        for track_idx, track in enumerate(self.midi_file.tracks):
            current_time = 0.0
            
            # Iterate through all messages in the track
            for msg in track:
                # Update current time (MIDI uses delta time)
                current_time += msg.time
                
                # Check for note events
                if msg.type == 'note_on' and msg.velocity > 0:
                    # Note on event (velocity > 0)
                    event = NoteEvent(
                        note=msg.note,
                        channel=msg.channel,
                        velocity=msg.velocity,
                        time=current_time,
                        event_type='note_on'
                    )
                    self.note_events.append(event)
                    
                elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    # Note off event (or note_on with velocity 0)
                    event = NoteEvent(
                        note=msg.note,
                        channel=msg.channel,
                        velocity=0,
                        time=current_time,
                        event_type='note_off'
                    )
                    self.note_events.append(event)
        
        return self.note_events
    
    def validate(self) -> Tuple[bool, List[ValidationError]]:
        """
        Validate that each note-on event has a corresponding note-off event
        and that note-on occurs before note-off.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
            is_valid is True if all notes are valid, False otherwise
        """
        self.validation_errors = []
        
        # Track active notes by (note, channel) key
        active_notes: Dict[Tuple[int, int], NoteEvent] = {}
        
        for event in self.note_events:
            key = (event.note, event.channel)
            
            if event.event_type == 'note_on':
                # Check if note is already active (missing note_off)
                if key in active_notes:
                    error = ValidationError(
                        note=event.note,
                        channel=event.channel,
                        error_type='missing_note_off',
                        message=f"Note {event.note} on channel {event.channel} started at "
                               f"{active_notes[key].time} without a note_off before new note_on at {event.time}",
                        timestamp=active_notes[key].time
                    )
                    self.validation_errors.append(error)
                
                # Mark note as active
                active_notes[key] = event
                
            elif event.event_type == 'note_off':
                # Check if note was previously started
                if key not in active_notes:
                    error = ValidationError(
                        note=event.note,
                        channel=event.channel,
                        error_type='missing_note_on',
                        message=f"Note {event.note} on channel {event.channel} has note_off at "
                               f"{event.time} without a preceding note_on",
                        timestamp=event.time
                    )
                    self.validation_errors.append(error)
                else:
                    note_on_event = active_notes[key]
                    
                    # Validate that note_on comes before note_off
                    if note_on_event.time > event.time:
                        error = ValidationError(
                            note=event.note,
                            channel=event.channel,
                            error_type='invalid_timing',
                            message=f"Note {event.note} on channel {event.channel} has note_on at "
                                   f"{note_on_event.time} after note_off at {event.time}",
                            timestamp=note_on_event.time
                        )
                        self.validation_errors.append(error)
                    
                    # Remove from active notes
                    del active_notes[key]
        
        # Check for notes that were never closed
        for key, event in active_notes.items():
            error = ValidationError(
                note=event.note,
                channel=event.channel,
                error_type='unclosed_note',
                message=f"Note {event.note} on channel {event.channel} started at "
                       f"{event.time} but never received a note_off",
                timestamp=event.time
            )
            self.validation_errors.append(error)
        
        is_valid = len(self.validation_errors) == 0
        return is_valid, self.validation_errors
    
    def report_errors(self) -> str:
        """
        Generate a human-readable report of validation errors.
        
        Returns:
            String containing the error report
        """
        if not self.validation_errors:
            return "No validation errors found. MIDI file is valid."
        
        report = [f"Found {len(self.validation_errors)} validation error(s):\n"]
        
        for idx, error in enumerate(self.validation_errors, 1):
            report.append(f"{idx}. [{error.error_type}] {error.message}")
        
        return "\n".join(report)


def validate_midi_file(filepath: str, verbose: bool = True) -> bool:
    """
    Convenience function to validate a MIDI file.
    
    Args:
        filepath: Path to the MIDI file to validate
        verbose: If True, print detailed error report
        
    Returns:
        True if the file is valid, False otherwise
    """
    parser = MIDIParser(filepath)
    
    try:
        # Parse the MIDI file
        parser.parse()
        
        # Validate note timing
        is_valid, errors = parser.validate()
        
        # Print report if verbose
        if verbose:
            print(f"\nValidating MIDI file: {filepath}")
            print("-" * 60)
            print(parser.report_errors())
            print("-" * 60)
        
        return is_valid
        
    except Exception as e:
        if verbose:
            print(f"Error processing MIDI file: {e}")
        return False


if __name__ == "__main__":
    """
    Command-line interface for MIDI validation.
    Usage: python midi_parser.py <midi_file_path>
    """
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python midi_parser.py <midi_file_path>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    is_valid = validate_midi_file(filepath, verbose=True)
    
    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)
