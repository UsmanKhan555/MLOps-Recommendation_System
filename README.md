# Music Recommendation System Using Facial Recognition

Overview

This application uses facial recognition to detect the user's emotion from a photo and recommends music based on the detected emotion. It leverages a convolutional neural network trained on the CK+ dataset for emotion recognition and uses the YouTube API to fetch music that matches the detected emotions.

# Installation and Running Instructions

## Install Required Packages

pip install -r requirements.txt

## Train

python src/model.py

## Test

python src/test.py

## Start the Flask Application

python app.py
