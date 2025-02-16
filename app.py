import os
import streamlit as st
import requests
import datetime
import numpy as np
from sentence_transformers import SentenceTransformer
from io import BytesIO
import random
import mindhaven_be as backend


# ---- BACKEND STARTUP: LOAD ANY SAVED CHUNKS (optional)
backend.load_chunks_from_disk()


# Streamlit UI
st.set_page_config(page_title="MindHaven", page_icon=":herb:", layout="centered")

st.title("🧘 MindHaven")
st.write("AI-Powered Mental Health Companion")
st.write("Talk to an empathetic AI for emotional support and well-being tips.")

# Mood Tracking & Journaling
st.sidebar.header("📖 Mood Tracker & Journal")
mood = st.sidebar.selectbox("How do you feel today?", ["Happy", "Stressed", "Anxious", "Sad"])
journal_entry = st.sidebar.text_area("Write about your day...")

# Save Journal Entry
if st.sidebar.button("Save Journal Entry"):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    with open("journal.txt", "a") as file:
        file.write(f"{date} - Mood: {mood}\n{journal_entry}\n\n")
    st.sidebar.success("Entry saved! ✅")

# View Saved Journal Entries
st.sidebar.header("📜 Past Journal Entries")
if os.path.exists("journal.txt"):
    with open("journal.txt", "r") as file:
        journal_logs = file.readlines()
        if journal_logs:
            st.sidebar.text_area("Previous Entries", "".join(journal_logs), height=200)
        else:
            st.sidebar.write("No journal entries yet.")
else:
    st.sidebar.write("No journal entries found.")

# Upload PDF Files
st.header("📂 Upload Mental Health Documents")
uploaded_file = st.file_uploader("Upload file(s) (e.g., therapy guides, self-help books)", type=["txt", "pdf", "docx"], accept_multiple_files=True)
if uploaded_file:
    if st.button("Process Upload"):
        result_msg = backend.process_files(uploaded_file)  # Updated function name
        st.success(result_msg)

# AI Chat Section
st.header("💬 AI Support Chat")
user_input = st.text_area("How are you feeling? Share your thoughts.")

if st.button("Get AI Support"):
    if user_input:
        response = backend.answer_user_query(user_input)
        # response = chat_with_ai(user_input, mood)
        st.subheader("AI Response:")
        st.write(response)
    else:
        st.warning("Please enter a message.")

# Guided Meditation & Relaxation
st.header(":herb: Guided Meditation & Relaxation")
st.write("Click below to start a short guided meditation.")
if st.button("Start 5-Minute Meditation"):
    st.video("https://www.youtube.com/watch?v=inpok4MKVLM")  

# Daily Wellness Tip
st.sidebar.header("🌟 Daily Wellness Tip")
tips = [
    "Take a 10-minute walk outside to clear your mind.",
    "Practice deep breathing exercises for stress relief.",
    "Write down three things you're grateful for today.",
    "Drink plenty of water and stay hydrated!"
]
st.sidebar.write(random.choice(tips))
