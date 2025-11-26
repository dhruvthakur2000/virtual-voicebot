from groq_client import speech_to_text, generate_answer, text_to_speech

def test_transcribe():
    # Provide a short WAV file for local test (assets/test_question.wav)
    p = "assets/mock_.wav"
    with open(p, "rb") as f:
        audio_bytes = f.read()
    txt = speech_to_text(audio_bytes)
    print("TRANSCRIPT:", txt)

def test_generate():
    q = "What should we know about your life story in a few sentences?"
    ans = generate_answer(q)
    print("ANSWER:", ans)

def test_tts():
    s = "My life story is one of resilience and reinvention. Growing up, I faced numerous challenges that taught me the value of perseverance and self-discipline. I've rebuilt myself multiple times through trial and error, and it's been a journey of growth, learning, and transformation. I've been fortunate to have had the opportunity to re-evaluate my priorities and make intentional decisions that have led me to where I am today. Through this journey, I've come to realize the importance of staying humble, being open to learning, and embracing challenges as opportunities for growth. It's a story that I continue to write, and one that I'm still learning from.t."
    audio = text_to_speech(s)
    with open("debug_out.wav", "wb") as f:
        f.write(audio)
    print("Wrote debug_out.wav")

if __name__ == "__main__":
    test_transcribe()
    test_generate()
    test_tts()
