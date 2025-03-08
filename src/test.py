import pytest
import numpy as np
from tensorflow.keras.models import load_model
from data_loader import load_and_split_data

@pytest.fixture(scope="module")
def load_data():
    return load_and_split_data('CK')

@pytest.fixture(scope="module")
def model():
    return load_model('models/mobilenetv2_emotion_model.keras')

def test_accuracy(model, load_data):
    _, test_images, _, test_labels = load_data

    # Ensure test images have 3 channels 
    if len(test_images.shape) == 3: 
        test_images = np.repeat(test_images[..., np.newaxis], 3, axis=-1)  

    # Normalize pixel values to match training format
    test_images = test_images.astype('float32') / 255.0

    # Evaluate model on test data
    loss, accuracy = model.evaluate(test_images, test_labels, verbose=1)

    # Ensure accuracy is above threshold
    assert accuracy > 0.7, f"❌ Model accuracy too low: {accuracy:.2f}"
