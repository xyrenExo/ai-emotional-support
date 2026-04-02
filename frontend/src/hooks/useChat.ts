import { useState, useCallback, useRef } from "react";
import { Message, FeatureToggles, ChatResponse } from "@/types";
import { chatAPI } from "@/lib/api";

export const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [features, setFeatures] = useState<FeatureToggles>({
    music: false,
    breathing: false,
    mental: false,
    insight: false,
    professional_help: false,
  });

  const sendMessage = useCallback(
    async (content: string) => {
      // Add user message
      const userMessage: Message = {
        id: Date.now().toString(),
        content,
        role: "user",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);

      try {
        const response: ChatResponse = await chatAPI.sendMessage({
          message: content,
          session_id: sessionId || undefined,
          features,
        });

        // Save session ID if new
        if (!sessionId && response.session_id) {
          setSessionId(response.session_id);
        }

        // Add assistant message
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: response.response,
          role: "assistant",
          timestamp: new Date(),
          emotion: response.emotion,
        };

        setMessages((prev) => [...prev, assistantMessage]);

        return response;
      } catch (error: any) {
        console.error("Error sending message:", error);

        let errorMessage =
          "I'm having trouble connecting. Please check your internet connection and try again.";

        if (error.type === "TIMEOUT") {
          errorMessage =
            "The server is taking too long to respond. Please try again.";
        } else if (error.type === "NETWORK_ERROR") {
          errorMessage =
            "Cannot reach the server. Please check your internet connection.";
        } else if (error.response?.status === 429) {
          errorMessage =
            "Too many requests. Please wait a moment and try again.";
        } else if (error.response?.status === 500) {
          errorMessage =
            "Server error. Please try again later or refresh the page.";
        } else if (error.response?.status === 503) {
          errorMessage =
            "Server is currently unavailable. Please try again later.";
        } else if (error.response?.data?.error) {
          errorMessage = error.response.data.error;
        }

        // Add error message
        const errorMessage_Obj: Message = {
          id: (Date.now() + 1).toString(),
          content: errorMessage,
          role: "assistant",
          timestamp: new Date(),
        };

        setMessages((prev) => [...prev, errorMessage_Obj]);
      } finally {
        setIsLoading(false);
      }
    },
    [sessionId, features],
  );

  const clearChat = useCallback(() => {
    setMessages([]);
    setSessionId(null);
  }, []);

  const toggleFeature = useCallback((feature: keyof FeatureToggles) => {
    setFeatures((prev) => ({
      ...prev,
      [feature]: !prev[feature],
    }));
  }, []);

  return {
    messages,
    isLoading,
    features,
    sendMessage,
    clearChat,
    toggleFeature,
  };
};
