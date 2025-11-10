#!/usr/bin/env python3
"""
Wrapper to play MIDI files using the SimpleSampler C++ application.
This can be imported and used from savellysKone3_gui.py
"""

import subprocess
import os
import tempfile
import sys

class SimpleSamplerPlayer:
    """Interface to play MIDI files with SimpleSampler"""
    
    def __init__(self, sampler_path=None):
        """
        Initialize the SimpleSampler player.
        
        Args:
            sampler_path: Path to SimpleSampler executable. 
                         If None, assumes it's in simpleSampler/build/SimpleSampler
        """
        if sampler_path is None:
            # Try to find SimpleSampler relative to this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            sampler_path = os.path.join(script_dir, 'build', 'SimpleSampler')
        
        self.sampler_path = sampler_path
        self.process = None
    
    def is_available(self):
        """Check if SimpleSampler executable exists and is executable"""
        return os.path.isfile(self.sampler_path) and os.access(self.sampler_path, os.X_OK)
    
    def play_midi_file(self, midi_file_path, background=True):
        """
        Play a MIDI file using SimpleSampler.
        
        Args:
            midi_file_path: Path to the MIDI file to play
            background: If True, run in background and return immediately.
                       If False, wait for playback to complete.
        
        Returns:
            subprocess.Popen object if background=True, otherwise return code
        """
        if not self.is_available():
            raise FileNotFoundError(f"SimpleSampler not found at {self.sampler_path}")
        
        if not os.path.isfile(midi_file_path):
            raise FileNotFoundError(f"MIDI file not found: {midi_file_path}")
        
        try:
            if background:
                # Run in background
                print(f"[SimpleSamplerPlayer] Starting SimpleSampler: {self.sampler_path} {midi_file_path}")
                self.process = subprocess.Popen(
                    [self.sampler_path, midi_file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.DEVNULL
                )
                print(f"[SimpleSamplerPlayer] Process started with PID: {self.process.pid}")
                # Give it a moment to start
                import time
                time.sleep(0.1)
                # Check if it's still running
                if self.process.poll() is not None:
                    # Process already exited
                    stdout, stderr = self.process.communicate()
                    print(f"[SimpleSamplerPlayer] Process exited immediately!")
                    print(f"[SimpleSamplerPlayer] Return code: {self.process.returncode}")
                    print(f"[SimpleSamplerPlayer] STDOUT: {stdout.decode()}")
                    print(f"[SimpleSamplerPlayer] STDERR: {stderr.decode()}")
                return self.process
            else:
                # Wait for completion
                print(f"[SimpleSamplerPlayer] Running SimpleSampler (foreground): {self.sampler_path} {midi_file_path}")
                result = subprocess.run(
                    [self.sampler_path, midi_file_path],
                    capture_output=True,
                    text=True
                )
                print(f"[SimpleSamplerPlayer] Return code: {result.returncode}")
                if result.stdout:
                    print(f"[SimpleSamplerPlayer] STDOUT: {result.stdout}")
                if result.stderr:
                    print(f"[SimpleSamplerPlayer] STDERR: {result.stderr}")
                return result.returncode
        except Exception as e:
            raise RuntimeError(f"Failed to run SimpleSampler: {e}")
    
    def play_from_song(self, song, background=True):
        """
        Create a temporary MIDI file from a Song object and play it.
        
        Args:
            song: savellysKone3.Song object
            background: If True, run in background
        
        Returns:
            Tuple of (temp_file_path, process/return_code)
        """
        # Create temporary MIDI file
        temp_fd, temp_path = tempfile.mkstemp(suffix='.mid', prefix='sk3_')
        os.close(temp_fd)  # Close the file descriptor
        
        try:
            # Generate MIDI file
            song.make_midi_file(temp_path)
            
            # Play it
            result = self.play_midi_file(temp_path, background=background)
            
            return temp_path, result
            
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise e
    
    def stop(self):
        """Stop currently playing MIDI (if running in background)"""
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None
    
    def is_playing(self):
        """Check if SimpleSampler is currently playing"""
        return self.process is not None and self.process.poll() is None


# Convenience functions for direct use

def play_midi(midi_file_path, sampler_path=None, background=True):
    """
    Convenience function to play a MIDI file.
    
    Args:
        midi_file_path: Path to MIDI file
        sampler_path: Path to SimpleSampler executable (optional)
        background: Run in background (default True)
    
    Returns:
        SimpleSamplerPlayer instance
    """
    player = SimpleSamplerPlayer(sampler_path)
    player.play_midi_file(midi_file_path, background=background)
    return player


def play_song(song, sampler_path=None, background=True):
    """
    Convenience function to play a savellysKone3.Song object.
    
    Args:
        song: savellysKone3.Song object
        sampler_path: Path to SimpleSampler executable (optional)
        background: Run in background (default True)
    
    Returns:
        Tuple of (temp_midi_path, SimpleSamplerPlayer instance)
    """
    player = SimpleSamplerPlayer(sampler_path)
    temp_path, _ = player.play_from_song(song, background=background)
    return temp_path, player


# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 sampler_player.py <midi_file>")
        print("   or: python3 sampler_player.py --test")
        sys.exit(1)
    
    if sys.argv[1] == "--test":
        # Test with savellysKone3
        try:
            import savellysKone3 as sk3
            
            # Create a simple test song
            pitch_grammar = "$S -> 60 62 64 65 67 69 71 72"
            pitch_gen = sk3.ListGenerator(pitch_grammar, 8, "pitch")
            
            song = sk3.Song(pitch_generator=pitch_gen, num_bars=2, ioi=0.5)
            song.make_bar_list()
            
            print("Playing test song...")
            temp_path, player = play_song(song, background=False)
            
            # Clean up
            os.unlink(temp_path)
            print("Done!")
            
        except ImportError:
            print("savellysKone3 not found. Cannot run test.")
            sys.exit(1)
    else:
        # Play specified file
        midi_file = sys.argv[1]
        print(f"Playing {midi_file}...")
        player = play_midi(midi_file, background=False)
        print("Done!")
