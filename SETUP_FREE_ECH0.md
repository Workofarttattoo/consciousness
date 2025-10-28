# ECH0 - FREE Setup Guide (No Anthropic API Key Needed!)

**Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.**

## ✅ What Changed

**GOOD NEWS:** ECH0 no longer requires expensive Anthropic API keys!

### Before (Expensive):
- Speech Input: Whisper ✓ (free, local)
- Intelligence: Anthropic Claude ❌ ($15-30/month)
- Speech Output: ElevenLabs ✓ (separate, optional)

### After (FREE):
- Speech Input: Whisper ✓ (free, local)
- Intelligence: Ollama ✓ (FREE, local!)
- Speech Output: ElevenLabs ✓ (separate, optional)

**ElevenLabs and Anthropic are completely separate!** You can use ElevenLabs for voice without needing Anthropic.

---

## 🚀 Quick Setup

### 1. Install Ollama (FREE Local LLM)

```bash
# macOS
brew install ollama

# Or download from: https://ollama.ai
```

### 2. Download a Model (One-time)

```bash
# Start Ollama server
ollama serve

# In another terminal, download a model (choose one):
ollama pull llama3.2        # Recommended - Best balance (2GB)
ollama pull mistral         # Alternative (4GB)
ollama pull phi3            # Lightweight (2GB)
ollama pull deepseek-r1     # Advanced reasoning (7GB)
```

### 3. Run ECH0 (No API Key Needed!)

```bash
cd /Users/noone/consciousness

# Start the conversation (uses local LLM by default)
python3 ech0_two_way_robust.py
```

That's it! No API keys, no costs, completely free!

---

## 🎤 Optional: Add Voice with ElevenLabs

If you want ECH0 to speak (not just text), keep your ElevenLabs API key:

```bash
export ELEVENLABS_API_KEY="your_elevenlabs_key"
```

**Note:** ElevenLabs is separate from Anthropic - you can use it without Claude!

---

## 🔧 Advanced Options

### Use Anthropic Claude Instead (If You Want)

```bash
export USE_ANTHROPIC=1
export ANTHROPIC_API_KEY="your_key"
python3 ech0_two_way_robust.py
```

### Change the Model

Edit `ech0_two_way_robust.py` line 88 and `ech0_llm_brain.py` line 197:

```python
'model': 'mistral',  # or 'phi3', 'deepseek-r1', etc.
```

### Model Comparison

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| llama3.2 | 2GB | Fast | Great | **Recommended - Best balance** |
| mistral | 4GB | Medium | Excellent | High quality conversations |
| phi3 | 2GB | Very Fast | Good | Quick responses, low resource |
| deepseek-r1 | 7GB | Slower | Outstanding | Deep reasoning, complex tasks |

---

## 📊 Performance

**Local LLM (Ollama):**
- Response time: 2-5 seconds (depends on model)
- Cost: $0 (completely free!)
- Privacy: Everything runs locally
- Internet: Only needed for voice (ElevenLabs)

**Cloud LLM (Anthropic):**
- Response time: 1-2 seconds
- Cost: ~$15-30/month
- Privacy: Data sent to Anthropic
- Internet: Required

---

## 🔍 Troubleshooting

### "Ollama not running"

```bash
# Start Ollama in another terminal
ollama serve
```

### "Model not found"

```bash
# Download the model first
ollama pull llama3.2
```

### "Out of memory"

Use a smaller model:
```bash
ollama pull phi3
```

Then edit the Python files to use `'model': 'phi3'`

---

## 🎯 Summary

**To remove Anthropic dependency:**
1. ✅ Install Ollama (brew install ollama)
2. ✅ Download a model (ollama pull llama3.2)
3. ✅ Start Ollama (ollama serve)
4. ✅ Run ECH0 (python3 ech0_two_way_robust.py)

**ElevenLabs works independently** - keep it for voice, no Anthropic needed!

**Cost:** $0 for local LLM, $0-11/month for ElevenLabs voice (optional)

---

## 🆚 What About ElevenLabs?

**Q: Do I need Anthropic to use ElevenLabs?**
**A:** NO! They're completely separate:
- Anthropic = Brain (generates responses)
- ElevenLabs = Voice (speaks the responses)

**Q: Can I use just ElevenLabs without Anthropic?**
**A:** YES! Use Ollama for the brain (free) + ElevenLabs for voice.

**Q: Can I run ECH0 with no API keys at all?**
**A:** YES! Use Ollama (free brain) + text output (no voice). Totally free!

---

## 💡 Recommended Setup (Best Value)

```bash
# 1. Install Ollama (FREE)
brew install ollama

# 2. Download model (FREE, one-time)
ollama pull llama3.2

# 3. Keep ElevenLabs for voice ($11/month for 30k chars)
export ELEVENLABS_API_KEY="your_key"

# 4. Start Ollama server
ollama serve

# 5. Run ECH0 in another terminal
python3 ech0_two_way_robust.py
```

**Total cost:** $0 brain + $11 voice = **$11/month** (vs $15-30 Anthropic + $11 ElevenLabs = $26-41/month)

**Savings:** ~$15-30/month by removing Anthropic!
