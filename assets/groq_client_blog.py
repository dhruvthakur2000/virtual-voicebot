import yaml
import os
from groq import Groq
from persona_prompt import PERSONA_PROMPT

#load full prompt
#-------------
def load_persona():
    """Combine YAML + persona prompt + user text into a single prompt for the model."""
    
    # Load YAML
    with open("persona.yaml", "r", encoding="utf-8") as f:
        persona_data = yaml.safe_load(f)

    # Load persona prompt
    from persona_prompt import PERSONA_PROMPT
    
    # Merge both into one system prompt
    system_prompt = (
        PERSONA_PROMPT
        + "\n\nAdditional Persona Configurations:\n"
        + yaml.dump(persona_data)
    )
    
    return system_prompt

#client initialization
#---------------------
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(" GROQ_API_KEY not found in environment variables.")
    
    return Groq(api_key=api_key)

#transcription
#-------------
def transcribe_audio(audio_file_path: str):
    """
    Converts speech to text using Groq Whisper-Large-V3.
    audio_file_path = local .wav or .mp3 file
    """

    client = get_groq_client()

    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3"
        )

    return transcription.text

# LLM RESPONSE (Llama 3.1)
# -------------------------------
def generate_llm_reply(user_text: str):
    """
    Sends text to Llama model with persona conditioning.
    """
    system_prompt = load_persona()
    client = get_groq_client()

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ],
        max_tokens=600,
        temperature=0.7
    )

    return response.choices[0].message["content"]