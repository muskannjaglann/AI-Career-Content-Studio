import os
import requests
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ==========================================
# CONFIGURATIONssssss
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

# Automatic model cascade prioritizing the most reliable and capable models
MODELS_CASCADE = [
    "gemini-3.6-flash",
    "gemini-flash-latest",
    "gemini-3.5-flash-lite",
    "gemini-3.7-flash",
    "gemini-3.8-flash",
]

def generate_content(client, user_message, system_prompt=None):
    """
    Automatically generates content using the best working AI model.
    Cascades silently to backup models if a model experiences temporary spikes or downtime,
    ensuring zero disruption to the user.
    """
    config = None
    if system_prompt:
        config = genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
        )

    last_error = None
    for model_name in MODELS_CASCADE:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_message,
                config=config
            )
            if response and response.text:
                return response.text
        except Exception as e:
            # Silently log for server debugging and cascade to next model
            print(f"Model cascade fallback from {model_name}: {e}")
            last_error = e
            continue

    raise Exception(f"AI service temporarily unavailable. Please try again shortly. (Details: {last_error})")

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
    "Create high-impact posts, viral Instagram Reels & video scripts with AI, "
    "and discover real-world inspiration from creators."
)

st.divider()

# ==========================================
# SIDEBAR
st.sidebar.title("🎨 Content Studio")

content_type = st.sidebar.selectbox(
    "Content Type",
    [
        "Instagram Reel / Video Script",
        "YouTube Shorts / TikTok Script",
        "YouTube Video Concept & Outline",
        "LinkedIn Post",
        "Instagram Caption & Carousel",
        "X / Twitter Post / Thread",
        "Professional Email / Newsletter",
        "Blog Outline / Article"
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
        placeholder="Example: 3 Career mistakes in your 20s (Reel) or How to network (LinkedIn)"
    )

    audience = st.text_input(
        "👥 Target Audience",
        placeholder="Example: College students, young creators, job seekers"
    )

    additional_instructions = st.text_area(
        "📝 Additional Instructions",
        placeholder="Example: 30-45s fast pace, hook in first 3s, suggest B-roll & on-screen text."
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

        is_video_content = any(
            k in content_type.lower()
            for k in ["reel", "video", "shorts", "tiktok"]
        )

        if is_video_content:
            system_prompt = (
                "You are an expert viral video strategist, creative director, and scriptwriter. "
                "Craft a high-retention video script and creator blueprint formatted clearly so "
                "content creators can read it, perform it, and get inspired to film. "
                "Return ONLY the final structured creative script. Do not explain your process."
            )
            format_guide = """
- FORMAT FOR VIDEO/REEL CREATORS:
  1. 🎬 Hook & Opening Scene (First 3-5s: exact words to say + visual action / on-screen hook)
  2. 🎥 Scene-by-Scene Script (Spoken voiceover + visual directions / B-roll suggestions + text overlays)
  3. 🎯 Strong Call-to-Action (CTA) (Closing line to drive follows, saves, or shares)
  4. 💡 Creator Inspiration & Filming Notes (Pacing, music/audio vibe, camera angle, caption idea)
"""
        else:
            system_prompt = (
                "You are an expert professional content writer, digital creator, and career-branding specialist. "
                "Return ONLY the final engaging content. Do not explain your process."
            )
            format_guide = "- Make it platform-native, engaging, and directly ready to publish or inspire the creator."

        user_message = f"""Create a {content_type} about:

TOPIC:
{topic}

TARGET AUDIENCE:
{audience_text}

TONE:
{tone}

REQUIREMENTS:
- Make the content engaging, actionable, and inspiring for the creator.
- Tailor specifically to the format and pacing of {content_type}.
{format_guide}
- Use clear and compelling language.
- Avoid unnecessary repetition or generic filler.
- {emoji_instruction}
- {additional_instructions}"""

        with st.spinner("✨ Creating your content..."):
            try:
                generated_content = generate_content(
                    client,
                    user_message=user_message,
                    system_prompt=system_prompt,
                )

                st.success("✨ Content generated successfully!")

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

                system_prompt_ideas = (
                    "You are a content strategy expert. "
                    "Do not copy or reproduce any creator's script. "
                    "Use the videos only as research inspiration. Make every idea original."
                )

                user_message_ideas = f"""The user wants to create content about:

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
5. Short explanation"""

                with st.spinner(
                    "🧠 Generating original content ideas..."
                ):
                    idea_text = generate_content(
                        client,
                        user_message=user_message_ideas,
                        system_prompt=system_prompt_ideas,
                    )

                    st.markdown("### 💡 Strategic Content Ideas")
                    st.write(idea_text)

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
    "Powered by Content Studio AI Engine & YouTube Data API"
)