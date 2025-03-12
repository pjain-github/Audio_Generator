import streamlit as st
from audio_util import AudioUtil
import asyncio
from video_reverse import VideoReverser
import tempfile


def main():

    st.title("Audio Generator")

    st.sidebar.header("Settings")
    mode = st.sidebar.radio("Select Mode", ["Audio Generation", "Video Reversal"])

    if mode == "Audio Generation":

        if "text_input" not in st.session_state:
            st.session_state["text_input"] = None
        if "audio_path" not in st.session_state:
            st.session_state["audio_path"] = None
        if "sub_path" not in st.session_state:
            st.session_state["sub_path"] = None

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

    elif mode == "Video Reversal":

        vr = VideoReverser()
        if "video_path" not in st.session_state:
            st.session_state["video_path"] = None
        if "reversed_video" not in st.session_state:
            st.session_state["reversed_video"] = None

        uploaded_video = st.file_uploader("Upload your video file", type=["mp4"])
        
        if uploaded_video:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                temp_file.write(uploaded_video.read())
                st.session_state.video_path = temp_file.name
                st.success("Video uploaded successfully!")

            st.markdown("---")
            
            if st.button("Reverse Video"):

                reversed_video = vr.reverse_video(input_path=st.session_state.video_path, temp=False)

                st.session_state.reversed_video = reversed_video

                if st.session_state.reversed_video:
                    st.markdown(
                        f"""
                        <style>
                            video {{
                                max-height: 400px; /* Limit video height */
                                width: auto;
                                display: block;
                                margin: auto;
                            }}
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.video(st.session_state.reversed_video)
        

if __name__=="__main__":
    main()