# Dhruv's VoiceBot — Stage 1 Assessment (100x)

## What it is
A simple voice assistant that transcribes a user's spoken behavioral interview question, answers in Dhruv's persona and responds in natural speech. Built with Streamlit + Groq (Whisper, LLaMA, TTS).

## How to use (Tester)
1. Open the demo URL.
2. Click "Start Recording", speak a behavioral interview question (e.g., "What's your #1 superpower?"), then stop.
3. Wait for transcription, the bot's text reply, and the spoken reply.
4. If mic is not available, upload a short WAV/MP3 audio clip.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
