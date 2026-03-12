import streamlit as st
from src.graph import run_debate

# -------------------------
# Page Config
# -------------------------

st.set_page_config(page_title="AI Debate Arena", page_icon="⚔️", layout="wide")

# -------------------------
# Header
# -------------------------

st.title("⚔️ AI Debate Arena")
st.caption("Two AI agents debate any topic. A Judge AI declares the winner.")
st.divider()

# -------------------------
# Input
# -------------------------

topic = st.text_input(
    "Enter a debate topic:",
    placeholder="e.g. AI will replace software engineers by 2030",
    max_chars=200,
)

col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    start = st.button("Start Debate", type="primary", use_container_width=True)
with col2:
    clear = st.button("🔄 Clear", use_container_width=True)

if clear:
    st.rerun()

# -------------------------
# Run Debate
# -------------------------

if start and topic:
    with st.spinner("🤖 Agents are preparing their arguments..."):
        try:
            result = run_debate(topic)

            st.divider()
            st.subheader(f"🎯 Topic: *{topic}*")
            st.divider()

            # Two column layout for arguments
            col_for, col_against = st.columns(2)

            with col_for:
                st.markdown("### 🟢 Argument FOR")
                st.markdown(result["for_argument"])

            with col_against:
                st.markdown("### 🔴 Argument AGAINST")
                st.markdown(result["against_argument"])

            st.divider()

            # Judge verdict
            st.markdown("### ⚖️ Judge's Verdict")
            st.markdown(result["verdict"])

            # Show error if any (non-fatal)
            if result.get("error"):
                st.warning(f"Minor issue during run: {result['error']}")

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

elif start and not topic:
    st.warning("Please enter a topic first!")
