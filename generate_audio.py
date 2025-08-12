from gtts import gTTS
import json
import os

os.makedirs("audio", exist_ok=True)

with open("ramayana.json", "r", encoding="utf-8") as file:
    stories = json.load(file)

for story in stories:
    title = story['title']
    summary = story.get('summary', '')
    filename = f"audio/{title.replace(' ', '_').lower()}.mp3"

    if not os.path.exists(filename) and summary:
        print(f"🔊 Generating audio for: {title}")
        tts = gTTS(summary, lang='en')
        tts.save(filename)
