import mlflow
from mlflow import pyfunc
from data_loader import load_and_split_data
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import numpy as np

def create_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(7, activation='softmax')
    ])
    return model

def train_model():
    mlflow.set_tracking_uri('your_tracking_uri')  # Set to your MLflow server URI
    mlflow.set_experiment('Emotion Detection Model Training')

    with mlflow.start_run():
        train_images, test_images, train_labels, test_labels = load_and_split_data('CK') 
        model = create_model()
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        # Train model
        history = model.fit(train_images, train_labels, epochs=10, validation_data=(test_images, test_labels))

        # Log parameters, metrics, and model
        mlflow.log_param("epochs", 10)
        mlflow.log_metric("train_accuracy", history.history['accuracy'][-1])
        mlflow.log_metric("validation_accuracy", history.history['val_accuracy'][-1])

        # Save and log the model
        model_path = "models/ckplus_model.h5"
        model.save(model_path)
        mlflow.keras.log_model(model, "model", registered_model_name="EmotionDetectionModel")

if __name__ == "__main__":
    train_model()
