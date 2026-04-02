# 🧠 Emotional Support AI - Anonymous Mental Health Assistant

An advanced AI-powered emotional support system providing 24/7 anonymous, compassionate conversations to help users navigate life's challenges. Built with cutting-edge AI models and modern web technologies.

---

## 🌟 Features

- **AI-Powered Conversations**: Real-time emotional analysis and empathetic responses powered by Google Gemini, RoBERTa, and DialoGPT
- **Emotion Detection**: Advanced NLP to understand user emotions and feelings in real-time
- **Crisis Detection**: Intelligent crisis keyword detection with immediate resources and hotline recommendations
- **Mental Wellness Tools**:
  - 🎵 Music Suggestions (curated calming playlists)
  - 🌬️ Breathing Exercises (guided relaxation techniques)
  - 🧘 Mental Exercises (cognitive reframing & mindfulness)
  - 💡 Mood Insights (emotional pattern analysis)
  - 👨‍⚕️ Professional Help (connect with licensed therapists)
- **Anonymous & Confidential**: No user accounts or personal data collection required
- **Session Management**: Conversation history per session with emotion tracking
- **Rate Limiting**: Built-in API rate limiting to prevent abuse
- **Security**: XSS protection, CORS configuration, input sanitization

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Next.js)                       │
│  ├─ Chat Interface (React Components)                            │
│  ├─ Real-time Message Display                                    │
│  ├─ Feature Toggle UI (Music, Breathing, etc.)                   │
│  └─ Emotion Display & Analytics                                  │
└──────────────────────┬──────────────────────────────────────────┘
                       │ HTTPS/HTTP
┌──────────────────────▼──────────────────────────────────────────┐
│                     NGINX (Reverse Proxy)                        │
│  ├─ SSL/TLS Termination                                          │
│  ├─ Request Routing (frontend → port 3000, backend → port 5000)│
│  ├─ Rate Limiting                                                │
│  └─ Security Headers                                             │
└──────────────────────┬──────────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼──────────┐    ┌────────────▼────────┐
│  BACKEND (Flask) │    │  AUXILIARY SERVICES │
├──────────────────┤    ├─────────────────────┤
│ API Routes:      │    │ • PostgreSQL        │
│ • /api/chat      │    │ • Redis             │
│ • /api/analyze   │    │ • Hugging Face      │
│ • /api/health    │    │ • Google Gemini     │
│ • /api/crisis... │    │                     │
│                  │    │                     │
│ Services:        │    │                     │
│ • ChatService    │    │                     │
│ • Middleware     │    │                     │
│ • Error Handler  │    │                     │
└──────────────────┘    └─────────────────────┘
        │
        └─── ML Models ───┬──────────────────┐
                          │                  │
              ┌───────────▼──────┐  ┌──────▼─────────────┐
              │ Emotion Detector │  │ Empathy Refiner    │
              │ (RoBERTa)        │  │ (DialoGPT)         │
              │ - 27 emotions    │  │ - Enhanced empathy │
              │ - Intensity      │  │ - Better responses │
              └──────────────────┘  └────────────────────┘
                          │
              ┌───────────▴──────────┐
              │  Crisis Detector     │
              │  (Pattern Matching)  │
              │  - Hotline detect    │
              │  - Resources         │
              └──────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend

- **Next.js 14.0** - React framework with SSR & static generation
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Beautiful SVG icons
- **Axios** - HTTP client for API communication
- **Framer Motion** - Smooth animations
- **Chart.js** - Data visualization

### Backend

- **Flask 2.3** - Lightweight Python web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-Limiter** - Rate limiting
- **Transformers (Hugging Face)** - Pre-trained ML models
  - **RoBERTa** - Emotion detection (27 emotion classes)
  - **DialoGPT** - Empathetic dialogue generation
- **Google Gemini API** - Advanced LLM for response generation
- **PyTorch** - Deep learning framework
- **Pydantic** - Data validation
- **SQLAlchemy** - ORM for database operations

### Infrastructure

- **Docker & Docker Compose** - Containerization
- **PostgreSQL 15** - Relational database
- **Redis 7** - Session storage & caching
- **Nginx** - Reverse proxy & web server
- **Gunicorn** - WSGI HTTP server for Flask

---

## 📊 Data Flow

1. **User sends message** → Frontend (Next.js)
2. **Frontend sends to Flask API** → `/api/chat` endpoint
3. **Backend processes message**:
   - Emotion Detection (RoBERTa)
   - Crisis Detection (pattern matching)
   - Gemini API (generate initial response)
   - Empathy Refiner (DialoGPT enhancement)
4. **Response returned** with metadata:
   - Response text
   - Detected emotions
   - Crisis status
   - Session ID
5. **Frontend displays** in chat interface with emotion indicators

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git
- Linode account (for deployment) or local Docker installation

### Local Development

1. **Clone repository**

   ```bash
   git clone https://github.com/xyrenExo/ai-emotional-support.git
   cd ai-emotional-support
   ```

2. **Create `.env` file**

   ```bash
   cp .env.example .env
   # Edit .env with your Gemini API key
   ```

3. **Start containers**

   ```bash
   docker-compose up -d
   ```

4. **Access application**
   - Frontend: http://localhost:3000
   - API Health: http://localhost:5000/api/health

### Environment Variables

```env
# Required
GEMINI_API_KEY=your_api_key_here

# Optional (defaults provided)
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@postgres:5432/emotion_db
ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.com
FLASK_ENV=production
NODE_ENV=production
```

---

## 📡 API Endpoints

### Chat Endpoint

**POST** `/api/chat`

Request:

