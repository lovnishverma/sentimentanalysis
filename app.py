import os
from flask import Flask, render_template, request
from textblob import TextBlob
from google.cloud import translate_v2 as translate
from google.cloud import language

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "react-ef60e-firebase-adminsdk-hqoze-e399bdac16.json"

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
        client = translate.Client()
        result = client.translate(text, target_language='en')
        english_text = result['translatedText']
        blob = TextBlob(english_text)

    client = language.LanguageServiceClient()  # Initialize the language client
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    sentiment_score = sentiment.score

    if sentiment_score > 0:
        sentiment_label = 'Positive'
    elif sentiment_score < 0:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'

    return render_template('index.html', text=text, sentiment=sentiment_label)

# Rest of the code remains the same

if __name__ == '__main__':
    app.run(debug=True)
