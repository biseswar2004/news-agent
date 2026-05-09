# 🎙️ The News Agent

> An AI-powered personalised morning news briefing agent that automatically fetches news, generates a spoken script, converts it to audio, and delivers it to your Telegram every morning — completely free.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20App-black?style=flat-square&logo=flask)
![Gemini](https://img.shields.io/badge/Gemini-AI-teal?style=flat-square&logo=google)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

# 📸 Preview

> Dashboard · History · Settings · Logs — all in one clean web interface.

---

# ✨ Features

- 📡 Fetches news from multiple sources — BBC, TechCrunch, Times of India, NDTV, The Verge
- 🧹 Removes duplicate stories using semantic similarity
- 🤖 AI generates personalised spoken scripts using Gemini AI
- 🎙️ Converts scripts into natural voice MP3 audio
- 📲 Sends briefing directly to Telegram
- 🖥️ Clean Flask web dashboard
- 🗄️ SQLite database for storing briefings and logs
- ⏰ Automatic daily scheduling
- 💰 Completely free to run

---

# 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Backend | Flask |
| Frontend | HTML + CSS + JavaScript |
| Database | SQLite + SQLAlchemy |
| AI Model | Google Gemini 1.5 Flash |
| Backup AI | Groq + Llama 3 |
| News Sources | RSS Feeds + NewsAPI |
| Text to Speech | gTTS |
| Messaging | Telegram Bot API |
| Scheduler | APScheduler |
| Deployment | Render.com |

---

# 🎙️ The News Agent

> AI-powered personalised morning news briefing agent.

---

# 📁 Project Structure

```text
news-agent/
├── app.py              # Flask web server — all routes
├── main.py             # Master pipeline runner
├── scraper.py          # Fetches news from RSS + NewsAPI
├── summariser.py       # Gemini/Groq AI script generator
├── tts.py              # Text to speech MP3 converter
├── delivery.py         # Telegram bot delivery
├── scheduler.py        # Daily 7AM auto-scheduler
├── database.py         # SQLite database models + queries
├── templates/          # HTML pages
│   ├── base.html       # Shared layout + navbar + footer
│   ├── index.html      # Dashboard — today's briefing
│   ├── history.html    # All past briefings
│   ├── settings.html   # User preferences
│   └── logs.html       # Agent run logs
├── static/
│   ├── css/style.css   # Full dashboard styling
│   └── js/main.js      # JavaScript — run, save, copy
├── audio/              # Generated MP3 files
├── .env                # API keys (never upload this)
├── requirements.txt    # Python dependencies
└── Procfile            # Render deployment config
```

---

# 🚀 How to Run Locally

## Step 1 -- Clone the repository

```bash
git clone https://github.com/biseswar2004/news-agent.git
cd news-agent
```

---

## Step 2 -- Create virtual environment

```bash
python -m venv venv
```

---

## Step 3 -- Activate virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Step 4 -- Install dependencies

```bash
pip install -r requirements.txt
```

---

## Step 5 -- Create `.env` file

```env
GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
NEWS_API_KEY=your_newsapi_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
YOUR_NAME=Your Name
YOUR_TOPICS=AI,cricket,India tech,startups
```

---

## Step 6 -- Run the Flask app

```bash
python app.py
```

Open in browser:

```text
http://localhost:5000
```

---

## Step 7 -- Run full pipeline manually

```bash
python main.py
```

---

## Step 8 -- Run scheduler

```bash
python scheduler.py
```

---

# 🔑 Free API Keys

| Service | Website |
|---|---|
| Gemini AI | https://aistudio.google.com |
| Groq | https://console.groq.com |
| NewsAPI | https://newsapi.org |
| Telegram Bot | https://telegram.me/BotFather |

---

# 🧠 How It Works

```text
Scheduler starts automatically
        ↓
Fetches news from multiple sources
        ↓
Duplicate articles removed
        ↓
Gemini AI creates spoken script
        ↓
gTTS converts script to MP3
        ↓
Telegram bot sends briefing
        ↓
User receives morning news audio
```

---

# 💡 Key Technical Concepts Used

- API Integration — Gemini, Groq, NewsAPI, Telegram Bot API
- NLP / Embeddings — semantic deduplication
- LLM Prompting — structured prompt engineering
- Task Scheduling — APScheduler cron jobs
- Database Design — SQLite with SQLAlchemy ORM
- Fallback Architecture — Gemini → Groq → basic script
- Full Stack Web App — Flask backend + HTML/CSS/JS frontend

---

# 👤 Author

## Biseswar Mohapatra
