import os 
import openai
import json
import requests
from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from pdf_retriever import *
from get_weather import *

MAX_TOKENS = 100
token_prompt = f"최대 답변이 {MAX_TOKENS} 개 단어 이내로 해줘"

app = Flask(__name__) 
load_dotenv() # # .env 파일에서 환경 변수를 로드합니다

# PDF에서 자료를 찾을 수 없을 때, chatGPT 에서 생성한 정답을 리턴하도록 한다. 
def get_chatGPT_output(client, model_version,user_input, prompt):
    # CHAT GPT API 객체 생성
    response = client.chat.completions.create(
        model= model_version, #"gpt-4-mini",
        messages=[
                {"role":"system", "content": prompt}, 
                {"role": "user", "content": user_input}
                #"role":"system", "content": "You are a helpful assistant, and you will kindly answer questions about the Kakao Bootcamp in the future. 사용자들은 한국어로 질문할 거고, 너도 한국어로 대답해야돼"}, 
        ],
        temperature=0.5, # 출력의 다양성 조절 (0~1), 높을 수록 창의적인 대답
        #top_p =       # 출력의 다양성 조절 (0~1), 확률의 누적 분포 기반
        max_tokens=MAX_TOKENS, # 최대 출력 토큰 개수 
        n = 1,            # 생성 답변 개수 
        stop= None      #
    )

    output_txt =  response.choices[0].message.content
    return output_txt

def contains_weather_topic(client, model_version, user_input): #날씨 데이터를 담고 있는지 물어본다. 
    prompt = f"You are a classifier. If {user_input} is a question about weather return 'YES'. If not, return 'NO'."
    result = get_chatGPT_output(client, model_version, user_input, prompt)
    if result == "YES": return True 
    return False 

def contains_traffic_topic(client, model_version,user_input): #날씨 데이터를 담고 있는지 물어본다. 
    # prompt = f"You are a classifier and if {user_input} is a question about asking routes using public transportation return 'YES'  if not return 'NO'"
    # 아래는 딱 최적경로만 찾는 route를 위한 prompt
    prompt = "You are a classifier. " \
            "If {user_input} is a question about public transportation routes with a specific origin and destination, return 'YES'. If not, return 'NO'."
    result =  get_chatGPT_output(client, model_version, user_input, prompt)
    if result == "YES": return True 
    return False 

@app.route("/llm", methods=['POST'])
def llm():
    # RESTful API로 받아온 user input txt를 받아온다. 
    params = request.get_json()
    if not params: # 입력이 없을 경우 에러 메시지 출력 
        return jsonify({"error": "No input data provided"}), 400
    usr_input = params['msg']

    # (1) RAG 기법 적용한 QA 체인 생성 
    response = qa_chain(usr_input) 
    if not response['result']: # RAG를 수행하지 못했을 때 - 에러 메시지 생성
        return jsonify({"error": "No response from RAG"}), 400 # 로깅으로 바꾸기 
    
    # RAG로 부터 적절한 답변을 받았을 때
    if not any(phrase in response['result'] for phrase in ["죄송", "모르겠습니다", "알 수 없습니다", "확인할 수 없습니다"]): 
        return response['result']
    
    # (2) RAG에 없는 정보 일 때 - 날씨/교통에 대한 질문인지 파악!
    client = openai.OpenAI(api_key=open_api_key) # 오픈AI 클라이언트 생성 
    
    # (2)-1. WEATHER 에 대한 정보를 포함하고 있을 때 
    if contains_weather_topic(client, model_version, usr_input): 
        weather_info = get_weather_prompt() # 날씨 정보, string  
        prompt = f"You are a helpful assistant, and you will kindly answer questions about current weather."\
                    "한국어로 대답해야해. 현재 날씨 정보는 다음과 같아. {weather_info},"\
                    "이 날씨 정보를 다 출력할 필요는 없고 , 주어진 질문에 필요한 답만 해줘 " \
                    f"{token_prompt}"
        return get_chatGPT_output(client, model_version,usr_input, prompt)
    # (2)-2. 교통 에 대한 정보를 포함하고 있는가? 
    elif contains_traffic_topic(client, model_version,usr_input): 
        #  API를 가져온다. 
        # prompt에 추가한다. 
        # prompt 예시: - prompt: 이러한 질문이 들어왔다. 그리고 현재 날씨 정보는 이렇다. 너가 적절한 답변을 설계해줘"
        pass
    
    else:
        prompt = "You are a helpful assistant."\
                 "and you will kindly answer questions about the Kakao Bootcamp in the future." \
                 "The students are based in Pangyo, Seongnam, KR."\
                 "사용자들은 한국어로 질문할 거고, 너도 한국어로 대답해야돼" \
                 f"{token_prompt}"
        gpt_response = get_chatGPT_output(client, model_version,usr_input, prompt)
        return gpt_response

if __name__ == '__main__':
    # weather API 변수 정의 
    WEATHER_API_KEY, LOCATION = os.environ.get("WEATHER_API_KEY"), os.environ.get("LOCATION")
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={WEATHER_API_KEY}'

    # LLM 변수 정의 
    open_api_key = os.environ.get("OPENAI_API_KEY") # API 키 설정
    pdf_path = './data/data.pdf' # PDF 경로를 지정해주기 - 추후에 모든 pdf 읽도록  바꾸도록 지정하기 
    model_version = "gpt-4-mini"
    
    
    # RAG를 위한 vectorDB와 qa chain 을 로드함. 
    documents = load_pdf(pdf_path)
    vectordb = vectorDB(documents, open_api_key)
    retriever = vectordb.as_retriever(search_kwargs={"k": 1}) # 유사도가 높은 결과 1개 반환 
    qa_chain = create_qa_chain(retriever, model_version, open_api_key)


    app.run(port=5000,debug=True)



"""@app.route('/', methods=['GET'])
def chatGPT():
    # API 키 설정
    open_api_key = os.getenv("OPENAI_API_KEY")
    if not open_api_key:
        return jsonify({'error': 'API key not found'}), 500
    
    openai.api_key = open_api_key

    # OpenAI API 요청
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "한국의 대통령은 누구입니까?"},
        ],
        temperature=0,
        max_tokens=100
    )

    # 응답 추출
    message_content = response.choices[0].message["content"]
    return jsonify({'response': message_content})


if __name__ == '__main__':
    app.run(port=5000, debug=True)"""
    

