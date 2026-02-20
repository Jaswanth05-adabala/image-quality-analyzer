from flask import Flask, render_template, request
import cv2
import numpy as np
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def analyze_image_quality(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Variance of Laplacian for blur detection
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Normalize score
    score = min(laplacian_var / 1000, 1.0)

    blur = max(0, 1 - score) * 100
    heavy_blur = max(0, blur - 30)
    clear = 100 - (blur + heavy_blur)

    if heavy_blur > 50:
        verdict = "HEAVY_BLUR"
        reason = "The image has very low sharpness, likely caused by motion blur or incorrect focus."
        suggestions = [
            "Use a tripod or stable surface",
            "Increase lighting conditions",
            "Avoid hand movement while capturing",
            "Ensure proper focus before clicking"
        ]
    elif blur > 30:
        verdict = "BLUR"
        reason = "The image is slightly blurred and lacks edge clarity."
        suggestions = [
            "Hold the camera steady",
            "Improve lighting",
            "Clean the camera lens"
        ]
    else:
        verdict = "CLEAR"
        reason = "The image has good sharpness and well-defined edges."
        suggestions = [
            "Great job! Image quality is good",
            "Maintain steady hands while capturing",
            "Use good lighting for best results"
        ]

    return {
        "blur": round(blur, 2),
        "heavy_blur": round(heavy_blur, 2),
        "clear": round(clear, 2),
        "verdict": verdict,
        "reason": reason,
        "suggestions": suggestions
    }

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_url = None

    if request.method == "POST":
        file = request.files["image"]
        if file:
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

            result = analyze_image_quality(image_path)
            image_url = image_path

    return render_template("index.html", result=result, image_url=image_url)

if __name__ == "__main__":
    app.run()