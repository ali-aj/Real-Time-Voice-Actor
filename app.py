import streamlit as st
st.set_page_config(page_title="Real Time Voice Actor", layout="wide", initial_sidebar_state="expanded")

from datetime import datetime
from utils.voice_recognition import transcribe_and_translate, SUPPORTED_LANGUAGES

# Sidebar
with st.sidebar:
    st.title("🎙️ Real Time Voice Actor")
    st.markdown("---")
    st.info("Upload audio files to get transcriptions.")

# Main content
st.header("Upload Audio File")

uploaded_file = st.file_uploader("Choose an audio file", type=['wav', 'mp3', 'm4a', 'aac', 'ogg', 'wma', 'flac', 'alac', 'aiff', 'opus'])
note_title = st.text_input("Note Title (optional)", key="upload_title")
target_language = st.selectbox(
    "Select translation language (optional)", 
    ['original'] + SUPPORTED_LANGUAGES,
    index=0
)

if uploaded_file:
    file_details = {
        "Filename": uploaded_file.name,
        "FileType": uploaded_file.type,
        "FileSize": f"{uploaded_file.size / 1024:.2f} KB"
    }
    st.write("File Details:", file_details)
    
    if st.button("Transcribe", key="transcribe_btn"):
        try:
            with st.spinner("Transcribing and translating..."):
                result = transcribe_and_translate(uploaded_file, target_language)
                
                if result['original']:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    note_data = {
                        "title": note_title or uploaded_file.name,
                        "text": result['original'],
                        "timestamp": timestamp
                    }
                    st.success("Processing completed!")
                    
                    # Display results in an expandable section
                    with st.expander("View Results", expanded=True):
                        # Original content
                        st.markdown("### Original Transcription")
                        st.write(result['original'])
                        if result['original_speech']:
                            st.markdown("#### Listen")
                            st.markdown(result['original_speech']['audio_html'], unsafe_allow_html=True)
                        
                        # Translation content
                        if result['translated']:
                            st.markdown(f"### Translation ({result['target_language']})")
                            st.write(result['translated'])
                            if result['translated_speech']:
                                st.markdown("#### Listen")
                                st.markdown(result['translated_speech']['audio_html'], unsafe_allow_html=True)
                        
                        # Download buttons
                        st.markdown("### Downloads")
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.download_button(
                                label="Download Original Text",
                                data=result['original'],
                                file_name=f"transcription_{timestamp}.txt",
                                mime="text/plain"
                            )
                        
                        if result['original_speech']:
                            with col2:
                                st.download_button(
                                    label="Download Original Audio",
                                    data=result['original_speech']['audio_bytes'],
                                    file_name=f"original_speech_{timestamp}.mp3",
                                    mime="audio/mp3"
                                )
                        
                        if result['translated']:
                            with col3:
                                st.download_button(
                                    label="Download Translation",
                                    data=result['translated'],
                                    file_name=f"translation_{timestamp}.txt",
                                    mime="text/plain"
                                )
                            
                            if result['translated_speech']:
                                with col4:
                                    st.download_button(
                                        label="Download Translated Audio",
                                        data=result['translated_speech']['audio_bytes'],
                                        file_name=f"translated_speech_{timestamp}.mp3",
                                        mime="audio/mp3"
                                    )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Custom CSS for better UI
st.markdown("""
    <style>
        .stButton button {
            border-radius: 20px;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .stProgress .st-bo {
            background-color: #4CAF50;
        }
        .stAlert {
            border-radius: 10px;
        }
        .streamlit-expanderHeader {
            background-color: #f0f2f6;
            border-radius: 10px;
        }
        /* Dark theme support */
        @media (prefers-color-scheme: dark) {
            .stButton button {
                background-color: #2E7D32;
            }
            .streamlit-expanderHeader {
                background-color: #262730;
            }
        }
    </style>
""", unsafe_allow_html=True)