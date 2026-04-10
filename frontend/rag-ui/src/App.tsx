import { useState } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState("");
  const [className, setClassName] = useState("class7");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question) return;

    const userMessage: Message = {
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);

    const res = await fetch(
      `http://localhost:8002/ask?question=${question}&class_name=${className}`
    );

    const data = await res.json();

    const botMessage: Message = {
      role: "assistant",
      content: data.answer,
    };

    setMessages((prev) => [...prev, botMessage]);
    setLoading(false);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      askQuestion();
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>NCERT RAG Chat</h1>
        <select
          value={className}
          onChange={(e) => setClassName(e.target.value)}
          className="class-select"
        >
          <option value="class5">Class 5</option>
          <option value="class6">Class 6</option>
          <option value="class7">Class 7</option>
          <option value="class8">Class 8</option>
          <option value="class9">Class 9</option>
          <option value="class10">Class 10</option>
        </select>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="empty-state">
            <p>Ask a question about NCERT textbooks</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`message ${msg.role === "user" ? "user-message" : "ai-message"}`}
          >
            <div className="message-avatar">
              {msg.role === "user" ? "👤" : "🤖"}
            </div>
            <div className="message-content">
              <p>{msg.content}</p>
            </div>
          </div>
        ))}

        {loading && (
          <div className="message ai-message">
            <div className="message-avatar">🤖</div>
            <div className="message-content typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
      </div>

      <div className="chat-input-container">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Ask your question..."
          className="chat-input"
          rows={1}
        />
        <button onClick={askQuestion} className="send-button" disabled={!question.trim()}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
          </svg>
        </button>
      </div>

      <style>{`
        .chat-container {
          width: 100%;
          max-width: 900px;
          height: 100vh;
          margin: 0 auto;
          display: flex;
          flex-direction: column;
          background: #0f0f23;
          border-radius: 0;
          box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }

        .chat-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 20px 24px;
          background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
          color: white;
        }

        .chat-header h1 {
          font-size: 1.5rem;
          font-weight: 600;
        }

        .class-select {
          padding: 8px 16px;
          border-radius: 20px;
          border: none;
          background: rgba(255, 255, 255, 0.2);
          color: white;
          font-size: 0.9rem;
          cursor: pointer;
          outline: none;
        }

        .class-select option {
          background: #1a1a2e;
          color: white;
        }

        .chat-messages {
          flex: 1;
          overflow-y: auto;
          padding: 24px;
          display: flex;
          flex-direction: column;
          gap: 16px;
        }

        .empty-state {
          display: flex;
          align-items: center;
          justify-content: center;
          height: 100%;
          color: #666;
          font-size: 1.1rem;
        }

        .message {
          display: flex;
          gap: 12px;
          animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }

        .user-message {
          flex-direction: row-reverse;
        }

        .message-avatar {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 1.2rem;
          flex-shrink: 0;
        }

        .user-message .message-avatar {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .ai-message .message-avatar {
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }

        .message-content {
          max-width: 70%;
          padding: 14px 18px;
          border-radius: 18px;
          line-height: 1.6;
        }

        .user-message .message-content {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-bottom-right-radius: 4px;
        }

        .ai-message .message-content {
          background: #1e1e3f;
          color: #e0e0e0;
          border-bottom-left-radius: 4px;
        }

        .ai-message .message-content.typing {
          display: flex;
          gap: 4px;
          align-items: center;
          padding: 16px 20px;
        }

        .ai-message .message-content.typing span {
          width: 8px;
          height: 8px;
          background: #667eea;
          border-radius: 50%;
          animation: bounce 1.4s infinite ease-in-out both;
        }

        .ai-message .message-content.typing span:nth-child(1) { animation-delay: -0.32s; }
        .ai-message .message-content.typing span:nth-child(2) { animation-delay: -0.16s; }

        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1); }
        }

        .chat-input-container {
          display: flex;
          gap: 12px;
          padding: 20px 24px;
          background: #1a1a2e;
          border-top: 1px solid #2a2a4a;
        }

        .chat-input {
          flex: 1;
          padding: 14px 18px;
          border-radius: 25px;
          border: 1px solid #3a3a5a;
          background: #0f0f23;
          color: white;
          font-size: 1rem;
          resize: none;
          outline: none;
          transition: border-color 0.2s;
        }

        .chat-input:focus {
          border-color: #667eea;
        }

        .chat-input::placeholder {
          color: #666;
        }

        .send-button {
          width: 50px;
          height: 50px;
          border-radius: 50%;
          border: none;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: transform 0.2s, opacity 0.2s;
        }

        .send-button:hover:not(:disabled) {
          transform: scale(1.05);
        }

        .send-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        @media (max-width: 600px) {
          .chat-header h1 {
            font-size: 1.2rem;
          }
          .message-content {
            max-width: 85%;
          }
          .chat-messages {
            padding: 16px;
          }
        }
      `}</style>
    </div>
  );
}

export default App;
