<<<<<<< HEAD
'use client';

import React from 'react';
import { Bot } from 'lucide-react';

const TypingIndicator: React.FC = () => {
    return (
        <div className="flex justify-start animate-in slide-in-from-bottom-2 duration-300">
            <div className="flex flex-row items-start space-x-2 max-w-[80%]">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 dark:bg-gray-600 flex items-center justify-center">
                    <Bot className="w-4 h-4 text-gray-700 dark:text-white" />
                </div>

                <div className="typing-indicator">
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                </div>
            </div>
        </div>
    );
};

=======
'use client';

import React from 'react';
import { Bot } from 'lucide-react';

const TypingIndicator: React.FC = () => {
    return (
        <div className="flex justify-start animate-in slide-in-from-bottom-2 duration-300">
            <div className="flex flex-row items-start space-x-2 max-w-[80%]">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 dark:bg-gray-600 flex items-center justify-center">
                    <Bot className="w-4 h-4 text-gray-700 dark:text-white" />
                </div>

                <div className="typing-indicator">
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                </div>
            </div>
        </div>
    );
};

>>>>>>> 6a97c5ff1caff98b22d3c35a1de0b0b2e5252662
export default TypingIndicator;