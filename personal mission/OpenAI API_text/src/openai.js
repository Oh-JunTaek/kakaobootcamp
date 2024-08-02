const axios = require('axios');
require('dotenv').config();

const openaiApiKey = process.env.OPENAI_API_KEY;

const openaiApi = axios.create({
  baseURL: 'https://api.openai.com/v1',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': Bearer ${openaiApiKey},
  },
});

const generateText = async (prompt) => {
  try {
    const response = await openaiApi.post('/completions', {
      model: 'text-davinci-003',
      prompt: prompt,
      max_tokens: 100,
    });
    return response.data.choices[0].text;
  } catch (error) {
    console.error('Error generating text:', error);
    throw error;
  }
};

module.exports = {
  generateText,
};