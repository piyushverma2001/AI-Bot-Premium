import axios from "axios";

const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://127.0.0.1:8080",
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
  },
});

export const sendMessageToBot = async (message) => {
  if (!message) {
    console.error("Message is empty");
    return "Error: Message cannot be empty";
  }

  try {
    const { data } = await apiClient.post("/chat", { message });
    console.log("API Response:", data);
    return data.reply;
  } catch (error) {
    console.error(
      "API Error:",
      error.response ? error.response.data : error.message
    );
    return "Error: Unable to get response";
  }
};
