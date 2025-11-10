cmake_minimum_required(VERSION 3.16)
project(SimpleSampler VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find SFML
find_package(SFML 3.0 COMPONENTS Audio System REQUIRED)

# Include directories
include_directories(${PROJECT_SOURCE_DIR}/include)

# Source files
set(SOURCES
    src/main.cpp
    src/MidiParser.cpp
    src/SineWaveSynth.cpp
    src/Envelope.cpp
    src/AudioEngine.cpp
)

# Header files
set(HEADERS
    include/MidiParser.h
    include/SineWaveSynth.h
    include/Envelope.h
    include/AudioEngine.h
)

# Create executable
add_executable(${PROJECT_NAME} ${SOURCES} ${HEADERS})

# Link SFML libraries
target_link_libraries(${PROJECT_NAME} SFML::Audio SFML::System)

# Installation
install(TARGETS ${PROJECT_NAME} DESTINATION bin)
