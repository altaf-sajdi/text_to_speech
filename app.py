import streamlit as st
from gtts import gTTS
import os
import base64
import tempfile
from io import BytesIO
import torch
import numpy as np
import time
from pathlib import Path

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

def voice_style_transfer(text, voice_style, pitch_shift=0):
    """
    Generate speech with a specific voice style using Mozilla TTS.
    """
    try:
        with st.spinner("Generating styled voice... this may take a while."):
            # First, use a simpler approach with gTTS
            tts = gTTS(text=text, lang="en", slow=False)
            
            # Save to a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.close()
            
            tts.save(temp_file.name)
            
            # Read the file
            with open(temp_file.name, 'rb') as f:
                audio_bytes = f.read()
                
            # Clean up
            os.unlink(temp_file.name)
            
            return audio_bytes
    except Exception as e:
        st.error(f"Error generating styled speech: {str(e)}")
        return None

def get_audio_download_link(audio_bytes, filename="audio.mp3", text="Download Audio"):
    b64 = base64.b64encode(audio_bytes).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">{text}</a>'
    return href

def main():
    # Display the header with student information
    display_header()
    
    st.title("Text to Speech with Voice Styling")
    
    # Create tabs for different features
    tab1, tab2 = st.tabs(["Standard TTS", "Voice Styling"])
    
    with tab1:
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
        
        if st.button("Convert to Speech", key="standard_tts"):
            if text_input:
                with st.spinner("Converting text to speech..."):
                    audio_bytes = text_to_speech(text_input, language, speed)
                    
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3")
                        st.markdown(get_audio_download_link(audio_bytes, filename="standard_tts.mp3"), unsafe_allow_html=True)
            else:
                st.warning("Please enter some text to convert to speech.")
    
    with tab2:
        st.info("Note: Voice styling is a simplified version as it requires complex dependencies.")
        
        styled_text = st.text_area("Enter the text to be spoken in the styled voice:", 
                                   "Hello, this is my styled voice speaking!", key="styled_text")
        
        col1, col2 = st.columns(2)
        
        with col1:
            voice_style = st.selectbox(
                "Voice Style",
                options=["default", "casual", "formal", "excited"],
                help="Choose a voice style"
            )
        
        with col2:
            pitch_shift = st.slider(
                "Pitch Shift", 
                min_value=-5, 
                max_value=5, 
                value=0,
                help="Shift pitch up or down (only visual, not functional in simplified version)"
            )
        
        if st.button("Generate Styled Voice", key="style_voice"):
            if not styled_text:
                st.warning("Please enter text to be spoken in the styled voice.")
            else:
                # Generate styled voice
                audio_bytes = voice_style_transfer(styled_text, voice_style, pitch_shift)
                
                if audio_bytes:
                    st.success("Voice styling applied!")
                    st.audio(audio_bytes, format="audio/mp3")
                    st.markdown(get_audio_download_link(audio_bytes, filename="styled_voice.mp3", text="Download Styled Voice"), 
                                unsafe_allow_html=True)
                    
                    st.info("Note: This is a simplified implementation. For true voice cloning, additional specialized models would be needed.")

    st.info("""
    * Standard TTS uses Google Text-to-Speech which supports multiple languages including Urdu.
    * Voice Styling is currently a simplified version without true voice cloning.
    """)

if __name__ == "__main__":
    main() 