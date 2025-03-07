# SwagDigitClassifier3000


### Web Application for Handwritten Digit Recognition

SwagDigitClassifier3000 is a web application that integrates a machine learning model to recognize handwritten digits. The project includes a Flask backend, a simple HTML frontend, and Docker support for deployment.
Work Plan

- Project initialization on GitHub
- Dependencies in a virtual environment
- Analysis of the .ipynb notebook
- Backend creation [`app.py`](app.py)
- Frontend development
- Testing and deployment
- Deployment with Docker


---

## Integrating a Model into a Web Application

### Project Structure

```
SwagDigitClassifier3000/
├── app.py                      # Flask backend handling predictions
├── digit_classifier.pkl        # Trained digit classification model
├── digits_par_jean-michel_version_0.3b.ipynb  # Model training notebook
├── Dockerfile                  # Docker containerization setup
├── out.png                     # Sample output image
├── poetry.lock                 # Poetry dependency lockfile
├── pyproject.toml              # Poetry configuration
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
└── templates
    └── index.html              # Frontend UI
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

---

### Development Workflow

#### 1. Model Training
- The model is trained using [`digits_par_jean-michel_version_0.3b.ipynb`](digits_par_jean-michel_version_0.3b.ipynb).
- The trained model is saved as [`digit_classifier.pkl`](digit_classifier.pkl).

#### 2. Backend Setup
- [`app.py`](app.py) is a Flask API that loads [`digit_classifier.pkl`](digit_classifier.pkl) and processes user-submitted images.

#### 3. Frontend Interface
- The UI is built in [`templates/index.html`](templates/index.html) and allows users to draw digits on a canvas.
- The drawn image is sent to the Flask backend for prediction.
#### 4. Running the Application
To start the Flask server:
```sh
python app.py
```
Then open `http://127.0.0.1:5000/` in your browser.

---

### Deployment

#### 1. Run with Docker
To build and run the container:
```sh
docker build -t <my-app> .
docker run -p 5000:5000 <my-app> 
```


*Copyright Hélène Finot - Formation DevOps 2025*

