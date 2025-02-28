import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split

def load_and_split_data(dataset_path, image_size=(48, 48), test_size=0.2, random_state=42):
    # Define emotion labels
    emotions = {
        'anger': 0, 'contempt': 1, 'disgust': 2, 'fear': 3,
        'happy': 4, 'sadness': 5, 'surprise': 6
    }
    # store images and labels
    images = []
    labels = []

    #loop through all the folders in the dataset
    for emotion, label in emotions.items():
        emotion_path = os.path.join(dataset_path, emotion)
        for image_file in os.listdir(emotion_path):
            image_path = os.path.join(emotion_path, image_file)
            # Read the image in grayscale format
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            # Resize the image
            if img is not None:
                img = cv2.resize(img, image_size)
                images.append(img)
                labels.append(label)
    # Convert the list to numpy arrays for better performance
    images = np.array(images)
    labels = np.array(labels)

    return train_test_split(
        images, labels, test_size=test_size, random_state=random_state
    )


