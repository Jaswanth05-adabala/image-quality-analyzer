from flask import Flask, render_template, request
import cv2
import numpy as np
from PIL import Image
import io
import base64
import os

app = Flask(__name__)

def analyze_blur(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Heuristic thresholds
    if laplacian_var < 50:
        verdict = "Heavy Blur"
        reason = "Image is extremely blurred due to strong motion or defocus."
        suggestions = [
            "Use a tripod or stable surface",
            "Improve lighting",
            "Avoid camera shake",
            "Use higher shutter speed"
        ]
        blur = 20
        heavy_blur = 75
        clear = 5

    elif laplacian_var < 120:
        verdict = "Blur"
        reason = "Image has noticeable blur, likely due to mild motion or focus issue."
        suggestions = [
            "Hold camera steady",
            "Tap to focus before capture",
            "Increase light exposure"
        ]
        blur = 55
        heavy_blur = 20
        clear = 25

    else:
        verdict = "Clear"
        reason = "Image is sharp and clear with good focus."
        suggestions = [
            "No improvement needed",
            "Image is suitable for use"
        ]
        blur = 10
        heavy_blur = 5
        clear = 85

    return blur, heavy_blur, clear, verdict, reason, suggestions


@app.route("/", methods=["GET", "POST"])
def index():
    image_data = None
    blur = heavy_blur = clear = None
    verdict = reason = None
    suggestions = []

    if request.method == "POST":
        file = request.files["image"]
        if file:
            img_bytes = file.read()
            image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            open_cv_image = np.array(image)
            open_cv_image = open_cv_image[:, :, ::-1].copy()

            blur, heavy_blur, clear, verdict, reason, suggestions = analyze_blur(open_cv_image)

            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            image_data = base64.b64encode(buffered.getvalue()).decode()

    return render_template(
        "index.html",
        image_data=image_data,
        blur=blur,
        heavy_blur=heavy_blur,
        clear=clear,
        verdict=verdict,
        reason=reason,
        suggestions=suggestions
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)