```json
{
  "message": "I'm feeling anxious about my presentation",
  "session_id": "uuid-optional",
  "features": {
    "music": true,
    "breathing": true,
    "mental": false,
    "insight": true,
    "professional_help": false
  }
}
```

Response:

```json
{
  "response": "I understand your anxiety about...",
  "emotion": {
    "primary_emotion": "nervousness",
    "intensity": 0.85,
    "is_negative": true,
    "all_emotions": {...}
  },
  "crisis": {
    "is_crisis": false,
    "high_risk": false,
    "severity": "none"
  },
  "session_id": "uuid"
}
```

### Emotion Analysis

**POST** `/api/analyze`

Request:

```json
{
  "message": "I feel sad today"
}
```

### Crisis Resources

**GET** `/api/crisis-resources`

Returns hotlines and mental health resources.

### Health Check

**GET** `/api/health`

---

## 🔧 Configuration

### Rate Limiting

- Default: 100 requests/day per IP
- Chat endpoint: 30 requests/minute
- Configurable in `backend/app/config.py`

### Database

- **PostgreSQL**: For persistent data (optional)
- **SQLite**: Default (development)

### Model Caching

- Models downloaded at build time
- Cached in `./backend/models` volume
- Supported by Docker layer caching

---

## 🌐 Deployment to Linode

1. **SSH into Linode server**

   ```bash
   ssh root@your-linode-ip
   ```

2. **Clone repository**

   ```bash
   git clone https://github.com/xyrenExo/ai-emotional-support.git
   cd ai-emotional-support
   ```

3. **Create `.env` with production values**

   ```bash
   nano .env
   ```

4. **Build & start**

   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

5. **Verify deployment**
   ```bash
   curl https://your-domain.com/api/health
   docker-compose ps
   docker-compose logs -f backend
   ```

### SSL/TLS Setup

- Place certificates in `./ssl/` directory:
  - `./ssl/cert.pem`
  - `./ssl/key.pem`
- Nginx automatically redirects HTTP → HTTPS

---

## 🐛 Troubleshooting

### Build fails with "dockerfile parse error"

- **Cause**: Git merge conflict markers in Dockerfile
- **Solution**: Run `git status` and resolve conflicts

### Chat not responding

- **Cause**: `GEMINI_API_KEY` not set or invalid
- **Solution**: Verify `.env` file has valid API key

### Database connection error

- **Cause**: PostgreSQL not running or credentials wrong
- **Solution**: Check `docker-compose logs postgres`

### Frontend can't reach backend

- **Cause**: CORS misconfiguration
- **Solution**: Verify `ALLOWED_ORIGINS` includes frontend hostname

### Models not downloading

- **Cause**: Internet timeout during Docker build
- **Solution**: Run `docker-compose build --no-cache` again

---

## 📈 Performance & Monitoring

### Metrics to Track

- Response time: `/api/chat` should return in < 5 seconds
- Error rate: Monitor HTTP 500 responses
- Model inference time: Logged in `docker-compose logs backend`
- Database query time: Optimizable with indexing

### Logs

```bash
# View all logs
docker-compose logs

# Follow backend logs
docker-compose logs -f backend

# Follow frontend logs
docker-compose logs -f frontend
```

---

## 🔒 Security Considerations

✅ **Implemented**

- HTTPS/TLS encryption
- CORS whitelisting
- Rate limiting (per IP)
- Input sanitization & validation
- XSS protection
- CSRF protection via session tokens
- Security headers (X-Frame-Options, X-Content-Type-Options)

⚠️ **To Implement (Production)**

- User authentication
- Database encryption at rest
- API key rotation
- Audit logging
- Penetration testing
- DDoS protection (Cloudflare, AWS Shield)

---

## 📚 File Structure

```
emotional-support-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes.py          # API endpoints
│   │   │   └── middleware.py      # Security & CORS
│   │   ├── models/
│   │   │   ├── emotion_model.py   # RoBERTa emotion detection
│   │   │   ├── crisis_detector.py # Crisis keyword detection
│   │   │   ├── gemini_client.py   # Gemini API wrapper
│   │   │   └── empathy_refiner.py # DialoGPT enhancement
│   │   ├── services/
│   │   │   ├── chat_service.py    # Main chat logic
│   │   │   └── analysis_service.py# Analytics
│   │   ├── __init__.py            # Flask app factory
│   │   └── config.py              # Configuration
│   ├── requirements.txt           # Python dependencies
│   ├── Dockerfile                 # Backend container
│   └── wsgi.py                    # Gunicorn entry point
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── chat/              # Chat page
│   │   │   └── layout.tsx         # Layout
│   │   ├── components/            # React components
│   │   ├── hooks/                 # Custom hooks
│   │   ├── lib/                   # Utilities
│   │   └── types/                 # TypeScript types
│   ├── package.json               # Node dependencies
│   ├── tsconfig.json              # TypeScript config
│   └── Dockerfile                 # Frontend container
├── nginx/
│   └── nginx.conf                 # Reverse proxy config
├── docker-compose.yml             # Container orchestration
├── .env.example                   # Environment template
└── README.md                       # This file
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## ⚖️ License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📞 Support & Resources

- **Suicide & Crisis Lifeline**: 988 (US)
- **Crisis Text Line**: Text HOME to 741741
- **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/

---

## 🎯 Future Roadmap

- [ ] User authentication & persistence
- [ ] Video/voice chat support
- [ ] Integration with calendars for therapy appointments
- [ ] AI-powered mood journaling
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Real therapist matchmaking
- [ ] Advanced analytics dashboard
- [ ] Offline mode support

---

**Built with ❤️ for mental health and well-being**

Last Updated: April 2026
