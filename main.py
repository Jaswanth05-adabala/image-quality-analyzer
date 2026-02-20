from flask import Flask, render_template, request
import cv2
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def analyze_image(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    variance = cv2.Laplacian(img, cv2.CV_64F).var()

    if variance < 100:
        return 10, 80, 10, "HEAVY BLUR", "Image is extremely blurred", "Retake image with proper focus and lighting"
    elif variance < 300:
        return 60, 20, 20, "BLUR", "Image has noticeable blur", "Use tripod or increase shutter speed"
    else:
        return 10, 5, 85, "CLEAR", "Image is sharp and clear", "No improvement needed"


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_url = None

    if request.method == "POST":
        if "image" not in request.files:
            return render_template("index.html", error="No file uploaded")

        file = request.files["image"]

        if file.filename == "":
            return render_template("index.html", error="No file selected")

        path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(path)

        blur, heavy, clear, verdict, reason, suggestion = analyze_image(path)

        result = {
            "blur": blur,
            "heavy_blur": heavy,
            "clear": clear,
            "verdict": verdict,
            "reason": reason,
            "suggestion": suggestion
        }

        image_url = path

    return render_template("index.html", result=result, image_url=image_url)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)