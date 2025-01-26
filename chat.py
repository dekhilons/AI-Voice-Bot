import openai
from gtts import gTTS
import os
import sounddevice as sd
import numpy as np
import wave
from pygame import mixer

class AI_Assistant:
    def __init__(self):
        # Initialize OpenAI API key
        self.openai_api_key = ""  # Replace with your OpenAI API key
        self.client = openai.OpenAI(api_key=self.openai_api_key)

        # Prompt
        self.full_transcript = [
            {"role": "system", "content": "You are a receptionist at a dental clinic. Be resourceful and efficient."},
        ]

    ###### Step 2: Real-Time Transcription with sounddevice ######
    def start_transcription(self):
        print("Listening...")
        sample_rate = 16000  # Sample rate in Hz
        duration = 5  # Duration of recording in seconds

        while True:
            print("Speak now...")
            try:
                # Record audio
                audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
                sd.wait()  # Wait for the recording to finish

                # Save the audio to a file
                with wave.open("audio.wav", "wb") as f:
                    f.setnchannels(1)
                    f.setsampwidth(2)  # 2 bytes for int16
                    f.setframerate(sample_rate)
                    f.writeframes(audio.tobytes())

                # Transcribe using Whisper API
                transcript = self.transcribe_with_whisper("audio.wav")
                print(f"Patient: {transcript}")
                self.generate_ai_response(transcript)
            except Exception as e:
                print(f"An error occurred: {e}")

    def transcribe_with_whisper(self, audio_file):
        with open(audio_file, "rb") as f:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        return response.text

    ###### Step 3: Pass transcript to ChatGPT API ######
    def generate_ai_response(self, transcript):
        self.full_transcript.append({"role": "user", "content": transcript})

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.full_transcript
        )

        ai_response = response.choices[0].message.content
        self.generate_audio(ai_response)

    ###### Step 4: Generate audio with gTTS and pygame ######
    def generate_audio(self, text):
        self.full_transcript.append({"role": "assistant", "content": text})
        print(f"AI Receptionist: {text}")

        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")

        # Initialize pygame mixer
        mixer.init()
        mixer.music.load("response.mp3")
        mixer.music.play()

        # Wait for the audio to finish playing
        while mixer.music.get_busy():
            continue

# Greeting
greeting = "Thank you for calling Vancouver dental clinic. My name is Sandy, how may I assist you?"
ai_assistant = AI_Assistant()
ai_assistant.generate_audio(greeting)
ai_assistant.start_transcription()