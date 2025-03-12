from modelstore import ModelStore
import pickle
import numpy as np
import setuptools
import os

# Patch NumPy 2.0 : define np.float_ if not exist to fix this AttributeError: `np.float_` was removed in the NumPy 2.0 release. Use `np.float64` instead
if not hasattr(np, 'float_'):
    np.float_ = np.float64

# Define stockage directory
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Initiate ModelStore with a local storage
model_store = ModelStore.from_file_system(root_directory=MODEL_DIR)

# Load model
with open("digit_classifier.pkl", 'rb') as f:
    model = pickle.load(f)
# print(type(model))

# Save model in  modelstore
meta_data = model_store.sklearn.upload("other", model = model, model_id="test")
print(f"Model sucessfully load! MetaData : {meta_data}")