from flask import Flask, render_template, request
import cv2
import numpy as np
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        file = request.files["image"]

        if file:
            # Read image
            image_bytes = np.frombuffer(file.read(), np.uint8)
            image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Blur detection using Laplacian
            blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

            # Logic
            if blur_score < 50:
                blur = 20
                heavy_blur = 75
                clear = 5
                verdict = "HEAVY BLUR"
                reason = "Image is extremely blurred"
                suggestion = "Use tripod, increase focus, avoid motion"
            elif blur_score < 150:
                blur = 50
                heavy_blur = 30
                clear = 20
                verdict = "BLUR"
                reason = "Image is slightly blurred"
                suggestion = "Improve lighting and camera stability"
            else:
                blur = 10
                heavy_blur = 5
                clear = 85
                verdict = "CLEAR"
                reason = "Image is sharp and clear"
                suggestion = "No improvement needed"

            result = {
                "blur": blur,
                "heavy_blur": heavy_blur,
                "clear": clear,
                "verdict": verdict,
                "reason": reason,
                "suggestion": suggestion
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)