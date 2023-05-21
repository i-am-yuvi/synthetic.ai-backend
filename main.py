from flask import Flask, request
from bs4 import BeautifulSoup
import requests
import openai
import nltk
import os
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.get_json()
    link = data['link']
    type_content = data['option']

    # Scrape content
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()

    # Tokenize the text and limit it to the first 1500 tokens
    tokens = word_tokenize(text)
    tokens = tokens[:1500]
    input_text = ' '.join(tokens)

    # Generate text with OpenAI
    openai.api_key = "OPENAI_API_KEY"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Give me " + type_content + " similar to " + input_text},
        ]
    )

    generated_text = response['choices'][0]['message']['content']

    return {'content': generated_text}

if __name__ == "__main__":
    app.run(debug=True)
