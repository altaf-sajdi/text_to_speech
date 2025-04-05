import streamlit as st
from gtts import gTTS
import os
import base64
from io import BytesIO

# Set page configuration and add student information
st.set_page_config(page_title="Text to Speech App", layout="wide")

# Add student information at the top
def display_header():
    st.markdown("""
    <div style="background-color:#f0f2f6;padding:10px;border-radius:10px;margin-bottom:10px;">
        <h1 style="color:#ff4b4b;text-align:center;font-size:28px;">ALTAF SAJDI</h1>
        <h3 style="color:#0068c9;text-align:center;font-size:18px;">GIAIC Student</h3>
    </div>
    """, unsafe_allow_html=True)

def text_to_speech(text, language='en', speed=1.0):
    # Convert speed to the slow parameter (slow=True when speed < 0.75)
    slow = speed < 0.75
    
    try:
        tts = gTTS(text=text, lang=language, slow=slow)
        
        # Save to a BytesIO object
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        
        return mp3_fp.read()
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None

def get_audio_download_link(audio_bytes, filename="audio.mp3", text="Download Audio"):
    b64 = base64.b64encode(audio_bytes).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">{text}</a>'
    return href

def main():
    # Display the header with student information
    display_header()
    
    st.title("Text to Speech App")
    
    text_input = st.text_area("Enter the text you want to convert to speech:", 
                              "Hello, welcome to this text to speech application!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        language = st.selectbox(
            "Language",
            options=[
                "en", "ur", "hi", "ar", "fr", "es", "de", "it", "ja", "ko", "zh-CN"
            ],
            format_func=lambda x: {
                "en": "English", 
                "ur": "Urdu",
                "hi": "Hindi",
                "ar": "Arabic",
                "fr": "French",
                "es": "Spanish",
                "de": "German",
                "it": "Italian",
                "ja": "Japanese",
                "ko": "Korean",
                "zh-CN": "Chinese"
            }.get(x, x),
            index=0
        )
    
    with col2:
        speed = st.slider("Voice Speed", min_value=0.5, max_value=1.5, value=1.0, step=0.1, 
                         help="Values below 0.75 will use the 'slow' mode. Higher values use normal speed.")
    
    if st.button("Convert to Speech"):
        if text_input:
            with st.spinner("Converting text to speech..."):
                audio_bytes = text_to_speech(text_input, language, speed)
                
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")
                    st.markdown(get_audio_download_link(audio_bytes, filename="speech.mp3"), unsafe_allow_html=True)
        else:
            st.warning("Please enter some text to convert to speech.")
    
    st.info("This app uses Google Text-to-Speech (gTTS) which supports multiple languages including Urdu.")

if __name__ == "__main__":
    main() 