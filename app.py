import streamlit as st
from audio_util import AudioUtil
import asyncio


def main():

    if "text_input" not in st.session_state:
        st.session_state["text_input"] = None
    if "audio_path" not in st.session_state:
        st.session_state["audio_path"] = None
    if "sub_path" not in st.session_state:
        st.session_state["sub_path"] = None

    st.title("Audio Generator")

    audio_util = AudioUtil()

        
    text_input = st.text_area("Enter Text for Audio")
    if text_input:
        st.session_state.text_input = text_input
        
    pitch = st.slider("Pitch Adjustment (Hz)", -30, 30, 0)
    speed = st.slider("Speed Adjustment (%)", -50, 50, 0)

    if pitch <=0:
        pitch = f"{pitch}Hz" if pitch != 0 else None
    else:
        pitch = f"+{pitch}Hz" if pitch != 0 else None
    
    if speed<=0:
        speed = f"{speed}%" if speed != 0 else None
    else:
        speed = f"+{speed}%" if speed != 0 else None


    # Generate Audio
    if st.button("Generate Audio"):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_path = loop.run_until_complete(audio_util.text_to_speech_edge(text=st.session_state.text_input, rate=speed, pitch=pitch))

        if not audio_path:
            st.error("Error generating audio. Check your input or API settings.")
        else:
            st.session_state.audio_path = audio_path
            st.success("Audio generated successfully!")
        
    if st.session_state.audio_path:
        st.audio(st.session_state.audio_path, format='audio/mp3')
        
if __name__=="__main__":
    main()