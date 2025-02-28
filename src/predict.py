import cv2
import numpy as np
from tensorflow.keras.models import load_model

def predict_emotion(img_path, model_path='models/ckplus_model.h5'):
    """
    Predicts the emotion of a face in an image.
    """
    model = load_model(model_path)
    #Read the image in grayscale and resize it to 48x48
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (48, 48))
    #reshape image to match the input shape of the model
    img = img.reshape(1, 48, 48, 1) / 255.0
    #predict the emotion
    prediction = model.predict(img)
    #get index of the emotion with highest probability
    emotion_index = np.argmax(prediction)
    emotions = ['anger', 'contempt', 'disgust', 'fear', 'happy', 'sadness', 'surprise']
    return emotions[emotion_index]
