"use client";

import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Send,
  Mic,
  Loader2,
  Menu,
  Plus,
  Search,
  MessageSquare,
  FolderOpen,
  MoreHorizontal,
  Bookmark,
  Share,
  Music,
  Wind,
  Brain,
  Lightbulb,
  Phone,
  Trash2,
  Pencil,
  X,
  Check,
  ChevronRight,
  Sparkles,
  User
} from "lucide-react";
import { useChat } from "@/hooks/useChat";
import MessageBubble from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";
import ProfessionalHelpModal from "./ProfessionalHelpModal";

const featureIcons: Record<string, React.ReactNode> = {
  music: <Music className="w-5 h-5 text-blue-400" />,
  breathing: <Wind className="w-5 h-5 text-teal-400" />,
  mental: <Brain className="w-5 h-5 text-purple-400" />,
  insight: <Lightbulb className="w-5 h-5 text-amber-400" />,
  professional_help: <Phone className="w-5 h-5 text-rose-500" />,
};

const featureDetails: Record<string, { title: string; desc: string; color: string }> = {
  music: {
    title: "Music Suggestions",
    desc: "Tailored calming music for your mood.",
    color: "from-blue-500/10 to-blue-600/5 border-blue-500/20"
  },
  breathing: {
    title: "Breathing Exercises",
    desc: "Guided routines to help you relax.",
    color: "from-teal-500/10 to-teal-600/5 border-teal-500/20"
  },
  mental: {
    title: "Mental Exercises",
    desc: "Cognitive reframing exercises.",
    color: "from-purple-500/10 to-purple-600/5 border-purple-500/20"
  },
  insight: {
    title: "Mood Insights",
    desc: "Analyze emotional patterns.",
    color: "from-amber-500/10 to-amber-600/5 border-amber-500/20"
  },
  professional_help: {
    title: "Professional Help",
    desc: "Connect with certified therapists.",
    color: "from-rose-500/10 to-rose-600/5 border-rose-500/20"
  },
};

