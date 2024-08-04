// .env 파일에 저장된 환경 변수를 불러옵니다.
require('dotenv').config();

// HTTP 요청을 위해 axios 라이브러리를 불러옵니다.
const axios = require('axios');

// 환경 변수에서 OpenAI API 키를 불러옵니다.
const openaiApiKey = process.env.OPENAI_API_KEY;

// OpenAI API와 통신하여 응답을 받아오는 비동기 함수입니다.
const getOpenAIResponse = async (prompt) => {
  try {
    // OpenAI API에 POST 요청을 보냅니다. (GPT-4o mini 모델 사용)
    const response = await axios.post('https://api.openai.com/v1/chat/completions', {
      model: 'gpt-4o-mini', // 사용할 모델 지정
      messages: [{ role: 'user', content: prompt }], // 대화 형태로 메시지 전달
      max_tokens: 100 // 생성할 최대 토큰 수
    }, {
      headers: {
        'Authorization': `Bearer ${openaiApiKey}` // 인증을 위한 API 키 헤더 설정
      }
    });
    // 응답 데이터를 반환합니다.
    return response.data;
  } catch (error) {
    // 에러가 발생하면 에러 내용을 콘솔에 출력합니다.
    console.error(error);
  }
};

// getOpenAIResponse 함수를 모듈로 내보냅니다.
module.exports = { getOpenAIResponse };