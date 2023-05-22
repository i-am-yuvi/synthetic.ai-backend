import os
from flask import Flask, request
from bs4 import BeautifulSoup
import requests
import openai
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from flask_cors import CORS

app = Flask(__name__)
app.run(
    host="localhost",
    port=5000
)
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

    tokens = word_tokenize(text)
    if len(tokens) > 1500:
        tokens = tokens[:1500]
    input_text = ' '.join(tokens)


    # Generate text with OpenAI
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="text-davinci-003",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text},
        ]
    )

    generated_text = response['choices'][0]['message']['content']

    return {'content': generated_text}

if __name__ == "__main__":
    app.run(debug=True)
