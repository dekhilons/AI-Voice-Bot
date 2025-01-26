# AI Dental Receptionist Assistant

This project is an AI-powered receptionist assistant for a dental clinic. It listens to patient queries via voice input, transcribes them to text, generates responses using OpenAI's GPT-3.5-turbo, and replies using text-to-speech (TTS).

## Features
- **Real-Time Voice Input:** Records audio using `sounddevice`.
- **Transcription:** Converts speech to text using OpenAI's Whisper API.
- **AI-Powered Responses:** Leverages OpenAI's GPT-3.5-turbo for contextual, human-like replies.
- **Text-to-Speech Output:** Converts AI-generated text to voice using `gTTS` and plays it with `pygame`.
