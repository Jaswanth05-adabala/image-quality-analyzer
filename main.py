from flask import Flask, render_template, request
import cv2
import numpy as np
import os

app = Flask(__name__)

def analyze_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Laplacian variance (blur detection)
    variance = cv2.Laplacian(img, cv2.CV_64F).var()

    # Normalize to percentage ranges
    if variance < 100:
        blur = 10
        heavy_blur = 80
        clear = 10
        verdict = "HEAVY BLUR"
        reason = "Image is extremely blurred"
        suggestion = "Retake image with better focus and lighting"
    elif variance < 300:
        blur = 60
        heavy_blur = 20
        clear = 20
        verdict = "BLUR"
        reason = "Image has noticeable blur"
        suggestion = "Use tripod or increase shutter speed"
    else:
        blur = 10
        heavy_blur = 5
        clear = 85
        verdict = "CLEAR"
        reason = "Image is sharp and clear"
        suggestion = "No improvement needed"

    return {
        "blur": blur,
        "heavy_blur": heavy_blur,
        "clear": clear,
        "verdict": verdict,
        "reason": reason,
        "suggestion": suggestion
    }

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_url = None

    if request.method == "POST":
        file = request.files["image"]
        if file:
            upload_path = os.path.join("static", file.filename)
            file.save(upload_path)

            result = analyze_image(upload_path)
            image_url = upload_path

    return render_template("index.html", result=result, image_url=image_url)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)