import streamlit as st
import cv2
import numpy as np

st.set_page_config(
    page_title="Image Quality Analyzer",
    layout="centered"
)

st.title("📸 Image Quality Analyzer")
st.write("Upload an image to analyze Blur, Heavy Blur, and Clear percentage")

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)

def analyze_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    score = min(lap_var / 1000, 1.0)

    blur = round((1 - score) * 100, 2)
    heavy_blur = round(max(0, blur - 30), 2)
    clear = round(100 - blur, 2)

    if heavy_blur > 50:
        verdict = "HEAVY BLUR"
        reason = "Image has very low sharpness (motion or focus issue)"
        suggestion = "Use tripod, better lighting, avoid movement"
    elif blur > 30:
        verdict = "BLUR"
        reason = "Image is slightly blurred"
        suggestion = "Hold camera steady and focus properly"
    else:
        verdict = "CLEAR"
        reason = "Image is sharp and clear"
        suggestion = "No improvement needed"

    return blur, heavy_blur, clear, verdict, reason, suggestion

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    st.image(img, caption="Uploaded Image", width=700)

    blur, heavy_blur, clear, verdict, reason, suggestion = analyze_image(img)

    st.subheader("📊 Analysis Result")

    st.write(f"Blur: **{blur}%**")
    st.progress(int(min(blur, 100)))

    st.write(f"Heavy Blur: **{heavy_blur}%**")
    st.progress(int(min(heavy_blur, 100)))

    st.write(f"Clear: **{clear}%**")
    st.progress(int(min(clear, 100)))

    st.subheader(f"✅ Final Verdict: {verdict}")
    st.write(f"**Reason:** {reason}")
    st.write(f"**Suggestion:** {suggestion}")