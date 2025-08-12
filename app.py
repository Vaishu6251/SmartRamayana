# app.py
import streamlit as st
import json
import os
import random

# set page config first
st.set_page_config(page_title="Ramayana Book Bites", layout="wide")

try:
    from gtts import gTTS
    _GTTs_AVAILABLE = True
except Exception:
    _GTTs_AVAILABLE = False

try:
    from daily_shloka import get_daily_shloka
    _HAS_DAILY_SHLOKA = True
except Exception:
    _HAS_DAILY_SHLOKA = False

try:
    from quiz_data import quiz_data
except Exception as e:
    st.error(f"Could not import quiz_data.py: {e}")
    st.stop()

# -------- Language selection --------
lang_map = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te"
}
selected_language = st.selectbox("🌐 Choose Language", list(lang_map.keys()))
lang_code = lang_map[selected_language]

# -------- Translations for labels --------
labels = {
    "chapter": {"en": "Chapter", "hi": "अध्याय", "te": "అధ్యాయం"},
    "characters": {"en": "Characters", "hi": "पात्र", "te": "పాత్రలు"},
    "location": {"en": "Location", "hi": "स्थान", "te": "ప్రదేశం"},
    "quote": {"en": "Quote", "hi": "उद्धरण", "te": "సూక్తి"},
    "summary": {"en": "Summary", "hi": "सारांश", "te": "సారాంశం"},
    "moral": {"en": "Moral", "hi": "नीति", "te": "నీతి"},
    "story": {"en": "STORY", "hi": "कहानी", "te": "కథ"},
    "submit_quiz": {"en": "Submit Quiz", "hi": "क्विज़ जमा करें", "te": "క్విజ్ సమర్పించండి"},
    "quiz_unavailable": {
        "en": "📌 Quiz not available for this Kanda yet. (No matching key in quiz_data.py)",
        "hi": "📌 इस खंड के लिए अभी क्विज़ उपलब्ध नहीं है। (quiz_data.py में कोई मिलान कुंजी नहीं है)",
        "te": "📌 ఈ ఖండకు ఇంకా క్విజ్ అందుబాటులో లేదు. (quiz_data.py లో సంబంధిత కీ లేదు)"
    },
    "answer_prompt": {
        "en": "Answer the following questions based on what you just read!",
        "hi": "जो आपने अभी पढ़ा उसके आधार पर निम्नलिखित प्रश्नों के उत्तर दें!",
        "te": "మీరు ఇప్పటివరకు చదివిన వాటిపై ఆధారపడి క్రింది ప్రశ్నలకు సమాధానమివ్వండి!"
    },
    "audio_unavailable": {
        "en": "Audio narration not available.",
        "hi": "ऑडियो उपलब्ध नहीं है।",
        "te": "ఆడియో వివరణ అందుబాటులో లేదు."
    },
    "listen_narration": {
        "en": "Listen to the Story Narration",
        "hi": "कहानी की ध्वनि सुनें",
        "te": "కథ వాయిస్ వినండి"
    },
    "bookmark_story": {
        "en": "Bookmark this Story",
        "hi": "इस कहानी को बुकमार्क करें",
        "te": "ఈ కథను బుక్మార్క్ చేయండి"
    },
    "remove_bookmark": {
        "en": "Remove Bookmark",
        "hi": "बुकमार्क हटाएं",
        "te": "బుక్మార్క్ తొలగించండి"
    },
    "kanda_quiz": {
        "en": "Kanda Quiz",
        "hi": "कांड क्विज़",
        "te": "కాండా క్విజ్"
    },
    "quiz_second_occurrence_msg": {
        "en": "Quiz for this Kanda will be shown on the second occurrence of {kanda}.",
        "hi": "इस कांड के लिए क्विज़ दूसरी बार {kanda} पर दिखाई देगा।",
        "te": "ఈ కాండా యొక్క క్విజ్ {kanda} రెండవ సారి వచ్చినప్పుడు చూపించబడుతుంది."
    }
}

