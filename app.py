import os
import requests
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ==========================================
# CONFIGURATION
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not GEMINI_API_KEY:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

if not YOUTUBE_API_KEY:
    st.error("YouTube API key not found. Check your .env file.")
    st.stop()

# Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Page configuration
st.set_page_config(
    page_title="AI Career Content Studio",
    page_icon="✨",
    layout="wide"
)

# ==========================================
# HEADER
st.title("✨ AI Career Content Studio")

st.write(
    "Create content with AI and discover real-world inspiration "
    "from YouTube creators."
)

st.divider()

# ==========================================
# SIDEBAR
st.sidebar.title("🎨 Content Studio")

content_type = st.sidebar.selectbox(
    "Content Type",
    [
        "LinkedIn Post",
        "Instagram Caption",
        "X / Twitter Post",
        "Professional Email",
        "Blog Outline"
    ]
)

tone = st.sidebar.selectbox(
    "Tone",
    [
        "Professional",
        "Casual",
        "Friendly",
        "Formal",
        "Creative",
        "Inspirational"
    ]
)

emoji_mode = st.sidebar.checkbox(
    "✨ Include Emojis"
)

# ==========================================
# TABS
create_tab, inspiration_tab = st.tabs(
    [
        "✨ Create Content",
        "🎥 YouTube Inspiration"
    ]
)

# ==========================================
# CREATE CONTENT TAB
with create_tab:

    st.header("✨ AI Content Generator")

    topic = st.text_input(
        "🎯 What do you want to create content about?",
        placeholder="Example: Personal growth for college students"
    )

    audience = st.text_input(
        "👥 Target Audience",
        placeholder="Example: College students and young professionals"
    )

    additional_instructions = st.text_area(
        "📝 Additional Instructions",
        placeholder="Example: Keep it engaging and end with a strong CTA."
    )

    if st.button("🚀 Generate Content", type="primary"):

        if not topic:
            st.warning("Please enter a topic first.")
            st.stop()

        audience_text = audience or "general professional audience"

        emoji_instruction = (
            "Use relevant emojis naturally."
            if emoji_mode
            else "Do not use emojis."
        )

        prompt = f"""
You are an expert professional content writer and career-branding
specialist.

Create a {content_type} about:

TOPIC:
{topic}

TARGET AUDIENCE:
{audience_text}

TONE:
{tone}

REQUIREMENTS:
- Make the content engaging and useful.
- Make it appropriate for the selected platform.
- Use clear and professional language.
- Avoid unnecessary repetition.
- {emoji_instruction}
- {additional_instructions}

Return ONLY the final content.
Do not explain your process.
"""

        with st.spinner("✨ Creating your content..."):

            try:

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                generated_content = response.text

                st.success("Content generated successfully!")

                st.subheader("📄 Generated Content")

                st.text_area(
                    "Your content",
                    generated_content,
                    height=350
                )

                st.metric(
                    "Character Count",
                    len(generated_content)
                )

            except Exception as e:

                st.error(
                    f"Something went wrong while generating content: {e}"
                )


# ==========================================
# YOUTUBE INSPIRATION TAB
with inspiration_tab:

    st.header("🎥 YouTube Inspiration Finder")

    st.write(
        "Discover real videos and creators related to your content topic."
    )

    search_topic = st.text_input(
        "🔎 What topic do you want inspiration for?",
        placeholder="Example: self improvement for young women"
    )

    number_of_videos = st.slider(
        "Number of videos",
        min_value=3,
        max_value=10,
        value=5
    )

    if st.button("🔎 Find Inspiration", type="primary"):

        if not search_topic:
            st.warning("Please enter a topic to search.")
            st.stop()

        with st.spinner("🎥 Finding relevant videos..."):

            try:

                youtube_url = (
                    "https://www.googleapis.com/youtube/v3/search"
                )

                params = {
                    "part": "snippet",
                    "q": search_topic,
                    "type": "video",
                    "maxResults": number_of_videos,
                    "order": "relevance",
                    "key": YOUTUBE_API_KEY
                }

                response = requests.get(
                    youtube_url,
                    params=params,
                    timeout=10
                )

                data = response.json()

                if response.status_code != 200:

                    st.error(
                        "YouTube API error: "
                        + str(data)
                    )
                    st.stop()

                videos = data.get("items", [])

                if not videos:

                    st.info(
                        "No videos found. Try another topic."
                    )
                    st.stop()

                st.success(
                    f"Found {len(videos)} relevant videos!"
                )

                # Save videos for AI analysis
                video_information = []

                # --------------------------------------
                # DISPLAY VIDEOS
                for video in videos:

                    video_id = video["id"]["videoId"]
                    snippet = video["snippet"]

                    title = snippet["title"]
                    channel = snippet["channelTitle"]
                    description = snippet.get(
                        "description",
                        ""
                    )
                    thumbnail = snippet["thumbnails"]["high"]["url"]

                    video_information.append(
                        f"""
Title: {title}
Channel: {channel}
Description: {description}
"""
                    )

                    st.image(
                        thumbnail,
                        width=320
                    )

                    st.subheader(title)

                    st.write(
                        f"👤 **Creator:** {channel}"
                    )

                    if description:
                        st.write(
                            description[:300] + "..."
                        )

                    st.video(
                        f"https://www.youtube.com/watch?v={video_id}"
                    )

                    st.divider()

                # --------------------------------------
                # AI CONTENT IDEAS
                st.header("💡 AI Content Ideas")

                combined_information = "\n".join(
                    video_information
                )

                idea_prompt = f"""
You are a content strategy expert.

The user wants to create content about:

{search_topic}

Here are real YouTube videos found for this topic:

{combined_information}

Based on the general themes and content angles,
generate 5 ORIGINAL content ideas.

For each idea provide:

1. Content title
2. Unique angle
3. Suggested platform
4. Suggested hook
5. Short explanation

IMPORTANT:
Do not copy or reproduce any creator's script.
Use the videos only as research inspiration.
Make every idea original.
"""

                with st.spinner(
                    "🧠 Generating original content ideas..."
                ):

                    idea_response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=idea_prompt
                    )

                    st.write(
                        idea_response.text
                    )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Could not connect to YouTube: {e}"
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# ==========================================
# FOOTER
st.divider()

st.caption(
    "✨ AI Career Content Studio | "
    "Powered by Gemini + YouTube Data API"
)