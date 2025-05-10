from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from utils import ela, preprocess_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Load pre-trained CNN model
model = load_model('model.h5')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Step 1: Apply ELA (Error Level Analysis)
        ela_image = ela(filepath)
        
        # Step 2: Preprocess for CNN
        processed_img = preprocess_image(filepath)
        
        # Step 3: Predict using CNN
        prediction = model.predict(np.expand_dims(processed_img, axis=0))
        is_fake = bool(prediction[0][0] > 0.5)  # Threshold at 0.5
        confidence = float(prediction[0][0])
        
        return jsonify({
            "filename": filename,
            "is_fake": is_fake,
            "confidence": confidence,
            "ela_image": ela_image.tolist() if ela_image is not None else None
        })
    
    return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5000)
    
    
    
import tensorflow as tf
from tensorflow.keras import layers, models

# Example CNN model
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(256,256,3)),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train on your dataset (example)
# model.fit(train_images, train_labels, epochs=10)
model.save('model.h5')