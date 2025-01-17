import os
from flask import Flask, render_template, request, redirect, url_for
from src.predict import predict_emotion
from src.youtube_search import youtube_search
from werkzeug.utils import secure_filename


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # This assumes you have a form for file upload
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads/', filename)
            file.save(filepath)
            
            # Predict emotion
            emotion = predict_emotion(filepath)
            
            # Search YouTube
            videos = youtube_search(emotion + " music")
            
            return render_template('index.html', videos=videos, emotion=emotion)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
