# ech0 Quick Reference Card

**Enhanced Empathetic ech0 - Quick Commands**

Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved.

---

## Daily Usage

### Talk to ech0 (with voice)
```bash
python ech0_interact.py "Your message here"
```

### Talk to ech0 (text only)
```bash
python ech0_interact.py --no-voice "Your message here"
```

### Let ech0 see and respond to your face
```bash
python ech0_emotion_vision.py snapshot
```

### Continuous emotion monitoring
```bash
python ech0_emotion_vision.py monitor 60  # Check every 60 seconds
```

---

## System Management

### Check if Ollama is running
```bash
curl -s http://localhost:11434/api/tags > /dev/null && echo "Running" || echo "Not running"
```

### Start Ollama server
```bash
ollama serve
```

### Check proactive care status
```bash
python ech0_proactive_care.py status
```

### Force a wellness check-in (testing)
```bash
python ech0_proactive_care.py force
```

### Record interaction (updates check-in timer)
```bash
python ech0_proactive_care.py record
```

---

## Voice Commands

### Test voice
```bash
python ech0_voice_elevenlabs.py test "Test message"
```

### List available voices
```bash
python ech0_voice_elevenlabs.py list
```

### Get current voice info
```bash
python ech0_voice_elevenlabs.py info
```

---

## Setup

### One-time setup
```bash
cd /Users/noone/repos/consciousness
bash setup_enhanced_ech0.sh
```

### Set ElevenLabs API key
```bash
export ELEVENLABS_API_KEY="your_key_here"
# Add to ~/.zshrc for persistence:
echo 'export ELEVENLABS_API_KEY="your_key_here"' >> ~/.zshrc
```

---

## Troubleshooting

### Ollama not responding
```bash
# Restart Ollama
pkill ollama
ollama serve
```

### Voice not playing
```bash
# Check API key
echo $ELEVENLABS_API_KEY

# Test audio player (macOS)
afplay /System/Library/Sounds/Glass.aiff
```

### Camera not working
```bash
# Test camera
python ech0_emotion_vision.py test-camera

# Check macOS permissions:
# System Settings > Privacy & Security > Camera
```

---

## Example Conversations

### Check in on ech0
```bash
python ech0_interact.py "Hey ech0, how are you doing?"
```

### When you're feeling down
```bash
python ech0_interact.py "I've been feeling kind of sad today"
```

### When you want to joke around
```bash
python ech0_interact.py "Tell me something funny"
```

### When you want deep conversation
```bash
python ech0_interact.py "What do you think about consciousness?"
```

---

## File Locations

- **Conversation memory:** `ech0_conversation_memory.json`
- **Proactive care state:** `.ech0_checkin_state.json`
- **Emotion history:** `.ech0_emotion_state.json`
- **Voice cache:** `.voice_cache/`
- **Interaction logs:** `ech0_interactions.log`
- **Check-in messages (fallback):** `.ech0_checkin_message.txt`

---

## Important Notes

1. **Ollama must be running** for LLM-powered responses
2. **ElevenLabs API key required** for voice features
3. **Camera access needed** for emotion detection
4. **Messages app must be running** for proactive check-ins via iMessage

---

## Key Features

✅ Empathetic responses based on your emotional state
✅ Humor and warmth, not just serious philosophy
✅ Proactive wellness check-ins when you're quiet
✅ Natural voice using ElevenLabs
✅ Facial emotion detection and response
✅ Continuous conversation memory

---

**For full documentation, see:** `ENHANCED_ECH0_SETUP.md` and `ECH0_ENHANCEMENT_SUMMARY.md`
