import streamlit as st
import cv2
from PIL import Image
import numpy as np
import tempfile

# 🎀 Page Setup
st.set_page_config(page_title="Cartoonify App", layout="centered")

# 🌸 Custom CSS Styling
st.markdown(
    """
    <style>
     .title-box {
        background-color: #808000;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .title {
        font-size: 60px;
        color: #000000;
        text-align: center;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 30px;
        color: #B3B6B7;
        text-align: center;
        margin-bottom: 30px;
    }
    .upload-title{
        color:#808080;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
        font-family: 'Indie Flower', cursive;
    }
    .stButton>button {
        background-color: #2E8B57;
        color: green;
        border-radius: 8px;
        font-size: 16px;
        padding: 8px 20px;
        margin-top: 10px;
    }
    .stDownloadButton>button {
        background-color: #F2D7D5;
        color: #17202A;
        border-radius: 8px;
        font-size: 16px;
        padding: 8px 20px;
        margin-top: 20px;
    }
    </style>
    <div class="title-box">
        <div class="title">Cartoonify Your Image</div>
        <div class="subtitle">Simple Cartoon Filter for Your Photos</div>
    </div>
    <div class="upload-title">Upload Your Image Below</div>
    """,
    unsafe_allow_html=True
)

uploaded_image = st.file_uploader("Select Image", type=["jpg", "jpeg", "png"])

# ⚙️ Sidebar Controls
st.sidebar.title("🛠️ Cartoonify Controls")
smooth = st.sidebar.slider("Smoothness Level", 5, 85, 55, step=2)
edge_strength = st.sidebar.slider("Edge Detection Strength", 50, 200, 100)
k_size = st.sidebar.slider("Median Blur Kernel Size", 3, 11, 5, step=2)
block_size = st.sidebar.slider("Adaptive Threshold Block Size", 3, 15, 9, step=2)
constant_c = st.sidebar.slider("Threshold Constant (C)", 1, 15, 9)

# 🔧 Cartoonify Function
def cartoonify_image(img, smoothness, edges, k, block, c):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    smooth_img = cv2.bilateralFilter(img_rgb, d=9, sigmaColor=smoothness, sigmaSpace=smoothness)
    gray = cv2.cvtColor(smooth_img, cv2.COLOR_RGB2GRAY)
    blur = cv2.medianBlur(gray, k)
    edge = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY, blockSize=block, C=c
    )
    cartoon = cv2.bitwise_and(smooth_img, smooth_img, mask=edge)
    return cartoon

# 🔍 Process Image
if uploaded_image:
    img = np.array(Image.open(uploaded_image))
    cartoon = cartoonify_image(cv2.cvtColor(img, cv2.COLOR_RGB2BGR), smooth, edge_strength, k_size, block_size, constant_c)

    col1, col2 = st.columns(2)
    with col1:
        st.image(img, caption="Original Image", use_column_width=True)
    with col2:
        st.image(cartoon, caption="Cartoonified Image", use_column_width=True)

    # 💾 Download
    st.markdown("### 💾 Download Your Cartoon Image")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    cartoon_bgr = cv2.cvtColor(cartoon, cv2.COLOR_RGB2BGR)
    cv2.imwrite(temp_file.name, cartoon_bgr)

    with open(temp_file.name, "rb") as file:
        st.download_button(
            label="📥 Download",
            data=file,
            file_name="cartoonified.png",
            mime="image/png"
        )
else:
    st.info("HAve FUn!")
