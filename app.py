import streamlit as st

# Page Config - MUST be first st command
st.set_page_config(page_title="EV Insight 2025: Omni-Model System", layout="wide")

# Now import other modules with error handling
try:
    from src.config import Config
    from src.graph_workflow import EVGraph
    import time
    import os
except Exception as e:
    st.error(f"❌ Import Error: {e}")
    st.stop()

# Check if running on Streamlit Cloud (local models won't work there)
IS_CLOUD = os.getenv("STREAMLIT_SHARING_MODE") is not None or os.getenv("STREAMLIT_CLOUD") is not None

# Sidebar - Model Selection & Config
with st.sidebar:
    st.title("⚙️ Neural Config")
    st.subheader("Active Agents")
    
    # Only show local models if running locally
    if IS_CLOUD:
        drafter_options = [Config.MODEL_GPT5, Config.MODEL_CLAUDE]
        critic_options = [Config.MODEL_GROK4]
        st.warning("⚠️ Local models (Llama, DeepSeek) are not available on Streamlit Cloud. Use cloud models only.")
    else:
        drafter_options = [Config.MODEL_GPT5, Config.MODEL_CLAUDE, Config.LOCAL_LLAMA]
        critic_options = [Config.LOCAL_DEEPSEEK, Config.MODEL_GROK4]
    
    drafter_model = st.selectbox("Drafting Agent", drafter_options)
    critic_model = st.selectbox("Critique/Logic Agent", critic_options)
    
    iterations = st.slider("Debate Iterations", min_value=1, max_value=5, value=3)
    
    st.divider()
    st.info("System Status: Online \nTarget Date: Dec 2025")

# Main Interface
st.title("⚡ EV Business Field Analysis: 2025 Edition")
st.markdown("### The Council of Experts")

# State Management
if "messages" not in st.session_state:
    st.session_state.messages = []

# User Input
query = st.chat_input("Enter scope (e.g., 'EV Battery Swapping Trends in India 2025')...")

if query:
    # 1. Initialize the Graph
    ev_graph = EVGraph()
    app = ev_graph.build_graph()
    
    # 2. Prepare Initial State
    initial_state = {
        "scope": query,
        "draft": "",
        "critique": "",
        "iteration_count": 0,
        "max_iterations": iterations, # From Sidebar
        "search_data": "",
        "drafter_model": drafter_model, # From Sidebar
        "critic_model": critic_model    # From Sidebar
    }
    
    # 3. Create the "War Room" Layout
    st.markdown(f"### 🔭 Analyzing: {query}")
    status_container = st.status("🚀 System Running...", expanded=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📝 Draft Evolution")
        draft_box = st.empty()
    with col2:
        st.subheader("⚖️ Critique Board")
        critique_box = st.empty()
        
    # 4. Run the Graph Stream
    # We iterate through the graph events
    for output in app.stream(initial_state):
        
        # Handle Research Output
        if 'research' in output:
            status_container.write("✅ Research Complete: Data Gathered")
            with st.expander("View Raw Data"):
                st.write(output['research']['search_data'])
                
        # Handle Draft Output
        if 'drafter' in output:
            draft_text = output['drafter']['draft']
            count = output['drafter']['iteration_count']
            status_container.write(f"✍️ Draft Version {count} Generated")
            draft_box.markdown(f"**--- Draft v{count} ---**\n\n{draft_text}")
            
        # Handle Critique Output
        if 'critic' in output:
            critique_text = output['critic']['critique']
            status_container.write("🤔 Critique Received")
            critique_box.info(f"**Critique:**\n\n{critique_text}")

    status_container.update(label="Analysis Complete!", state="complete", expanded=False)
    
    # 5. Final Result Display
    st.success("🎉 Final Report Section Generated")
    final_content = output.get('drafter', {}).get('draft', "Error: No draft finalized.")
    st.markdown("---")
    st.markdown(final_content)
    
    # 6. Download Option (Simple Text for now)
    st.download_button(
        "Download Section", 
        data=final_content, 
        file_name=f"{query.replace(' ', '_')}.md"
    )