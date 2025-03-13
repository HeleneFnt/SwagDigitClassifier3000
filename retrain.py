from sklearn.datasets import load_digits as lds
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
import os
from PIL import Image
from io import BytesIO
from modelstore import ModelStore


# Patch NumPy 2.0 : define np.float_ if not exist to fix this AttributeError: `np.float_` was removed in the NumPy 2.0 release. Use `np.float64` instead
if not hasattr(np, 'float_'):
    np.float_ = np.float64

# Load digits data
d = lds(n_class=10)
X_train, y_train = d.data, d.target
print("d.data=", d.data)
print("d.target=", d.target)

# Load help_data from modelstore
for file in os.listdir('help_data'):
    filename = file.title()
    name, _ = os.path.splitext(filename)  # split name and extension
    y = name.split('-')[1]  # get the target value
    print("y=", y)

    # Open binary image and convert to grayscale
    img_obj = Image.open(os.path.join('help_data', file)).convert('L')
    # Resize image to 8x8 
    img_obj = img_obj.resize((8, 8))
    
    # Convert image to numpy array
    img_np = np.array(img_obj, dtype=np.float32)
    # Normalize pixel values to match the digits dataset (0-16)
    img_np = (img_np / 255.0) * 16.0
    # Flatten array to match shape (1, 64)
    img_np = img_np.flatten().reshape(1, -1)
    print("img_np shape=", img_np.shape)

    # Append to X_train and y_train
    X_train = np.vstack((X_train, img_np))
    y_train = np.append(y_train, y)

# Split data after processing all help_data images
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.15, random_state=42)
print("Data split complete")
print("X_train shape", X_train.shape, "X_test shape", X_test.shape, "y_train shape", y_train.shape, "y_test shape", y_test.shape)

# Instantiate object with 3 neighbors
knn_clf = KNeighborsClassifier(n_neighbors=3)

# Fit the model
model = knn_clf.fit(X_train, y_train)

# Save model to local file system
model_store = ModelStore.from_file_system(root_directory='models')

# Upload model
meta_data = model_store.upload("digit_classifier", model = model)
# print("Model uploaded with ID:", meta_data['model_id'])

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print(f"KNN model accuracy: {accuracy:4f}")

# Debug: show original digits data
print("d.data=", d.data)
print("d.target=", d.target)
