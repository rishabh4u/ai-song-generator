import openai
import streamlit as st
import requests

# Set your OpenAI API key here
openai.api_key = st.secrets["openai_api_key"]  # We'll store this securely in Streamlit secrets

# Function to simulate melody generation
def generate_melody(lyrics, genre, mood):
    # This is a placeholder function for melody generation. You can replace this with an actual model.
    return "https://your-audio-file-url.com/sample.mp3"  # Replace with actual generated audio URL

# Streamlit UI setup
st.title("AI Song Generator")
st.write("Enter a prompt to generate a song with both lyrics and melody.")

# User input for song details
prompt = st.text_area("Enter your song idea or prompt here:", placeholder="Write a song about...")
genre = st.selectbox("Select Genre:", ["Pop", "Rock", "Jazz", "Hip-Hop", "Classical"])
mood = st.selectbox("Select Mood:", ["Happy", "Sad", "Energetic", "Calm", "Romantic"])

# Generate button
if st.button("Generate Song"):
    if prompt:
        # 1. Generate song lyrics using GPT-4
        try:
            lyrics_prompt = f"Write {genre} song lyrics that are {mood} based on: {prompt}"
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Specify GPT model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that writes song lyrics."},
                    {"role": "user", "content": lyrics_prompt}
                ]
            )
            lyrics = response['choices'][0]['message']['content'].strip()
            st.subheader(f"Generated {genre} Song Lyrics (Mood: {mood}):")
            st.text(lyrics)

            # 2. Simulate melody generation
            st.subheader("Generated Melody:")
            melody_url = generate_melody(lyrics, genre, mood)
            st.audio(melody_url, format="audio/mp3")

        except Exception as e:
            st.error(f"Error generating song: {str(e)}")
    else:
        st.warning("Please enter a song idea or prompt!")
