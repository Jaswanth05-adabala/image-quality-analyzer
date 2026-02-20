from flask import Flask, render_template, request
import os
import cv2
import numpy as np

app = Flask(__name__)

def analyze_image_quality(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        return "Invalid Image", 0, "Could not read image", "Upload a valid image"

    laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()

    if laplacian_var < 100:
        return "Heavy Blur", 85, "Image is extremely blurred", "Use a tripod or better focus"
    elif laplacian_var < 300:
        return "Blur", 60, "Image lacks sharpness", "Increase lighting or focus"
    else:
        return "Clear", 90, "Image is sharp and clear", "No changes needed"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        file = request.files["image"]

        if file:
            upload_path = os.path.join("static", file.filename)
            file.save(upload_path)

            quality, percent, reason, suggestion = analyze_image_quality(upload_path)

            result = {
                "quality": quality,
                "percent": percent,
                "reason": reason,
                "suggestion": suggestion,
                "image": upload_path
            }

    return render_template("index.html", result=result)

# 🔴 THIS PART IS THE MOST IMPORTANT (Render Fix)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)