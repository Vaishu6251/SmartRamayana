from gtts import gTTS
import os
import tempfile
import pygame

# Initialize Pygame mixer for playing audio
pygame.mixer.init()

# Language code mapping
LANGUAGE_CODES = {
    "en": "en",     # English
    "te": "te",     # Telugu
    "hi": "hi",     # Hindi
    "sa": "sa"      # Sanskrit (NOTE: Sanskrit is often unsupported directly, fallback to Hindi)
}

def play_text(text, lang_code):
    # Use Hindi for Sanskrit if gTTS doesn't support Sanskrit directly
    if lang_code == "sa":
        lang_code = "hi"

    try:
        tts = gTTS(text=text, lang=lang_code)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            temp_path = tmpfile.name
            tts.save(temp_path)

        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()

        # Wait until the audio finishes
        while pygame.mixer.music.get_busy():
            continue

        os.remove(temp_path)

    except Exception as e:
        print(f"Text-to-speech failed: {e}")
