import axios, { AxiosError } from "axios";

const API_BASE_URL =
  typeof window !== "undefined"
    ? "/api"
    : process.env.NEXT_PUBLIC_API_URL || "http://backend:5000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 60000, // 60 second timeout
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error);
    if (error.code === "ECONNABORTED") {
      return Promise.reject({
        message: "Request timed out. The server is taking too long to respond.",
        status: 504,
      });
    }
    if (!error.response) {
      return Promise.reject({
        message: "Network error. Please check your internet connection.",
        status: 0,
      });
    }
    return Promise.reject(error);
  },
);

export interface ChatRequest {
  message: string;
  session_id?: string;
  features: {
    music: boolean;
    breathing: boolean;
    mental: boolean;
    insight: boolean;
    professional_help: boolean;
  };
}

export const chatAPI = {
  sendMessage: async (data: ChatRequest) => {
    try {
      const response = await api.post("/chat", data);
      return response.data;
    } catch (error) {
      console.error("Error sending message:", error);
      throw error;
    }
  },

  analyzeEmotion: async (message: string) => {
    try {
      const response = await api.post("/analyze", { message });
      return response.data;
    } catch (error) {
      console.error("Error analyzing emotion:", error);
      throw error;
    }
  },

  getCrisisResources: async () => {
    try {
      const response = await api.get("/crisis-resources");
      return response.data;
    } catch (error) {
      console.error("Error getting crisis resources:", error);
      throw error;
    }
  },

  healthCheck: async () => {
    try {
      const response = await api.get("/health");
      return response.data;
    } catch (error) {
      console.error("Error checking health:", error);
      throw error;
    }
  },
};
