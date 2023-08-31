import os
from flask import Flask, render_template, request
from google.cloud import translate_v2 as translate
from google.cloud import language_v1

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "react-ef60e-firebase-adminsdk-hqoze-e399bdac16.json"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    language = request.form['language']

    if language == 'english':
        blob = TextBlob(text)
    elif language == 'hindi':
        # Use Google Cloud Translation API
        client = translate.Client()
        result = client.translate(text, target_language='en')
        english_text = result['translatedText']
        blob = TextBlob(english_text)
    
    sentiment_score = blob.sentiment.polarity

    if sentiment_score > 0:
        sentiment = 'Positive'
    elif sentiment_score < 0:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return render_template('index.html', text=text, sentiment=sentiment)

# Rest of the code remains the same

if __name__ == '__main__':
    app.run(debug=True)
