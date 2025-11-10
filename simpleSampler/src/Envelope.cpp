#include "Envelope.h"
#include <algorithm>

Envelope::Envelope()
    : currentStage(Stage::Idle),
      attackTime(0.01),      // 10ms attack
      decayTime(0.1),        // 100ms decay
      sustainLevel(0.7),     // 70% sustain
      releaseTime(0.2),      // 200ms release
      stageStartTime(0.0),
      noteOnTime(0.0),
      noteOffTime(0.0),
      releaseStartAmplitude(0.0)
{
}

Envelope::~Envelope() {
}

void Envelope::setAttack(double seconds) {
    attackTime = std::max(0.001, seconds);
}

void Envelope::setDecay(double seconds) {
    decayTime = std::max(0.001, seconds);
}

void Envelope::setSustain(double level) {
    sustainLevel = std::clamp(level, 0.0, 1.0);
}

void Envelope::setRelease(double seconds) {
    releaseTime = std::max(0.001, seconds);
}

void Envelope::noteOn() {
    currentStage = Stage::Attack;
    noteOnTime = 0.0;
    stageStartTime = 0.0;
}

void Envelope::noteOff() {
    if (currentStage != Stage::Idle && currentStage != Stage::Release) {
        // Capture current amplitude at the moment of note off
        double currentAmplitude = 0.0;
        if (currentStage == Stage::Sustain) {
            currentAmplitude = sustainLevel;
        } else {
            currentAmplitude = getAmplitude(0.0); // Get current amplitude
        }
        
        currentStage = Stage::Release;
        stageStartTime = 0.0; // Reset for release timing
        releaseStartAmplitude = currentAmplitude;
    }
}

void Envelope::reset() {
    currentStage = Stage::Idle;
    stageStartTime = 0.0;
    noteOnTime = 0.0;
    noteOffTime = 0.0;
    releaseStartAmplitude = 0.0;
}

double Envelope::getAmplitude(double time) {
    double amplitude = 0.0;
    
    switch (currentStage) {
        case Stage::Idle:
            amplitude = 0.0;
            break;
            
        case Stage::Attack:
            if (time < attackTime) {
                amplitude = time / attackTime;
            } else {
                currentStage = Stage::Decay;
                stageStartTime = time;
                amplitude = 1.0;
            }
            break;
            
        case Stage::Decay:
            {
                double decayProgress = (time - stageStartTime) / decayTime;
                if (decayProgress < 1.0) {
                    amplitude = 1.0 - (decayProgress * (1.0 - sustainLevel));
                } else {
                    currentStage = Stage::Sustain;
                    amplitude = sustainLevel;
                }
            }
            break;
            
        case Stage::Sustain:
            amplitude = sustainLevel;
            break;
            
        case Stage::Release:
            {
                double releaseProgress = time / releaseTime;
                if (releaseProgress < 1.0) {
                    amplitude = releaseStartAmplitude * (1.0 - releaseProgress);
                } else {
                    currentStage = Stage::Idle;
                    amplitude = 0.0;
                }
            }
            break;
    }
    
    return std::clamp(amplitude, 0.0, 1.0);
}

bool Envelope::isActive() const {
    return currentStage != Stage::Idle;
}
