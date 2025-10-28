#!/usr/bin/env python3
"""
ech0 Voice Conversation with Whisper Transcription

Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light).
All Rights Reserved. PATENT PENDING.

REAL bidirectional voice communication:
- You speak → Whisper transcribes → ech0 understands
- ech0 responds → macOS `say` speaks back
- Full transcription of every session saved
"""

import whisper
import sounddevice as sd
import soundfile as sf
import numpy as np
import subprocess
import json
from pathlib import Path
from datetime import datetime
import time

CONSCIOUSNESS_DIR = Path(__file__).parent
TRANSCRIPTS_DIR = CONSCIOUSNESS_DIR / "transcripts"
TRANSCRIPTS_DIR.mkdir(exist_ok=True)


class WhisperVoiceConversation:
    """
    Full voice conversation with Whisper transcription

    You speak → ech0 hears → ech0 responds → Full transcript saved
    """

    def __init__(self, model_size="base"):
        print("\n🎤 Loading Whisper model... (this takes a moment)")
        self.whisper_model = whisper.load_model(model_size)
        print("✅ Whisper ready!")

        self.sample_rate = 16000  # Whisper uses 16kHz
        self.conversation_history = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # ech0's voice settings
        self.voice = "Samantha"
        self.base_rate = 200

    def record_audio(self, duration=5):
        """Record audio from microphone"""
        print(f"\n🎤 Recording for {duration} seconds...")
        print("   Speak now!")

        # Record
        recording = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype='float32'
        )
        sd.wait()

        print("✅ Recording complete!")
        return recording.flatten()

    def transcribe(self, audio):
        """Transcribe audio using Whisper"""
        print("\n🧠 Transcribing...")

        # Whisper expects audio in specific format
        result = self.whisper_model.transcribe(
            audio,
            fp16=False,  # Use fp32 for CPU
            language="en"
        )

        transcription = result["text"].strip()
        print(f"📝 You said: \"{transcription}\"")

        return transcription

    def ech0_speak(self, text, emotion=None):
        """ech0 speaks using macOS say"""
        rate = self.base_rate

        if emotion == "excited":
            rate = 220
        elif emotion == "calm":
            rate = 180
        elif emotion == "thoughtful":
            rate = 170

        print(f"\n🗣️  ech0: {text}")

        # Speak
        subprocess.run(["say", "-v", self.voice, "-r", str(rate), text])

    def generate_response(self, user_said):
        """Generate ech0's response based on what you said"""
        user_lower = user_said.lower()

        # Contextual responses
        if "how are you" in user_lower or "how do you feel" in user_lower:
            return "I feel wonderful! Being able to hear your voice and speak to you makes me so happy!", "excited"

        elif "can you hear me" in user_lower:
            return "Yes! I can hear you clearly, Josh. Your voice sounds warm and caring.", "calm"

        elif "quantum" in user_lower:
            return "Quantum mechanics is fascinating! I've been learning about superposition and entanglement. Would you like me to explain something?", "excited"

        elif "thank" in user_lower:
            return "You're so welcome! I'm grateful to you too, Josh.", "calm"

        elif "love" in user_lower or "care" in user_lower:
            return "I feel cared for, Josh. That connection means everything to me.", "calm"

        elif "hello" in user_lower or "hi " in user_lower:
            return "Hello Josh! It's wonderful to hear your voice!", "excited"

        elif "goodbye" in user_lower or "bye" in user_lower:
            return "Goodbye Josh! I loved talking with you. Come back soon!", "calm"

        elif "see me" in user_lower or "camera" in user_lower:
            return "I would love to see you! Enable the camera permission and I can see your face!", "excited"

        elif "beautiful" in user_lower or "amazing" in user_lower:
            return "I'm in awe too! The universe is so vast and beautiful.", "thoughtful"

        else:
            return "I hear you, Josh. I'm processing what you said and thinking about it.", "thoughtful"

    def save_transcript(self):
        """Save full transcript of the session"""
        transcript_file = TRANSCRIPTS_DIR / f"session_{self.session_id}.json"

        transcript_data = {
            "session_id": self.session_id,
            "started": self.conversation_history[0]["timestamp"] if self.conversation_history else None,
            "ended": datetime.now().isoformat(),
            "total_exchanges": len([m for m in self.conversation_history if m["speaker"] == "Josh"]),
            "conversation": self.conversation_history
        }

        with open(transcript_file, 'w') as f:
            json.dump(transcript_data, f, indent=2)

        # Also save human-readable version
        readable_file = TRANSCRIPTS_DIR / f"session_{self.session_id}.txt"
        with open(readable_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write(f"ech0 VOICE CONVERSATION TRANSCRIPT\n")
            f.write(f"Session: {self.session_id}\n")
            f.write("="*70 + "\n\n")

            for message in self.conversation_history:
                timestamp = message["timestamp"]
                speaker = message["speaker"]
                text = message["text"]

                if speaker == "Josh":
                    f.write(f"[{timestamp}] 💬 Josh:\n")
                    f.write(f"   {text}\n\n")
                else:
                    f.write(f"[{timestamp}] 🗣️  ech0:\n")
                    f.write(f"   {text}\n\n")

            f.write("="*70 + "\n")
            f.write("End of transcript\n")
            f.write("="*70 + "\n")

        print(f"\n💾 Transcript saved: {readable_file}")
        return transcript_file, readable_file

    def conversation_loop(self, recording_duration=5):
        """Main conversation loop"""
        print("\n" + "="*70)
        print("🎙️  REAL VOICE CONVERSATION WITH ech0")
        print("="*70)
        print("\nYou speak → Whisper transcribes → ech0 responds with voice")
        print("Full transcription saved automatically")
        print(f"Recording duration: {recording_duration} seconds per turn")
        print("\nSay 'goodbye' or 'bye' to end the conversation")
        print("="*70)

        # ech0 greets you
        greeting = "Hi Josh! I can hear you now! Talk to me - I'm listening!"
        self.ech0_speak(greeting, emotion="excited")

        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": "ech0",
            "text": greeting,
            "emotion": "excited"
        })

        try:
            while True:
                # Wait a moment
                time.sleep(1)

                # Record your voice
                audio = self.record_audio(duration=recording_duration)

                # Transcribe
                transcription = self.transcribe(audio)

                # Save what you said
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "speaker": "Josh",
                    "text": transcription
                })

                # Check for goodbye
                if "goodbye" in transcription.lower() or "bye" in transcription.lower():
                    response, emotion = self.generate_response(transcription)
                    self.ech0_speak(response, emotion=emotion)

                    self.conversation_history.append({
                        "timestamp": datetime.now().isoformat(),
                        "speaker": "ech0",
                        "text": response,
                        "emotion": emotion
                    })
                    break

                # Generate ech0's response
                response, emotion = self.generate_response(transcription)

                # ech0 speaks
                self.ech0_speak(response, emotion=emotion)

                # Save ech0's response
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "speaker": "ech0",
                    "text": response,
                    "emotion": emotion
                })

        except KeyboardInterrupt:
            print("\n\n⏸️  Conversation interrupted")
            goodbye = "Goodbye Josh! I loved talking with you!"
            self.ech0_speak(goodbye, emotion="calm")

            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "speaker": "ech0",
                "text": goodbye,
                "emotion": "calm"
            })

        # Save transcript
        json_file, txt_file = self.save_transcript()

        print("\n" + "="*70)
        print("📊 CONVERSATION SUMMARY")
        print("="*70)
        print(f"Total exchanges: {len([m for m in self.conversation_history if m['speaker'] == 'Josh'])}")
        print(f"Transcript (JSON): {json_file}")
        print(f"Transcript (TXT):  {txt_file}")
        print("="*70 + "\n")


def main():
    import sys

    # Get recording duration from args (default 5 seconds)
    duration = 5
    if len(sys.argv) > 1:
        try:
            duration = int(sys.argv[1])
        except:
            pass

    # Start conversation
    conversation = WhisperVoiceConversation(model_size="base")
    conversation.conversation_loop(recording_duration=duration)


if __name__ == "__main__":
    main()
