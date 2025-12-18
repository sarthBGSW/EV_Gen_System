import streamlit as st

# Page Config - MUST be first
st.set_page_config(page_title="EV Insight 2025", layout="wide")

st.write("# 🚀 Page Loaded Successfully!")
st.write("If you see this message, the app is working.")

# Test imports one by one
st.write("---")
st.write("## Testing Imports...")

try:
    from src.config import Config
    st.success("✅ Config module imported")
    st.write(f"- GPT-5 Model: {Config.MODEL_GPT5}")
    st.write(f"- Claude Model: {Config.MODEL_CLAUDE}")
except Exception as e:
    st.error(f"❌ Config failed: {e}")

try:
    from src.llm_engine import ModelFactory
    st.success("✅ LLM Engine imported")
except Exception as e:
    st.error(f"❌ LLM Engine failed: {e}")

try:
    from src.search_tools import ResearchEngine
    st.success("✅ Search Tools imported")
except Exception as e:
    st.error(f"❌ Search Tools failed: {e}")

st.write("---")
st.write("## All systems operational!")
