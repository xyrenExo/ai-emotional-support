"use client";

import React from "react";
import ReactMarkdown from "react-markdown";
import { motion, AnimatePresence } from "framer-motion";
import { Message } from "@/types";
import { User, Bot, Music, Wind, Brain, Lightbulb, Phone, Smile, Frown, AlertCircle, Heart, Zap, HelpCircle } from "lucide-react";

interface MessageBubbleProps {
  message: Message;
}

const featureIcons: Record<string, React.ReactNode> = {
  "🎵 MUSIC SUGGESTIONS": <Music className="w-5 h-5 text-blue-400" />,
  "🌬️ BREATHING EXERCISES": <Wind className="w-5 h-5 text-teal-400" />,
  "🧠 MENTAL EXERCISE": <Brain className="w-5 h-5 text-purple-400" />,
  "💡 MOOD INSIGHTS": <Lightbulb className="w-5 h-5 text-amber-400" />,
  "👨‍⚕️ PROFESSIONAL SUPPORT": <Phone className="w-5 h-5 text-rose-400" />,
};

const emotionConfig: Record<string, { icon: React.ReactNode; color: string; bg: string }> = {
  joy: { icon: <Smile className="w-3.5 h-3.5" />, color: "text-amber-400", bg: "bg-amber-400/10 border-amber-400/20" },
  sadness: { icon: <Frown className="w-3.5 h-3.5" />, color: "text-blue-400", bg: "bg-blue-400/10 border-blue-400/20" },
  anger: { icon: <Zap className="w-3.5 h-3.5" />, color: "text-rose-400", bg: "bg-rose-400/10 border-rose-400/20" },
  fear: { icon: <AlertCircle className="w-3.5 h-3.5" />, color: "text-purple-400", bg: "bg-purple-400/10 border-purple-400/20" },
  caring: { icon: <Heart className="w-3.5 h-3.5" />, color: "text-pink-400", bg: "bg-pink-400/10 border-pink-400/20" },
  neutral: { icon: <HelpCircle className="w-3.5 h-3.5" />, color: "text-slate-400", bg: "bg-slate-400/10 border-slate-400/20" },
};

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === "user";

  const parseResponse = (content: string) => {
    const sections = content.split("---").map((s) => s.trim());
    const mainContent = sections[0];
    const features = sections.slice(1);
    return { mainContent, features };
  };

  const { mainContent, features } = parseResponse(message.content);
  const emotion = message.emotion?.primary_emotion || "neutral";
  const config = emotionConfig[emotion] || emotionConfig.neutral;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className={`flex ${isUser ? "justify-end" : "justify-start"} mb-8`}
    >
      <div className={`flex ${isUser ? "flex-row-reverse" : "flex-row"} items-start gap-4 max-w-[85%]`}>
        <motion.div 
          whileHover={{ scale: 1.1 }}
          className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-lg ${
            isUser 
              ? "bg-gradient-to-br from-accent-500 to-accent-700 border border-white/10" 
              : "bg-slate-800 border border-white/5"
          }`}
        >
          {isUser ? (
            <User className="w-5 h-5 text-white" />
          ) : (
            <Bot className="w-5 h-5 text-accent-400" />
          )}
        </motion.div>

        <div className="flex flex-col gap-2">
          <div className={`${isUser ? "chat-message-user" : "chat-message-assistant w-full"}`}>
            {/* Main response content */}
            <div className={`prose prose-slate dark:prose-invert max-w-none ${isUser ? "text-white" : "text-slate-300 prose-p:leading-[1.8] prose-p:mb-6 prose-p:tracking-wide text-[16px]"}`}>
              <ReactMarkdown>{mainContent}</ReactMarkdown>
            </div>

            {/* Feature sections */}
            <AnimatePresence mode="popLayout">
              {features.length > 0 && (
                <motion.div 
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  className="space-y-4 mt-2"
                >
                  {features.map((feature, idx) => {
                    const lines = feature.split("\n");
                    const featureTitle = lines[0];
                    const featureContent = lines.slice(1).join("\n").trim();
                    const icon = Object.entries(featureIcons).find(([key]) => feature.includes(key))?.[1] || null;

                    return (
                      <motion.div
                        key={idx}
                        initial={{ x: -10, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        transition={{ delay: 0.2 + idx * 0.1 }}
                        className="p-4 rounded-xl bg-white/[0.03] border border-white/[0.05] hover:bg-white/[0.05] transition-all"
                      >
                        <div className="flex items-center gap-2 mb-2 border-b border-white/[0.05] pb-2">
                          {icon}
                          <h4 className="font-bold text-sm tracking-wide text-white uppercase italic">
                            {featureTitle}
                          </h4>
                        </div>
                        <div className="prose prose-sm dark:prose-invert max-w-none prose-p:leading-relaxed">
                          <ReactMarkdown>{featureContent}</ReactMarkdown>
                        </div>
                      </motion.div>
                    );
                  })}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Emotion Badge */}
          {!isUser && emotion && (
            <motion.div 
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className={`emotion-badge w-fit border ${config.bg} ${config.color}`}
            >
              {config.icon}
              <span>Detected: {emotion}</span>
            </motion.div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default MessageBubble;
