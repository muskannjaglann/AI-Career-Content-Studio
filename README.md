# ✨ AI Career Content Studio

An AI-powered content creation and research platform built with Python, Streamlit, Gemini, and the YouTube Data API.

## 🚀 Features

- 🤖 Multi-Model AI Generation (4 Gemini Models: `gemini-3.7-flash`, `gemini-3.5-flash-lite`, `gemini-3.6-flash`, `gemini-3.1-pro`)
- 🔀 Multi-Model Comparison Studio (generate variations across all 4 models side-by-side)
- 🛡️ Resilient Model Fallback Cascade (automatically tries alternative models if one is rate-limited or unavailable)
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
- Google Gemini API (Multi-Model: Gemini 3.7 Flash, 3.5 Flash-Lite, 3.6 Flash, 3.1 Pro)
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