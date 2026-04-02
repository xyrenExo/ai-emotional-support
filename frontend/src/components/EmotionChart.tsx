'use client';

import React, { useEffect, useRef } from 'react';
import { Chart, registerables } from 'chart.js';
import { EmotionResult } from '@/types';

Chart.register(...registerables);

interface EmotionChartProps {
    emotionHistory: EmotionResult[];
}

const EmotionChart: React.FC<EmotionChartProps> = ({ emotionHistory }) => {
    const chartRef = useRef<HTMLCanvasElement>(null);
    const chartInstanceRef = useRef<Chart | null>(null);

    useEffect(() => {
        if (!chartRef.current || emotionHistory.length === 0) return;

        // Destroy existing chart
        if (chartInstanceRef.current) {
            chartInstanceRef.current.destroy();
        }

        const ctx = chartRef.current.getContext('2d');
        if (!ctx) return;

        // Prepare data
        const labels = emotionHistory.map((_, index) => `Msg ${index + 1}`);
        const intensityData = emotionHistory.map(e => e.intensity * 100);

        // Group emotions by type
        const positiveEmotions = ['joy', 'love', 'admiration', 'gratitude', 'excitement', 'optimism', 'approval', 'caring'];
        const negativeEmotions = ['sadness', 'anger', 'fear', 'anxiety', 'disappointment', 'grief', 'remorse', 'disgust'];

        const positiveCounts = emotionHistory.map(e =>
            positiveEmotions.includes(e.primary_emotion) ? 1 : 0
        );

        const negativeCounts = emotionHistory.map(e =>
            negativeEmotions.includes(e.primary_emotion) ? 1 : 0
        );

        // Create chart
        chartInstanceRef.current = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Emotional Intensity (%)',
                        data: intensityData,
                        borderColor: 'rgb(59, 130, 246)',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.3,
                        fill: true,
                        yAxisID: 'y',
                    },
                    {
                        label: 'Positive Emotions',
                        data: positiveCounts,
                        borderColor: 'rgb(34, 197, 94)',
                        backgroundColor: 'rgba(34, 197, 94, 0.1)',
                        borderWidth: 2,
                        pointRadius: 4,
                        pointHoverRadius: 6,
                        type: 'scatter',
                        yAxisID: 'y1',
                    },
                    {
                        label: 'Negative Emotions',
                        data: negativeCounts,
                        borderColor: 'rgb(239, 68, 68)',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        borderWidth: 2,
                        pointRadius: 4,
                        pointHoverRadius: 6,
                        type: 'scatter',
                        yAxisID: 'y1',
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            boxWidth: 10,
                        },
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    if (context.dataset.label === 'Emotional Intensity (%)') {
                                        label += `${context.parsed.y.toFixed(1)}%`;
                                    } else {
                                        label += context.parsed.y === 1 ? 'Yes' : 'No';
                                    }
                                }
                                return label;
                            },
                            afterBody: (context) => {
                                const dataIndex = context[0].dataIndex;
                                const emotion = emotionHistory[dataIndex];
                                return [`Emotion: ${emotion.primary_emotion}`];
                            },
                        },
                    },
                },
                scales: {
                    y: {
                        title: {
                            display: true,
                            text: 'Intensity (%)',
                        },
                        min: 0,
                        max: 100,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)',
                        },
                    },
                    y1: {
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Emotion Type',
                        },
                        min: -0.5,
                        max: 1.5,
                        ticks: {
                            stepSize: 1,
                            callback: (value) => {
                                if (value === 0) return 'Neutral';
                                if (value === 1) return 'Present';
                                return '';
                            },
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                    },
                },
            },
        });

        // Cleanup
        return () => {
            if (chartInstanceRef.current) {
                chartInstanceRef.current.destroy();
            }
        };
    }, [emotionHistory]);

    // Calculate statistics
    const getStatistics = () => {
        if (emotionHistory.length === 0) return null;

        const avgIntensity = emotionHistory.reduce((sum, e) => sum + e.intensity, 0) / emotionHistory.length;
        const negativeCount = emotionHistory.filter(e => e.is_negative).length;
        const positiveCount = emotionHistory.length - negativeCount;
        const mostCommonEmotion = emotionHistory
            .map(e => e.primary_emotion)
            .reduce((a, b, i, arr) =>
                arr.filter(v => v === a).length >= arr.filter(v => v === b).length ? a : b
            );

        return {
            avgIntensity: (avgIntensity * 100).toFixed(1),
            positivePercentage: ((positiveCount / emotionHistory.length) * 100).toFixed(1),
            negativePercentage: ((negativeCount / emotionHistory.length) * 100).toFixed(1),
            mostCommonEmotion,
            totalMessages: emotionHistory.length,
        };
    };

    const stats = getStatistics();

    return (
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
            <h3 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">
                Emotional Journey
            </h3>

            <div className="h-80 mb-6">
                <canvas ref={chartRef} />
            </div>

            {stats && (
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mt-4">
                    <div className="text-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                        <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                            {stats.avgIntensity}%
                        </div>
                        <div className="text-xs text-gray-600 dark:text-gray-400">Avg Intensity</div>
                    </div>

                    <div className="text-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                        <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                            {stats.positivePercentage}%
                        </div>
                        <div className="text-xs text-gray-600 dark:text-gray-400">Positive</div>
                    </div>

                    <div className="text-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                        <div className="text-2xl font-bold text-red-600 dark:text-red-400">
                            {stats.negativePercentage}%
                        </div>
                        <div className="text-xs text-gray-600 dark:text-gray-400">Negative</div>
                    </div>

                    <div className="text-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                        <div className="text-xl font-bold text-purple-600 dark:text-purple-400 capitalize">
                            {stats.mostCommonEmotion}
                        </div>
                        <div className="text-xs text-gray-600 dark:text-gray-400">Most Common</div>
                    </div>

                    <div className="text-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                        <div className="text-2xl font-bold text-gray-600 dark:text-gray-400">
                            {stats.totalMessages}
                        </div>
                        <div className="text-xs text-gray-600 dark:text-gray-400">Messages</div>
                    </div>
                </div>
            )}

            <div className="mt-4 text-sm text-gray-500 dark:text-gray-400 text-center">
                Chart shows your emotional intensity and patterns over time
            </div>
        </div>
    );
};

export default EmotionChart;