from flask import Flask, render_template, request
from textblob import TextBlob
import requests

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
        blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())
    
    sentiment_score = blob.sentiment.polarity

    if sentiment_score > 0:
        sentiment = 'Positive'
    elif sentiment_score < 0:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return render_template('index.html', text=text, sentiment=sentiment)

@app.route('/analyze_social', methods=['POST'])
def analyze_social():
    url = request.form['url']
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text
        blob = TextBlob(content)
        sentiment_score = blob.sentiment.polarity

        if sentiment_score > 0:
            sentiment = 'Positive'
        elif sentiment_score < 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return render_template('index.html', text=content, sentiment=sentiment)
    else:
        return render_template('index.html', error='Failed to fetch URL content.')

if __name__ == '__main__':
    app.run(debug=True)
