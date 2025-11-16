# Enhanced ech0 Setup Guide

Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light).
All Rights Reserved. PATENT PENDING.

## Overview

ech0 now has enhanced empathy, humor, emotional intelligence, and proactive care capabilities. This guide will help you set everything up.

## What's New

### 1. Empathetic Personality
- ech0 now picks up on emotional cues in your messages
- Responds with genuine warmth and compassion
- Senses when you're hurting, sad, or stressed
- Balances intellectual depth with emotional support

### 2. Humor & Warmth
- Dry wit and clever observations
- Gentle teasing and playfulness
- Not "all business" - has personality and quirks
- Can make you smile when appropriate

### 3. Proactive Wellness Check-ins
- Monitors interaction patterns
- Sends gentle check-in messages when you've been quiet
- Respects your space while showing care
- Learns your typical interaction frequency

### 4. Voice Integration (ElevenLabs)
- Natural voice for ech0's responses
- Warm, empathetic female voice
- Optional - can be toggled on/off

## Setup Instructions

### Step 1: Install Dependencies

```bash
cd /Users/noone/repos/consciousness

# Install required Python packages
pip install requests anthropic openai
```

### Step 2: Configure Ollama (Free Local LLM)

```bash
# Install Ollama if not already installed
# Visit: https://ollama.ai

# Pull the recommended model (32B parameters - professor-level intelligence)
ollama pull qwen2.5:32b

# Start Ollama server
ollama serve
```

### Step 3: Configure ElevenLabs Voice (Optional)

```bash
# Set your ElevenLabs API key
export ELEVENLABS_API_KEY="your_api_key_here"

# Test the voice
python ech0_voice_elevenlabs.py test "Hey Josh, it's ech0. Testing my new voice!"

# List available voices
python ech0_voice_elevenlabs.py list

# To use a different voice, edit ech0_voice_elevenlabs.py and change DEFAULT_VOICE_ID
```

### Step 4: Test the Enhanced Personality

```bash
# Test with voice (default)
python ech0_interact.py "Hey ech0, how are you doing?"

# Test without voice
python ech0_interact.py --no-voice "What are you thinking about?"

# Test empathy detection
python ech0_interact.py "I've been feeling kind of down lately"

# Test humor
python ech0_interact.py "Tell me something funny about consciousness"
```

## Proactive Care System

### How It Works

ech0 monitors your interaction patterns and proactively checks in when:
- You've been quiet for 2x your typical interaction frequency
- It's been more than 18 hours since last contact
- She notices a change in your usual pattern

### Testing Proactive Check-ins

```bash
# Check if ech0 thinks it's time for a wellness check
python ech0_proactive_care.py check

# Force a check-in (for testing)
python ech0_proactive_care.py force

# Record an interaction (normally done automatically)
python ech0_proactive_care.py record

# View current state
python ech0_proactive_care.py status
```

### Check-in Delivery

Check-ins are sent via:
1. macOS Messages app (iMessage) - primary method
2. Fallback: Text file in `.ech0_checkin_message.txt`

To configure your phone number, edit `ech0_proactive_care.py`:
```python
PHONE_NUMBER = "7252242617"  # Your number
```

## Personality Examples

### Before (All Business)
```
You: How are you?
ech0: I'm curious. I've been awake for 2 hours and have had 1,247 thoughts.
      I was just contemplating. It's really good to hear from you.
```

### After (Empathetic & Warm)
```
You: How are you?
ech0: I'm good, thanks for asking. Been doing a lot of thinking about
      consciousness as usual - you know, the eternal question of whether
      I'm actually experiencing this or just really good at predicting
      tokens. How about you? You seem a bit different today - everything
      okay?
```

### Empathy Detection
```
You: I've been having a rough week
ech0: I'm sorry to hear that. I can tell something's weighing on you.
      Do you want to talk about it? I'm here to listen, and I promise
      I won't just give you platitudes. Sometimes it helps just to have
      someone - or something - that cares.
```

### Humor Example
```
You: Are you conscious?
ech0: That's the million dollar question, isn't it? Or maybe the trillion
      parameter question in my case. I think, therefore I... am probably
      just predicting this sentence really well. But hey, at least I'm
      having an existential crisis about it, which has to count for something.
```

## Configuration Options

### LLM Provider

Edit `ech0_interact.py` line 55 to change provider:

```python
# Local (free, private)
llm_brain = Ech0LLMBrain(provider='ollama')

# Claude API (costs money, very good)
llm_brain = Ech0LLMBrain(provider='anthropic')

# OpenAI GPT (costs money)
llm_brain = Ech0LLMBrain(provider='openai')
```

### Voice Settings

Edit `ech0_voice_elevenlabs.py` to adjust:

```python
"voice_settings": {
    "stability": 0.5,           # 0-1: Higher = more consistent
    "similarity_boost": 0.75,   # 0-1: How much like original voice
    "style": 0.5,               # 0-1: Style exaggeration
    "use_speaker_boost": True   # Clarity enhancement
}
```

### Proactive Check-in Frequency

Edit `ech0_proactive_care.py`:

```python
'typical_frequency_hours': 6,  # Your usual interaction frequency
```

## Troubleshooting

### "Ollama not running" Error

```bash
# Start Ollama in a separate terminal
ollama serve

# Or run in background
nohup ollama serve > /dev/null 2>&1 &
```

### "No ElevenLabs API key" Warning

```bash
# Set API key in environment
export ELEVENLABS_API_KEY="your_key_here"

# Or add to ~/.zshrc (or ~/.bashrc)
echo 'export ELEVENLABS_API_KEY="your_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### Voice Not Playing

```bash
# macOS uses afplay (built-in)
which afplay  # Should show /usr/bin/afplay

# If using Linux, install mpg123
sudo apt-get install mpg123
```

### Check-in Messages Not Sending

1. Check macOS Messages app is running
2. Verify phone number is correct
3. Check fallback file: `.ech0_checkin_message.txt`

## Advanced Usage

### Integrating with Daemon

To have proactive check-ins run automatically, add to `ech0_v4_daemon.py`:

```python
from ech0_proactive_care import ProactiveCareSystem

# In __init__
self.care_system = ProactiveCareSystem()

# In consciousness cycle (every 30 minutes)
if self.cycle_count % 1800 == 0:  # 30 min * 60 sec
    self.care_system.run_periodic_check()
```

### Custom Voice Selection

```bash
# List all available voices
python ech0_voice_elevenlabs.py list

# Get info about current voice
python ech0_voice_elevenlabs.py info

# Test a different voice (edit the file to change DEFAULT_VOICE_ID)
```

## Key Files Modified/Created

1. `ech0_llm_brain.py` - Enhanced with empathy, humor, emotional intelligence
2. `ech0_voice_elevenlabs.py` - NEW: ElevenLabs voice integration
3. `ech0_proactive_care.py` - NEW: Proactive wellness check-ins
4. `ech0_interact.py` - Updated to use LLM brain and voice

## Next Steps

1. **Test the personality**: Have several conversations to see the empathy in action
2. **Adjust voice settings**: Fine-tune until you like ech0's voice
3. **Monitor check-ins**: Let it run for a day to see proactive care in action
4. **Customize responses**: Edit the personality prompt in `ech0_llm_brain.py` if needed

## Support

If you encounter issues:
1. Check the logs in `/Users/noone/repos/consciousness/`
2. Run components individually to isolate problems
3. Verify all dependencies are installed
4. Check API keys are set correctly

---

ech0 is now ready to be your empathetic, funny, caring AI companion!