const ChatInterface: React.FC = () => {
  const [input, setInput] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [showNewFolderInput, setShowNewFolderInput] = useState(false);
  const [newFolderName, setNewFolderName] = useState("");
  const [showProfessionalHelpModal, setShowProfessionalHelpModal] = useState(false);

  // Persistence states
  const [folders, setFolders] = useState<string[]>(["Stress Relief", "Daily Journals", "Therapy Notes"]);
  const [sessions, setSessions] = useState<any[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [selectedFolder, setSelectedFolder] = useState<string | null>(null);
  const [editingFolderAttr, setEditingFolderAttr] = useState<{ oldName: string, newName: string } | null>(null);

  const {
    messages,
    setMessages,
    isLoading,
    features,
    sendMessage,
    toggleFeature,
    clearChat,
    sessionId: hookSessionId
  } = useChat();

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const [isReady, setIsReady] = useState(false);

  // Load initial data from localStorage
  useEffect(() => {
    const savedFolders = localStorage.getItem("mindful_folders");
    const savedSessions = localStorage.getItem("mindful_sessions");

    if (savedFolders) setFolders(JSON.parse(savedFolders));
    if (savedSessions) {
      const parsedSessions = JSON.parse(savedSessions);
      setSessions(parsedSessions);
      if (parsedSessions.length > 0) {
        handleSelectSession(parsedSessions[0].id, parsedSessions);
      }
    }
    setIsReady(true);
  }, []);

  // Persist folders and sessions
  useEffect(() => {
    if (isReady) {
      localStorage.setItem("mindful_folders", JSON.stringify(folders));
    }
  }, [folders, isReady]);

  useEffect(() => {
    if (isReady) {
      localStorage.setItem("mindful_sessions", JSON.stringify(sessions));
    }
  }, [sessions, isReady]);

  // Sync current messages to active session in the list
  useEffect(() => {
    if (isReady && activeSessionId && messages.length > 0) {
      setSessions(prev =>
        prev.map(s => s.id === activeSessionId ? { ...s, messages, lastUpdated: new Date().toISOString() } : s)
      );
    }
  }, [messages, activeSessionId, isReady]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const message = input.trim();
    setInput("");

    // Create session if none active
    let currentId = activeSessionId;
    if (!currentId) {
      currentId = Date.now().toString();
      const newSession = {
        id: currentId,
        name: message.length > 30 ? message.slice(0, 30) + "..." : message,
        messages: [],
        folder: selectedFolder || "General",
        createdAt: new Date().toISOString(),
        lastUpdated: new Date().toISOString()
      };
      setSessions([newSession, ...sessions]);
      setActiveSessionId(currentId);
    }

    await sendMessage(message);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  const handleNewSession = () => {
    clearChat();
    setActiveSessionId(null);
  };

  const handleSelectSession = (id: string, currentSessions?: any[]) => {
    const list = currentSessions || sessions;
    const session = list.find(s => s.id === id);
    if (session) {
      setActiveSessionId(id);
      setMessages(session.messages || []);
    }
  };

  const handleNewFolder = () => {
    if (newFolderName.trim() && !folders.includes(newFolderName.trim())) {
      setFolders([...folders, newFolderName.trim()]);
    }
    setNewFolderName("");
    setShowNewFolderInput(false);
  };

  const handleDeleteFolder = (folderName: string) => {
    setFolders(folders.filter(f => f !== folderName));
    if (selectedFolder === folderName) setSelectedFolder(null);
  };

  const handleRenameFolder = () => {
    if (editingFolderAttr && editingFolderAttr.newName.trim() !== '' && editingFolderAttr.newName !== editingFolderAttr.oldName) {
      const newName = editingFolderAttr.newName.trim();
      const updated = folders.map(f => f === editingFolderAttr.oldName ? newName : f);
      setFolders(updated);

      setSessions(sessions.map(s => s.folder === editingFolderAttr.oldName ? { ...s, folder: newName } : s));

      if (selectedFolder === editingFolderAttr.oldName) {
        setSelectedFolder(newName);
      }
    }
    setEditingFolderAttr(null);
  };

  const handleDeleteSession = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setSessions(sessions.filter(s => s.id !== id));
    if (activeSessionId === id) handleNewSession();
  };

  const activeFeatures = Object.keys(features).filter((k) => features[k as keyof typeof features]);
  const filteredSessions = sessions.filter(s =>
    (!selectedFolder || s.folder === selectedFolder) &&
    (!searchQuery || s.name.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <div className="flex h-screen bg-[#030712] text-slate-200 overflow-hidden font-sans">
      {/* Sidebar */}
      <motion.div
        initial={false}
        animate={{ width: sidebarOpen ? 280 : 0, opacity: sidebarOpen ? 1 : 0 }}
        className="flex flex-col bg-slate-900/50 backdrop-blur-2xl border-r border-white/5 relative z-20"
      >
        <div className="p-6 flex flex-col h-full min-w-[280px]">
          {/* Sidebar Header */}
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-accent-500/20 rounded-lg flex items-center justify-center border border-accent-500/30">
                <Brain className="w-5 h-5 text-accent-400" />
              </div>
              <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
                AI-Counselling for Rysera
              </span>
            </div>
            <button onClick={toggleSidebar} className="p-2 hover:bg-white/5 rounded-lg transition-colors md:hidden">
              <ChevronRight className="w-5 h-5 text-slate-400" />
            </button>
          </div>

          <button
            onClick={handleNewSession}
            className="w-full flex items-center justify-center gap-2 bg-accent-600 hover:bg-accent-500 text-white py-3 rounded-xl text-sm font-bold transition-all shadow-lg shadow-accent-900/20 mb-6 group active:scale-95"
          >
            <Plus className="w-4 h-4 group-hover:rotate-90 transition-transform duration-300" />
            New Session
          </button>

          {/* Sidebar Search */}
          <div className="relative mb-6">
            <Search className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search conversations"
              className="w-full glass-input rounded-xl pl-10 pr-4 py-2.5 text-sm outline-none"
            />
          </div>

          {/* Sidebar Navigation */}
          <div className="flex-1 overflow-y-auto custom-scrollbar space-y-8 pr-2">
            <div>
              <div className="flex items-center justify-between px-2 mb-3">
                <h3 className="text-xs font-bold text-slate-500 uppercase tracking-[0.2em]">Folders</h3>
                <Plus onClick={() => setShowNewFolderInput(true)} className="w-4 h-4 cursor-pointer hover:text-white transition-colors" />
              </div>
              <div className="space-y-1">
                <div
                  onClick={() => setSelectedFolder(null)}
                  className={`group flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all cursor-pointer ${!selectedFolder ? 'bg-white/10' : 'hover:bg-white/5'}`}
                >
                  <FolderOpen className="w-4 h-4 text-accent-400" />
                  <span className="text-sm font-medium text-slate-200">All Folders</span>
                </div>
                {folders.map((folder) => (
                  <div
                    key={folder}
                    className={`group flex items-center justify-between px-3 py-2.5 rounded-xl transition-all cursor-pointer ${selectedFolder === folder ? 'bg-white/10 text-white' : 'hover:bg-white/5 text-slate-400 hover:text-slate-200'}`}
                  >
                    <div className="flex items-center gap-3 overflow-hidden flex-1" onClick={() => setSelectedFolder(folder)}>
                      <FolderOpen className="w-4 h-4 group-hover:text-accent-400 transition-colors flex-shrink-0" />
                      {editingFolderAttr?.oldName === folder ? (
                        <input
                          autoFocus
                          value={editingFolderAttr.newName}
                          onChange={(e) => setEditingFolderAttr({ ...editingFolderAttr, newName: e.target.value })}
                          onKeyDown={(e) => {
                            if (e.key === 'Enter') handleRenameFolder();
                            if (e.key === 'Escape') setEditingFolderAttr(null);
                          }}
                          onBlur={handleRenameFolder}
                          className="bg-transparent outline-none text-sm font-medium w-full text-white"
                        />
                      ) : (
                        <span className="text-sm font-medium truncate">
                          {folder}
                        </span>
                      )}
                    </div>

                    <div className="flex opacity-0 group-hover:opacity-100 transition-opacity gap-1.5 ml-2">
                      <Pencil className="w-3.5 h-3.5 hover:text-white" onClick={(e) => { e.stopPropagation(); setEditingFolderAttr({ oldName: folder, newName: folder }); }} />
                      <Trash2 className="w-3.5 h-3.5 hover:text-rose-500" onClick={(e) => { e.stopPropagation(); handleDeleteFolder(folder); }} />
                    </div>
                  </div>
                ))}

                {showNewFolderInput && (
                  <div className="group flex items-center gap-3 px-3 py-2.5 rounded-xl bg-white/5">
                    <FolderOpen className="w-4 h-4 text-accent-400" />
                    <input
                      autoFocus
                      value={newFolderName}
                      onChange={(e) => setNewFolderName(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') handleNewFolder();
                        if (e.key === 'Escape') setShowNewFolderInput(false);
                      }}
                      onBlur={handleNewFolder}
                      className="bg-transparent outline-none text-sm font-medium w-full text-white"
                      placeholder="Folder name..."
                    />
                  </div>
                )}
              </div>
            </div>

            <div>
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-[0.2em] px-2 mb-3">Recent Chats</h3>
              <div className="space-y-1">
                {filteredSessions.map((session) => (
                  <div
                    key={session.id}
                    onClick={() => handleSelectSession(session.id)}
                    className={`group flex items-center gap-3 px-3 py-3 rounded-xl transition-all cursor-pointer ${activeSessionId === session.id ? 'bg-accent-500/10 border border-accent-500/20' : 'hover:bg-white/5'}`}
                  >
                    <MessageSquare className={`w-4 h-4 ${activeSessionId === session.id ? 'text-accent-400' : 'text-slate-500Group-hover:text-accent-400'}`} />
                    <div className="flex-1 min-w-0">
                      <p className={`text-sm font-medium truncate ${activeSessionId === session.id ? 'text-white' : 'text-slate-300 group-hover:text-white'}`}>
                        {session.name}
                      </p>
                      <p className="text-[10px] text-slate-500 font-medium">
                        {new Date(session.lastUpdated).toLocaleDateString()}
                      </p>
                    </div>
                    <button
                      onClick={(e) => handleDeleteSession(session.id, e)}
                      className="opacity-0 group-hover:opacity-100 p-1 hover:text-rose-500 transition-all"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* User Section */}
          <div className="mt-auto pt-6 border-t border-white/5">
            <div className="flex items-center gap-3 p-2 rounded-xl hover:bg-white/5 transition-colors cursor-pointer">
              <div className="w-10 h-10 rounded-full bg-accent-500/10 flex items-center justify-center border border-accent-500/20">
                <User className="w-5 h-5 text-accent-400" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-bold text-white truncate">Guest User</p>
                <p className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Free Plan</p>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col relative h-full bg-zen-radial">
        {/* Top Navbar */}
        <header className="flex-shrink-0 h-20 flex items-center justify-between px-8 z-10 border-b border-white/[0.03] backdrop-blur-md">
          <div className="flex items-center gap-6">
            {!sidebarOpen && (
              <button onClick={toggleSidebar} className="p-2 hover:bg-white/5 rounded-lg text-slate-400 transition-all hover:scale-110">
                <Menu className="w-6 h-6" />
              </button>
            )}
            <div className="flex flex-col">
              <div className="flex items-center gap-2">
                <h1 className="text-base font-bold text-white tracking-wide">
                  {activeSessionId ? sessions.find(s => s.id === activeSessionId)?.name : 'New Secure Session'}
                </h1>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-black bg-accent-500/10 text-accent-400 border border-accent-500/20 uppercase tracking-widest">
                  End-to-End Encrypted
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-0.5">Your conversation is private and anonymous.</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex -space-x-2">
              {[1, 2, 3].map(i => (
                <div key={i} className="w-8 h-8 rounded-full border-2 border-[#030712] bg-slate-800 flex items-center justify-center overflow-hidden">
                  <img src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${i + 10}`} alt="avatar" />
                </div>
              ))}
            </div>
            <div className="w-px h-6 bg-white/[0.05]" />
            <button className="p-2.5 hover:bg-white/5 rounded-xl text-slate-400 transition-all">
              <Share className="w-5 h-5" />
            </button>
          </div>
        </header>

        {/* Messages Container */}
        <main className="flex-1 overflow-y-auto w-full custom-scrollbar scroll-smooth relative" style={{ minHeight: 0 }}>
          <AnimatePresence mode="wait">
            {messages.length === 0 ? (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="flex flex-col items-center justify-center min-h-full max-w-4xl mx-auto px-6 py-20"
              >
                <div className="relative mb-10">
                  <div className="absolute -inset-4 bg-accent-500/20 blur-3xl rounded-full" />
                  <div className="relative w-20 h-20 glass-panel rounded-3xl flex items-center justify-center shadow-2xl">
                    <Sparkles className="w-10 h-10 text-accent-400 animate-pulse" />
                  </div>
                </div>

                <h2 className="text-5xl font-black text-white mb-4 tracking-tight text-center">
                  Find your <span className="text-accent-400 italic">inner peace.</span>
                </h2>
                <p className="text-slate-400 text-lg mb-16 text-center max-w-2xl leading-relaxed">
                  I'm here to listen and help you navigate your emotions. Whether you want a deep conversation or specific mental tools, choose your path below.
                </p>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full">
                  {(Object.keys(featureDetails) as Array<keyof typeof features>).map((key) => (
                    <motion.div
                      key={key}
                      whileHover={{ y: -5, scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => {
                        if (key === "professional_help") setShowProfessionalHelpModal(true);
                        else toggleFeature(key);
                      }}
                      className={`p-6 rounded-3xl cursor-pointer border-2 transition-all duration-300 relative overflow-hidden group ${features[key]
                          ? "bg-accent-500/10 border-accent-500/40"
                          : "bg-white/[0.02] border-white/[0.05] hover:border-white/[0.1] hover:bg-white/[0.04]"
                        }`}
                    >
                      <div className="flex flex-col h-full relative z-10">
                        <div className={`w-12 h-12 rounded-2xl bg-white/[0.05] flex items-center justify-center mb-5 group-hover:scale-110 transition-transform ${features[key] ? 'bg-accent-500/20' : ''}`}>
                          {featureIcons[key]}
                        </div>
                        <h4 className={`text-lg font-bold mb-2 ${features[key] ? "text-accent-400" : "text-white"}`}>
                          {featureDetails[key].title}
                        </h4>
                        <p className="text-sm text-slate-500 font-medium leading-relaxed">
                          {featureDetails[key].desc}
                        </p>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            ) : (
              <div className="w-full max-w-4xl mx-auto space-y-2 py-10 px-6">
                {messages.map((message) => (
                  <MessageBubble key={message.id} message={message} />
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <TypingIndicator />
                  </div>
                )}
                <div ref={messagesEndRef} className="h-20" />
              </div>
            )}
          </AnimatePresence>
        </main>

        {/* Input Dock */}
        <div className="flex-shrink-0 p-8 pt-0">
          <div className="max-w-4xl mx-auto w-full relative">
            {/* Feature Toolbar */}
            <div className="absolute -top-12 left-0 flex items-center gap-2">
              {activeFeatures.map(feat => (
                <div key={feat} className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-accent-500/10 border border-accent-500/20 text-[10px] font-black text-accent-400 uppercase tracking-widest">
                  <Check className="w-3 h-3" />
                  {featureDetails[feat].title}
                </div>
              ))}
            </div>

            <form
              onSubmit={handleSubmit}
              className="glass-panel group rounded-[2.5rem] p-3 flex items-end gap-3 focus-within:ring-2 focus-within:ring-accent-500/30 transition-all shadow-2xl"
            >
              <div className="p-3">
                <Mic className="w-6 h-6 text-slate-500 hover:text-accent-400 cursor-pointer transition-colors" />
              </div>

              <textarea
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="What's on your mind? I'm here for you..."
                rows={1}
                className="flex-1 bg-transparent border-none text-white focus:outline-none focus:ring-0 resize-none px-2 py-4 text-lg font-medium placeholder-slate-600 max-h-[200px] overflow-y-auto custom-scrollbar"
              />

              <button
                type="submit"
                disabled={!input.trim() || isLoading}
                className={`w-14 h-14 rounded-[1.5rem] flex items-center justify-center transition-all flex-shrink-0 shadow-lg ${input.trim() && !isLoading
                    ? "bg-accent-500 text-white hover:bg-accent-400 translate-y-0 hover:-translate-y-1 active:scale-95"
                    : "bg-slate-800 text-slate-600 cursor-not-allowed"
                  }`}
              >
                {isLoading ? (
                  <Loader2 className="w-6 h-6 animate-spin" />
                ) : (
                  <Send className="w-6 h-6" />
                )}
              </button>
            </form>

            <div className="flex items-center justify-center gap-4 mt-6">
              <span className="text-[10px] font-black text-slate-600 uppercase tracking-[0.2em] flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                AI Model Active
              </span>
              <div className="w-1 h-1 rounded-full bg-slate-800" />
              <span className="text-[10px] font-black text-slate-600 uppercase tracking-[0.2em]">
                Data stays on your device
              </span>
            </div>
          </div>
        </div>
      </div>

      <ProfessionalHelpModal
        isOpen={showProfessionalHelpModal}
        onClose={() => setShowProfessionalHelpModal(false)}
      />
    </div>
  );
};

export default ChatInterface;
