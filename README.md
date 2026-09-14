# ✨ AI Career Content Studio

An AI-powered content creation and research platform built with Python, Streamlit, Gemini, and the YouTube Data API.

## 🚀 Features

- ⚡ Intelligent Automated AI Generation (auto-optimizes for speed and reasoning with zero manual configuration)
- 🛡️ Resilient Model Fallback Cascade (automatically handles model routing and fallbacks silently behind the scenes)
- 🎬 Instagram Reels & Video Creator Studio (Reels scripts, YouTube Shorts / TikTok scripts, scene-by-scene B-roll & visual hooks)
- 🎯 Platform-specific content creation (LinkedIn Posts, Instagram Captions & Carousels, X / Twitter Threads, Newsletters, Blog Outlines)
- 💡 Creator-First Format (text blueprints with spoken script, visual cues, on-screen text, audio vibe, and filming inspiration)
- 🎨 Multiple writing tones (Professional, Casual, Friendly, Formal, Creative, Inspirational)
- 🎥 Real-time YouTube inspiration search
- 👤 Discover relevant creators and videos
- 🧠 AI-generated original content ideas
- 📊 Content research and analysis

## 🛠️ Tech Stack

- Python
- Streamlit
- Google GenAI API (with automated multi-model fallback cascade)
- YouTube Data API v3
- REST APIs
- python-dotenv

## 🏗️ Architecture

User → Streamlit UI → Gemini API / YouTube API → AI-generated insights

## 🔐 Environment Variables

Create a `.env` file:

GEMINI_API_KEY=your_gemini_api_key
YOUTUBE_API_KEY=your_youtube_api_key

API keys are kept private and are not committed to GitHub.

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py

🎯 Purpose

AI Career Content Studio helps students, creators, and young professionals research content trends and create original platform-ready content using Generative AI.