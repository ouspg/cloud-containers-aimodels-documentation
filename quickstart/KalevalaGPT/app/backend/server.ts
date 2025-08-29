const dotenv = require("dotenv");
const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();
app.use(cors());
app.use(express.json());
dotenv.config();

const API_KEY = process.env.API_KEY;

app.post("/api/chat", async (req: { body: { question: any; top_k: any; similarity_cutoff: any; }; }, res: {
    json: (arg0: {
      answer: any; context: any; // optional, used by Show Info button
      sources: any;
    }) => void; status: (arg0: number) => { (): any; new(): any; json: { (arg0: { answer: string; }): void; new(): any; }; };
  }) => {
  const { question, top_k, similarity_cutoff } = req.body;

  try {
    // Send the message + optional parameters to the AI backend
    const aiResponse = await axios.post("http://86.50.168.231:8000/query", {
      question: question,
      top_k: top_k,
      similarity_cutoff: similarity_cutoff, 
    },
    {
      headers: { "x-api-key": API_KEY }
  });

  // Extract only the assistant's answer
  let { answer, context, sources } = aiResponse.data;

  if (answer) {
    const splitAnswer = answer.split("<|assistant|>");
    if (splitAnswer.length > 1) {
      answer = splitAnswer[1].trim();  // take everything after <|assistant|>
      answer = answer.replaceAll("</s>", "").trim()
    } else {
      answer = answer = answer.replaceAll("</s>", "").trim(); // fallback if tag not found
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
