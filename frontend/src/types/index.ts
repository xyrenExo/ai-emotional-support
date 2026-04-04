export interface Message {
  id: string;
  content: string;
  role: "user" | "assistant";
  timestamp: Date;
  emotion?: EmotionResult;
  crisis?: CrisisResult;
}

export interface EmotionResult {
  primary_emotion: string;
  intensity: number;
  is_negative: boolean;
  all_emotions?: Record<string, number>;
}

export interface ChatResponse {
  response: string;
  emotion: EmotionResult;
  crisis: CrisisResult;
  session_id: string;
}

export interface CrisisResult {
  is_crisis: boolean;
  high_risk: boolean;
  severity: "none" | "medium" | "high";
  resources?: Record<string, string>;
}

export interface FeatureToggles {
  music: boolean;
  breathing: boolean;
  mental: boolean;
  insight: boolean;
  professional_help: boolean;
}

export interface ChatSession {
  id: string;
  messages: Message[];
  emotionHistory: EmotionResult[];
}
