import pickle
from flask import Flask, render_template, request, jsonify
import base64
import io
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

# Load model
f = open("digit_classifier.pkl" , 'rb')
model = pickle.load(f)


# Route 66
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Evil road 666
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    # Decode the base64 image
    base64_img = data['image']
    base64_img = base64_img.split(',')[1]
    img = base64.b64decode(base64_img)

    # Image process and improvment for prediction
    img = Image.open(io.BytesIO(img))
    
    img_convert = img.convert('L')
    img_invert = ImageOps.invert(img_convert)
    img_resized = img_invert.resize((8,8))
    img_resized.save("out.png")
    img_array = np.array(img_resized).reshape(1, -1)

    img_array_bis = np.array(img_resized, dtype=np.float64)
    img_array = img_array_bis.reshape(1, -1)
    # img_array = img_array / 16.0  # Normalization on [0,1]
    print(img_array)

    result = model.predict(img_array)
    print(model.predict_proba(img_array))
    return jsonify({"result":str(result[0])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 5000, debug=True)
