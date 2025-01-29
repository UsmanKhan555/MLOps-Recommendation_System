import pytest
from tensorflow.keras.models import load_model
from data_loader import load_and_split_data

@pytest.fixture(scope="module")
def load_data():
    return load_and_split_data('CK')

@pytest.fixture(scope="module")
def model():
    return load_model('models/ckplus_model.h5')

def test_accuracy(model, load_data):
    _, test_images, _, test_labels = load_data
    loss, accuracy = model.evaluate(test_images, test_labels, verbose=0)
    assert accuracy > 0.7 