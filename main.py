from flask import Flask, render_template, request
import os
import cv2
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def analyze_image(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    score = min(laplacian_var / 1000, 1.0)

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


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_url = None

    if request.method == "POST":
        file = request.files.get("image")
        if file and file.filename:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))