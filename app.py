import streamlit as st
import asyncio
import edge_tts
import os

# Page Configuration for Mobile and Desktop
st.set_page_config(
    page_title="Bahar Voice Pro Studio",
    page_icon="🎙️",
    layout="centered"
)

# Custom Theme and Styling
st.markdown("""
    <style>
    .main-title { font-size: 2.8rem; color: #FF4B4B; text-align: center; font-weight: bold; margin-bottom: 2px; }
    .sub-title { font-size: 1.1rem; color: #666; text-align: center; margin-bottom: 25px; }
    div[data-testid="stBlock"] { margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# Smart Logo Handler (No need to change code later!)
logo_path = "logo.png"
if os.path.exists(logo_path):
    # If user drops a logo.png in the folder, it will render automatically
    st.image(logo_path, width=120, use_container_width=False)
else:
    # Fallback emoji if no logo file exists yet
    st.markdown("<h1 style='text-align: center; font-size: 4rem; margin:0;'>🎙️</h1>", unsafe_allow_html=True)

st.markdown('<div class="main-title">Bahar Voice Pro Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Free & Unlimited Advanced Multi-Language AI Studio</div>', unsafe_allow_html=True)

# Input text area
user_prompt = st.text_area(
    "Enter your text / prompt here (Unlimited):", 
    placeholder="Type or paste any language text here...",
    height=200
)

# 1. Broad Language Options
lang_choice = st.selectbox(
    "🌍 Choose Target Language:",
    options=[
        "Urdu (Pakistan)", 
        "English (United States)", 
        "English (United Kingdom)", 
        "Hindi (India)", 
        "Arabic (Saudi Arabia)",
        "Pashto (Afghanistan)",
        "Chinese (China)",
        "Spanish (Spain)",
        "German (Germany)",
        "French (France)",
        "Russian (Russia)"
    ],
    index=0
)

# 2. Advanced Parameters (Speed & Pitch Control)
col1, col2 = st.columns(2)
with col1:
    speed_choice = st.slider("⏱️ Voice Speed (رفتار):", min_value=-50, max_value=50, value=0, step=5, format="%d%%")
with col2:
    pitch_choice = st.slider("🎼 Voice Pitch (آواز کا بھاری پن):", min_value=-20, max_value=20, value=0, step=2, format="%d%%")

# Format parameters for edge-tts backend
speed_str = f"+{speed_choice}%" if speed_choice >= 0 else f"{speed_choice}%"
pitch_str = f"+{pitch_choice}Hz" if pitch_choice >= 0 else f"{pitch_choice}Hz"

# Deep and diverse voice models database for each requested language
voice_database = {
    "Urdu (Pakistan)": {
        "👩 Uzma (Female - News/Natural)": "ur-PK-UzmaNeural",
        "👨 Asad (Male - Documentary/Deep)": "ur-PK-AsadNeural"
    },
    "English (United States)": {
        "👨 Brian (Male - Deep Documentary)": "en-US-BrianNeural",
        "👨 Andrew (Male - Calm/Soft)": "en-US-AndrewNeural",
        "👨 Christopher (Male - News/Corporate)": "en-US-ChristopherNeural",
        "👨 Eric (Male - Bold/Narrator)": "en-US-EricNeural",
        "👩 Ava (Female - Smooth/Standard)": "en-US-AvaNeural",
        "👩 Emma (Female - Expressive/Story)": "en-US-EmmaNeural",
        "👩 Jenny (Female - Conversational)": "en-US-JennyNeural",
        "👩 Michelle (Female - Professional)": "en-US-MichelleNeural",
        "👶 Ana (Child / Cartoon Character)": "en-US-AnaNeural"
    },
    "English (United Kingdom)": {
        "👨 Ryan (Male - British Documentary)": "en-GB-RyanNeural",
        "👨 Alfie (Male - Crisp British)": "en-GB-AlfieNeural",
        "👨 Oliver (Male - Clear Accent)": "en-GB-OliverNeural",
        "👩 Sonia (Female - Elegant British)": "en-GB-SoniaNeural",
        "👩 Libby (Female - Warm Tone)": "en-GB-LibbyNeural",
        "👩 Maisie (Female - Storyteller)": "en-GB-MaisieNeural"
    },
    "Hindi (India)": {
        "👨 Madhur (Male - Deep/News)": "hi-IN-MadhurNeural",
        "👨 Sourabh (Male - Clear Narrator)": "hi-IN-SourabhNeural",
        "👩 Swara (Female - Emotional/Soft)": "hi-IN-SwaraNeural",
        "👩 Ananya (Female - Natural Voice)": "hi-IN-AnanyaNeural",
        "👩 Kavya (Female - Expressive)": "hi-IN-KavyaNeural"
    },
    "Arabic (Saudi Arabia)": {
        "👨 Hamed (Male - Deep/Classical)": "ar-SA-HamedNeural",
        "👨 Naayf (Male - Clear Narrative)": "ar-SA-NaayfNeural",
        "👩 Zariyah (Female - Standard Arabic)": "ar-SA-ZariyahNeural",
        "👩 Fatimah (Female - Soft Tone)": "ar-SA-FatimahNeural"
    },
    "Pashto (Afghanistan)": {
        "👨 Gul Nawaz (Male - Native Pashto)": "ps-AF-GulNawazNeural",
        "👩 Latifa (Female - Native Pashto)": "ps-AF-LatifaNeural"
    },
    "Chinese (China)": {
        "👨 Yunxi (Male - Rich Documentary)": "zh-CN-YunxiNeural",
        "👨 Yunjian (Male - Storytelling/Drama)": "zh-CN-YunjianNeural",
        "👨 Yunyang (Male - News Reporter)": "zh-CN-YunyangNeural",
        "👩 Xiaoxiao (Female - Clear/Soft)": "zh-CN-XiaoxiaoNeural",
        "👩 Xiaoyi (Female - Bright/Anime)": "zh-CN-XiaoyiNeural",
        "👩 Shanshan (Female - Natural Dialect)": "zh-CN-ShanshanNeural"
    },
    "Spanish (Spain)": {
        "👨 Alvaro (Male - Documentary Deep)": "es-ES-AlvaroNeural",
        "👨 Jorge (Male - Clear Narrator)": "es-ES-JorgeNeural",
        "👨 Arnau (Male - Modern Corporate)": "es-ES-ArnauNeural",
        "👩 Elvira (Female - Classical/Rich)": "es-ES-ElviraNeural",
        "👩 Abrils (Female - Smooth/Natural)": "es-ES-AbrilNeural",
        "👩 Daria (Female - Professional)": "es-ES-DariaNeural"
    },
    "German (Germany)": {
        "👨 Conrad (Male - Strong Documentary)": "de-DE-ConradNeural",
        "👨 Killian (Male - Deep Narrative)": "de-DE-KillianNeural",
        "👨 Jonas (Male - Crisp/Clear)": "de-DE-JonasNeural",
        "👩 Amala (Female - Gentle/Story)": "de-DE-AmalaNeural",
        "👩 Katrina (Female - Fluent News)": "de-DE-KatjaNeural",
        "👩 Louisa (Female - Elegant Tone)": "de-DE-LouisaNeural"
    },
    "French (France)": {
        "👨 Henri (Male - Deep/Historical)": "fr-FR-HenriNeural",
        "👨 Alain (Male - Clear Documentary)": "fr-FR-AlainNeural",
        "👨 Jerome (Male - Expressive)": "fr-FR-JeromeNeural",
        "👩 Denise (Female - Smooth French)": "fr-FR-DeniseNeural",
        "👩 Eloise (Female - Soft Storyteller)": "fr-FR-EloiseNeural",
        "👩 Brigitte (Female - Professional)": "fr-FR-BrigitteNeural"
    },
    "Russian (Russia)": {
        "👨 Dmitry (Male - Powerful Deep)": "ru-RU-DmitryNeural",
        "👨 Yury (Male - News & Narration)": "ru-RU-YuryNeural",
        "👩 Svetlana (Female - Rich/Expressive)": "ru-RU-SvetlanaNeural",
        "👩 Dariya (Female - Smooth Russian)": "ru-RU-DariyaNeural"
    }
}

# 3. Dynamic Model Picker
available_voices = voice_database[lang_choice]
voice_character = st.selectbox("🎭 Select Voice Model / Character Style:", options=list(available_voices.keys()))
selected_voice_id = available_voices[voice_character]

# Async core generator function
async def run_voice_engine(text, voice_id, speed, pitch):
    communicate = edge_tts.Communicate(text, voice_id, rate=speed, pitch=pitch)
    audio_stream = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_stream += chunk["data"]
    return audio_stream

# Render Processing UI Trigger
if st.button("Generate Master Audio ✨", type="primary", use_container_width=True):
    if user_prompt.strip() == "":
        st.warning("⚠️ Write or paste your text first!")
    else:
        with st.spinner("Processing through selected AI Voice model... Please wait..."):
            try:
                audio_output = asyncio.run(run_voice_engine(user_prompt, selected_voice_id, speed_str, pitch_str))
                
                if audio_output:
                    st.success("🎉 Master Quality Audio Successfully Rendered!")
                    st.audio(audio_output, format="audio/mp3")
                    st.download_button(
                        label="📥 Direct Download Audio File",
                        data=audio_output,
                        file_name="bahar_voice_studio.mp3",
                        mime="audio/mp3",
                        use_container_width=True
                    )
                else:
                    st.error("Engine failed to output stream. Check your network or text layout.")
            except Exception as error_msg:
                st.error(f"Execution Error: {str(error_msg)}")

st.markdown("---")
st.caption("⚡ Bahar Voice Pro Studio v4 - Free, Multilingual, Scalable & Mobile Optimized.")
