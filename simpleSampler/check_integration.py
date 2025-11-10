#!/usr/bin/env python3
"""
Quick installer/tester for SimpleSampler GUI integration.

Run this script to:
1. Check if SimpleSampler is built
2. Test the sampler_player module
3. Verify integration readiness
"""

import os
import sys
import subprocess

def check_executable():
    """Check if SimpleSampler executable exists"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(script_dir, 'build', 'SimpleSampler')
    
    if os.path.isfile(exe_path) and os.access(exe_path, os.X_OK):
        print("✓ SimpleSampler executable found")
        print(f"  Location: {exe_path}")
        return True
    else:
        print("✗ SimpleSampler executable not found")
        print(f"  Expected: {exe_path}")
        return False

def check_build_system():
    """Check if build system is set up"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cmake_cache = os.path.join(script_dir, 'build', 'CMakeCache.txt')
    
    if os.path.isfile(cmake_cache):
        print("✓ CMake build configured")
        return True
    else:
        print("✗ CMake not configured")
        return False

def test_sampler_player():
    """Test the sampler_player module"""
    try:
        from sampler_player import SimpleSamplerPlayer
        player = SimpleSamplerPlayer()
        
        if player.is_available():
            print("✓ sampler_player module working")
            return True
        else:
            print("✗ sampler_player module loaded but SimpleSampler not available")
            return False
    except ImportError as e:
        print(f"✗ Failed to import sampler_player: {e}")
        return False

def check_savellysKone3():
    """Check if savellysKone3 is available"""
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    
    try:
        import savellysKone3
        print("✓ savellysKone3.py found")
        return True
    except ImportError:
        print("✗ savellysKone3.py not found in parent directory")
        return False

def offer_build():
    """Offer to build SimpleSampler"""
    print()
    print("SimpleSampler needs to be built.")
    response = input("Build now? (y/n): ").strip().lower()
    
    if response == 'y':
        script_dir = os.path.dirname(os.path.abspath(__file__))
        build_dir = os.path.join(script_dir, 'build')
        
        try:
            print("\nRunning CMake...")
            subprocess.run(['cmake', '..'], cwd=build_dir, check=True)
            
            print("\nBuilding...")
            subprocess.run(['make'], cwd=build_dir, check=True)
            
            print("\n✓ Build successful!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n✗ Build failed: {e}")
            return False
        except FileNotFoundError:
            print("\n✗ cmake or make not found. Please install build tools.")
            return False
    
    return False

def main():
    print("=" * 60)
    print("SimpleSampler Integration Checker")
    print("=" * 60)
    print()
    
    # Check components
    exe_ok = check_executable()
    build_ok = check_build_system()
    module_ok = test_sampler_player()
    sk3_ok = check_savellysKone3()
    
    print()
    print("-" * 60)
    print()
    
    # Determine status
    if exe_ok and module_ok:
        print("✓✓✓ SimpleSampler integration is ready! ✓✓✓")
        print()
        print("You can now:")
        print("  1. Run the example: python3 example_integration.py")
        print("  2. Integrate into GUI: See GUI_INTEGRATION.md")
        print()
        
        if not sk3_ok:
            print("Note: savellysKone3.py not found in parent directory.")
            print("      This is only needed for the example script.")
        
        return 0
    
    elif not exe_ok:
        print("SimpleSampler needs to be built.")
        print()
        
        if offer_build():
            # Re-check after build
            if check_executable() and test_sampler_player():
                print()
                print("✓✓✓ Build successful! Integration ready! ✓✓✓")
                return 0
        else:
            print()
            print("To build manually:")
            print("  cd build")
            print("  cmake ..")
            print("  make")
        
        return 1
    
    else:
        print("Integration not ready. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
