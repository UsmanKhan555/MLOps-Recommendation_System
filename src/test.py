from tensorflow.keras.models import load_model
from data_loader import load_and_split_data

def test_model():
    _, test_images, _, test_labels = load_and_split_data('CK') 
    model = load_model('models/ckplus_model.h5')
    loss, accuracy = model.evaluate(test_images, test_labels)
    print(f"Test Loss: {loss}")
    print(f"Test Accuracy: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    test_model()
