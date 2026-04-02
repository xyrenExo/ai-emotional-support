<<<<<<< HEAD
'use client';

import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Message } from '@/types';
import { User, Bot } from 'lucide-react';

interface MessageBubbleProps {
    message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
    const isUser = message.role === 'user';

    return (
        <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-in slide-in-from-bottom-2 duration-300`}>
            <div className={`flex ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start space-x-2 max-w-[80%]`}>
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${isUser ? 'bg-calm-500' : 'bg-gray-300 dark:bg-gray-600'
                    }`}>
                    {isUser ? (
                        <User className="w-4 h-4 text-white" />
                    ) : (
                        <Bot className="w-4 h-4 text-gray-700 dark:text-white" />
                    )}
                </div>

                <div className={isUser ? 'chat-message-user' : 'chat-message-assistant'}>
                    <ReactMarkdown className="prose dark:prose-invert max-w-none">
                        {message.content}
                    </ReactMarkdown>

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

=======
'use client';

import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Message } from '@/types';
import { User, Bot } from 'lucide-react';

interface MessageBubbleProps {
    message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
    const isUser = message.role === 'user';

    return (
        <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-in slide-in-from-bottom-2 duration-300`}>
            <div className={`flex ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start space-x-2 max-w-[80%]`}>
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${isUser ? 'bg-calm-500' : 'bg-gray-300 dark:bg-gray-600'
                    }`}>
                    {isUser ? (
                        <User className="w-4 h-4 text-white" />
                    ) : (
                        <Bot className="w-4 h-4 text-gray-700 dark:text-white" />
                    )}
                </div>

                <div className={isUser ? 'chat-message-user' : 'chat-message-assistant'}>
                    <ReactMarkdown className="prose dark:prose-invert max-w-none">
                        {message.content}
                    </ReactMarkdown>

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

>>>>>>> 6a97c5ff1caff98b22d3c35a1de0b0b2e5252662
export default MessageBubble;