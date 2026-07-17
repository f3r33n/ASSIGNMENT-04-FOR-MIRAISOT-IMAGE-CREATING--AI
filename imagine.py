from urllib.parse import quote
import random
import requests
import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="centered"
)

st.title("🎨 AI Image Studio")
st.write("Generate beautiful AI images using Pollinations AI.")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Settings")

magic_enhance = st.sidebar.checkbox(
    "✨ Enable Magic Enhance"
)

width = st.sidebar.slider(
    "Image Width",
    min_value=256,
    max_value=1024,
    value=512,
    step=64
)

height = st.sidebar.slider(
    "Image Height",
    min_value=256,
    max_value=1024,
    value=512,
    step=64
)

art_style = st.sidebar.selectbox(
    "🎨 Art Style",
    [
        "Realistic",
        "Anime",
        "Cyberpunk",
        "Fantasy",
        "Vinatge",
        "Digital Art"
    ]
)

# ---------------- SURPRISE PROMPTS ----------------
surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A floating city above the clouds",
    "A robot playing cricket on moon",
    "A dragon working in an office"
]

# ---------------- USER INPUT ----------------
prompt = st.text_input(
    "Describe the image you want to generate..." , value=None , placeholder = "Imagine here....."
)

col1, col2 = st.columns(2)

generate = col1.button("🎨 Generate Image")
surprise = col2.button("🎲 Surprise Me!")

# Surprise Button
if surprise: ## Added a Surprise Me button that randomly selects a creative  prompt using Python's random module and instantly generates an AI image.

    prompt = random.choice(surprise_prompts)
    st.info(f"🎲 Surprise Prompt: {prompt}")
    generate = True

# ---------------- IMAGE GENERATION ----------------
if generate:

    if not prompt:
        st.warning("⚠️ Please enter a prompt first.")
        st.stop()

    full_prompt = f"{prompt}, {art_style}"

    if magic_enhance:
        ## Added a Magic Enhance feature that automatically appends
        # descriptive keywords to the prompt, helping the AI generate
          # more detailed and higher-quality images.
        full_prompt += (
            ", masterpiece, 8k resolution,"
            " highly detailed,"
            " trending on artstation,"
            " unreal engine 5 render"
        )

    encoded_prompt = quote(full_prompt)

    url = (
        f"https://image.pollinations.ai/prompt/"
        f"{encoded_prompt}"
        f"?width={width}&height={height}" #We modified the image URL to include ?width={width}&height={height} so that thses 
        #values will get sent to poolination ai and it will create the image accordingly
    )

    with st.spinner("🎨 Creating your masterpiece..."):

        try:
            response = requests.get(url, timeout=60)

            if response.status_code == 200:

                st.success("✅ Image Generated Successfully!")

                st.image(
                    response.content,
                    caption=full_prompt,
                    use_container_width=True
                )

                st.download_button(
                    label="📥 Download Image",
                    data=response.content,
                    file_name=f"{art_style}_image.png", #here we made image to get downloaded as png and make it {art_style} as per what the user will type
                    # so if user creates anime image the image would get downloaded with name as anime image .png etc
                    mime="image/png"
                )

            else:
                st.error("❌ Failed to generate image.")

        except requests.exceptions.RequestException:
            st.error("❌ Network error. Please try again.")