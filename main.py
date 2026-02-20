from flask import Flask, render_template, request
import os
import cv2

app = Flask(__name__)

def analyze_image_quality(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return "Invalid", 0, "Unreadable image", "Upload a valid image"

    score = cv2.Laplacian(img, cv2.CV_64F).var()

    if score < 100:
        return "Heavy Blur", 85, "Too much blur", "Use tripod or focus"
    elif score < 300:
        return "Blur", 60, "Low sharpness", "Improve lighting"
    else:
        return "Clear", 95, "Good quality", "No action needed"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        img = request.files["image"]
        path = os.path.join("static", img.filename)
        img.save(path)

        q, p, r, s = analyze_image_quality(path)
        result = {
            "quality": q,
            "percent": p,
            "reason": r,
            "suggestion": s,
            "image": path
        }

    return render_template("index.html", result=result)

# 🚨 THIS LINE IS NON-NEGOTIABLE
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)