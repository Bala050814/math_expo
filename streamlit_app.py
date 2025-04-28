import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import streamlit as st
import cv2
from PIL import Image

def bilinear_transform(b, a, fs):
    """Apply bilinear transformation to convert analog filter to digital filter"""
    bz, az = signal.bilinear(b, a, fs)
    return bz, az

def plot_frequency_response(bz, az, fs):
    """Plot frequency response of the digital filter"""
    w, h = signal.freqz(bz, az, worN=1024)
    freq = w * fs / (2 * np.pi)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(freq, 20 * np.log10(abs(h)), label='Magnitude Response', color='dodgerblue', linewidth=2)
    ax.set_xlabel('Frequency (Hz)', fontsize=12)
    ax.set_ylabel('Magnitude (dB)', fontsize=12)
    ax.set_title('Frequency Response of Digital Filter', fontsize=14, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    
    st.pyplot(fig)

def warp_image(image, scale_x, scale_y):
    """Apply bilinear transformation to warp an image"""
    height, width = image.shape[:2]
    new_width = int(width * scale_x)
    new_height = int(height * scale_y)
    warped_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    return warped_image

# Streamlit UI
st.set_page_config(page_title="Math Calculator", page_icon="➗", layout="centered")

# Inject custom CSS for background and general styling
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(
            rgba(0, 0, 0, 0.6),
            rgba(0, 0, 0, 0.6)
        ), url('https://img.freepik.com/free-vector/mathematics-background-geometric-frame-modern-education-design-vector_53876-156362.jpg?t=st=1745862070~exp=1745865670~hmac=b5889d580078a655e78e4402e00657090792f0540c1354391cc7090c52f0767d&w=1380');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        font-family: 'Arial', sans-serif;
        color: white;
    }

    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        font-size: 18px;
        border-radius: 8px;
        border: none;
        transition: 0.3s;
        width: 100%;
    }

    .stButton>button:hover {
        background-color: #ff5733;
        transform: scale(1.05);
    }

    .calculator-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
        margin-top: 30px;
    }

    @media (max-width: 768px) {
        .calculator-container {
            flex-direction: column;
            align-items: center;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Title and Introduction
st.title("✨ Interactive Bilinear Transformation Calculator ✨")
st.write("Dynamically adjust parameters and visualize transformations with an enhanced UI.")

# Input parameters
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🔢 Input Parameters")
    b = st.text_input("📌 Numerator Coefficients (comma-separated):", "1, 0")
    a = st.text_input("📌 Denominator Coefficients (comma-separated):", "1, 1")
    fs = st.slider("🎚️ Sampling Frequency (Hz):", min_value=1, max_value=1000, value=100, step=1)
    scale_x = st.slider("🔄 Image Warp Scale X", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
    scale_y = st.slider("🔄 Image Warp Scale Y", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

    if st.button("🚀 Compute & Visualize"):
        b = np.array([float(i) for i in b.split(',')])
        a = np.array([float(i) for i in a.split(',')])
        
        bz, az = bilinear_transform(b, a, fs)
        st.success("✅ Computation Successful!")
        st.write("*🔢 Digital Filter Coefficients:*")
        st.write(f"🔹 Numerator: {bz}")
        st.write(f"🔹 Denominator: {az}")
        
        with col2:
            st.header("📊 Frequency Response")
            plot_frequency_response(bz, az, fs)

# Image upload and processing (optional)
# Uncomment the following block to enable image upload:
# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     image = np.array(image)
#     st.image(image, caption="🖼 Original Image", use_column_width=True)
#     warped_image = warp_image(image, scale_x, scale_y)
#     st.image(warped_image, caption="🎨 Warped Image", use_column_width=True)
