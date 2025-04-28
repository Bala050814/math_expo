# streamlit_app.py

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import streamlit as st

# Page setup
st.set_page_config(page_title="Math Calculator", page_icon="➗", layout="centered")

# Inject custom CSS (without floating card)
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://img.freepik.com/free-vector/mathematics-background-geometric-frame-modern-education-design-vector_53876-156362.jpg?t=st=1745862070~exp=1745865670~hmac=b5889d580078a655e78e4402e00657090792f0540c1354391cc7090c52f0767d&w=1380');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        font-family: 'Arial', sans-serif;
        color: white;
        text-align: center;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 22px;
        border-radius: 8px;
        padding: 14px 28px;
        width: 80%;
        margin: auto;
    }
    .stButton>button:hover {
        background-color: #ff5733;
        transform: scale(1.05);
    }
    .stTextInput>div>div>input {
        text-align: center;
        font-size: 20px;
        width: 100%;
    }
    .stSlider>div>div>div>div {
        background: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# Main page content (centered naturally)
st.title("✨ Interactive Bilinear Transformation Calculator ✨")
st.write("Dynamically adjust parameters and visualize transformations.")

# Input fields
b_input = st.text_input("📌 Enter Numerator Coefficients (comma-separated):", "1, 0")
a_input = st.text_input("📌 Enter Denominator Coefficients (comma-separated):", "1, 1")
fs = st.slider("🎚️ Sampling Frequency (Hz):", min_value=1, max_value=1000, value=100, step=1)

# Compute button
if st.button("🚀 Compute & Visualize"):
    try:
        # Parse the input
        b = np.array([float(i.strip()) for i in b_input.split(',')])
        a = np.array([float(i.strip()) for i in a_input.split(',')])

        # Bilinear transform
        bz, az = signal.bilinear(b, a, fs)

        # Show results
        st.success("✅ Computation Successful!")
        st.markdown("### 🔢 Digital Filter Coefficients")
        st.markdown(f"**Numerator (bz):** {bz}")
        st.markdown(f"**Denominator (az):** {az}")

        # Plot frequency response
        w, h = signal.freqz(bz, az, worN=1024)
        freq = w * fs / (2 * np.pi)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(freq, 20 * np.log10(abs(h)), color='dodgerblue', linewidth=2)
        ax.set_xlabel('Frequency (Hz)', fontsize=16)
        ax.set_ylabel('Magnitude (dB)', fontsize=16)
        ax.set_title('📊 Frequency Response of Digital Filter', fontsize=18, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.7)

        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error: {e}")
