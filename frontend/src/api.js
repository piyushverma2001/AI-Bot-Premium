import axios from "axios";

/**
 * Axios instance for interacting with the chatbot API.
 */
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://127.0.0.1:8080",
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Global interceptor for responses and errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("HTTP Error:", error);
    return Promise.reject(error);
  }
);

/**
 * Sends a message to the chatbot and returns the bot's reply.
 *
 * @param {string} message - The message to send to the chatbot.
 * @returns {Promise<string>} - A promise that resolves to the chatbot's reply.
 */
export const sendMessageToBot = async (message) => {
  if (!message || message.trim() === "") {
    console.error("Message is empty or whitespace only");
    return "Error: Message cannot be empty";
  }

  try {
    const { data } = await apiClient.post("/chat", { message });
    if (data && data.reply) {
      console.log("API Response:", data);
      return data.reply;
    } else {
      console.error("Unexpected response structure:", data);
      return "Error: Unexpected response from API";
    }
  } catch (error) {
    const errorMsg =
      error.response && error.response.data && error.response.data.error
        ? error.response.data.error
        : error.message || "Unable to get response";
    console.error("API Error:", errorMsg);
    return `Error: ${errorMsg}`;
  }
};
