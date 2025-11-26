import os
import json
import logging
from pathlib import Path
import streamlit as st
import yaml
from groq import Groq
from persona_prompt import PERSONA_PROMPT


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("groq_client")


# Load persona.yaml 
# -----------------
PERSONA_YAML_PATH = Path("persona.yaml")

if PERSONA_YAML_PATH.exists():
    with open(PERSONA_YAML_PATH, "r", encoding="utf-8") as f:
        persona_yaml = yaml.safe_load(f)
else:
    persona_yaml = None
    logger.warning("persona.yaml not found. Using only PERSONA_PROMPT.")


# Initialize Groq Client
# -----------------------
#API_KEY = os.environ.get("GROQ_API_KEY")
API_KEY=st.secrets["GROQ_API_KEY"]

if not API_KEY:
    raise RuntimeError(" GROQ_API_KEY missing!")

client = Groq(api_key=API_KEY)
logger.info("Groq client initialized successfully.")


# Persona Prompt Builder
# ----------------------
def build_full_prompt():
    """Build final system prompt: YAML + base persona."""
    
    yaml_section = ""
    if persona_yaml:
        traits = persona_yaml.get("persona", {}).get("traits", [])
        tone_avoid = persona_yaml.get("persona", {}).get("tone", {}).get("avoid", [])
        rules = persona_yaml.get("persona", {}).get("rules", [])

        yaml_section = (
            "## YAML TRAITS\n" + "\n".join(f"- {t}" for t in traits) + "\n\n"
            "## AVOID\n" + "\n".join(f"- {t}" for t in tone_avoid) + "\n\n"
            "## RULES\n" + "\n".join(f"- {r}" for r in rules) + "\n\n"
        )

    final_prompt = (
        f"{yaml_section}"
        f"## BASE PERSONA\n{PERSONA_PROMPT}\n\n"
        "## INSTRUCTIONS\n"
        "Respond as Dhruv: humble, structured, conversational, reflective, story-driven.\n"
        "Keep answers 50–150 words. Avoid bragging.\n"
    )

    return final_prompt


# Speech → Text (Whisper)
# -----------------------
def speech_to_text(audio_bytes: bytes, filename: str = "input.wav") -> str:
    """Send audio bytes to Groq Whisper and return transcript."""
    try:
        response = client.audio.transcriptions.create(
            file=(filename, audio_bytes),
            model="whisper-large-v3"
        )
        return response.text
    except Exception as e:
        logger.exception("Whisper transcription failed: %s", e)
        return ""


# Text → LLaMA Response
# ---------------------
def generate_answer(user_text: str, temperature: float = 0.5, max_tokens: int = 300) -> str:
    """Send user message to LLaMA model with persona conditioning."""
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": build_full_prompt()},
                {"role": "user", "content": user_text}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        return completion.choices[0].message.content

    
    except Exception as e:
        logger.exception("LLM generation failed: %s", e)
        return "Sorry, I couldn't generate an answer right now."


# Text → Speech (TTS)
# -------------------
def text_to_speech(text: str, voice: str = "male-en-1") -> bytes:
    """Convert text to speech using Groq xtts-v2."""
    try:
        resp = client.audio.speech.create(
            model="playai-tts",
            voice="Fritz-PlayAI" ,
            input=text
        )

        # Groq returns raw audio bytes directly
        return resp.read()

    except Exception as e:
        logger.exception("TTS generation failed: %s", e)
        return b""
