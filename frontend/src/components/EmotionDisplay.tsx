'use client';

import React from 'react';
import { EmotionResult } from '@/types';
import { Smile, Frown, Meh, Heart, Zap } from 'lucide-react';

interface EmotionDisplayProps {
    emotion: EmotionResult;
}

const EmotionDisplay: React.FC<EmotionDisplayProps> = ({ emotion }) => {
    const getEmotionIcon = () => {
        const primary = emotion.primary_emotion;
        if (['joy', 'love', 'admiration', 'gratitude', 'excitement', 'optimism'].includes(primary)) {
            return <Heart className="w-4 h-4 text-red-500" />;
        }
        if (['sadness', 'grief', 'disappointment', 'remorse'].includes(primary)) {
            return <Frown className="w-4 h-4 text-blue-500" />;
        }
        if (['anger', 'annoyance', 'disgust', 'disapproval'].includes(primary)) {
            return <Zap className="w-4 h-4 text-orange-500" />;
        }
        return <Meh className="w-4 h-4 text-gray-500" />;
    };

    const getEmotionColor = () => {
        const intensity = emotion.intensity;
        if (intensity > 0.7) return 'bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-200';
        if (intensity > 0.4) return 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-800 dark:text-yellow-200';
        return 'bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-200';
    };

    return (
        <div className={`flex items-center space-x-2 px-3 py-1 rounded-full ${getEmotionColor()}`}>
            {getEmotionIcon()}
            <span className="text-sm font-medium capitalize">
                {emotion.primary_emotion}
            </span>
            <span className="text-xs">
                {(emotion.intensity * 100).toFixed(0)}%
            </span>
        </div>
    );
};

export default EmotionDisplay;