def tr(label_key):
    entry = labels.get(label_key)
    if not entry:
        return label_key
    return entry.get(lang_code, entry.get("en"))

# -------- Daily shloka --------
if _HAS_DAILY_SHLOKA:
    try:
        shloka = get_daily_shloka(lang_code)
    except Exception:
        shloka = ""
else:
    shloka = ""

if shloka:
    st.markdown("### 🕉️ Today's Shloka")
    st.markdown(f"> {shloka}")

# -------- Load stories --------
RAMAYANA_JSON = "ramayana.json"
if not os.path.exists(RAMAYANA_JSON):
    st.error(f"{RAMAYANA_JSON} not found in the app directory.")
    st.stop()

with open(RAMAYANA_JSON, "r", encoding="utf-8") as f:
    try:
        stories = json.load(f)
    except Exception as e:
        st.error(f"Error parsing {RAMAYANA_JSON}: {e}")
        st.stop()

if not isinstance(stories, list):
    st.error("ramayana.json should contain a JSON array of story objects.")
    st.stop()

# Helper functions
def get_localized_field(field_value, lang_code):
    if isinstance(field_value, dict):
        return field_value.get(lang_code) or field_value.get("en") or next(iter(field_value.values()))
    return field_value

def extract_characters(char_field, lang_code):
    if not char_field:
        return []
    if isinstance(char_field, dict):
        val = char_field.get(lang_code) or char_field.get("en")
        if isinstance(val, list):
            return val
        if isinstance(val, str):
            return [val]
        for v in char_field.values():
            if isinstance(v, list):
                return v
        return []
    if isinstance(char_field, list):
        if all(isinstance(x, dict) for x in char_field):
            out = []
            for entry in char_field:
                out.append(entry.get(lang_code) or entry.get("en") or next(iter(entry.values())))
            return out
        return [str(x) for x in char_field]
    return [str(char_field)]

def normalize_key(s: str):
    if not s:
        return ""
    return "".join(ch for ch in s.lower() if ch.isalnum())

# Build sidebar list (English titles used as stable keys)
story_titles_en = []
for s in stories:
    title_field = s.get("title", {})
    if isinstance(title_field, dict):
        title_en = title_field.get("en") or next(iter(title_field.values()))
    else:
        title_en = title_field or "Untitled Story"
    story_titles_en.append(title_en)

selected_title = st.sidebar.selectbox("📚 Choose a Ramayana Story", story_titles_en)

# Bookmarks
st.sidebar.markdown("---")
st.sidebar.markdown("📌 **Bookmarked Stories**")
if "bookmarked_stories" not in st.session_state:
    st.session_state.bookmarked_stories = []

if st.session_state.bookmarked_stories:
    for t in st.session_state.bookmarked_stories:
        st.sidebar.markdown(f"✅ {t}")
else:
    st.sidebar.markdown("No bookmarks yet.")

# find the selected story and its index among same-chapter entries
selected_story = None
selected_index_among_same = 0
same_chapter_list = []
for s in stories:
    t_field = s.get("title", {})
    t_en = t_field.get("en") if isinstance(t_field, dict) else t_field
    if t_en == selected_title:
        pass

# locate selected_story and build same-chapter occurrences for chapter-level repetition handling
for idx, s in enumerate(stories):
    t_field = s.get("title", {})
    t_en = t_field.get("en") if isinstance(t_field, dict) else t_field
    if t_en == selected_title:
        selected_story = s
        break

if not selected_story:
    st.error("Selected story not found in data.")
    st.stop()

# Build a list of stories that share the same normalized chapter name (for occurrence counting)
chapter_field_all = []
for s in stories:
    ch = s.get("chapter")
    if isinstance(ch, dict):
        ch_en = ch.get("en") or next(iter(ch.values()))
    else:
        ch_en = ch or ""
    chapter_field_all.append(normalize_key(ch_en))

