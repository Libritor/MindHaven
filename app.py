import os, datetime, random, json, re
import streamlit as st

import mindhaven_be as backend  # your helper module

# ------------- 1. FIRST Streamlit command ------------------------
st.set_page_config(
    page_title="MindHaven",
    page_icon=":herb:",
    layout="centered"          # centred looks nicer on mobile; change to "wide" if you prefer
)
# -----------------------------------------------------------------

# ------------- 2. Custom CSS & Mobile Viewport -------------------
st.markdown(
    """
    <style>
        /* Remove ALL Streamlit chrome (header, footer, deploy btn, red bar) */
        .stApp > header,
        .stDeployButton,
        .st-emotion-cache-uf99v8,          /* red loading bar container */
        footer {visibility:hidden; height:0 !important;}
        .block-container {padding-top:0.5rem;}
    </style>

    <!-- mobile scaling -->
    <meta name="viewport" content="width=device-width, initial-scale=1">
    """,
    unsafe_allow_html=True
)
# -----------------------------------------------------------------

# ---- BACKEND STARTUP --------------------------------------------
backend.load_chunks_from_disk()
# -----------------------------------------------------------------

# -------------------  MAIN UI  -----------------------------------
st.title("🧘 MindHaven")
st.write("AI-Powered Mental Health Companion")
st.write("Talk to an empathetic AI for emotional support and well-being tips.")

# ── Sidebar: Mood tracker & journal ──────────────────────────────
st.sidebar.header("📖 Mood Tracker & Journal")
mood = st.sidebar.selectbox("How do you feel today?",
                            ["Happy", "Stressed", "Anxious", "Sad"])
journal_entry = st.sidebar.text_area("Write about your day…")

if st.sidebar.button("Save Journal Entry"):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    with open("journal.txt", "a", encoding="utf-8") as f:
        f.write(f"{date} – Mood: {mood}\n{journal_entry}\n\n")
    st.sidebar.success("Entry saved ✅")

# View saved entries
st.sidebar.header("📜 Past Journal Entries")
if os.path.exists("journal.txt"):
    with open("journal.txt", "r", encoding="utf-8") as f:
        st.sidebar.text_area("Previous Entries", f.read(), height=200)
else:
    st.sidebar.write("No journal entries yet.")

# ── File upload ──────────────────────────────────────────────────
st.header("📂 Upload Mental-Health Documents")
files = st.file_uploader("Upload PDFs or text files",
                         type=["txt", "pdf", "docx"],
                         accept_multiple_files=True)
if files and st.button("Process Upload"):
    st.success(backend.process_files(files))

# ── AI chat ──────────────────────────────────────────────────────
st.header("💬 AI Support Chat")
user_input = st.text_area("How are you feeling?")

if st.button("Get AI Support"):
    if user_input:
        st.subheader("AI Response:")
        st.write(backend.answer_user_query(user_input))
    else:
        st.warning("Please enter a message first.")

# ── Guided meditation ────────────────────────────────────────────
st.header(":herb: Guided Meditation & Relaxation")
if st.button("Start 5-Minute Meditation"):
    st.video("https://www.youtube.com/watch?v=inpok4MKVLM")

# ── Daily tip ────────────────────────────────────────────────────
st.sidebar.header("🌟 Daily Wellness Tip")
st.sidebar.write(random.choice([
    "Take a 10-minute walk outside to clear your mind.",
    "Practice deep breathing for stress relief.",
    "Write down three things you're grateful for today.",
    "Drink plenty of water and stay hydrated!"
]))
# -----------------------------------------------------------------
