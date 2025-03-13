# SwagDigitClassifier3000


### Web Application for Handwritten Digit Recognition

SwagDigitClassifier3000 is a web application that integrates a machine learning model to recognize handwritten digits. The project includes a Flask backend, a simple HTML frontend, and Docker support for deployment.
Work Plan

- Project initialization on GitHub
- Dependencies in a virtual environment
- Analysis of the .ipynb notebook
- Backend creation [`app.py`](app.py)
- Frontend development
- Monitoring & Metrics: Prometheus is integrated to monitor prediction latency and total predictions. Grafana is used for visualization.
- ModelStore: Models are stored and versioned using the modelstore package.
- Testing and deployment
- Deployment with Docker


---

## Integrating a Model into a Web Application

### Project Structure

```
SwagDigitClassifier3000/
├── add_model_to_store.py       # Script to upload the trained model to ModelStore
├── app.py                      # Flask backend handling predictions and metrics
├── digit_classifier.pkl        # Trained digit classification model
├── digits_par_jean-michel_version_0.3b.ipynb  # Model training notebook
├── Dockerfile                  # Docker containerization setup for the web application
├── docker-compose.yaml         # Docker compose for Prometheus and Grafana
├── grafana-data                # Persistent volume for Grafana data
├── help_data                   # Collected help images from users (used to retrain the model)
├── models                      # ModelStore directory storing versioned models
├── out.png                     # Sample output image (for debugging purposes)
├── poetry.lock                 # Poetry dependency lockfile
├── prometheus.yml              # Prometheus configuration file
├── pyproject.toml              # Poetry project configuration
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies list (for pip installations)
└── templates
    └── index.html              # Frontend UI allowing users to draw digits
```

---

### Installation & Setup

#### 1. Clone the Repository
```sh
git clone https://github.com/your-username/SwagDigitClassifier3000.git
cd SwagDigitClassifier3000
```

#### 2. Create a Virtual Environment & Install Dependencies
Using Poetry:
```sh
poetry install
```
Using pip:
```sh
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```
Additional Dependencies for Monitoring 

"pillow" and "prometheus-client"

---

### Development Workflow

#### 1. Model Training
- The model is trained using [`digits_par_jean-michel_version_0.3b.ipynb`](digits_par_jean-michel_version_0.3b.ipynb).
- The trained model is saved as [`digit_classifier.pkl`](digit_classifier.pkl).

#### 2. Backend Setup
- [`app.py`](app.py) is a Flask API that loads [`digit_classifier.pkl`](digit_classifier.pkl) and processes user-submitted images.

Metrics: Prometheus is integrated to track:

    Request processing time
    Total number of predictions
    Last predicted value
    Timestamps of predictions

Routes:

    / : Renders the main interface.
    /api/predict : Handles POST requests with image data.
    /helpdata : Receives new images (with label) to help improve the model.
    /metrics : Exposes Prometheus metrics.

#### 3. Frontend Interface
- **UI**: The UI in templates/index.html provides a canvas for drawing digits.
- **Data Collection**: The drawn image is sent via JavaScript to the /api/predict endpoint for predictions and to /helpdata for collecting additional training data.


#### 4. ModelStore Integration

- **Model Upload**: Use add_model_to_store.py to upload the trained model into the ModelStore.
- **Retraining**: The retrain.py script combines the original digits data with user-collected 'A' images from help_data to retrain the model.

#### 5. Running the Application
* To start the Flask server:
```sh
python app.py
```
Then open `http://127.0.0.1:5000/` in your browser.


* To start Prometheus Server (Integrated in the App)

The application automatically starts a Prometheus exporter on port 8000. You can verify it using:

```sh
ss -tulnp | grep :8000
curl http://127.0.0.1:8000
```
---

### Deployment

#### 1. Run with Docker
To build and run the container:
```sh
docker build -t <my-app> .
docker run -p 5000:5000 <my-app> 
```
#### 2. Deploy Prometheus and Grafana via Docker Compose

Create a [`docker-compose.yml`](docker-compose.yaml) 
Also, create the [`prometheus.yml`](prometheus.yml) configuration file
Then, start the services:

```sh
docker-compose up -d
```
Access:

    Prometheus: http://localhost:9090/
    Grafana: http://localhost:3000/
    (Default login: admin/admin)

---

### Monitoring and Metrics Visualization

    Prometheus: Collects metrics from the Flask application.
    Grafana: Visualize metrics like prediction count, processing time, and last predicted value.
    Add Prometheus as a data source in Grafana with URL http://prometheus:9090.

### Conservation of Client Images

    Data Collection: User images and labels are saved in the help_data directory via the /helpdata route.
    Usage: These images are used for retraining the model (see retrain.py) to incorporate user feedback.

### Additional Resources

    * [Prometheus Client Python Documentation](https://prometheus.github.io/client_python/getting-started/three-step-demo/)
    * [Monitoring Web App with Prometheus and Grafana](https://medium.com/@fenari.kostem/monitoring-your-web-app-with-prometheus-and-grafana-a-step-by-step-guide-8286dae606c7)
    * [Machine Learning in Production – Data and Concept Drift](https://towardsdatascience.com/machine-learning-in-production-why-you-should-care-about-data-and-concept-drift-d96d0bc907fb/)
    
---

*Copyright Hélène Finot - Formation DevOps 2025*

