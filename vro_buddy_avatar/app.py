import streamlit as st
import requests
import base64
import os

# ------------------------------
# CONFIGURATION
# ------------------------------
st.set_page_config(page_title="VRO Buddy Avatar", layout="centered")
ELEVENLABS_API_KEY = st.secrets.get("ELEVENLABS_API_KEY", "")
DID_API_KEY = st.secrets.get("DID_API_KEY", "")

# ------------------------------
# UI LAYOUT
# ------------------------------
st.title("🤖 VRO Buddy Avatar")
st.write("AI Avatar introducing VRO in English and Hindi with natural lip-sync.")

# Static avatar image (provided)
avatar_path = "result-pic-7.png"
st.image(avatar_path, width=300, caption="VRO Buddy")

# ------------------------------
# INPUTS
# ------------------------------
language = st.radio("Select Language", ["English", "Hindi"])
script_text = st.text_area(
    "Enter your intro script:",
    "Hello! I’m VRO Buddy. Welcome to VRO! Let's explore the world of innovation together!" 
    if language == "English" else 
    "नमस्ते! मैं हूँ VRO Buddy. VRO में आपका स्वागत है! आइए मिलकर नवाचार की दुनिया में कदम रखें!"
)

# ------------------------------
# GENERATE AUDIO (Text-to-Speech)
# ------------------------------
def generate_tts_elevenlabs(text, lang):
    voice_id = "Rachel" if lang == "English" else "Bella"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        audio_path = "output_audio.mp3"
        with open(audio_path, "wb") as f:
            f.write(response.content)
        return audio_path
    else:
        st.error("TTS generation failed.")
        st.write(response.text)
        return None

# ------------------------------
# GENERATE LIP-SYNC VIDEO (D-ID)
# ------------------------------
def generate_lipsync_video(audio_path):
    with open(audio_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode("utf-8")

    url = "https://api.d-id.com/talks"
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "source_url": "https://yourdomain.com/vro_avatar.png",  # optional: replace with hosted image
        "audio": {"data": audio_b64, "driver_url": "audio://default"}
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        talk_id = response.json().get("id")
        st.success("Video generation started...")
        video_url = f"https://api.d-id.com/talks/{talk_id}"
        return video_url
    else:
        st.error("Lip-sync video generation failed.")
        st.write(response.text)
        return None

# ------------------------------
# ACTION BUTTON
# ------------------------------
if st.button("🎬 Generate VRO Buddy Intro"):
    if ELEVENLABS_API_KEY and DID_API_KEY:
        with st.spinner("Generating audio..."):
            audio_path = generate_tts_elevenlabs(script_text, language)
        if audio_path:
            st.audio(audio_path, format="audio/mp3")

            with st.spinner("Creating lip-synced avatar video..."):
                video_url = generate_lipsync_video(audio_path)
                if video_url:
                    st.video(video_url)
    else:
        st.warning("Please add your API keys in Streamlit secrets.")

# ------------------------------
# README Info
# ------------------------------
st.markdown("""
### 📘 README
**TTS Engine:** [ElevenLabs](https://elevenlabs.io)  
**Lip-Sync Engine:** [D-ID API](https://www.d-id.com/)  
**Languages Supported:** English, Hindi  
**Instructions:**
1. Add `ELEVENLABS_API_KEY` and `DID_API_KEY` in `.streamlit/secrets.toml`
2. Upload the static image `vro_avatar.png`
3. Enter your intro script and click *Generate VRO Buddy Intro*.
4. The app will create a multilingual lip-synced avatar video.
""")


# ------------------------------
# FOOTER 
# ------------------------------

st.markdown("---")
    st.markdown("""
    <div style='text-align: center;'>
        <p>Developed with ❤️ using Streamlit</p>
        <p>© 2025 Prerna Gyanchandani.</p>
    </div>
    """, unsafe_allow_html=True)
