import streamlit as st
from st_audiorec import st_audiorec
from groq_client import speech_to_text, generate_answer, text_to_speech
from pydub import AudioSegment



st.set_page_config(page_title="Dhruv's Self VoiceBot", layout="centered",page_icon="assets/Icon.ico")
st.title("🎤 Dhruv's VoiceBot ")

st.markdown(
    "Press **Start Recording**, ask a question aloud, then press **Stop Recording**. "
    "Or upload a short WAV/MP3 audio clip. Click **Generate Answer** to get the reply."
)


# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_bot_reply" not in st.session_state:
    st.session_state.last_bot_reply = None

st.write("Press record, speak your question, and wait for the assistant's response.")


audio_bytes = st_audiorec()
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    # Speech → Text
    # -------------------------------
    st.subheader("📝 Transcribing your speech...")
    transcript = speech_to_text(audio_bytes)

    if transcript.strip() == "":
        st.error("Could not understand audio. Try again.")
    else:
        st.success("Transcription complete!")
        st.write(f"**You said:** {transcript}")

     
        # LLaMA → Answer
        # -------------------------------
        st.subheader("🤖 Generating Dhruv-style answer...")
        answer = generate_answer(transcript)

        st.write("### 💬 Bot Answer")
        st.write(answer)


        # TTS → Voice Output
        # -------------------------------
        st.subheader("🔊 Playing voice response...")
        tts_audio = text_to_speech(answer)

        if tts_audio:
            st.audio(tts_audio, format="audio/mp3")
        else:
            st.error("TTS failed. Try again.")