from pathlib import Path
import streamlit as st
from backend.pipeline import query_knowledge_base, run_video_pipeline

# 1. Page Setup
st.set_page_config(page_title="Video-to-Knowledge", page_icon="🎬", layout="wide")

# Subtle UI polish
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.75rem;
            padding-bottom: 2rem;
            max-width: 1250px;
        }
        .hero-box {
            background: linear-gradient(135deg, #131A2A 0%, #1E1B4B 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 14px;
            padding: 1.25rem 1.75rem;
            margin-bottom: 1.5rem;
        }
        .hero-title {
            font-size: 1.85rem;
            font-weight: 700;
            color: #FFFFFF;
            margin: 0;
        }
        .hero-sub {
            color: #A5B4FC;
            font-size: 0.98rem;
            margin: 0.25rem 0 0 0;
        }
        .source-card {
            background-color: #0B0F19;
            border-left: 3px solid #6366F1;
            border-radius: 0 8px 8px 0;
            padding: 0.65rem 0.9rem;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# 2. Session State
if "video_path" not in st.session_state:
    st.session_state.video_path = None
if "video_name" not in st.session_state:
    st.session_state.video_name = None
if "is_processed" not in st.session_state:
    st.session_state.is_processed = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "video_start_time" not in st.session_state:
    st.session_state.video_start_time = 0

# 3. Header
st.markdown(
    """
    <div class="hero-box">
        <h1 class="hero-title">🎬 Video-to-Knowledge</h1>
        <p class="hero-sub">Turn videos into searchable knowledge.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 4. Two Columns: Left for Video, Right for Chat
left_col, right_col = st.columns([1, 1.3], gap="large")

# --- LEFT SIDE: UPLOAD & PROCESS ---
with left_col:
    st.subheader("1. Upload Video")
    uploaded_file = st.file_uploader("Upload an MP4 video", type=["mp4"])

    if uploaded_file is not None:
        save_path = UPLOAD_DIR / uploaded_file.name

        # Only save and reset if a brand-new video is uploaded
        if st.session_state.video_name != uploaded_file.name:
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state.video_path = str(save_path)
            st.session_state.video_name = uploaded_file.name
            st.session_state.is_processed = False
            st.session_state.chat_history = []
            st.session_state.video_start_time = 0

        st.caption(f"Selected: **{st.session_state.video_name}**")
        st.video(
            st.session_state.video_path,
            start_time=st.session_state.video_start_time,
        )

        if st.button("Process Video", type="primary", use_container_width=True):
            with st.status("Processing video...", expanded=True) as status:
                progress_bar = st.progress(0)

                for percent, message, is_done in run_video_pipeline(st.session_state.video_path):
                    st.write(message)
                    progress_bar.progress(percent)
                    if is_done:
                        st.session_state.is_processed = True
                        status.update(label="Ready!", state="complete", expanded=False)

        if st.session_state.is_processed:
            st.success("Video processed! Ask questions on the right.")

# --- RIGHT SIDE: CHAT Q&A ---
with right_col:
    title_col, clear_col = st.columns([4, 1])
    with title_col:
        st.subheader("2. Ask Questions")
    with clear_col:
        if st.session_state.chat_history and st.button("Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    chat_box = st.container(height=470, border=True)

    with chat_box:
        if not st.session_state.is_processed:
            st.info("Upload and process a video on the left to start chatting.")
        elif not st.session_state.chat_history:
            st.info("Video indexed! Ask any question about the video below.")
        else:
            for msg_idx, item in enumerate(st.session_state.chat_history):
                with st.chat_message("user"):
                    st.write(item["question"])

                with st.chat_message("assistant"):
                    st.write(item["answer"])

                    if item["sources"]:
                        with st.expander(f"View Video Timestamps ({len(item['sources'])})"):
                            for src_idx, src in enumerate(item["sources"]):
                                info_col, btn_col = st.columns([3.5, 1.3])
                                with info_col:
                                    st.markdown(
                                        f"""
                                        <div class="source-card">
                                            <strong>[Source {src['rank']} • {src['timestamp']}]</strong>
                                            <span style="color:#A5B4FC;">{src['topic']}</span><br/>
                                            <span style="color:#D1D5DB;">{src['text']}</span>
                                        </div>
                                        """,
                                        unsafe_allow_html=True,
                                    )
                                with btn_col:
                                    if st.button(
                                        f"▶ {src['timestamp'].split(' - ')[0]}",
                                        key=f"jump_{msg_idx}_{src_idx}",
                                        use_container_width=True,
                                    ):
                                        st.session_state.video_start_time = src["start_seconds"]
                                        st.rerun()

    user_question = st.chat_input(
        "Ask a question about the video...",
        disabled=not st.session_state.is_processed,
    )

    if user_question:
        with st.spinner("Searching video knowledge..."):
            result = query_knowledge_base(user_question, st.session_state.video_path)

        st.session_state.chat_history.append({
            "question": user_question,
            "answer": result["answer"],
            "sources": result["sources"],
        })
        st.rerun()