# normalized chapter of the selected story
chapter_field = selected_story.get("chapter")
if isinstance(chapter_field, dict):
    chapter_en = chapter_field.get("en") or next(iter(chapter_field.values()))
else:
    chapter_en = chapter_field or ""
normalized_selected_chapter = normalize_key(chapter_en)

# compute the occurrence index of this selected story among stories that share the same normalized chapter
occurrence_index = 0
for i, norm in enumerate(chapter_field_all):
    if norm == normalized_selected_chapter:
        s = stories[i]
        t_field = s.get("title", {})
        t_en = t_field.get("en") if isinstance(t_field, dict) else t_field
        if t_en == selected_title:
            occurrence_index = sum(1 for j in range(i) if chapter_field_all[j] == normalized_selected_chapter)
            break

def safe_get_story(field_name):
    val = selected_story.get(field_name)
    return get_localized_field(val, lang_code) if val is not None else ""

# Display story
st.subheader(f"📖 {safe_get_story('title')}")
st.markdown(f"**🧙 {tr('chapter')}:** {safe_get_story('chapter')}")
characters_list = extract_characters(selected_story.get("characters"), lang_code)
st.markdown(f"**👤 {tr('characters')}:** {', '.join(characters_list) if characters_list else 'N/A'}")
st.markdown(f"**📍 {tr('location')}:** {safe_get_story('location')}")
quote = safe_get_story("quote")
if quote:
    st.markdown(f"**💬 {tr('quote')}:** _{quote}_")
st.write(f"**🔍 {tr('summary')}:** {safe_get_story('summary')}")
moral = safe_get_story("moral")
if moral:
    st.success(f"**🌟 {tr('moral')}:** {moral}")

# Long description display
long_desc = selected_story.get("long_description", "")
if isinstance(long_desc, dict):
    content = long_desc.get(lang_code) or long_desc.get("en") or ""
else:
    content = long_desc or ""
if content:
    st.markdown(f"### 📜 {tr('story')}")
    st.write(content)

# Bookmark buttons
if selected_title not in st.session_state.bookmarked_stories:
    if st.button(f"🔖 {tr('bookmark_story')}"):
        st.session_state.bookmarked_stories.append(selected_title)
        st.success(tr("bookmark_story") + (" added!" if lang_code == "en" else " हो गया!" if lang_code == "hi" else " జోడించబడింది!"))
else:
    if st.button(f"❌ {tr('remove_bookmark')}"):
        st.session_state.bookmarked_stories.remove(selected_title)
        st.warning(tr("remove_bookmark") + (" done." if lang_code == "en" else " हो गया।" if lang_code == "hi" else " పూర్తయింది."))

# Audio narration
st.markdown(f"## 🎧 {tr('listen_narration')}")
audio_dir = "audio"
os.makedirs(audio_dir, exist_ok=True)
audio_filename = f"{selected_title.replace(' ', '_').lower()}_{lang_code}.mp3"
audio_path = os.path.join(audio_dir, audio_filename)

audio_text_parts = [
    shloka,
    safe_get_story("title"),
    safe_get_story("chapter"),
    ", ".join(characters_list),
    safe_get_story("location"),
    safe_get_story("quote"),
    safe_get_story("summary"),
    content
]
audio_text = ". ".join([p for p in audio_text_parts if p])

if _GTTs_AVAILABLE and audio_text:
    if not os.path.exists(audio_path):
        try:
            tts = gTTS(text=audio_text, lang=lang_code if lang_code in {"en", "hi", "te"} else "en")
            tts.save(audio_path)
        except Exception as e:
            st.warning(f"⚠️ Could not generate audio: {e}")
    if os.path.exists(audio_path):
        with open(audio_path, "rb") as af:
            st.audio(af.read(), format="audio/mp3")
else:
    st.info(tr("audio_unavailable"))

