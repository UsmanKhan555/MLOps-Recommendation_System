import cv2
import numpy as np
from tensorflow.keras.models import load_model

def predict_emotion(img_path, model_path='models/ckplus_model.h5'):
    model = load_model(model_path)
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (48, 48))
    img = img.reshape(1, 48, 48, 1) / 255.0
    prediction = model.predict(img)
    emotion_index = np.argmax(prediction)
    emotions = ['anger', 'contempt', 'disgust', 'fear', 'happy', 'sadness', 'surprise']
    return emotions[emotion_index]
