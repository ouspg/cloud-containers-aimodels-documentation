const dotenv = require("dotenv");
const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();
app.use(cors());
app.use(express.json());
dotenv.config();

const API_KEY = process.env.API_KEY;

app.post("/api/chat", async (req, res) => {
  const { question, top_k, similarity_cutoff } = req.body;

  try {
    const aiResponse = await axios.post(
      "http://localhost:8000/query",
      {
        question: question,
        top_k: top_k,
        similarity_cutoff: similarity_cutoff,
      },
      {
        headers: { "x-api-key": API_KEY }
      }
    );

    let { answer, context, sources } = aiResponse.data;

    if (answer) {
      // Existing assistant-tag logic
      const splitAnswer = answer.split("<|assistant|>");
      if (splitAnswer.length > 1) {
        answer = splitAnswer[1].trim();
      }

      // Remove stop tokens
      answer = answer.replaceAll("</s>", "").trim();

      // Remove unwanted continuation patterns
      const stopPatterns = [
        "User Question:",
        "User:",
        "Question:",
        "### User",
        "### Instruction"
      ];

      for (const pattern of stopPatterns) {
        const idx = answer.indexOf(pattern);
        if (idx !== -1) {
          answer = answer.slice(0, idx).trim();
        }
      }
    }

    res.json({
      answer,
      context,
      sources,
    });

  } catch (err) {
    console.error(err);
    res.status(500).json({ answer: "Error: could not reach KalevalaGPT" });
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Backend running on http://localhost:${PORT}`));
