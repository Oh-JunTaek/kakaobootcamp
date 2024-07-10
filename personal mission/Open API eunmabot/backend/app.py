from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

app = Flask(__name__)
CORS(app)

# 환경 변수에서 OpenAI API 키와 MongoDB URI를 가져옵니다.
openai.api_key = os.getenv('OPENAI_API_KEY')
mongodb_uri = os.getenv('MONGODB_URI')

# API 키와 MongoDB URI가 올바르게 로드되었는지 확인합니다.
print(f"OpenAI API Key: {openai.api_key}")
print(f"MongoDB URI: {mongodb_uri}")

# MongoDB 설정
client = MongoClient(mongodb_uri)
db = client.chatbot

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')

        print(f"User message: {user_message}")

        # OpenAI API를 사용하여 응답을 생성합니다.
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

        # 사용자 메시지와 OpenAI 응답을 MongoDB에 저장합니다.
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
