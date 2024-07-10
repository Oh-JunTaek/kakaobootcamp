from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# OpenAI API key and MongoDB URI from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
mongodb_uri = os.getenv('MONGODB_URI')

# Check if API key and MongoDB URI are loaded correctly
print(f"OpenAI API Key: {openai.api_key}")
print(f"MongoDB URI: {mongodb_uri}")

# MongoDB setup
client = MongoClient(mongodb_uri)
db = client.chatbot

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')

        print(f"User message: {user_message}")

        # OpenAI API call using the latest method
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )

        response_text = response.choices[0].message["content"].strip()

        print(f"OpenAI response: {response_text}")

        # Save message and response to MongoDB
        db.chats.insert_one({
            'message': user_message,
            'response': response_text
        })

        return jsonify({'response': response_text})
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
