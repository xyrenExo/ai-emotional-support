import { useState, useCallback, useRef } from "react";
import { Message, FeatureToggles, ChatResponse } from "@/types";
import { chatAPI } from "@/lib/api";

// Generate guaranteed unique IDs
const uid = () => `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;

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

  // Ref to prevent duplicate sends (e.g. double-click, StrictMode)
  const isSending = useRef(false);

  const sendMessage = useCallback(
    async (content: string) => {
      if (isSending.current || !content.trim()) return;
      isSending.current = true;

      const userMessage: Message = {
        id: uid(),
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

        if (!sessionId && response.session_id) {
          setSessionId(response.session_id);
        }

        const assistantMessage: Message = {
          id: uid(),
          content: response.response,
          role: "assistant",
          timestamp: new Date(),
          emotion: response.emotion,
          crisis: response.crisis,
        };

        setMessages((prev) => [...prev, assistantMessage]);
        return response;
      } catch (error: any) {
        console.error("Error sending message:", error);

        let errorMessage = "I'm having trouble connecting right now. Please try again in a moment.";
        if (error.type === "TIMEOUT") {
          errorMessage = "The server is taking too long. Please try again.";
        } else if (error.response?.status === 429) {
          errorMessage = "Too many requests. Please wait a moment and try again.";
        } else if (error.response?.status === 500) {
          errorMessage = "Server error. Please try again later.";
        } else if (error.response?.data?.error) {
          errorMessage = error.response.data.error;
        }

        const errorMsg: Message = {
          id: uid(),
          content: errorMessage,
          role: "assistant",
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, errorMsg]);
      } finally {
        setIsLoading(false);
        isSending.current = false;
      }
    },
    [sessionId, features],
  );

  const clearChat = useCallback(() => {
    setMessages([]);
    setSessionId(null);
    isSending.current = false;
  }, []);

  const toggleFeature = useCallback((feature: keyof FeatureToggles) => {
    setFeatures((prev) => ({
      ...prev,
      [feature]: !prev[feature],
    }));
  }, []);

  return {
    messages,
    setMessages,
    isLoading,
    features,
    sendMessage,
    clearChat,
    toggleFeature,
    sessionId,
  };
};
