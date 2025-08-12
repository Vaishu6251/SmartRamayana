from gtts import gTTS

text = "This is a test audio to verify gTTS is working."
tts = gTTS(text=text, lang='en')
tts.save("test_audio.mp3")
