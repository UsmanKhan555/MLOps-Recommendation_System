from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from data_loader import load_and_split_data
import numpy as np

#Create a MobileNetV2 model for emotion recognition with pre-trained weights
def create_mobilenetv2_model(input_shape=(48, 48, 3), num_classes=7):
    # Create the base MobileNetV2 model with pre-trained weights
    base_model = MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights='imagenet'
    )
    
    #Freeze the base model layers
    for layer in base_model.layers:
        layer.trainable = False
    
    # Add custom layers on top
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    # Create the final model
    model = Model(inputs=base_model.input, outputs=predictions)
    
    return model

def train_model():
    """
    Train the emotion recognition model using MobileNetV2
    """
    # Load and split data
    train_images, test_images, train_labels, test_labels = load_and_split_data('CK')
    
    # Convert grayscale images to RGB (MobileNetV2 expects 3 channels)
    train_images_rgb = np.repeat(train_images[..., np.newaxis], 3, axis=-1)
    test_images_rgb = np.repeat(test_images[..., np.newaxis], 3, axis=-1)
    
    # Normalize pixel values
    train_images_rgb = train_images_rgb / 255.0
    test_images_rgb = test_images_rgb / 255.0
    
    # Create MobileNetV2 model
    model = create_mobilenetv2_model(input_shape=(48, 48, 3), num_classes=7)
    
    # Compile the model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    # Train the model
    model.fit(
        train_images_rgb, train_labels,
        epochs=15,
        validation_data=(test_images_rgb, test_labels),
        batch_size=32
    )
    
    # Save the model
    model.save('models/mobilenetv2_emotion_model.keras')
    print("MobileNetV2 model trained and saved.")

if __name__ == "__main__":
    train_model()