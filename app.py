import openai
import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
import requests  # Add this line to import requests
import os

# Set your OpenAI API key here
openai.api_key = st.secrets["openai_api_key"]  # Securely stored in Streamlit secrets

# Function to simulate melody generation (static audio file for now)
def generate_melody():
    return "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"  # Static melody URL

# Function to convert lyrics into speech using gTTS (Google Text-to-Speech)
def lyrics_to_speech(lyrics, file_name="lyrics.mp3"):
    tts = gTTS(lyrics)
    tts.save(file_name)
    return file_name

# Function to mix lyrics audio with melody using pydub
def mix_lyrics_and_melody(lyrics_audio_file, melody_audio_file, output_file="final_song.mp3"):
    # Load the lyrics and melody audio files
    lyrics_sound = AudioSegment.from_file(lyrics_audio_file)
    melody_sound = AudioSegment.from_file(melody_audio_file)

    # Overlay the lyrics onto the melody
    combined = melody_sound.overlay(lyrics_sound, position=0)

    # Export the combined audio file
    combined.export(output_file, format="mp3")
    return output_file

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
        # 1. Generate song lyrics using GPT-3.5 Turbo (updated API)
        try:
            lyrics_prompt = f"Write {genre} song lyrics that are {mood} based on: {prompt}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that writes song lyrics."},
                    {"role": "user", "content": lyrics_prompt}
                ]
            )
            lyrics = response['choices'][0]['message']['content'].strip()
            st.subheader(f"Generated {genre} Song Lyrics (Mood: {mood}):")
            st.text(lyrics)

            # 2. Convert the lyrics to speech using gTTS
            lyrics_audio_file = "lyrics.mp3"
            lyrics_to_speech(lyrics, lyrics_audio_file)

            # 3. Simulate melody generation (using a static URL)
            st.subheader("Generated Melody:")
            melody_url = generate_melody()

            # Download the melody audio locally (so it can be combined)
            melody_audio_file = "melody.mp3"
            melody_response = requests.get(melody_url)
            with open(melody_audio_file, "wb") as f:
                f.write(melody_response.content)

            # 4. Combine the lyrics and melody into a final song
            final_song_file = mix_lyrics_and_melody(lyrics_audio_file, melody_audio_file)

            # 5. Play the final combined song
            st.subheader("Final Song:")
            st.audio(final_song_file)

        except Exception as e:
            st.error(f"Error generating song: {str(e)}")
    else:
        st.warning("Please enter a song idea or prompt!")
