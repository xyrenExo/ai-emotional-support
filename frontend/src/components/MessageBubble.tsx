"use client";

import React from "react";
import ReactMarkdown from "react-markdown";
import { Message } from "@/types";
import { User, Bot, Music, Wind, Brain, Lightbulb, Phone } from "lucide-react";

interface MessageBubbleProps {
  message: Message;
}

const featureIcons: Record<string, React.ReactNode> = {
  "🎵 MUSIC SUGGESTIONS": <Music className="w-4 h-4 text-blue-400" />,
  "🌬️ BREATHING EXERCISES": <Wind className="w-4 h-4 text-cyan-400" />,
  "🧠 MENTAL EXERCISE": <Brain className="w-4 h-4 text-purple-400" />,
  "💡 MOOD INSIGHTS": <Lightbulb className="w-4 h-4 text-yellow-400" />,
  "👨‍⚕️ PROFESSIONAL SUPPORT": <Phone className="w-4 h-4 text-red-400" />,
};

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === "user";

  // Parse response to separate main content from feature sections
  const parseResponse = (content: string) => {
    const sections = content.split("---").map((s) => s.trim());
    const mainContent = sections[0];
    const features = sections.slice(1);

    return { mainContent, features };
  };

  const { mainContent, features } = parseResponse(message.content);

  return (
    <div
      className={`flex ${isUser ? "justify-end" : "justify-start"} animate-in slide-in-from-bottom-2 duration-300`}
    >
      <div
        className={`flex ${isUser ? "flex-row-reverse" : "flex-row"} items-start space-x-2 max-w-[85%]`}
      >
        <div
          className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
            isUser ? "bg-calm-500" : "bg-gray-300 dark:bg-gray-600"
          }`}
        >
          {isUser ? (
            <User className="w-4 h-4 text-white" />
          ) : (
            <Bot className="w-4 h-4 text-gray-700 dark:text-white" />
          )}
        </div>

        <div
          className={`${isUser ? "chat-message-user" : "chat-message-assistant"} space-y-4`}
        >
          {/* Main response content */}
          <div className="prose dark:prose-invert max-w-none">
            <ReactMarkdown>{mainContent}</ReactMarkdown>
          </div>

          {/* Feature sections */}
          {features.length > 0 &&
            features.map((feature, idx) => {
              const featureTitle = feature.split("\n")[0];
              const featureContent = feature
                .split("\n")
                .slice(1)
                .join("\n")
                .trim();
              const icon =
                Object.entries(featureIcons).find(([key]) =>
                  feature.includes(key)
                )?.[1] || null;

              return (
                <div
                  key={idx}
                  className="mt-3 p-3 rounded-lg bg-gradient-to-br from-surface-700/50 to-surface-800/50 border border-surface-600/50"
                >
                  <div className="flex items-center gap-2 mb-2">
                    {icon}
                    <h4 className="font-semibold text-sm text-gray-100">
                      {featureTitle || `Feature ${idx + 1}`}
                    </h4>
                  </div>
                  <div className="prose dark:prose-invert prose-sm max-w-none">
                    <ReactMarkdown>{featureContent}</ReactMarkdown>
                  </div>
                </div>
              );
            })}

          {/* Emotion indicator */}
          {message.emotion && !isUser && (
            <div className="mt-2 pt-2 border-t border-gray-200 dark:border-gray-700">
              <span className="text-xs opacity-70">
                Detected emotion: {message.emotion.primary_emotion}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;
