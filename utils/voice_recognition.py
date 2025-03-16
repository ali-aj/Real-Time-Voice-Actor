import whisper
import streamlit as st
import tempfile
import os
import torch
from pydub import AudioSegment
from deep_translator import GoogleTranslator
from gtts import gTTS
import io
import base64

# Constants for audio
CHANNELS = 1
RATE = 16000

# Add this after the existing constants
SUPPORTED_LANGUAGES = GoogleTranslator().get_supported_languages()

# Language mapping dictionary for gTTS
GTTS_LANGUAGE_MAP = {
    'afrikaans': 'af', 'arabic': 'ar', 'bengali': 'bn', 'bosnian': 'bs', 'catalan': 'ca',
    'czech': 'cs', 'danish': 'da', 'german': 'de', 'greek': 'el', 'english': 'en',
    'spanish': 'es', 'estonian': 'et', 'finnish': 'fi', 'french': 'fr', 'gujarati': 'gu',
    'hindi': 'hi', 'croatian': 'hr', 'hungarian': 'hu', 'indonesian': 'id', 'icelandic': 'is',
    'italian': 'it', 'hebrew': 'iw', 'japanese': 'ja', 'javanese': 'jw', 'khmer': 'km',
    'korean': 'ko', 'latin': 'la', 'latvian': 'lv', 'malayalam': 'ml', 'marathi': 'mr',
    'myanmar': 'my', 'nepali': 'ne', 'dutch': 'nl', 'norwegian': 'no', 'polish': 'pl',
    'portuguese': 'pt', 'romanian': 'ro', 'russian': 'ru', 'sinhala': 'si', 'slovak': 'sk',
    'albanian': 'sq', 'serbian': 'sr', 'sundanese': 'su', 'swedish': 'sv', 'swahili': 'sw',
    'tamil': 'ta', 'telugu': 'te', 'thai': 'th', 'filipino': 'tl', 'turkish': 'tr',
    'ukrainian': 'uk', 'urdu': 'ur', 'vietnamese': 'vi', 'chinese': 'zh'
}

def get_language_code(language):
    """Convert language name to ISO 639-1 code for gTTS"""
    language = language.lower()
    
    # If it's already a valid ISO code, return it
    if len(language) == 2:
        return language
        
    # Try to get from our mapping
    if language in GTTS_LANGUAGE_MAP:
        return GTTS_LANGUAGE_MAP[language]
    
    # Default to English if language not found
    st.warning(f"Language '{language}' not supported, falling back to English")
    return 'en'

def init_model():
    """Initialize the Whisper model with error handling"""
    try:
        # Check if CUDA is available and set the device accordingly
        device = "cuda" if torch.cuda.is_available() else "cpu"
        st.info(f"Using device: {device}")
        
        # Load the tiny model for better performance
        return whisper.load_model("tiny", device=device)
    except Exception as e:
        st.error(f"Error initializing Whisper model: {str(e)}")
        return None

@st.cache_resource
def get_whisper_model():
    """Get or create the Whisper model instance"""
    if 'whisper_model' not in st.session_state:
        st.session_state.whisper_model = init_model()
    return st.session_state.whisper_model

def transcribe_file(uploaded_file):
    """Transcribe an uploaded audio file with automatic language detection"""
    model = get_whisper_model()
    if model is None:
        st.error("Failed to load the transcription model. Please try again.")
        return None

    tmp_path = None
    wav_path = None
    try:
        # Get file extension
        file_ext = uploaded_file.name.split('.')[-1].lower()
        
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_ext}') as tmp_file:
            tmp_path = tmp_file.name
            tmp_file.write(uploaded_file.getvalue())
        
        # Convert to WAV if not already WAV format
        if file_ext != 'wav':
            wav_path = tmp_path.rsplit('.', 1)[0] + '.wav'
            audio = AudioSegment.from_file(tmp_path)
            audio.export(wav_path, format='wav')
            transcribe_path = wav_path
        else:
            transcribe_path = tmp_path
        
        # Transcribe with automatic language detection
        result = model.transcribe(
            transcribe_path,
            fp16=False  # Disable half-precision for better compatibility
        )
        
        # Display detected language
        detected_lang = result.get('language', 'unknown')
        st.info(f"Detected language: {detected_lang}")
        
        return result['text']
    except Exception as e:
        st.error(f"Error processing audio file: {str(e)}")
        return None
    finally:
        # Cleanup temporary files
        for path in [tmp_path, wav_path]:
            if path and os.path.exists(path):
                try:
                    os.unlink(path)
                except:
                    pass

def translate_text(text, target_language):
    """Translate text to target language"""
    try:
        translator = GoogleTranslator(source='auto', target=target_language)
        translated_text = translator.translate(text)
        return translated_text
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return None

def generate_speech(text, lang='en'):
    """Generate speech from text using gTTS"""
    try:
        # Get the correct language code
        lang_code = get_language_code(lang)
        
        # Create a bytes buffer for the audio
        audio_buffer = io.BytesIO()
        
        # Generate speech
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Convert to base64 for HTML audio player
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode()
        audio_html = f'<audio controls><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'
        
        return {
            'audio_html': audio_html,
            'audio_bytes': audio_buffer.getvalue()
        }
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None

def transcribe_and_translate(uploaded_file, target_language=None):
    """Transcribe an uploaded audio file, translate it, and generate speech"""
    transcribed_text = transcribe_file(uploaded_file)
    
    result = {
        'original': transcribed_text,
        'translated': None,
        'target_language': None,
        'original_speech': None,
        'translated_speech': None
    }
    
    if transcribed_text:
        # Generate speech for original text
        detected_lang = result.get('language', 'en')
        result['original_speech'] = generate_speech(transcribed_text, lang=detected_lang)
        
        if target_language and target_language != 'original':
            translated_text = translate_text(transcribed_text, target_language)
            if translated_text:
                result['translated'] = translated_text
                result['target_language'] = target_language
                # Generate speech for translated text
                result['translated_speech'] = generate_speech(translated_text, lang=target_language)
    
    return result