import streamlit as st
import numpy as np
import wave
from io import BytesIO

def calculate_rms_from_bytes(audio_bytes):
    with wave.open(BytesIO(audio_bytes), 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        sample_width = wf.getsampwidth()
        if sample_width == 2:
            dtype = np.int16
        elif sample_width == 4:
            dtype = np.int32
        else:
            st.error("Unsupported sample width")
            return None
        samples = np.frombuffer(frames, dtype=dtype)
        rms = np.sqrt(np.mean(samples.astype(np.float64)**2))
        return round(rms, 2)

st.set_page_config(page_title="Audio Loudness Analyzer", layout="centered")
st.title("🎧 Audio Loudness Analyzer Using RMS")

uploaded_file = st.file_uploader("Upload a WAV file", type=["wav"])

if uploaded_file:
    st.audio(uploaded_file, format="audio/wav")
    audio_bytes = uploaded_file.read()
    rms_value = calculate_rms_from_bytes(audio_bytes)
    if rms_value:
        st.success(f"RMS Loudness Value: {rms_value}")
        if rms_value > 3000:
            st.write("🔊 Loud")
        else:
            st.write("🔈 Soft")
