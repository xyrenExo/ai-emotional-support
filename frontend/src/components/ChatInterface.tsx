'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, Loader2 } from 'lucide-react';
import { useChat } from '@/hooks/useChat';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';
import EmotionDisplay from './EmotionDisplay';
import FeatureToggles from './FeatureToggles';

const ChatInterface: React.FC = () => {
    const [input, setInput] = useState('');
    const { messages, isLoading, features, sendMessage, toggleFeature } = useChat();
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLTextAreaElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const message = input.trim();
        setInput('');
        await sendMessage(message);
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    const lastMessage = messages[messages.length - 1];
    const lastEmotion = lastMessage?.role === 'assistant' ? lastMessage.emotion : null;

    return (
        <div className="flex flex-col h-screen bg-gradient-to-br from-calm-50 to-sage-50 dark:from-gray-900 dark:to-gray-800">
            {/* Header */}
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-b border-gray-200 dark:border-gray-700 p-4">
                <div className="max-w-4xl mx-auto flex justify-between items-center">
                    <div>
                        <h1 className="text-2xl font-semibold text-gray-800 dark:text-white">
                            Emotional Support Assistant
                        </h1>
                        <p className="text-sm text-gray-600 dark:text-gray-300">
                            Anonymous & Safe Space
                        </p>
                    </div>
                    {lastEmotion && <EmotionDisplay emotion={lastEmotion} />}
                </div>
            </div>

            {/* Feature Toggles */}
            <div className="bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border-b border-gray-200 dark:border-gray-700">
                <div className="max-w-4xl mx-auto">
                    <FeatureToggles features={features} onToggle={toggleFeature} />
                </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4">
                <div className="max-w-4xl mx-auto space-y-4">
                    {messages.length === 0 && (
                        <div className="text-center text-gray-500 dark:text-gray-400 mt-20">
                            <div className="text-6xl mb-4">💙</div>
                            <h2 className="text-2xl font-semibold mb-2">Welcome to your safe space</h2>
                            <p className="text-lg">
                                Share what's on your mind. I'm here to listen and support you.
                            </p>
                            <p className="text-sm mt-4">
                                Remember: This is a private, anonymous conversation.
                            </p>
                        </div>
                    )}

                    {messages.map((message) => (
                        <MessageBubble key={message.id} message={message} />
                    ))}

                    {isLoading && <TypingIndicator />}
                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input */}
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-t border-gray-200 dark:border-gray-700 p-4">
                <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
                    <div className="flex space-x-2 items-end">
                        <div className="flex-1 relative">
                            <textarea
                                ref={inputRef}
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Type your message here..."
                                rows={1}
                                className="w-full px-4 py-3 bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-600 rounded-2xl focus:outline-none focus:ring-2 focus:ring-calm-500 focus:border-transparent resize-none"
                                style={{ minHeight: '48px', maxHeight: '120px' }}
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={!input.trim() || isLoading}
                            className="p-3 bg-calm-500 text-white rounded-full hover:bg-calm-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {isLoading ? (
                                <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                                <Send className="w-5 h-5" />
                            )}
                        </button>
                    </div>

                    <div className="text-xs text-center text-gray-500 dark:text-gray-400 mt-2">
                        Your privacy is protected. This conversation is anonymous.
                    </div>
                </form>
            </div>
        </div>
    );
};

export default ChatInterface;