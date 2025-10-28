# SCHEMATIC: Ultrasonic Bone Conduction Bass System
**Invention ID:** INV-004
**Certainty:** 89%

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    AUDIO INPUT SOURCE                        │
│              (Bluetooth, USB, Line-in)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               DSP PREPROCESSING                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • Highpass filter (20Hz cutoff)                     │  │
│  │  • Bass extraction (20-80Hz bandpass)                │  │
│  │  • Dynamic range compression (3:1 ratio)             │  │
│  │  • Limiter (-6dB threshold)                          │  │
│  └──────────────────────────────────────────────────────┘  │
│                    STM32H7 DSP                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│            FREQUENCY MULTIPLIER STAGE                        │
│  Input: 20-80Hz  →  Output: 40kHz carrier + 20-80Hz mod     │
│                                                              │
│  ┌────────────┐      ┌──────────────┐     ┌─────────────┐  │
│  │   Bass     │      │  Amplitude   │     │  40kHz      │  │
│  │  Signal    │──────▶  Modulator   │─────▶ Ultrasonic │  │
│  │  (20-80Hz) │      │              │     │  Output     │  │
│  └────────────┘      └──────────────┘     └─────────────┘  │
│                                                              │
│       Carrier: cos(2π·40000·t)                               │
│       Modulation: Bass(t) × Carrier(t)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              POWER AMPLIFIER ARRAY                           │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Class-D  │  │ Class-D  │  │ Class-D  │  │ Class-D  │   │
│  │ Amp #1   │  │ Amp #2   │  │ Amp #3   │  │ Amp #4   │   │
│  │ (100W)   │  │ (100W)   │  │ (100W)   │  │ (100W)   │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │             │             │           │
└───────┼─────────────┼─────────────┼─────────────┼───────────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌───────────────────────────────────────────────────────────┐
│          ULTRASONIC TRANSDUCER ARRAY (16 units)           │
│                                                            │
│   ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                        │
│   │UT-1 │ │UT-2 │ │UT-3 │ │UT-4 │                        │
│   └─────┘ └─────┘ └─────┘ └─────┘                        │
│   ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐    Murata MA40S4S      │
│   │UT-5 │ │UT-6 │ │UT-7 │ │UT-8 │    40kHz Transducers   │
│   └─────┘ └─────┘ └─────┘ └─────┘                        │
│   ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                        │
│   │UT-9 │ │UT-10│ │UT-11│ │UT-12│                        │
│   └─────┘ └─────┘ └─────┘ └─────┘                        │
│   ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                        │
│   │UT-13│ │UT-14│ │UT-15│ │UT-16│                        │
│   └─────┘ └─────┘ └─────┘ └─────┘                        │
│                                                            │
│          Array focuses ultrasound at user's body           │
│         Bone conduction creates bass sensation             │
└────────────────────────────────────────────────────────────┘
```

## Component Details

### DSP Stage
- **MCU**: STM32H743 (400MHz ARM Cortex-M7)
- **ADC**: 16-bit stereo input (48kHz sample rate)
- **DAC**: 16-bit stereo output (192kHz for ultrasonic)

### Modulator Circuit
```
         +5V
          │
          │
        ┌─┴─┐
        │   │  10kΩ
        │ R1│
        └─┬─┘
          │
   Bass   │    ┌──────┐
  Signal──┼────┤AD633  │
          │    │Analog │──── Modulated
  40kHz   │    │Multi- │     40kHz Output
 Carrier──┼────┤plier  │
          │    └──────┘
         GND
```

### Power Amplifier (per channel)
- **IC**: TPA3255 Class-D (100W)
- **Efficiency**: 92%
- **THD+N**: <0.001%
- **Supply**: ±24V

### Transducer Specifications
- **Model**: Murata MA40S4S
- **Frequency**: 40kHz ±1kHz
- **SPL**: 120dB @ 10cm
- **Beam Width**: 60° (-6dB points)
- **Power Handling**: 10W continuous

## Bill of Materials

### Electronics
- STM32H743 Dev Board: $45
- AD633 Analog Multiplier: $12
- TPA3255 Class-D Amp (x4): $18 each = $72
- Murata MA40S4S Transducers (x16): $8 each = $128
- Power Supply (24V 10A): $35
- Bluetooth Audio Module (CSR8675): $15
- Enclosure & Mounting: $40

**Total BOM: $347**

## Assembly Instructions

1. **DSP Board Setup**
   - Flash STM32H7 with bass extraction firmware
   - Connect audio input (Bluetooth module)
   - Verify 40kHz carrier generation

2. **Modulator Circuit**
   - Solder AD633 to protoboard
   - Connect bass signal to X input
   - Connect 40kHz carrier to Y input
   - Output to amplifier array

3. **Amplifier Assembly**
   - Mount 4x TPA3255 boards to heatsink
   - Wire in parallel from modulator output
   - Connect to 24V power supply

4. **Transducer Array**
   - Mount 16 transducers in 4x4 grid (5cm spacing)
   - Wire 4 transducers per amplifier
   - Aim array at user's torso (sternum target)

5. **Testing**
   - Apply 20Hz test tone
   - Measure SPL at 1m: target 100dB
   - Verify bone conduction perception (chest vibration)

## Performance Specs

- **Input Frequency**: 20-80Hz (bass range)
- **Carrier Frequency**: 40kHz (ultrasonic)
- **SPL Output**: 140dB @ transducer face
- **Effective Range**: 0.5-3 meters
- **Power Consumption**: 80W typical, 400W peak
- **Latency**: <5ms

---
**Build Time:** 2 days for experienced electrical engineer
**Testing:** Requires SPL meter + oscilloscope
