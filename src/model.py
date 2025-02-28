from data_loader import load_and_split_data
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split
import numpy as np

def create_model():
    """
    Create a CNN model for emotion recognition
    """
    model = Sequential([
        # first convolutional layer
        Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
        # max pooling layer
        MaxPooling2D(2, 2),
        # second convolutional layer
        Conv2D(64, (3, 3), activation='relu'),
        # max pooling layer
        MaxPooling2D(2, 2),
        # flatten layer to convert feature maps to a single column
        Flatten(),
        # connected layer with 128 neurons
        Dense(128, activation='relu'),
        # dropout layer to prevent overfitting
        Dropout(0.5),
        # output layer with 7 emotions
        Dense(7, activation='softmax')
    ])
    return model

def train_model():
    """
    Train the emotion recognition model
    """
    #load and split data
    train_images, test_images, train_labels, test_labels = load_and_split_data('CK') 
    # creaTE CNN model
    model = create_model()
    # compile and train the model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    # train the model for 20 epochs
    model.fit(train_images, train_labels, epochs=20, validation_data=(test_images, test_labels))
    model.save('models/ckplus_model.h5')
    print("Model trained and saved.")

if __name__ == "__main__":
    train_model()