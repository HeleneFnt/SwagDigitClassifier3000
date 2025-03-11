from http.client import REQUEST_TIMEOUT
import pickle
from flask import Flask, render_template, request, jsonify
import base64
import io
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
from prometheus_client import start_http_server, Summary, Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import os

app = Flask(__name__)

# Ensure help_data directory exists
HELP_DATA_DIR = "help_data"
os.makedirs(HELP_DATA_DIR, exist_ok=True)


# Determine metrics
REQUEST_TIMEOUT = Summary('request_processing_seconds', 'Time spent processing request')
TOTAL_PREDICTIONS = Counter('total_predictions', 'Total number of predictions made')
PREDICTED_VALUE = Gauge('predicted_value', 'Last predicted value')
PREDICTION_TIMESTAMPS = Counter('prediction_timestamps', 'Timestamps of predictions')

# Load model
f = open("digit_classifier.pkl" , 'rb')
model = pickle.load(f)


# Route 66
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Evil road 666 and decorate function with metrics 
@app.route('/api/predict', methods=['POST'])
@REQUEST_TIMEOUT.time() 
def predict():
    start_time = time.time() # start time metric
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

    # Prometheus metrics update
    TOTAL_PREDICTIONS.inc()
    PREDICTED_VALUE.set(result)
    PREDICTION_TIMESTAMPS.inc()

    elapsed_time = time.time() - start_time
    print(f"Prediction: {result}, Time taken: {elapsed_time:.4f} sec")

    return jsonify({"result":str(result[0])})

# Expose Prometheus metrics
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/helpdata', methods=['POST'])
def collect_help_data():
    data = request.get_json()
    base64_img = data['image'].split(',')[1]
    label = data['label']
    timestamp = int(time.time())
    filename = f"{timestamp}-{label}.png"
    
    img = Image.open(io.BytesIO(base64.b64decode(base64_img)))
    img.save(os.path.join(HELP_DATA_DIR, filename))
    return jsonify({"message": "Data saved successfully"})

if __name__ == '__main__':
    # Start prometheus on port 8000
    start_http_server(8000)
    app.run(host='0.0.0.0', port= 5000, debug=True, use_reloader=False) # Disable flask reloader for 'OSError: [Errno 98] Address already in use issue'