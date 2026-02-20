from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

# Load trained model
model = tf.keras.models.load_model("image_quality_model.h5")

CLASS_NAMES = ["blur", "clear", "heavy_blur"]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        file = request.files["image"]
        if file:
            img_path = os.path.join("static", file.filename)
            file.save(img_path)

            # Load & preprocess image
            img = image.load_img(img_path, target_size=(128, 128))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            prediction = model.predict(img_array)[0]

            # Convert probabilities to percentages (SAFE)
            blur_pct = int(round(prediction[0] * 100))
            clear_pct = int(round(prediction[1] * 100))
            heavy_blur_pct = int(round(prediction[2] * 100))

            final_index = np.argmax(prediction)
            final_label = CLASS_NAMES[final_index].upper()

            # Reason + suggestions
            if final_label == "CLEAR":
                reason = "The image has good sharpness and well-defined edges."
                suggestions = [
                    "Great job! Image quality is good.",
                    "Maintain steady hands while capturing.",
                    "Use good lighting for best results."
                ]
            elif final_label == "BLUR":
                reason = "The image has moderate blur due to slight motion or focus issues."
                suggestions = [
                    "Hold the camera steady.",
                    "Increase lighting conditions.",
                    "Avoid minor hand movement."
                ]
            else:
                reason = "The image has very low sharpness, likely caused by strong motion blur or incorrect focus."
                suggestions = [
                    "Use a tripod or stable surface.",
                    "Increase lighting conditions.",
                    "Avoid hand movement while capturing.",
                    "Ensure proper focus before clicking."
                ]

            result = {
                "image": img_path,
                "blur": blur_pct,
                "clear_pct": clear_pct,
                "heavy_blur": heavy_blur_pct,
                "final": final_label,
                "reason": reason,
                "suggestions": suggestions
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)