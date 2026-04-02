'use client';

import React from 'react';
import Link from 'next/link';
import { Heart, Shield, Brain, MessageCircle, ArrowRight } from 'lucide-react';

export default function LandingPage() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-calm-50 to-sage-50 dark:from-gray-900 dark:to-gray-800">
            {/* Hero Section */}
            <div className="relative overflow-hidden">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
                    <div className="text-center">
                        <div className="flex justify-center mb-8">
                            <div className="bg-calm-100 dark:bg-calm-900/50 rounded-full p-4">
                                <Heart className="w-12 h-12 text-calm-600 dark:text-calm-400" />
                            </div>
                        </div>

                        <h1 className="text-5xl md:text-7xl font-bold text-gray-900 dark:text-white mb-6">
                            Your Safe Space for
                            <span className="text-calm-600 dark:text-calm-400"> Emotional Support</span>
                        </h1>

                        <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
                            Anonymous, compassionate AI-powered conversations to help you navigate life's challenges.
                            Available 24/7, completely free.
                        </p>

                        <Link
                            href="/chat"
                            className="inline-flex items-center px-8 py-4 bg-calm-600 text-white rounded-full text-lg font-semibold hover:bg-calm-700 transition-all transform hover:scale-105 shadow-lg"
                        >
                            Start Anonymous Chat
                            <ArrowRight className="ml-2 w-5 h-5" />
                        </Link>
                    </div>
                </div>
            </div>

            {/* Features */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
                <div className="text-center mb-12">
                    <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                        How We Support You
                    </h2>
                    <p className="text-lg text-gray-600 dark:text-gray-300">
                        Advanced AI technology combined with human-like empathy
                    </p>
                </div>

                <div className="grid md:grid-cols-3 gap-8">
                    <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg">
                        <div className="bg-calm-100 dark:bg-calm-900/50 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                            <Brain className="w-6 h-6 text-calm-600" />
                        </div>
                        <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">
                            Emotion Detection
                        </h3>
                        <p className="text-gray-600 dark:text-gray-300">
                            Advanced AI understands your emotional state to provide personalized support
                        </p>
                    </div>

                    <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg">
                        <div className="bg-calm-100 dark:bg-calm-900/50 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                            <Shield className="w-6 h-6 text-calm-600" />
                        </div>
                        <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">
                            Complete Privacy
                        </h3>
                        <p className="text-gray-600 dark:text-gray-300">
                            100% anonymous conversations. No personal information ever required
                        </p>
                    </div>

                    <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg">
                        <div className="bg-calm-100 dark:bg-calm-900/50 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                            <MessageCircle className="w-6 h-6 text-calm-600" />
                        </div>
                        <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">
                            24/7 Availability
                        </h3>
                        <p className="text-gray-600 dark:text-gray-300">
                            Always here when you need someone to talk to, day or night
                        </p>
                    </div>
                </div>
            </div>

            {/* Footer */}
            <footer className="bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm border-t border-gray-200 dark:border-gray-700 py-8">
                <div className="max-w-7xl mx-auto px-4 text-center text-gray-600 dark:text-gray-400">
                    <p>© 2024 Emotional Support Assistant. Your privacy is our priority.</p>
                    <p className="text-sm mt-2">
                        If you're in crisis, please call 988 (Suicide and Crisis Lifeline) immediately.
                    </p>
                </div>
            </footer>
        </div>
    );
}