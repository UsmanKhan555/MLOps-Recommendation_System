import os
from flask import Flask, render_template, request
from src.predict import predict_emotion
from werkzeug.utils import secure_filename
from src.song_recommender import recommend_songs_by_emotion

app = Flask(__name__)

# Ensure upload directory exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Get song recommendations based on emotion
            videos, emotion = recommend_songs_by_emotion(filepath)
            
            return render_template('index.html', videos=videos, emotion=emotion)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)