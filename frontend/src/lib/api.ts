import axios from 'axios';

const API_BASE_URL = typeof window !== 'undefined' 
    ? '/api' 
    : process.env.NEXT_PUBLIC_API_URL || 'http://backend:5000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface ChatRequest {
    message: string;
    session_id?: string;
    features: {
        music: boolean;
        breathing: boolean;
        mental: boolean;
        insight: boolean;
        professional_help: boolean;
    };
}

export const chatAPI = {
    sendMessage: async (data: ChatRequest) => {
        const response = await api.post('/chat', data);
        return response.data;
    },

    analyzeEmotion: async (message: string) => {
        const response = await api.post('/analyze', { message });
        return response.data;
    },

    getCrisisResources: async () => {
        const response = await api.get('/crisis-resources');
        return response.data;
    },

    healthCheck: async () => {
        const response = await api.get('/health');
        return response.data;
    },
};