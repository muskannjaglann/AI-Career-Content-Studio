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

# 4 Gemini models configured for generation and fallback
models_to_try = [
    "gemini-3.7-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.1-pro"
]

def generate_content_with_gemini(client, user_message, system_prompt=None, preferred_model=None):
    """
    Attempts to generate content using the 4 Gemini models.
    If preferred_model is specified, tries that first, then cascades through the rest.
    Uses genai.types.GenerateContentConfig with system_instruction.
    Returns (generated_text, model_used).
    """
    candidates = list(models_to_try)
    if preferred_model and preferred_model in candidates:
        candidates.remove(preferred_model)
        candidates.insert(0, preferred_model)

    config = None
    if system_prompt:
        config = genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
        )

    last_error = None
    for model_name in candidates:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_message,
                config=config
            )
            return response.text, model_name
        except Exception as e:
            print(f"Model {model_name} failed or timed out. Trying next... Error: {e}")
            last_error = e
            continue

    raise Exception(f"All 4 Gemini models failed or timed out. Last error: {last_error}")

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

st.sidebar.divider()
st.sidebar.subheader("🤖 Gemini Models (4)")

model_choice = st.sidebar.selectbox(
    "Select Model Strategy",
    ["Auto (Try all 4 models in order)"] + [f"Primary: {m}" for m in models_to_try],
    help="Choose your preferred model or use Auto to automatically cascade through all 4 models."
)

compare_mode = st.sidebar.checkbox(
    "🔀 Multi-Model Mode (Compare all 4 models)",
    value=False,
    help="Generate content using all 4 Gemini models side-by-side to compare outputs."
)

with st.sidebar.expander("ℹ️ 4 Models Configured"):
    st.markdown("""
    - **`gemini-3.7-flash`**: High-speed hybrid reasoning
    - **`gemini-3.5-flash-lite`**: Ultra-fast lightweight model
    - **`gemini-3.6-flash`**: Versatile & balanced generation
    - **`gemini-3.1-pro`**: Advanced complex reasoning
    """)

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

        # Determine preferred model if not Auto
        preferred_model = None
        if not model_choice.startswith("Auto"):
            preferred_model = model_choice.replace("Primary: ", "").strip()

        if compare_mode:
            st.info("Generating content across all 4 Gemini models...")
            model_tabs = st.tabs([f"🤖 {m}" for m in models_to_try])

            for idx, m_name in enumerate(models_to_try):
                with model_tabs[idx]:
                    with st.spinner(f"Generating with {m_name}..."):
                        try:
                            config = genai.types.GenerateContentConfig(
                                system_instruction=system_prompt,
                            )
                            resp = client.models.generate_content(
                                model=m_name,
                                contents=user_message,
                                config=config
                            )
                            c_text = resp.text
                            st.success(f"Generated with **{m_name}**")
                            st.text_area(
                                f"Output ({m_name})",
                                c_text,
                                height=350,
                                key=f"tab_content_{m_name}"
                            )
                            st.metric("Character Count", len(c_text))
                        except Exception as err:
                            st.warning(f"Model `{m_name}` unavailable: {err}")
        else:
            with st.spinner("✨ Creating your content..."):
                try:
                    generated_content, used_model = generate_content_with_gemini(
                        client,
                        user_message=user_message,
                        system_prompt=system_prompt,
                        preferred_model=preferred_model
                    )

                    st.success(f"Content generated successfully using **{used_model}**!")

                    if preferred_model and used_model != preferred_model:
                        st.info(f"ℹ️ Preferred model `{preferred_model}` was unavailable; smoothly fell back to `{used_model}`.")

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

                # Determine preferred model if not Auto
                target_model = None
                if not model_choice.startswith("Auto"):
                    target_model = model_choice.replace("Primary: ", "").strip()

                with st.spinner(
                    "🧠 Generating original content ideas..."
                ):
                    idea_text, idea_model = generate_content_with_gemini(
                        client,
                        user_message=user_message_ideas,
                        system_prompt=system_prompt_ideas,
                        preferred_model=target_model
                    )

                    st.caption(f"🤖 Ideas generated using: `{idea_model}`")
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
    f"✨ AI Career Content Studio | "
    f"Powered by 4 Gemini Models ({', '.join(models_to_try)}) + YouTube Data API"
)