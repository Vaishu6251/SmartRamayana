import streamlit as st
import json
import os

# Page setup
st.set_page_config(page_title="Ramayana Book Bites", layout="wide")
st.title("📖 Ramayana Book Bites – Indian Classics Simplified")

# Load story data
with open("ramayana.json", "r", encoding="utf-8") as file:
    stories = json.load(file)

# Sidebar - story selector
story_titles = [story["title"] for story in stories]
selected_title = st.sidebar.selectbox("Choose a Ramayana Story", story_titles)

# Fetch selected story
selected_story = next(story for story in stories if story["title"] == selected_title)

# Story details
st.subheader(selected_story["title"])
st.markdown(f"**Chapter:** {selected_story.get('chapter', 'N/A')}")
st.markdown(f"**Characters:** {', '.join(selected_story.get('characters', []))}")
st.markdown(f"**Location:** {selected_story.get('location', 'N/A')}")
st.markdown(f"**Quote:** _{selected_story.get('quote', 'N/A')}_")
st.write(f"**Summary:** {selected_story['summary']}")
st.success(f"**Moral:** {selected_story['moral']}")

# Show image for selected story if it exists
image_path = f"images/{selected_story.get('image', '')}"
if os.path.exists(image_path):
    st.image(image_path, width=300)
else:
    st.warning("Image not found for this story.")
