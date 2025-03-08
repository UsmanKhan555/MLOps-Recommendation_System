import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

def predict_emotion(img_path, model_path='models/mobilenetv2_emotion_model.keras'):
    
    #Directly predicts the emotion from an image without separate face detection.
   
    # Load the model
    model = load_model(model_path)
    
    # Read the image and resize it to 48x48
    img = cv2.imread(img_path)
    img = cv2.resize(img, (48, 48))
    
    # Convert to RGB if it's not already
    if len(img.shape) == 2:  # If grayscale
        img_rgb = np.repeat(img[..., np.newaxis], 3, axis=-1)
    else:  # If already RGB/BGR
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Preprocess the image for MobileNetV2
    img_preprocessed = preprocess_input(img_rgb.astype('float32'))
    
    # Reshape image to match the input shape of the model
    img_preprocessed = img_preprocessed.reshape(1, 48, 48, 3)
    
    # Predict the emotion
    prediction = model.predict(img_preprocessed)
    
    # Get index of the emotion with highest probability
    emotion_index = np.argmax(prediction)
    
    # Map index to emotion name
    emotions = ['anger', 'contempt', 'disgust', 'fear', 'happy', 'sadness', 'surprise']
    return emotions[emotion_index]