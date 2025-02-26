import React, { useState } from "react";
import { sendMessageToBot } from "./api";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    console.log("User Message:", input);

    setInput("");

    try {
      const botReply = await sendMessageToBot(input);
      console.log("Bot Reply:", botReply);

      const botMessage = { role: "bot", content: botReply };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Error getting response:", error);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto", padding: "20px" }}>
      <h2>ChatBot</h2>
      <div
        style={{
          border: "1px solid #ccc",
          padding: "10px",
          height: "400px",
          overflowY: "scroll",
        }}
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              margin: "10px 0",
              textAlign: msg.role === "user" ? "right" : "left",
            }}
          >
            <strong>{msg.role === "user" ? "You" : "Bot"}: </strong>
            {msg.content}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type a message..."
        style={{ width: "80%", padding: "10px", marginTop: "10px" }}
      />
      <button onClick={handleSend} style={{ padding: "10px" }}>
        Send
      </button>
    </div>
  );
};

export default Chat;
