from flask import Flask, request, render_template, redirect, url_for
import tensorflow as tf
from werkzeug.utils import secure_filename
import os
from PIL import Image
import numpy as np

tf.config.set_visible_devices([], 'GPU')

app = Flask(__name__)
model = tf.keras.models.load_model('DCPL.h5')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((64, 64))  # Resize the image to match the input size of your model
    img = np.array(img) / 255.0  # Normalize the image
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Preprocess the image and make a prediction
        img = preprocess_image(filepath)
        prediction = model.predict(img)
        
        # Process the prediction to get readable output
        # Assuming you have 3 classes, adjust according to your model's output
        classes = ['Lung_Cancer', 'PNEUMONIA', 'COVID-19', 'Normal']
        predicted_class = classes[np.argmax(prediction)]
        
        return render_template('result.html', prediction=predicted_class)

    return redirect(request.url)

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
