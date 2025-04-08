import cv2
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Folder untuk upload file
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load model deteksi wajah OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Baca gambar dan deteksi wajah
            img = cv2.imread(filepath)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Gambar kotak di wajah yang terdeteksi
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Simpan gambar hasil deteksi
            detected_path = os.path.join(app.config['UPLOAD_FOLDER'], "detected_" + filename)
            cv2.imwrite(detected_path, img)

            return render_template("index.html", uploaded=True, image_path=detected_path)

    return render_template("index.html", uploaded=False)

if __name__ == "__main__":
    app.run(debug=True)
