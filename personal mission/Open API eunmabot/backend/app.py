from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

app = Flask(__name__)
CORS(app)

# 환경 변수에서 OpenAI API 키 및 MongoDB URI 가져오기
openai.api_key = os.getenv('OPENAI_API_KEY')
mongodb_uri = os.getenv('MONGODB_URI')

# API 키 및 MongoDB URI가 올바르게 로드되었는지 확인
print(f"OpenAI API Key done")
print(f"MongoDB URI: {mongodb_uri}")

# MongoDB 설정
client = MongoClient(mongodb_uri)
db = client.chatbot
print("MongoDB에 성공적으로 연결되었습니다.")

# 채팅 엔드포인트 정의
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')

        print(f"사용자 메시지: {user_message}")

        # 최신 방법을 사용하여 OpenAI API 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )

        response_text = response.choices[0].message["content"].strip()

        print(f"OpenAI 응답: {response_text}")

        # MongoDB에 메시지와 응답 저장
        db.chats.insert_one({
            'message': user_message,
            'response': response_text
        })

        return jsonify({'response': response_text})
    except openai.error.OpenAIError as e:
        print(f"OpenAI API 오류: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"일반 오류: {e}")
        return jsonify({'error': str(e)}), 500

# 채팅 기록 조회 엔드포인트 정의
@app.route('/api/chats', methods=['GET'])
def get_chats():
    try:
        chats = list(db.chats.find({}, {'_id': 0}))
        return jsonify({'chats': chats})
    except Exception as e:
        print(f"일반 오류: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
