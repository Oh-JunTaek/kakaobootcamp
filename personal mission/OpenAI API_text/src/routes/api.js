const express = require('express');
const { generateText } = require('../openai');

const router = express.Router();

router.post('/generate-text', async (req, res) => {
  const { prompt } = req.body;
  try {
    const generatedText = await generateText(prompt);
    res.json({ generatedText });
  } catch (error) {
    res.status(500).json({ error: 'Error generating text' });
  }
});

module.exports = router;