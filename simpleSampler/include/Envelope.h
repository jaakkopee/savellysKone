#ifndef ENVELOPE_H
#define ENVELOPE_H

class Envelope {
public:
    Envelope();
    ~Envelope();
    
    void setAttack(double seconds);
    void setDecay(double seconds);
    void setSustain(double level);     // 0.0 to 1.0
    void setRelease(double seconds);
    
    void noteOn();
    void noteOff();
    void reset();
    
    double getAmplitude(double time);  // Get envelope value at given time
    bool isActive() const;
    
private:
    enum class Stage {
        Idle,
        Attack,
        Decay,
        Sustain,
        Release
    };
    
    Stage currentStage;
    double attackTime;
    double decayTime;
    double sustainLevel;
    double releaseTime;
    
    double stageStartTime;
    double noteOnTime;
    double noteOffTime;
    double releaseStartAmplitude;
};

#endif // ENVELOPE_H
