'use client';

import React, { useState, useRef, useEffect } from 'react';
import { 
    Send, Mic, Loader2, Menu, Plus, Search, 
    MessageSquare, FolderOpen, MoreHorizontal, Bookmark, Share, 
    Music, Wind, Brain, Lightbulb, Phone
} from 'lucide-react';
import { useChat } from '@/hooks/useChat';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';

const featureIcons: Record<string, React.ReactNode> = {
    music: <Music className="w-5 h-5 text-accent-500" />,
    breathing: <Wind className="w-5 h-5 text-accent-500" />,
    mental: <Brain className="w-5 h-5 text-accent-500" />,
    insight: <Lightbulb className="w-5 h-5 text-accent-500" />,
    professional_help: <Phone className="w-5 h-5 text-red-500" />
};

const featureDetails: Record<string, { title: string, desc: string }> = {
    music: { title: "Music Suggestions", desc: "Tailored calming music for your mood." },
    breathing: { title: "Breathing Exercises", desc: "Guided routines to help you relax." },
    mental: { title: "Mental Exercises", desc: "Cognitive reframing exercises." },
    insight: { title: "Mood Insights", desc: "Analyze emotional patterns." },
    professional_help: { title: "Professional Help", desc: "Connect with certified therapists." }
};

const ChatInterface: React.FC = () => {
    const [input, setInput] = useState('');
    const [sidebarOpen, setSidebarOpen] = useState(true);
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

    const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

    const activeFeatures = Object.keys(features).filter((k) => features[k as keyof typeof features]);

    return (
        <div className="flex h-screen bg-surface-900 text-gray-200 overflow-hidden font-sans">
            
            {/* Sidebar */}
            <div className={`transition-all duration-300 flex flex-col bg-[#1A1A1A] border-r border-[#2A2A2A] ${sidebarOpen ? 'w-[260px] opacity-100' : 'w-0 opacity-0 overflow-hidden'}`}>
                {/* Sidebar Header */}
                <div className="p-4 flex items-center justify-between mt-2">
                    <div className="flex items-center gap-2 px-2 py-1.5 bg-[#252525] rounded-xl cursor-pointer hover:bg-[#303030] transition-colors flex-1">
                        <MessageSquare className="w-4 h-4 text-gray-400" />
                        <span className="text-sm font-medium">My Sessions</span>
                        <MoreHorizontal className="w-4 h-4 text-gray-500 ml-auto" />
                    </div>
                </div>

                {/* Sidebar Search */}
                <div className="px-4 mb-4">
                    <div className="relative">
                        <Search className="w-4 h-4 absolute left-3 top-2.5 text-gray-500" />
                        <input 
                            type="text" 
                            placeholder="Search" 
                            className="w-full bg-[#252525] text-sm text-gray-200 placeholder-gray-500 rounded-lg pl-9 pr-4 py-2 outline-none focus:ring-1 focus:ring-accent-500 border border-transparent focus:border-accent-500/50"
                        />
                    </div>
                </div>

                {/* Sidebar Folders */}
                <div className="flex-1 overflow-y-auto px-4 custom-scrollbar">
                    <div className="mb-6">
                        <h3 className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wider flex justify-between items-center">
                            Folders
                            <Plus className="w-3.5 h-3.5 cursor-pointer hover:text-gray-300" />
                        </h3>
                        <div className="space-y-1">
                            {['Stress Relief', 'Daily Journals', 'Therapy Notes'].map(folder => (
                                <div key={folder} className="flex items-center gap-2 text-sm text-gray-400 p-2 hover:bg-[#252525] rounded-lg cursor-pointer transition-colors">
                                    <FolderOpen className="w-4 h-4" />
                                    <span>{folder}</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div>
                        <h3 className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wider flex justify-between items-center">
                            Recent
                            <Plus className="w-3.5 h-3.5 cursor-pointer hover:text-gray-300" />
                        </h3>
                        <div className="space-y-1">
                            <div className="flex items-center gap-2 text-sm text-gray-300 p-2 bg-[#2A2A2B] rounded-lg cursor-pointer transition-colors">
                                <MessageSquare className="w-4 h-4 text-gray-500" />
                                <span className="truncate">Anxiety before presentation</span>
                                <MoreHorizontal className="w-4 h-4 text-gray-500 ml-auto opacity-0 group-hover:opacity-100" />
                            </div>
                            <div className="flex items-center gap-2 text-sm text-gray-400 p-2 hover:bg-[#2A2A2B] rounded-lg cursor-pointer transition-colors">
                                <MessageSquare className="w-4 h-4 text-gray-500" />
                                <span className="truncate">Feeling overwhelmed</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Sidebar Footer */}
                <div className="p-4 border-t border-[#2A2A2A]">
                    <button className="w-full flex items-center justify-center gap-2 bg-accent-500 hover:bg-accent-600 text-white py-2.5 rounded-xl text-sm font-semibold transition-all">
                        <Plus className="w-4 h-4" />
                        New Session
                    </button>
                </div>
            </div>

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col relative h-full bg-[#0E0E0E]">
                
                {/* Top Nav */}
                <div className="absolute top-0 left-0 right-0 p-4 flex justify-between items-center z-10 bg-gradient-to-b from-[#0E0E0E] to-transparent pointer-events-none">
                    <div className="flex items-center gap-4 pointer-events-auto">
                        <button onClick={toggleSidebar} className="p-2 hover:bg-surface-700 rounded-lg text-gray-400 transition-colors">
                            <Menu className="w-5 h-5" />
                        </button>
                        <div className="flex items-center gap-2">
                            <span className="text-sm font-medium text-gray-300">Emotional Support AI</span>
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-[#142A1E] text-accent-400 border border-accent-500/20">v2.0</span>
                        </div>
                    </div>
                    <div className="flex items-center gap-3 pointer-events-auto">
                        <Bookmark className="w-5 h-5 text-gray-400 cursor-pointer hover:text-gray-200" />
                        <Share className="w-5 h-5 text-gray-400 cursor-pointer hover:text-gray-200" />
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto w-full flex justify-center pt-20 pb-40 px-4 custom-scrollbar">
                    {messages.length === 0 ? (
                        <div className="flex flex-col items-center justify-center w-full max-w-3xl mt-10">
                            <div className="w-12 h-12 bg-[#1A1A1A] rounded-full flex items-center justify-center mb-6">
                                <Brain className="w-6 h-6 text-accent-500" />
                            </div>
                            <h2 className="text-3xl font-semibold text-white mb-2">How can I help you today?</h2>
                            <p className="text-gray-400 mb-10 text-center">
                                I provide a safe, anonymous space. Select support tools below or just start typing.
                            </p>
                            
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 w-full mb-8">
                                {(Object.keys(featureDetails) as Array<keyof typeof features>).map(key => (
                                    <div 
                                        key={key} 
                                        onClick={() => toggleFeature(key as keyof typeof features)}
                                        className={`p-4 rounded-2xl cursor-pointer border transition-all ${
                                            features[key] 
                                                ? 'bg-[#142A1E] border-accent-500/50 hover:bg-[#1A3326]' 
                                                : 'bg-[#1A1A1A] border-[#2A2A2A] hover:bg-[#252525] hover:border-[#3A3A3A]'
                                        }`}
                                    >
                                        <div className="mb-3">
                                            {featureIcons[key]}
                                        </div>
                                        <h4 className={`text-sm font-medium mb-1 ${features[key] ? 'text-accent-400' : 'text-gray-200'}`}>
                                            {featureDetails[key].title}
                                        </h4>
                                        <p className="text-xs text-gray-500">
                                            {featureDetails[key].desc}
                                        </p>
                                    </div>
                                ))}
                            </div>
                            
                            <div className="flex flex-wrap items-center justify-center gap-2">
                                <span className={`px-4 py-1.5 rounded-full text-xs font-medium cursor-pointer ${activeFeatures.length === 0 ? 'bg-[#3A3A3A] text-white' : 'text-gray-400 hover:bg-[#1A1A1A]'}`}>
                                    Just talk
                                </span>
                                {(Object.keys(featureDetails)).map((key) => (
                                   features[key as keyof typeof features] && (
                                       <span key={key} className="px-4 py-1.5 rounded-full text-xs font-medium cursor-pointer bg-[#142A1E] text-accent-400 border border-accent-500/20">
                                            {featureDetails[key].title}
                                       </span>
                                   )
                                ))}
                            </div>
                        </div>
                    ) : (
                        <div className="w-full max-w-3xl space-y-6">
                            {messages.map((message) => (
                                <MessageBubble key={message.id} message={message} />
                            ))}
                            {isLoading && <TypingIndicator />}
                            <div ref={messagesEndRef} />
                        </div>
                    )}
                </div>

                {/* Input Area */}
                <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-[#0E0E0E] via-[#0E0E0E]/90 to-transparent">
                    <div className="max-w-3xl mx-auto w-full">
                        <form onSubmit={handleSubmit} className="relative flex items-center bg-[#1A1A1A] border border-[#2A2A2A] rounded-2xl p-2 pl-4 focus-within:ring-1 focus-within:ring-[#3A3A3A] focus-within:border-[#3A3A3A] transition-all">
                            <Mic className="w-5 h-5 text-gray-400 hover:text-white cursor-pointer transition-colors" />
                            <textarea
                                ref={inputRef}
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Type your message here..."
                                rows={1}
                                className="flex-1 bg-transparent border-none text-white focus:outline-none focus:ring-0 resize-none px-3 py-2 text-sm placeholder-gray-500 max-h-[150px]"
                                style={{ minHeight: '40px' }}
                            />
                            <button
                                type="submit"
                                disabled={!input.trim() || isLoading}
                                className={`p-2.5 rounded-xl flex items-center justify-center transition-all ${
                                    input.trim() && !isLoading 
                                        ? 'bg-accent-500 text-white hover:bg-accent-600 shadow-lg shadow-accent-500/20 cursor-pointer' 
                                        : 'bg-[#2A2A2A] text-gray-500 cursor-not-allowed'
                                }`}
                            >
                                {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                            </button>
                        </form>
                        <div className="text-center mt-3">
                            <span className="text-[10px] text-gray-500">
                                This AI assistant can make mistakes. Please consider verifying important medical advice.
                            </span>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default ChatInterface;