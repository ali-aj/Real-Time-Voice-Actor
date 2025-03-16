# Real-Time Voice Actor 🎙️

A Streamlit-based web application that transcribes audio files, translates the content, and generates speech in multiple languages.

## Features

- 🎯 Audio transcription using OpenAI's Whisper model
- 🌍 Support for multiple languages
- 🔄 Real-time translation using Google Translate
- 🗣️ Text-to-speech conversion
- 📥 Download options for transcriptions and audio files
- 💻 CUDA support for faster processing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ali-aj/Real-Time-Voice-Actor.git
cd Real-Time-Voice-Actor
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

3. Upload an audio file (supported formats: WAV, MP3, M4A, AAC, OGG, WMA, FLAC, ALAC, AIFF, OPUS)

4. Optionally select a target language for translation

5. Click "Transcribe" to process the audio

## Supported Features

- **Audio Input**: Multiple audio format support
- **Transcription**: Automatic language detection and transcription
- **Translation**: Support for 50+ languages
- **Text-to-Speech**: Generate audio for both original and translated text
- **Download Options**: Save transcriptions and generated audio files

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── requirements.txt    # Project dependencies
└── utils/
    └── voice_recognition.py  # Core functionality
```

## Acknowledgments

- OpenAI Whisper for speech recognition
- Google Translate for translation services
- gTTS (Google Text-to-Speech) for speech synthesis
- Streamlit for the web interface