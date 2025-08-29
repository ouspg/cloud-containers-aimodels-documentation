import { useState, useRef, useEffect } from "react";
import logo from "/src/assets/kalevalagpt.jpg"; 

interface Message {
  sender: "user" | "bot";
  text: string;
  context?: string;           // bot, optional
  sources?: string[];         // bot, optional
  topK?: number;              // user
  similarityCutoff?: number;  // user
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  const [topK, setTopK] = useState(3);
  const [similarityCutoff, setSimilarityCutoff] = useState(0.5);

  const lastMessageRef = useRef<HTMLDivElement | null>(null);

  // Keep track of which messages have context visible
  const [visibleContext, setVisibleContext] = useState<Set<number>>(new Set());

  useEffect(() => {
    lastMessageRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg: Message = { 
    sender: "user", 
    text: input,
    topK: topK,
    similarityCutoff: similarityCutoff,
  };
  setMessages((prev) => [...prev, userMsg]);

    setInput("");

    try {
      const res = await fetch("http://localhost:5000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: input,
          top_k: topK,
          similarity_cutoff: similarityCutoff,
        }),
      });

      const data = await res.json();
      const botMsg: Message = {
        sender: "bot",
        text: data.answer,
        context: data.context,   // include context if backend sends it
        sources: data.sources,   // include sources if backend sends them
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error(err);
      const errMsg: Message = { sender: "bot", text: "Error: could not reach server" };
      setMessages((prev) => [...prev, errMsg]);
    }
  };

  const toggleContext = (index: number) => {
    setVisibleContext((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(index)) newSet.delete(index);
      else newSet.add(index);
      return newSet;
    });
  };

  const resetDefaults = () => {
    setTopK(3);
    setSimilarityCutoff(0.5);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "90vh", padding: "1rem" }}>
      <header style={{ display: "flex", alignItems: "center" }}>
        <img 
          src={logo} 
          alt="KalevalaGPT Logo" 
          style={{ width: "60px", height: "60px", marginRight: "12px" }} 
        />
        <h1 style={{ fontSize: "30px", fontWeight: "bold" }}>KalevalaGPT</h1>
      </header>

      {/* Chat messages */}
      <div style={{ flex: 1, overflowY: "auto", marginBottom: "1rem", border: "1px solid #ccc", padding: "0.5rem" }}>
        {messages.map((m, i) => {
          const isLast = i === messages.length - 1;
          return (
            <div key={i} ref={isLast ? lastMessageRef : null} style={{ textAlign: m.sender === "user" ? "right" : "left", margin: "0.25rem 0", position: "relative" }}>
              <span style={{ display: "inline-block", padding: "0.5rem 1rem", borderRadius: "12px", backgroundColor: m.sender === "user" ? "#007bff" : "#e0e0e0", color: m.sender === "user" ? "white" : "black", whiteSpace: "pre-wrap", maxWidth: "70%", position: "relative" }}>
                {m.text}
                {m.sender === "bot" && (m.context || m.sources?.length) && (
                  <button onClick={() => toggleContext(i)} style={{ position: "absolute", bottom: "-1.5rem", right: "0.25rem", fontSize: "0.7rem", padding: "2px 6px" }}>
                    {visibleContext.has(i) ? "Hide Info" : "Show Info"}
                  </button>
                )}
              </span>

              {m.sender === "user" && (
                <div style={{ fontSize: "0.75rem", color: "#888", marginTop: "0.2rem" }}>
                  Top K: {m.topK}, Similarity: {m.similarityCutoff}
                </div>
              )}

              {visibleContext.has(i) && (
                <div style={{ marginTop: "0.25rem", fontSize: "0.8rem", color: "#555", maxWidth: "70%", whiteSpace: "pre-wrap" }}>
                  {m.context && <div>{m.context}</div>}
                  {m.sources && m.sources.length > 0 && <div>Sources: {m.sources.join(", ")}</div>}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Options */}
      <div style={{ display: "flex", alignItems: "center", marginBottom: "0.5rem", gap: "0.5rem" }}>
        <label>
          How many documents to return (Top K):
          <input
            type="number"
            value={topK}
            min={1}
            max={10}
            onChange={(e) => setTopK(Math.min(10, Math.max(1, Number(e.target.value))))}
            style={{ width: "60px", marginLeft: "0.25rem" }}
          />
        </label>

        <label>
          Similarity threshold:
          <input
            type="number"
            step={0.05}
            min={0}
            max={1}
            value={similarityCutoff}
            onChange={(e) =>
              setSimilarityCutoff(Math.min(1, Math.max(0, Number(e.target.value))))
            }
            style={{ width: "60px", marginLeft: "0.25rem" }}
          />
        </label>

        <button onClick={resetDefaults} style={{ padding: "0.25rem 0.5rem" }}>
          Reset
        </button>
      </div>

      {/* Input + Send */}
      <div style={{ display: "flex" }}>
        <input
          style={{ flex: 1, padding: "0.5rem" }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter") sendMessage(); }}
          placeholder="Type your question..."
        />
        <button onClick={sendMessage} style={{ padding: "0.5rem 1rem" }}>
          Send
        </button>
      </div>
    </div>
  );
}
