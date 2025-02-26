import axios from "axios";

const API_URL = "http://127.0.0.1:8080/chat";

export const sendMessageToBot = async (message) => {
  try {
    const response = await axios.post(API_URL, { message });
    console.log("API Response:", response.data);
    return response.data.reply;
  } catch (error) {
    console.error(
      "API Error:",
      error.response ? error.response.data : error.message
    );
    return "Error: Unable to get response";
  }
};
