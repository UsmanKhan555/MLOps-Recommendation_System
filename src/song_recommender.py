from src.predict import predict_emotion
from src.youtube_search import youtube_search
import random

def recommend_songs_by_emotion(image_path, num_recommendations=5):
    
    #Recommends songs based on the emotion detected in an image.
    
    #deetect emotion directly from the image
    emotion = predict_emotion(image_path)
    
    # Create appropriate search queries based on the detected emotion
    search_queries = {
        'anger': ['angry music', 'rage music', 'heavy metal'],
        'contempt': ['rebellious music', 'alternative rock', 'punk music'],
        'disgust': ['intense music', 'dissonant music', 'experimental music'],
        'fear': ['calming music', 'relaxing music', 'ambient music'],
        'happy': ['upbeat happy music', 'feel good songs', 'pop music'],
        'sadness': ['melancholic music', 'sad songs', 'emotional ballads'],
        'surprise': ['uplifting music', 'exciting music', 'energetic songs']
    }
    
    # aselect a query randomly from the list for the detected emotion
    query = random.choice(search_queries[emotion])
    
    # Search for songs on YouTube
    recommended_songs = youtube_search(query)
    
    # Limit to the number of recommendations requested
    return recommended_songs[:num_recommendations], emotion