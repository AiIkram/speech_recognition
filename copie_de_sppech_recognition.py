# -*- coding: utf-8 -*-
"""Copie de Sppech recognition.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1w-1kwxDSFymPD45KV1ufK6_HBEjgyyxo
"""
import streamlit as st
import subprocess
import os
import speech_recognition as sr

def convert_to_wav(input_path, output_path):
    """Convert audio to WAV format using ffmpeg."""
    try:
        subprocess.run(
            ["ffmpeg", "-i", input_path, "-ar", "16000", "-ac", "1", output_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return output_path
    except Exception as e:
        return None

def transcribe_speech_from_file(file_path):
    # Convert audio to WAV format
    wav_path = f"{os.path.splitext(file_path)[0]}.wav"
    converted_path = convert_to_wav(file_path, wav_path)

    if not converted_path:
        return "Error: Failed to convert audio file to WAV format."

    # Initialize recognizer
    r = sr.Recognizer()
    try:
        with sr.AudioFile(converted_path) as source:
            audio = r.record(source)  # Read the entire audio file
        return r.recognize_google(audio)
    except Exception as e:
        return f"Error during transcription: {str(e)}"


def main():
    st.title("Speech Recognition App")
    uploaded_file = st.file_uploader("Upload an audio file (MP3, WAV, etc.)", type=["wav", "flac", "mp3", "aac"])
    
    if uploaded_file is not None:
        st.info("Processing uploaded audio file...")
        file_path = f"/tmp/{uploaded_file.name}"
        
        # Save uploaded file to temp directory
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Transcribe the uploaded file
        text = transcribe_speech_from_file(file_path)
        st.write("Transcription:", text)

if __name__ == "__main__":
    main()


