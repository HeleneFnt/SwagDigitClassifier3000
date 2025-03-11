from modelstore import ModelStore
import os
import pickle



# Define stockage directory
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Initiate ModelStore with a local storage
model_store = ModelStore.from_file_system(MODEL_DIR)

# Load model
model_path = "digit_classifier.pkl"
with open(model_path, 'rb') as f:
    model = pickle.load(f)
print(type(model))

# Save model in  modelstore
meta_data = model_store.upload("digit_classifier", ) # TO DO
print(f"Model sucessfully load! MetaData : {meta_data}")