# -------- Quiz Section --------
st.markdown("---")
st.markdown(f"## 🧠 {tr('kanda_quiz')}")

# Decide whether to show quiz for repeated Kandās
# Show quiz only on second occurrence for BalaKanda, AranyaKanda, and YuddhaKanda (as requested)
repeat_only_show_on_second = {"balakanda", "aranyakanda", "yuddhakanda"}  # normalized names

show_quiz = True
if normalized_selected_chapter in repeat_only_show_on_second:
    # occurrence_index is zero-based; second occurrence => index == 1
    if occurrence_index < 1:
        show_quiz = False

if not show_quiz:
    st.info(tr("quiz_second_occurrence_msg").format(kanda=safe_get_story("chapter")))
else:
    quiz_key_map = {normalize_key(k): k for k in quiz_data.keys()}

    candidates = []
    if isinstance(chapter_en, str) and chapter_en:
        candidates.append(chapter_en)
    localized_chapter = safe_get_story("chapter")
    if localized_chapter and localized_chapter != chapter_en:
        candidates.append(localized_chapter)
    candidates.append(selected_title)

    found_quiz_key = None
    for cand in candidates:
        nk = normalize_key(cand)
        if nk in quiz_key_map:
            found_quiz_key = quiz_key_map[nk]
            break

    # try partial substring match (fallback)
    if not found_quiz_key:
        lc = (localized_chapter or "").lower()
        for k in quiz_data.keys():
            if k.lower() in lc or lc in k.lower():
                found_quiz_key = k
                break

    if not found_quiz_key:
        st.warning(tr("quiz_unavailable"))
    else:
        raw_block = quiz_data[found_quiz_key]
        if isinstance(raw_block, dict):
            questions_for_lang = raw_block.get(lang_code) or raw_block.get("en") or next(iter(raw_block.values()))
        else:
            questions_for_lang = raw_block

        if not isinstance(questions_for_lang, list) or not questions_for_lang:
            st.warning(tr("quiz_unavailable"))
        else:
            st.info(tr("answer_prompt"))
            total_questions = len(questions_for_lang)
            user_answers = []

            with st.form("kanda_quiz_form"):
                for idx, q in enumerate(questions_for_lang):
                    question_text = q.get("question") if isinstance(q, dict) else str(q)
                    options = q.get("options", []) if isinstance(q, dict) else []
                    correct_answer = q.get("answer") if isinstance(q, dict) else None

                    if not isinstance(options, list):
                        options = [str(options)]

                    opt_copy = options.copy()
                    random.shuffle(opt_copy)

                    selected_opt = st.selectbox(f"Q{idx+1}: {question_text}", opt_copy, key=f"quiz_q_{idx}")
                    user_answers.append((selected_opt, correct_answer))
                submitted = st.form_submit_button(tr("submit_quiz"))

            if submitted:
                correct_count = 0
                results = []
                for i, (chosen, correct) in enumerate(user_answers):
                    ok = (chosen == correct)
                    if ok:
                        correct_count += 1
                    results.append((i + 1, ok, correct))
                st.success(f"✅ You got {correct_count} out of {total_questions} correct.")
                for qnum, ok, ans in results:
                    if ok:
                        st.markdown(f"**Q{qnum}:** <span style='color:green'>✅ Correct</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"**Q{qnum}:** <span style='color:red'>❌ Wrong — Correct: {ans}</span>", unsafe_allow_html=True)
                correct_line = " | ".join([f"Q{num}: {ans}" for num, _, ans in results])
                st.markdown(f"**✅ Correct Answers:** {correct_line}")

# -------- Image Display --------
st.markdown("---")
image_filename = selected_story.get("image", "")
if image_filename:
    image_path = os.path.join("images", image_filename)
    if os.path.exists(image_path):
        st.image(image_path, width=350)
    else:
        st.warning("⚠️ Image file declared but not found in images/ directory.")
else:
    st.info("No image provided for this story.")
