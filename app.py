import os
from flask import Flask, render_template, request
from google.cloud import speech
from google.cloud import language

app = Flask(__name__)

# set up Google Cloud credentials, replace the string with your own path
products_lineup = ['pencil', 'pen', 'toothpaste', 'shoes', 'mouse', 'notebook']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    # get the uploaded audio file
    audio_file = request.files["audio"]

    # save the audio file to a temporary location
    audio_file_path = "/tmp/uploaded_audio.wav"
    audio_file.save(audio_file_path)

    # convert audio to text using Speech-to-Text API
    text = transcribe(audio_file_path)

    # analyze sentiment and entities using Natural Language Processing API
    sentiment_score, sentiment_magnitude, results = analyze_text(text)

    sentiment = "Neutral"
    if sentiment_score > 0.3:
        sentiment = "Very Satisfied"
    elif sentiment_score > 0:
        sentiment = "Satisfied"
    elif sentiment_score == 0:
        sentiment = "Neutral"
    elif sentiment_score >= -0.3:
        sentiment = "Unsatisfied"
    else:
        sentiment = "Very Unsatisfied"

    # return the results
    return render_template("results.html", text=text, sentiment=sentiment,
                           sentiment_magnitude=sentiment_magnitude, results=results)

def transcribe(audio_file_path):
    # create a client for the Speech-to-Text API
    client = speech.SpeechClient()

    # read the audio file
    with open(audio_file_path, "rb") as audio_file:
        audio_data = audio_file.read()
    # configure the audio settings
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(language_code="en-US")
    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript


def analyze_text(text):
    # create a client for the Natural Language Processing API
    client = language.LanguageServiceClient()
    request = {'document' : {"type_": language.Document.Type.PLAIN_TEXT, "content": text}}

    sentiment = client.analyze_sentiment(request).document_sentiment
    entities = client.analyze_entities(request).entities
    sentiment_score = sentiment.score
    sentiment_magnitude = sentiment.magnitude
    results = [] # find what the customers talk about
    for entity in entities:
        if entity.name.lower() in products_lineup:
            results.append(entity.name.lower())
    if not results:
        for entity in entities:
            results.append(entity.name.lower())
    
    return sentiment_score, sentiment_magnitude, results

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
